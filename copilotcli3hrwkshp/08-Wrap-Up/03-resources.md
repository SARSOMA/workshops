# Resources & Further Learning

## Official Documentation

### GitHub Copilot CLI

- **Getting Started**: [docs.github.com/copilot/using-github-copilot/using-github-copilot-in-the-command-line](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line)
- **Built-in Help**: Run `copilot --help` or use `/help` in session
- **Changelog**: Check for updates with `copilot --version`

### GitHub Copilot General

- **Overview**: [github.com/features/copilot](https://github.com/features/copilot)
- **Documentation**: [docs.github.com/copilot](https://docs.github.com/en/copilot)
- **Copilot for Business**: [docs.github.com/copilot/overview-of-github-copilot/about-github-copilot-for-business](https://docs.github.com/en/copilot/overview-of-github-copilot/about-github-copilot-for-business)

---

## MCP (Model Context Protocol)

### MCP Specification

- **Official Spec**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- **MCP Servers Directory**: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

### Available MCP Servers

| Server | Purpose |
|--------|---------|
| GitHub (built-in) | GitHub operations |
| Azure DevOps | ADO integration |
| Filesystem | File operations |
| PostgreSQL/MySQL | Database queries |
| Brave Search | Web search |
| Fetch | HTTP requests |

---

## Learning Resources

### Prompt Engineering

- **Prompt Engineering Guide**: [promptingguide.ai](https://www.promptingguide.ai)
- **GitHub Copilot Prompting Guide**: Search GitHub docs for latest tips

### AI-Assisted Development

- **AI Pair Programming Patterns**: Community blog posts and tutorials
- **GitHub Blog**: [github.blog](https://github.blog) (search for Copilot)

---

## Community & Support

### Get Help

- **GitHub Community Discussions**: [github.com/orgs/community/discussions](https://github.com/orgs/community/discussions)
- **GitHub Support**: [support.github.com](https://support.github.com)
- **Stack Overflow**: Tag questions with `github-copilot`

### Report Issues

- **Feedback**: Use the feedback mechanisms in Copilot CLI
- **Bug Reports**: Through GitHub Support

---

## Related Tools

### VS Code Extensions

- **GitHub Copilot**: In-editor AI suggestions
- **GitHub Copilot Chat**: IDE-based chat interface
- **GitHub Copilot Labs**: Experimental features

### CLI Tools That Pair Well

| Tool | Purpose |
|------|---------|
| `gh` | GitHub CLI for issues, PRs |
| `az` | Azure CLI for cloud ops |
| `jq` | JSON processing |
| `fzf` | Fuzzy finding |

---

## Cheat Sheet

### Essential Commands

```bash
# Start Copilot
copilot                      # New session
copilot --continue           # Resume last session

# In-Session Commands
/help                        # Show all commands
/clear                       # Clear context
/context                     # Show loaded context
/diff                        # Show pending changes
/review                      # Code review
/compact                     # Reduce context
/mcp                         # Manage MCP servers
/exit                        # End session

# Keyboard Shortcuts
Shift+Tab                    # Toggle mode
Ctrl+T                       # Toggle reasoning
Ctrl+C                       # Cancel operation

# File/Reference Syntax
@filename                    # Include file
#123                         # Reference issue/PR
!command                     # Run shell command
```

### Configuration Locations

```
~/.copilot/
├── settings.json            # User settings
├── mcp-config.json          # MCP configuration  
└── copilot-instructions.md  # User instructions

.github/
└── copilot-instructions.md  # Repo instructions
```

---

## Workshop Files

All materials from this workshop are available in your Workshop01 directory:

```
Workshop01/
├── 00-Prerequisites/
├── 01-Introduction-Setup/
├── 02-Core-Concepts-Architecture/
├── 03-Context-Management/
├── 04-CLI-Fundamentals/
├── 05-Advanced-Capabilities/
├── 06-MCP-Extensibility/
├── 08-End-to-End-Workflows/
└── 09-Wrap-Up/
```

---

## What's Next?

### Immediate (This Week)

1. Use Copilot CLI for a real task at work
2. Set up instruction files for your main project
3. Practice the keyboard shortcuts

### Short Term (This Month)

1. Create a custom agent for repeated tasks
2. Add MCP servers for tools you use
3. Share tips with teammates

### Long Term

1. Stay updated with new features
2. Explore advanced MCP integrations
3. Contribute to community knowledge

---

## Feedback on This Workshop

We'd love to hear your feedback:

- What worked well?
- What could be improved?
- What topics need more depth?
- What's missing?

---

## Thank You!

Thanks for participating in this GitHub Copilot CLI Workshop!

Remember:
> The best way to learn is by doing. Start using Copilot CLI today!

---

**Happy coding with your AI pair programmer!** 🚀
