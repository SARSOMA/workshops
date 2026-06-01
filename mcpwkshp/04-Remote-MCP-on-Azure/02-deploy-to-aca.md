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
                                                     │         --outgoing-auth-strategy
                                                     │             UseHostingEnvironmentIdentity
                                                     │
                                                     ├─ env:   ASPNETCORE_URLS=http://0.0.0.0:5000
                                                     │         ALLOW_INSECURE_EXTERNAL_BINDING=true
                                                     │         AZURE_TOKEN_CREDENTIALS=
                                                     │             ManagedIdentityCredential
                                                     │
                                                     ├─ targetPort 5000  (HTTPS ingress)
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
  --target-port 5000 \
  --ingress external \
  --transport http \
  --system-assigned \
  --min-replicas 1 --max-replicas 1 \
  --cpu 0.5 --memory 1.0Gi \
  --env-vars \
      ASPNETCORE_ENVIRONMENT=Production \
      ASPNETCORE_URLS=http://0.0.0.0:5000 \
      ALLOW_INSECURE_EXTERNAL_BINDING=true \
      AZURE_TOKEN_CREDENTIALS=ManagedIdentityCredential \
      AZURE_MCP_DANGEROUSLY_DISABLE_HTTPS_REDIRECTION=true \
      AZURE_MCP_DANGEROUSLY_ENABLE_FORWARDED_HEADERS=true \
  --args "--transport, http, --read-only, --outgoing-auth-strategy, UseHostingEnvironmentIdentity, --dangerously-disable-http-incoming-auth"
```

> ⚠️ **Quote `--args` as a single string.** `az containerapp create --args` expects
> one space-separated string, not multiple shell tokens. Writing
> `--args "--transport" "http" "--mode" "all"` looks right but az treats only the
> first quoted token as the value and silently drops the rest, so the container
> starts with only `--transport` and exits.

> ⚠️ **Don't put `server start` in `--args`.** The image's `ENTRYPOINT` is already
> `["./server-binary", "server", "start"]`. Anything you pass via `--args` is
> *appended* to that, so adding `server start` produces
> `… server start server start --transport http …` → "Unrecognized command or
> argument 'server'" → container exits with code 1, no logs.

What each piece does:

| Flag / env var | Purpose |
|---|---|
| `--image …azure-mcp:latest` | Microsoft's published Azure MCP image |
| `--target-port 5000` | Must match `ASPNETCORE_URLS` below |
| `--ingress external --transport http` | Public HTTPS endpoint (ACA terminates TLS, forwards plain HTTP to the container) |
| `--system-assigned` | Creates the managed identity Azure MCP will use for outgoing Azure calls |
| `ASPNETCORE_URLS=http://0.0.0.0:5000` | Bind Kestrel to all interfaces. Without this, the server binds to `localhost` only and ACA ingress can't reach it. |
| `ALLOW_INSECURE_EXTERNAL_BINDING=true` | **Required** when you combine `--dangerously-disable-http-incoming-auth` with a non-loopback bind address. Without it, the server refuses to start and the container exits with code 1. |
| `AZURE_TOKEN_CREDENTIALS=ManagedIdentityCredential` | Tells `DefaultAzureCredential` to use the container's managed identity. The default chain in this image excludes MI — so without this, outgoing Azure calls fail with 401 even though the MI exists. |
| `AZURE_MCP_DANGEROUSLY_DISABLE_HTTPS_REDIRECTION=true` | ACA terminates TLS; the container sees plain HTTP. Skip the in-app HTTPS redirect. |
| `AZURE_MCP_DANGEROUSLY_ENABLE_FORWARDED_HEADERS=true` | Trust `X-Forwarded-Proto` from ACA so OAuth/metadata URLs use `https`. |
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

echo "Azure MCP URL: https://$FQDN/"
```

Save that URL — you'll paste it in §4.3.

> ⚠️ **The MCP endpoint is the FQDN root (`/`)**, not `/mcp`. Hitting `/mcp` returns
> `404 Not Found`. This trips up everyone the first time.

### Step 6 — Smoke test the endpoint

```bash
curl -s -i "https://$FQDN/" -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}'
```

You should get back a `200` with:

- response header `mcp-session-id: <some-id>` — capture this for subsequent calls
- `Content-Type: text/event-stream` — the response is SSE, not plain JSON
- a `data:` line whose payload is the JSON-RPC `initialize` result (server name, version, capabilities)

If you get `404` the URL is wrong (probably ends in `/mcp`). If you get a TLS
error or HTML, give ACA another ~30 seconds — first-revision warm-up can be slow.

The full handshake (initialize → initialized → tools/list → tools/call) is
walked through in §4.4.

---

## Troubleshooting

| Symptom | Likely fix |
|---------|-----------|
| `az containerapp create` fails: "extension not installed" | `az extension add --name containerapp --upgrade` |
| Container immediately exits with code 1, no logs | You forgot `ALLOW_INSECURE_EXTERNAL_BINDING=true` *or* you accidentally added `server start` to `--args` (it's already in the image ENTRYPOINT) |
| Container starts but ingress returns 404 / "no healthy upstream" | `--target-port` doesn't match the port in `ASPNETCORE_URLS` |
| `curl` to `/mcp` returns 404 | The MCP endpoint is `/`, not `/mcp` |
| `tools/call` returns 401 from Azure | `AZURE_TOKEN_CREDENTIALS` env var missing → DefaultAzureCredential isn't trying the MI |
| `subscription_list` returns an empty array | Reader role was assigned at RG scope, not subscription scope; or propagation isn't done (wait 60s) |
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
Why do we set `--target-port 5000`?

A) Arbitrary — pick any port
B) It must match the port in `ASPNETCORE_URLS` — that's what Kestrel binds to inside the container; ACA's ingress forwards HTTPS to that port
C) It's a Linux convention
D) Required by managed identity

<details><summary>Answer</summary>

**B.** We set `ASPNETCORE_URLS=http://0.0.0.0:5000`, so Kestrel listens on 5000; `--target-port` tells the ACA ingress where to forward.

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
→ [4.4 — The MCP handshake, on the wire](./04-mcp-handshake.md)
→ [4.5 — Auth deep-dive](./05-auth-deep-dive.md)
