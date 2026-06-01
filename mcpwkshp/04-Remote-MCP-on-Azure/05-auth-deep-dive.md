# 4.5 — Auth deep-dive: how the Azure MCP demo actually authenticates

This page unpacks exactly what's happening in the auth flow of the demo we deployed in §4.2 — and what you'd change in production. **Nothing new is deployed in this section.** It's reference material to use during the workshop Q&A.

---

## TL;DR

| Direction | In our demo | In production |
|-----------|-------------|----------------|
| Client → MCP server (incoming) | **No auth** — disabled by `--dangerously-disable-http-incoming-auth` | Entra OAuth 2.1 + PKCE (Bearer access token) |
| MCP server → Azure ARM (outgoing) | **System-assigned managed identity**, Reader role on the sub | MI (shared perms) **or** OBO (per-user perms) |
| Where secrets live | Nowhere — MI tokens come from the platform's MI endpoint | Same — still no secrets |
| Token lifetime | ~1h, auto-rotated | ~1h, auto-rotated |

---

## Two boundaries — keep them mentally separated

```
                       INCOMING                      OUTGOING
                  (client → MCP server)        (MCP server → Azure ARM)
                  ────────────────────         ─────────────────────────
   Demo:          DISABLED                     Managed Identity (Reader)
   Production:    OAuth 2.1 + Entra            Managed Identity or OBO
```

People conflate these all the time. They are independent knobs.

---

## End-to-end flow for "List my Azure subscriptions"

```
   ┌──────────────┐     ① HTTPS POST /             ┌────────────────────────────┐
   │  Copilot CLI │ ─────  (no auth header)  ─────►│  Azure Container App       │
   │   (laptop)   │                                │   azure-mcp:latest         │
   └──────────────┘                                │                            │
                                                  │   ② tool: subscription_list│
                                                  │      ↓                     │
                                                  │   ③ DefaultAzureCredential │
                                                  │      → MI token endpoint   │
                                                  └─────────────┬──────────────┘
                                                              │
                                                              │ ④ Bearer <MI token>
                                                              ▼
                                                ┌────────────────────────────┐
                                                │ Azure ARM / Resource Graph │
                                                │ RBAC: MI Reader on sub? ✓  │
                                                └────────────────────────────┘
```

### Step by step

| # | Where | What happens | Auth used |
|---|-------|--------------|-----------|
| 1 | Copilot CLI | User: *"List my subscriptions"* | — |
| 2 | Copilot CLI | LLM selects `subscription_list` from `azure-mcp-remote` | — |
| 3 | Laptop → ACA | `POST https://<fqdn>/` JSON-RPC `tools/call` | **None** (demo) |
| 4 | ACA | `azmcp` tool handler runs, calls Azure SDK | — |
| 5 | ACA → MI token endpoint | Request a token for `https://management.azure.com/` from the Container App's managed-identity endpoint | Container App's MI |
| 6 | ACA → ARM | `GET /subscriptions?api-version=...` with `Authorization: Bearer <MI token>` | **MI Bearer token** |
| 7 | ARM | RBAC check: MI has Reader on `/subscriptions/<SUB_ID>` → 200 OK | — |
| 8 | ACA → Laptop | MCP response with subscription JSON | — |
| 9 | Copilot CLI | LLM summarizes the result | — |

> 🔑 **Key takeaway:** your `az login` token is **never used** by this flow. The client carries no Azure credentials. The Container App's identity does all the talking to ARM.

---

## Why the demo runs without incoming auth

The flag `--dangerously-disable-http-incoming-auth` makes the server skip Entra token validation on the MCP endpoint. We accepted that risk *only* because:

1. The public FQDN isn't published anywhere
2. We deployed with `--read-only` — destructive tools aren't even loaded
3. The MI has only **Reader** on the subscription (so worst-case = info disclosure)
4. The whole resource group gets deleted at the end of the workshop

