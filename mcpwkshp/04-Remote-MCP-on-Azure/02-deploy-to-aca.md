# 4.2 — Deploy Azure MCP to Azure Container Apps

> ⚠️ **Demo mode warning.** These commands disable incoming auth (`--dangerously-disable-http-incoming-auth`) so the workshop demo "just works" with Copilot CLI. **Anyone who knows the URL can call your server and act with the managed identity's permissions.** Use a throwaway subscription, and run the `az group delete` cleanup at the end.

---

## Concept

We're going to:

1. Make a resource group + Container Apps environment
2. Create a Container App that runs `mcr.microsoft.com/azure-sdk/azure-mcp:latest` with HTTP transport
3. Give it a system-assigned managed identity + **Reader** on the subscription (outgoing auth)
4. Print the public FQDN for use in §4.3

```
az group create  →  az containerapp env create  →  az containerapp create
                                                     │
                                                     ├─ image: azure-mcp:latest
                                                     ├─ args:  --transport http
                                                     │         --mode all
                                                     │         --read-only
                                                     │         --dangerously-disable-http-incoming-auth
                                                     │
                                                     ├─ targetPort 8080  (HTTPS ingress)
                                                     │
                                                     └─ system-assigned MI  ─►  Reader on /subscriptions/...
```

---

## Practice

### Step 0 — Login + sub

```bash
az login
az account set --subscription "<your-sub-name-or-id>"
SUB_ID=$(az account show --query id -o tsv)
echo "Using subscription: $SUB_ID"
```

> On PowerShell, replace `$(...)` with `(...)` syntax: `$SUB_ID = az account show --query id -o tsv`

### Step 1 — Pick names + region

```bash
RG=rg-mcp-demo
LOCATION=eastus
ENV=env-mcp-demo
APP=azmcp-demo
```

### Step 2 — Resource group + Container Apps environment

```bash
az group create -n "$RG" -l "$LOCATION"

az containerapp env create \
  --name "$ENV" \
  --resource-group "$RG" \
  --location "$LOCATION"
```

### Step 3 — Create the Container App running Azure MCP

```bash
az containerapp create \
  --name "$APP" \
  --resource-group "$RG" \
  --environment "$ENV" \
  --image mcr.microsoft.com/azure-sdk/azure-mcp:latest \
  --target-port 8080 \
  --ingress external \
  --transport http \
  --system-assigned \
  --min-replicas 1 --max-replicas 1 \
  --cpu 0.5 --memory 1.0Gi \
  --env-vars \
      ASPNETCORE_ENVIRONMENT=Production \
      AZURE_MCP_DANGEROUSLY_DISABLE_HTTPS_REDIRECTION=true \
      AZURE_MCP_DANGEROUSLY_ENABLE_FORWARDED_HEADERS=true \
  --args \
      "--transport" "http" \
      "--mode" "all" \
      "--read-only" \
      "--outgoing-auth-strategy" "UseHostingEnvironmentIdentity" \
      "--dangerously-disable-http-incoming-auth" \
      "--namespace" "subscription" \
      "--namespace" "group"
```

What each piece does:

| Flag | Purpose |
|------|---------|
| `--image …azure-mcp:latest` | Microsoft's published Azure MCP image |
| `--target-port 8080` | Azure MCP listens on 8080 by default |
| `--ingress external --transport http` | Public HTTPS endpoint |
| `--system-assigned` | Creates the managed identity Azure MCP will use for outgoing Azure calls |
| `--transport http` (in `--args`) | Tell Azure MCP to speak MCP over HTTP, not stdio |
| `--mode all` | Expose each Azure MCP tool individually (best for tool selection) |
| `--read-only` | Disables any tool that mutates Azure resources |
| `--outgoing-auth-strategy UseHostingEnvironmentIdentity` | Use the ACA managed identity for downstream Azure calls |
| `--dangerously-disable-http-incoming-auth` | Demo only — disables Entra auth on inbound calls |
| `--namespace subscription --namespace group` | Only expose subscription + resource group tools (smaller tool list, faster) |

### Step 4 — Grant the MI Reader on the subscription

```bash
PRINCIPAL_ID=$(az containerapp identity show \
  --name "$APP" --resource-group "$RG" \
  --query principalId -o tsv)

az role assignment create \
  --assignee-object-id "$PRINCIPAL_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "Reader" \
  --scope "/subscriptions/$SUB_ID"
```

### Step 5 — Get the public URL

```bash
FQDN=$(az containerapp show -n "$APP" -g "$RG" \
  --query properties.configuration.ingress.fqdn -o tsv)

echo "Azure MCP URL: https://$FQDN/mcp"
```

Save that URL — you'll paste it in §4.3.

### Step 6 — Smoke test the endpoint

```bash
curl -s -i "https://$FQDN/mcp" -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'
```

You should get back a `200` with an MCP `initialize` response. If you get `404` or a TLS error, give ACA another ~30 seconds — first-revision warm-up can be slow.

---

## Troubleshooting

| Symptom | Likely fix |
|---------|-----------|
| `az containerapp create` fails: "extension not installed" | `az extension add --name containerapp --upgrade` |
| Container won't start | `az containerapp logs show -n "$APP" -g "$RG" --tail 100` |
| `403` calling Azure inside tools | Role assignment hasn't propagated yet; wait 60s and try again |
| `curl` returns HTML | You hit the ingress before MCP routing was ready — wait, then retry |

---

## Cleanup (run at the end of the workshop)

```bash
az group delete -n "$RG" --yes --no-wait
```

---

## Q&A

### Question 1
Why do we set `--target-port 8080`?

A) Arbitrary — pick any port
B) The Azure MCP container listens on 8080 by default; ACA needs to know which port to forward HTTPS to
C) It's a Linux convention
D) Required by managed identity

<details><summary>Answer</summary>

**B.** Confirmed by the official azd template in `microsoft/mcp`.

</details>

### Question 2
What does `--outgoing-auth-strategy UseHostingEnvironmentIdentity` do?

A) Logs in the user
B) Tells Azure MCP to use the container's managed identity (ACA's "hosting environment identity") when calling Azure
C) Encrypts the connection
D) Enables HTTPS

<details><summary>Answer</summary>

**B.** Same identity is used for *every* incoming caller — fine when all callers should have the same Azure permissions. The alternative is `UseOnBehalfOf` (token exchange per caller).

</details>

---

## Next

→ [4.3 — Connect from Copilot CLI](./03-connect-from-copilot.md)
