# §4 — Remote MCP on Azure (25 min)

**Goal**: take Microsoft's official **Azure MCP Server** (`microsoft/mcp` → image `mcr.microsoft.com/azure-sdk/azure-mcp:latest`), deploy it as an HTTPS-reachable service on **Azure Container Apps**, and call it from GitHub Copilot CLI as a **remote** MCP server.

This is the big "aha": once an MCP server is reachable over HTTP, *any* MCP-capable client can use it. Same protocol, different transport.

## Pages

1. [01-azure-mcp-intro.md](./01-azure-mcp-intro.md) — what Azure MCP is and why we host it
2. [02-deploy-to-aca.md](./02-deploy-to-aca.md) — `az` commands, end to end
3. [03-connect-from-copilot.md](./03-connect-from-copilot.md) — wire the ACA URL into Copilot CLI
4. [04-auth-deep-dive.md](./04-auth-deep-dive.md) — incoming vs outgoing auth, OAuth 2.1, On-Behalf-Of

## Deployment script

[`manifests/deploy.azcli`](./manifests/deploy.azcli) bundles every command in §4.2 into one script — handy if you want to re-deploy or share with a teammate.

## Cleanup

When you're done, run `az group delete -n rg-mcp-demo --yes --no-wait` to remove everything we created.