**Do not run a long-lived MCP server this way.** Anyone who learns the URL acts with the MI's permissions.

---

## What "outgoing auth" actually means

The server flag `--outgoing-auth-strategy` selects how Azure MCP authenticates **to Azure** when it executes a tool:

| Strategy | Behavior | When to pick it |
|----------|---------|------------------|
| `UseHostingEnvironmentIdentity` | Always use the container's MI (DefaultAzureCredential picks the platform's MI endpoint) | Demo / single-tenant / shared admin |
| `UseOnBehalfOf` | Take the caller's incoming Entra token, exchange it via OAuth 2.0 OBO for an ARM token scoped to that user | Multi-user, per-user RBAC |
| `UseAzureCli` | Use the host's `az login` (only relevant when running locally) | Local stdio mode |

In the demo we use the first one. Every caller — *whoever they are* — runs with the same MI permissions. That's why incoming auth and outgoing auth are independent: tightening incoming controls who can call the server; outgoing controls what those calls can do.

---

## Production-grade alternative — OAuth 2.1 + Entra

To turn this into a "real" deployment, you'd:

### 1. Create an Entra App Registration for the MCP server

```bash
az ad app create \
  --display-name "Azure MCP (workshop)" \
  --sign-in-audience AzureADMyOrg

APP_ID=$(az ad app list --display-name "Azure MCP (workshop)" --query "[0].appId" -o tsv)

# Expose an API scope (so clients can request `api://$APP_ID/.default`)
az ad app update --id "$APP_ID" --identifier-uris "api://$APP_ID"
```

### 2. Re-deploy without the dangerous flag and with audience env vars

```bash
az containerapp update \
  --name "$APP" --resource-group "$RG" \
  --set-env-vars \
      AZURE_MCP_AUTH__TENANTID="$TENANT_ID" \
      AZURE_MCP_AUTH__AUDIENCE="api://$APP_ID" \
  --args \
      "--transport" "http" \
      "--mode" "all" \
      "--read-only" \
      "--outgoing-auth-strategy" "UseHostingEnvironmentIdentity" \
      "--namespace" "subscription" \
      "--namespace" "group"
```

> Notice **`--dangerously-disable-http-incoming-auth` is gone**. The server now requires a valid Entra access token whose `aud` matches `api://$APP_ID` and whose `iss` is your tenant.

### 3. Update the Copilot CLI config to use OAuth

```json
{
  "mcpServers": {
    "azure-mcp-remote": {
      "type": "http",
      "url": "https://<fqdn>/",
      "auth": {
        "type": "oauth",
        "issuer": "https://login.microsoftonline.com/<tenant-id>/v2.0",
        "clientId": "<app-id>",
        "scopes": ["api://<app-id>/.default"]
      },
      "tools": ["*"]
    }
  }
}
```

The first time the user runs an Azure MCP tool, Copilot CLI launches an **OAuth 2.1 Authorization Code + PKCE** flow:

```
   ┌──────────────┐                                    ┌─────────────┐
   │  Copilot CLI │  ① open browser → authorize URL    │ Entra ID    │
   │   (laptop)   │ ──────────────────────────────────►│ login.micro │
   └──────────────┘   (with PKCE code_challenge)       │ softonline  │
          ▲                                            └──────┬──────┘
          │ ④ access_token + refresh_token                    │
          │                                                   │ ② user signs in
          │                                                   │   + consents
   ┌──────┴───────┐  ③ POST /token                            │
   │ loopback     │  code + code_verifier  ◄──────────────────┘
   │ redirect     │
   │ 127.0.0.1    │
   └──────────────┘

   then on every MCP call:

   Copilot CLI ─── Authorization: Bearer <access_token> ───► ACA → MCP server
                                                              │
                                                              │ validates iss,aud,exp,sig
                                                              ▼
                                                              tool runs
```

