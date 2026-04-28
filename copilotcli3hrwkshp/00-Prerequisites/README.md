# GitHub Copilot CLI Workshop - Prerequisites

> **📧 Please complete these steps at least 2 days before the workshop**

Welcome to the GitHub Copilot CLI Workshop! This document will help you prepare your environment so you can hit the ground running on workshop day.

## ⏱️ Estimated Setup Time

15-30 minutes (depending on your current environment)

---

## ✅ Checklist Summary

| Requirement | Status |
|-------------|--------|
| GitHub Account with Copilot Access | ⬜ |
| VS Code Installed | ⬜ |
| Terminal Setup | ⬜ |
| GitHub Copilot CLI Installed | ⬜ |
| Authentication Complete | ⬜ |
| Git Configured | ⬜ |
| Verification Successful | ⬜ |

---

## 1. GitHub Account & Copilot Access

### Required
- A GitHub.com account
- An **active GitHub Copilot subscription** (Individual, Business, or Enterprise)

### Verify Your Access
1. Go to [github.com/settings/copilot](https://github.com/settings/copilot)
2. Confirm you see "GitHub Copilot is active" or similar

> **💡 Note:** If you have access through your organization, ensure your admin has enabled GitHub Copilot CLI. Contact your organization admin if you're unsure.

### Don't Have Copilot?
- [Sign up for GitHub Copilot](https://github.com/features/copilot/plans) (free trial available)

---

## 2. VS Code Installation

We'll use VS Code with the integrated terminal for this workshop.

### Install VS Code
Download and install from: [code.visualstudio.com](https://code.visualstudio.com/)

### Recommended Extensions (Optional)
- **GitHub Copilot** - For comparison with CLI experience
- **GitHub Pull Requests** - For PR workflow demonstrations

---

## 3. Terminal Setup

### Windows
GitHub Copilot CLI requires **PowerShell 6 or higher**.

1. Check your PowerShell version:
   ```powershell
   $PSVersionTable.PSVersion
   ```

2. If you have version 5.x or lower, install PowerShell 7:
   - Download from [PowerShell GitHub releases](https://github.com/PowerShell/PowerShell/releases)
   - Or use winget:
     ```powershell
     winget install Microsoft.PowerShell
     ```

3. **Alternative:** Use Windows Subsystem for Linux (WSL)
   ```powershell
   wsl --install
   ```

### macOS
The default Terminal or iTerm2 works great. No additional setup needed.

### Linux
Any terminal emulator works (GNOME Terminal, Konsole, etc.). No additional setup needed.

---

## 4. Install GitHub Copilot CLI

Choose your installation method:

### Option A: Install Script (macOS & Linux) - Recommended
```bash
curl -fsSL https://gh.io/copilot-install | bash
```

Or with wget:
```bash
wget -qO- https://gh.io/copilot-install | bash
```

### Option B: Homebrew (macOS & Linux)
```bash
brew install copilot-cli
```

### Option C: WinGet (Windows)
```powershell
winget install GitHub.Copilot
```

### Option D: npm (All Platforms)
```bash
npm install -g @github/copilot
```

### Verify Installation
```bash
copilot --version
```

You should see output like: `copilot version 1.x.x`

---

## 5. Authenticate with GitHub

1. Start Copilot CLI:
   ```bash
   copilot
   ```

2. On first launch, you'll see the welcome screen. Use the `/login` command:
   ```
   /login
   ```

3. Follow the on-screen instructions:
   - A browser window will open
   - Authorize GitHub Copilot CLI
   - Return to your terminal

4. Verify authentication succeeded - you should see your username displayed

---

## 6. Git Configuration

Ensure Git is installed and configured:

### Check Git Installation
```bash
git --version
```

If not installed:
- **Windows:** Download from [git-scm.com](https://git-scm.com/)
- **macOS:** `xcode-select --install` or `brew install git`
- **Linux:** `sudo apt install git` or equivalent

### Configure Git Identity
```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

---

## 7. Final Verification

Run this verification checklist:

### Step 1: Launch Copilot CLI
```bash
copilot
```

### Step 2: Ask a Simple Question
Type this prompt and press Enter:
```
What is GitHub Copilot CLI?
```

### Step 3: Check Available Commands
```
/help
```

### Step 4: Verify GitHub Connection
```
List my GitHub repositories
```

### Step 5: Exit the Session
```
/exit
```

### ✅ Success Criteria
- [ ] Copilot CLI launches without errors
- [ ] You can see the welcome screen
- [ ] You're authenticated (your GitHub username is visible)
- [ ] You can get a response to a simple question
- [ ] The `/help` command shows available commands

---

## 🆘 Troubleshooting

### "copilot: command not found"
- Restart your terminal after installation
- Verify the installation path is in your `$PATH`
- Try reinstalling with a different method

### Authentication Issues
- Ensure you're logged into GitHub in your browser
- Try `/logout` then `/login` again
- Check if your organization has enabled Copilot CLI

### PowerShell Version Error (Windows)
- Install PowerShell 7: `winget install Microsoft.PowerShell`
- Launch with: `pwsh` instead of `powershell`

### Network/Proxy Issues
If you're behind a corporate proxy:
```bash
export HTTPS_PROXY=http://proxy.example.com:8080
export HTTP_PROXY=http://proxy.example.com:8080
```

### Rate Limiting
If you see rate limit errors:
- Each prompt uses your premium request quota
- Check your quota at [github.com/settings/copilot](https://github.com/settings/copilot)

---

## 📚 Pre-Workshop Reading (Optional)

If you want to get ahead:

1. [About GitHub Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)
2. [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
3. [GitHub Copilot CLI Best Practices](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices)

---

## 📧 Need Help?

If you encounter issues during setup:
1. Try the troubleshooting steps above
2. Check [GitHub Community Discussions](https://github.com/orgs/community/discussions)
3. Reach out to the workshop organizer

---

**See you at the workshop! 🚀**
