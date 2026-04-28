# GitHub Copilot CLI Workshop - Prerequisites

> **📧 Please complete these steps at least 2 days before the workshop**

Welcome to the GitHub Copilot CLI Workshop! Complete this setup guide so you're ready to hit the ground running.

## ⏱️ Estimated Setup Time

15-20 minutes

---

## ✅ Checklist Summary

| Requirement | Status |
|-------------|--------|
| GitHub Account with Copilot Access | ⬜ |
| GitHub Copilot CLI Installed | ⬜ |
| Authentication Complete | ⬜ |
| Git Configured | ⬜ |
| Terminal Ready | ⬜ |
| Verification Successful | ⬜ |

---

## 1. GitHub Account & Copilot Access

### Required
- A GitHub.com account
- An **active GitHub Copilot subscription** (Individual, Business, or Enterprise)

### Verify Your Access
1. Go to [github.com/settings/copilot](https://github.com/settings/copilot)
2. Confirm you see "GitHub Copilot is active"

> **💡 Note:** If you have access through your organization, ensure your admin has enabled GitHub Copilot CLI.

---

## 2. Install GitHub Copilot CLI

Choose your installation method:

### Option A: Install Script (macOS & Linux) — Recommended
```bash
curl -fsSL https://gh.io/copilot-install | bash
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

## 3. Terminal Setup

### Windows
GitHub Copilot CLI requires **PowerShell 6 or higher**.

Check your version:
```powershell
$PSVersionTable.PSVersion
```

If you have version 5.x or lower, install PowerShell 7:
```powershell
winget install Microsoft.PowerShell
```

### macOS / Linux
Any terminal works. No additional setup needed.

---

## 4. Authenticate with GitHub

1. Start Copilot CLI:
   ```bash
   copilot
   ```

2. On first launch, use the `/login` command:
   ```
   /login
   ```

3. Follow on-screen instructions:
   - A browser window opens
   - Authorize GitHub Copilot CLI
   - Return to your terminal

4. Verify authentication — you should see your username displayed

---

## 5. Git Configuration

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

## 6. Final Verification

### Step 1: Launch Copilot CLI
```bash
copilot
```

### Step 2: Ask a Simple Question
```
What is GitHub Copilot CLI?
```

### Step 3: Check Available Commands
```
/help
```

### Step 4: Exit
```
/exit
```

### ✅ Success Criteria
- [ ] Copilot CLI launches without errors
- [ ] You can see the welcome screen
- [ ] You're authenticated (your GitHub username is visible)
- [ ] You can get a response to a simple question

---

## 🆘 Troubleshooting

### "copilot: command not found"
- Restart your terminal after installation
- Verify the installation path is in your `$PATH`

### Authentication Issues
- Ensure you're logged into GitHub in your browser
- Try `/logout` then `/login` again
- Check if your organization has enabled Copilot CLI

### PowerShell Version Error (Windows)
- Install PowerShell 7: `winget install Microsoft.PowerShell`
- Launch with: `pwsh` instead of `powershell`

### Network/Proxy Issues
```bash
export HTTPS_PROXY=http://proxy.example.com:8080
export HTTP_PROXY=http://proxy.example.com:8080
```

---

## 📚 Optional Pre-Reading

- [About GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli/about-github-copilot-in-the-cli)
- [Using GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli/using-github-copilot-in-the-cli)

---

## 📧 Need Help?

If you encounter issues:
1. Try the troubleshooting steps above
2. Check [GitHub Community Discussions](https://github.com/orgs/community/discussions)
3. Reach out to the workshop organizer

---

**See you at the workshop! 🚀**