Tokens last ~1h; the refresh token is used silently for top-ups. No secret ever touches the user's filesystem in plaintext — Copilot CLI stores them in the OS keychain.

### 4. (Optional) Switch outgoing to On-Behalf-Of

If you want the user's Azure RBAC to be enforced (rather than the MI's):

```bash
--args \
    ... \
    "--outgoing-auth-strategy" "UseOnBehalfOf" \
    ...
```

Now the server takes the user's incoming token and runs an OBO exchange:

```
   user's access_token (audience=api://APP_ID)
                │
                ▼
   POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token
        grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer
        assertion=<user_token>
        scope=https://management.azure.com/.default
                │
                ▼
   new access_token (audience=management.azure.com, on behalf of <user>)
                │
                ▼
   ARM call → RBAC evaluated against THE USER, not the MI
```

The MI is now only used by the OBO exchange itself (it needs an Entra app secret or certificate to do the swap). The actual Azure work runs as the **caller**.

This is the right setting whenever multiple users with different Azure permissions share one MCP deployment.

---

## Common pitfalls

| Pitfall | Why it happens | Fix |
|--------|----------------|-----|
| `401 Unauthorized` on the MCP endpoint | You removed the disable flag but didn't add `auth.*` to `mcp-config.json` | Add the OAuth block + restart Copilot CLI |
| MI calls return `403 AuthorizationFailed` | RBAC role assignment hasn't propagated, or you assigned at the wrong scope | Wait 60s; verify scope is the **subscription**, not the RG |
| `aud` mismatch in token | Client requested `api://<wrong-app-id>/.default` | Re-check `clientId` in `mcp-config.json` matches the App Registration |
| OBO returns `AADSTS65001 consent required` | First-time use of the API scope | Run an admin consent: `az ad app permission admin-consent --id <APP_ID>` |
| Tokens look fine but ARM still 403 in OBO mode | The user's actual Azure RBAC doesn't grant access to the requested scope | Grant the user the role on the subscription (or scope down the question) |

---

## Q&A

### Question 1
In the demo, when Copilot CLI calls Azure MCP, what authenticates the request?

A) Your `az login` token  
B) **Nothing — incoming auth is disabled with `--dangerously-disable-http-incoming-auth`**  
C) A static API key in the MCP config  
D) mTLS

<details><summary>Answer</summary>

**B.** That's why the demo URL must stay private and the deployment is read-only.

</details>

### Question 2
What does the Container App's managed identity authenticate?

A) The client to the MCP server  
B) The MCP server to Microsoft's container registry  
C) **The MCP server's outgoing calls to Azure ARM/Resource Graph**  
D) Nothing — MIs are only for Key Vault

<details><summary>Answer</summary>

**C.** Outgoing calls only. Incoming calls are a separate auth boundary.

</details>

### Question 3
Why would you switch `--outgoing-auth-strategy` from `UseHostingEnvironmentIdentity` to `UseOnBehalfOf`?

A) It's faster  
B) **So Azure RBAC is evaluated against the *calling user* instead of the shared MI** — required for multi-user scenarios  
C) To remove the need for an Entra App Registration  
D) To avoid token validation

<details><summary>Answer</summary>

**B.** OBO trades the user's incoming Entra token for a downstream ARM token in their name.

</details>

---

## Further reading

- MCP spec — Authorization (2025-06): https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
- Azure MCP server source: https://github.com/microsoft/mcp/tree/main/servers/Azure.Mcp.Server
- DefaultAzureCredential ordering: https://learn.microsoft.com/azure/developer/intro/passwordless-overview
- Managed Identity in Container Apps: https://learn.microsoft.com/azure/container-apps/managed-identity
- OAuth 2.0 On-Behalf-Of flow: https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow
- App Service / ACA Easy Auth: https://learn.microsoft.com/azure/app-service/overview-authentication-authorization

---

## Next

→ [§5 — Wrap-up](../05-Wrap-Up/README.md)
