# §4 — Remote MCP on Azure (25 min)

> ## ⚠️ Demo only — do not use this config in production
>
> Throughout this section we deploy with `--dangerously-disable-http-incoming-auth`,
> which **turns off authentication on the MCP endpoint**. Anyone who knows the URL
> can call your server and act with the managed identity's permissions on your
> Azure subscription.
>
> We do this so the workshop runs in 25 minutes without an Entra app registration
> dance. **For real deployments, enable Entra OAuth on the inbound** — see
> [§4.5 — Auth deep dive](./05-auth-deep-dive.md) for the production setup.
>
> Use a **throwaway subscription** for the workshop, and run
> `az group delete -n rg-mcp-demo --yes --no-wait` when you're done.

---

**Goal**: take Microsoft's official **Azure MCP Server** (`microsoft/mcp` → image `mcr.microsoft.com/azure-sdk/azure-mcp:latest`), deploy it as an HTTPS-reachable service on **Azure Container Apps**, and call it from GitHub Copilot CLI as a **remote** MCP server.

This is the big "aha": once an MCP server is reachable over HTTP, *any* MCP-capable client can use it. Same protocol, different transport.

## Pages

1. [01-azure-mcp-intro.md](./01-azure-mcp-intro.md) — what Azure MCP is and why we host it
2. [02-deploy-to-aca.md](./02-deploy-to-aca.md) — `az` commands, end to end
3. [03-connect-from-copilot.md](./03-connect-from-copilot.md) — wire the ACA URL into Copilot CLI
4. [04-mcp-handshake.md](./04-mcp-handshake.md) — the actual JSON-RPC traffic, on the wire
5. [05-auth-deep-dive.md](./05-auth-deep-dive.md) — incoming vs outgoing auth, OAuth 2.1, On-Behalf-Of

## Deployment script

[`manifests/deploy.azcli`](./manifests/deploy.azcli) bundles every command in §4.2 into one script — handy if you want to re-deploy or share with a teammate.

## Cleanup

When you're done, run `az group delete -n rg-mcp-demo --yes --no-wait` to remove everything we created.
