# GitHub Copilot CLI Workshop

## Workshop Overview

This comprehensive workshop covers GitHub Copilot CLI from basics to advanced usage, including hands-on exercises and real-world workflows.

**Duration**: 3-4 hours (half day)  
**Audience**: Developers of all experience levels  
**Platforms**: Windows, macOS, Linux  

---

## Table of Contents

| Section | Title | Duration | Description |
|---------|-------|----------|-------------|
| [00](./00-Prerequisites/) | Prerequisites | Pre-work | Setup before the workshop |
| [01](./01-Introduction-Setup/) | Introduction & Setup | 20 min | What is Copilot CLI, first launch |
| [02](./02-Core-Concepts-Architecture/) | Core Concepts | 25 min | Architecture, configuration, context |
| [03](./03-Context-Management/) | Context Management | 20 min | Prompt engineering, sessions |
| [04](./04-CLI-Fundamentals/) | CLI Fundamentals | 30 min | Commands, modes, workflows |
| [05](./05-Advanced-Capabilities/) | Advanced Capabilities | 25 min | Custom agents, skills, automation |
| [06](./06-MCP-Extensibility/) | MCP Extensibility | 25 min | MCP servers, Azure DevOps |
| [07](./07-End-to-End-Workflows/) | End-to-End Workflows | 45 min | Hands-on scenarios |
| [08](./08-Wrap-Up/) | Wrap-Up | 15 min | Takeaways, best practices |

**Total**: ~3.5 hours (excluding breaks)

---

## Prerequisites

**Complete before the workshop!**

Send [00-Prerequisites/README.md](./00-Prerequisites/README.md) to participants 2 days prior.

Checklist:
- [ ] GitHub account with Copilot license
- [ ] Node.js 20+ installed
- [ ] Copilot CLI installed (`npm install -g @anthropic/copilot-cli`)
- [ ] Authenticated (`copilot auth login`)
- [ ] VS Code with terminal (recommended)

---

## Section Summaries

### Section 1: Introduction & Setup
- What is Copilot CLI and how it differs from IDE Copilot
- First launch and interface exploration
- Security model and trust boundaries

### Section 2: Core Concepts & Architecture  
- The agentic loop and tool layer
- Configuration hierarchy (CLI > Env > Repo > User > Org)
- Context window management and auto-compaction

### Section 3: Context Management
- Effective prompt engineering techniques
- Session management and resumption
- Workflow patterns and anti-patterns

### Section 4: CLI Fundamentals
- Complete command and shortcut reference
- Interactive, Plan, and Autopilot modes
- Practical terminal workflows

### Section 5: Advanced Capabilities
- Creating custom agent profiles
- Skills and automation templates
- Programmatic usage and CI/CD integration

### Section 6: MCP Extensibility
- Model Context Protocol concepts
- Adding and configuring MCP servers
- Azure DevOps integration (PAT setup, workflows)

### Section 7: End-to-End Workflows
- **Scenario 7.1**: Complete PR workflow
- **Scenario 7.2**: Code review with Copilot
- **Scenario 7.3**: Addressing PR feedback
- **Scenario 7.4**: Pipeline debugging

### Section 8: Wrap-Up
- Key takeaways and mental models
- Best practices and common pitfalls
- Resources for continued learning

---

## Suggested Schedule

### Morning Session (2 hours)

| Time | Section | Activity |
|------|---------|----------|
| 0:00 | Section 1 | Introduction & Setup |
| 0:20 | Section 2 | Core Concepts |
| 0:45 | Section 3 | Context Management |
| 1:05 | Break | 10 minutes |
| 1:15 | Section 4 | CLI Fundamentals |
| 1:45 | Section 5 | Advanced Capabilities |

### Afternoon Session (1.5 hours)

| Time | Section | Activity |
|------|---------|----------|
| 0:00 | Section 6 | MCP Extensibility |
| 0:25 | Section 7 | Hands-on Workflows |
| 1:10 | Section 8 | Wrap-Up & Q&A |

---

## Files Structure

```
Workshop01/
├── README.md                           # This file
├── requirement.txt                     # Original requirements
│
├── 00-Prerequisites/
│   └── README.md                       # Pre-workshop setup guide
│
├── 01-Introduction-Setup/
│   ├── README.md
│   ├── 01-overview.md
│   └── 02-setup.md
│
├── 02-Core-Concepts-Architecture/
│   ├── README.md
│   ├── 01-architecture.md
│   ├── 02-configuration.md
│   └── 03-context.md
│
├── 03-Context-Management/
│   ├── README.md
│   ├── 01-prompt-engineering.md
│   └── 02-session-management.md
│
├── 04-CLI-Fundamentals/
│   ├── README.md
│   ├── 01-commands-shortcuts.md
│   ├── 02-modes-interaction.md
│   └── 03-terminal-workflows.md
│
├── 05-Advanced-Capabilities/
│   ├── README.md
│   ├── 01-custom-agents.md
│   ├── 02-skills-automation.md
│   └── 03-programmatic-usage.md
│
├── 06-MCP-Extensibility/
│   ├── README.md
│   ├── 01-mcp-introduction.md
│   ├── 02-mcp-configuration.md
│   └── 03-azure-devops.md
│
├── 07-End-to-End-Workflows/
│   ├── README.md
│   ├── 01-pr-workflow.md
│   ├── 02-code-review.md
│   ├── 03-addressing-feedback.md
│   └── 04-pipeline-debugging.md
│
└── 08-Wrap-Up/
    ├── README.md
    ├── 01-key-takeaways.md
    ├── 02-best-practices.md
    └── 03-resources.md
```

---

## Quick Reference

### Essential Commands

```bash
copilot                    # Start new session
copilot --continue         # Resume previous session
Shift+Tab                  # Switch modes
/help                      # Show commands
/clear                     # Clear context
/context                   # Show loaded context
/diff                      # Show changes
/review                    # Code review
/mcp                       # Manage MCP servers
```

### File Syntax

```
@filename                  # Include file
@directory/                # Include directory info
#123                       # Reference issue/PR
!command                   # Run shell command
```

---

## Contributing

Feedback and improvements welcome! Please submit issues or pull requests.

---

**Happy learning!** 🚀
