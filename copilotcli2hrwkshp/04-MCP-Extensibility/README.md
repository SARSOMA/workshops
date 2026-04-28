# Section 4: MCP & Advanced Features

## Overview

This is the **core hands-on section** of the workshop. We'll cover Model Context Protocol (MCP), configure multiple MCP servers (Azure, ADO, WorkIQ, Bluebird), introduce Skills for automation, and create Custom Agents.

## Learning Objectives

By the end of this section, you will be able to:
- Explain what MCP is and why it matters
- Configure MCP servers: Azure MCP, ADO MCP, WorkIQ MCP, Bluebird MCP
- Understand where MCP configurations are stored
- Use Skills for repeatable tasks
- Create and use Custom Agents

## Duration

**35 minutes**

## Tutorials

| Tutorial | Duration | Description |
|----------|----------|-------------|
| [4.1 MCP Overview](./01-mcp-overview.md) | 8 min | What is MCP, architecture, built-in servers |
| [4.2 Configuring MCPs](./02-configuring-mcps.md) | 12 min | Azure, ADO, WorkIQ, Bluebird setup |
| [4.3 Skills](./03-skills.md) | 8 min | Using and understanding Skills |
| [4.4 Custom Agents](./04-custom-agents.md) | 7 min | Creating custom agents |

## Prerequisites

- Completed Sections 1-3
- Working Copilot CLI installation
- (Optional) Azure DevOps access for ADO MCP exercises

## Key Takeaways

- MCP enables Copilot CLI to integrate with external systems
- Configuration lives in `~/.copilot/mcp.json`
- Skills automate repeatable workflows
- Custom Agents provide specialized behavior for specific tasks
