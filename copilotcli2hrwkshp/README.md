# GitHub Copilot CLI Workshop (2-Hour Edition)

## Workshop Overview

A crisp, hands-on workshop covering GitHub Copilot CLI from fundamentals to advanced MCP integrations and real-world workflows.

**Duration**: 2 hours  
**Audience**: Developers of all experience levels  
**Platforms**: Windows, macOS, Linux  

---

## Table of Contents

| Section | Title | Duration | Description |
|---------|-------|----------|-------------|
| [00](./00-Prerequisites/) | Prerequisites | Pre-work | Setup before the workshop |
| [01](./01-Introduction-Setup/) | Introduction & Setup | 15 min | What is Copilot CLI, first launch |
| [02](./02-Core-Concepts/) | Core Concepts | 10 min | Architecture, configuration, context |
| [03](./03-CLI-Fundamentals/) | CLI Fundamentals | 15 min | Commands, modes, workflows |
| [04](./04-MCP-Extensibility/) | MCP & Advanced Features | 35 min | MCP servers, skills, custom agents |
| [05](./05-End-to-End-Workflows/) | End-to-End Workflows | 35 min | Real project: understand, change, PR, review |
| [06](./06-Wrap-Up/) | Wrap-Up | 10 min | Takeaways and resources |

**Total**: ~120 minutes

---

## Prerequisites

**Complete before the workshop!**

Send [00-Prerequisites/README.md](./00-Prerequisites/README.md) to participants **2 days prior**.

Quick Checklist:
- [ ] GitHub account with Copilot license
- [ ] GitHub Copilot CLI installed
- [ ] Authenticated with GitHub
- [ ] Git configured
- [ ] Terminal ready (PowerShell 6+ on Windows)

---

## Section Format

Each section follows the **Concept → Practice → Q&A** structure:

1. **Concept**: Brief explanation of key ideas
2. **Practice**: Hands-on prompts to try in Copilot CLI
3. **Q&A**: Multiple choice questions to test understanding

---

## Schedule

| Time | Section | Activity |
|------|---------|----------|
| 0:00 | Section 1 | Introduction & Setup |
| 0:15 | Section 2 | Core Concepts |
| 0:25 | Section 3 | CLI Fundamentals |
| 0:40 | **Break** | 5 minutes |
| 0:45 | Section 4 | MCP & Advanced Features |
| 1:20 | Section 5 | End-to-End Workflows |
| 1:55 | Section 6 | Wrap-Up & Q&A |

---

## Hands-On Project

This workshop uses the public GitHub repository **[SARSOMA/akri](https://github.com/SARSOMA/akri)** for hands-on exercises:

- Understanding a new codebase
- Making changes via Copilot CLI
- Creating and reviewing pull requests
- Practicing code review from the command line

---

## Quick Reference

### Essential Commands

```bash
copilot                    # Start new session
copilot --continue         # Resume previous session
Shift+Tab                  # Switch modes (Interactive ↔ Plan ↔ Auto)
/help                      # Show commands
/clear                     # Clear context
/mcp                       # Manage MCP servers
/diff                      # Show pending changes
/review                    # Code review
```

### File Syntax

```
@filename                  # Include file in context
@directory/                # Include directory info
#123                       # Reference issue/PR
!command                   # Run shell command
```

---

## Files Structure

```
copilotcli2hrwkshp/
├── README.md                           # This file
├── requirement.txt                     # Original requirements
│
├── 00-Prerequisites/
│   └── README.md                       # Pre-workshop setup guide
│
├── 01-Introduction-Setup/
│   ├── README.md                       # Section overview
│   └── 01-overview.md                  # Concept + Practice + Q&A
│
├── 02-Core-Concepts/
│   ├── README.md                       # Section overview
│   └── 01-architecture-config.md       # Concept + Practice + Q&A
│
├── 03-CLI-Fundamentals/
│   ├── README.md                       # Section overview
│   └── 01-commands-modes.md            # Concept + Practice + Q&A
│
├── 04-MCP-Extensibility/
│   ├── README.md                       # Section overview
│   ├── 01-mcp-overview.md              # MCP concepts
│   ├── 02-configuring-mcps.md          # Azure, ADO, WorkIQ, Bluebird
│   ├── 03-skills.md                    # Skills introduction
│   └── 04-custom-agents.md             # Custom agents
│
├── 05-End-to-End-Workflows/
│   ├── README.md                       # Section overview
│   ├── 01-project-setup.md             # Clone and understand akri
│   ├── 02-making-changes.md            # Make changes via CLI
│   ├── 03-pr-workflow.md               # Create PR
│   └── 04-code-review.md               # Review and comment
│
└── 06-Wrap-Up/
    └── README.md                       # Takeaways and resources
```

---

## Contributing

Feedback and improvements welcome! Please submit issues or pull requests.

---

**Let's get started! 🚀**
