# Complete WSL Development Environment Setup for GitHub Copilot CLI

A consolidated step-by-step guide to setting up Windows Subsystem for Linux (WSL) with all essential development tools for modern cloud-native development with GitHub Copilot CLI.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Install WSL](#install-wsl)
3. [Configure WSL for Optimal Performance](#configure-wsl-for-optimal-performance)
4. [Install Essential Linux Packages](#install-essential-linux-packages)
5. [Install Python](#install-python)
6. [Install Node.js and npm](#install-nodejs-and-npm)
7. [Install Azure CLI](#install-azure-cli)
8. [Install GitHub CLI](#install-github-cli)
9. [Install GitHub Copilot CLI](#install-github-copilot-cli)
10. [Configure Git](#configure-git)
11. [VS Code Integration](#vs-code-integration)
12. [Verification Checklist](#verification-checklist)
13. [Quick Reference](#quick-reference)

---

## Prerequisites

- **Windows 10 version 2004+** (Build 19041+) or **Windows 11**
- **Administrator access** to your Windows machine
- **Active GitHub Copilot subscription** (Individual, Business, or Enterprise)
- **Virtualization enabled** in BIOS (usually enabled by default)

---

## Install WSL

### Step 1: Enable WSL Feature

Open **PowerShell as Administrator** and run:

```powershell
# Install WSL with Ubuntu (default distribution)
wsl --install

# If WSL is already installed, just install Ubuntu
wsl --install -d Ubuntu
```

**Restart your computer** when prompted.

### Step 2: First Launch & User Setup

After restart, Ubuntu will launch automatically. Create your Linux username and password:

```
Enter new UNIX username: yourusername
New password: ********
Retype new password: ********
```

> ⚠️ **Important**: This password is for `sudo` commands inside Linux. Remember it!

### Step 3: Verify WSL 2 Installation

```powershell
# In PowerShell
wsl --list --verbose

# Expected output:
#   NAME      STATE           VERSION
# * Ubuntu    Running         2
```

If VERSION shows 1, upgrade to WSL 2:

```powershell
wsl --set-version Ubuntu 2
```

### Step 4: Update WSL

```powershell
wsl --update
wsl --version
```

---

## Configure WSL for Optimal Performance

### Create WSL Configuration File

Create `%USERPROFILE%\.wslconfig` (Windows side) for VM-level settings:

```powershell
# In PowerShell - create .wslconfig
notepad "$env:USERPROFILE\.wslconfig"
```

Add these optimized settings:

```ini
[wsl2]
memory=8GB
processors=4
swap=4GB
localhostForwarding=true

# Enable mirrored networking (Windows 11 22H2+)
networkingMode=mirrored

[experimental]
autoMemoryReclaim=gradual
sparseVhd=true
```

### Configure Linux-Side Settings

Inside WSL, create `/etc/wsl.conf`:

```bash
sudo nano /etc/wsl.conf
```

Add:

```ini
[automount]
enabled = true
root = /mnt/
options = "metadata,umask=22,fmask=11"

[interop]
enabled = true
appendWindowsPath = true

[boot]
systemd = true

[network]
generateHosts = true
generateResolvConf = true
```

**Apply changes:**

```powershell
# In PowerShell
wsl --shutdown
wsl
```

---

## Install Essential Linux Packages

### Update Package Lists

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Core Development Tools

```bash
# Build essentials (compilers, make, etc.)
sudo apt install -y build-essential

# Essential utilities
sudo apt install -y \
    curl \
    wget \
    git \
    unzip \
    zip \
    jq \
    tree \
    htop \
    vim \
    nano

# Networking tools
sudo apt install -y \
    ca-certificates \
    apt-transport-https \
    lsb-release \
    gnupg \
    openssh-client \
    net-tools \
    dnsutils

# Development libraries
sudo apt install -y \
    libssl-dev \
    libffi-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    liblzma-dev
```

---

## Install Python

### Option A: Install from Ubuntu Repositories (Quick)

```bash
# Install Python 3 and pip
sudo apt install -y python3 python3-pip python3-venv

# Create symlinks for convenience
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
```

### Option B: Install with pyenv (Recommended for Multiple Versions)

```bash
# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Install Python version
pyenv install 3.12.0
pyenv global 3.12.0
```

### Verify Python Installation

```bash
python --version
pip --version

# Expected output:
# Python 3.12.x
# pip 24.x.x
```

### Set Up Virtual Environment Best Practice

```bash
# Create a project with virtual environment
mkdir -p ~/projects/myproject
cd ~/projects/myproject
python -m venv .venv
source .venv/bin/activate
```

---

## Install Node.js and npm

### Option A: Install with nvm (Recommended)

```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# Reload shell
source ~/.bashrc

# Install latest LTS version
nvm install --lts

# Set default
nvm alias default node
```

### Option B: Install from NodeSource (Specific Version)

```bash
# Add NodeSource repository (Node.js 20.x LTS)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Install Node.js (includes npm)
sudo apt install -y nodejs
```

### Verify Installation

```bash
node --version
npm --version

# Expected output:
# v20.x.x
# 10.x.x
```

### Install Useful Global npm Packages

```bash
# TypeScript
npm install -g typescript ts-node

# Linting and formatting
npm install -g eslint prettier

# Development tools
npm install -g nodemon http-server
```

---

## Install Azure CLI

### Add Microsoft Repository and Install

```bash
# Update and install prerequisites
sudo apt update
sudo apt install -y ca-certificates curl apt-transport-https lsb-release gnupg

# Add Microsoft signing key
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
rm microsoft.gpg

# Add Azure CLI repository
CODENAME=$(lsb_release -cs)
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $CODENAME main" | \
    sudo tee /etc/apt/sources.list.d/azure-cli.list

# Install Azure CLI
sudo apt update
sudo apt install -y azure-cli
```

### Verify and Login

```bash
# Verify installation
az --version

# Login to Azure (opens browser)
az login

# Or use device code (if no browser)
az login --use-device-code

# Set default subscription
az account list --output table
az account set --subscription "Your-Subscription-Name"
```

### Useful Azure CLI Commands

```bash
# Show current account
az account show

# List subscriptions
az account list --output table

# Get access token (for debugging)
az account get-access-token

# Logout
az logout
```

---

## Install GitHub CLI

```bash
# Add GitHub CLI repository
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

# Install GitHub CLI
sudo apt update
sudo apt install -y gh
```

### Authenticate GitHub CLI

```bash
# Login to GitHub
gh auth login

# Follow prompts:
# ? What account do you want to log into? GitHub.com
# ? What is your preferred protocol for Git operations? HTTPS
# ? Authenticate Git with your GitHub credentials? Yes
# ? How would you like to authenticate GitHub CLI? Login with a web browser
```

### Verify Authentication

```bash
gh auth status

# Expected output:
# github.com
#   ✓ Logged in to github.com as yourusername
```

---

## Install GitHub Copilot CLI

### Installation

```bash
# Using npm (cross-platform)
npm install -g @github/copilot

# Or using the install script (recommended)
curl -fsSL https://gh.io/copilot-install | bash
```

### Verify Installation

```bash
copilot --version
```

### First Launch and Authentication

```bash
# Start Copilot CLI
copilot

# When prompted about trusted directories, choose:
# 1. Yes, proceed - Trust for this session only
# 2. Yes, and remember this folder - Trust permanently

# Login
/login

# Follow the browser authentication flow
```

### Configure Copilot CLI

Create configuration directory:

```bash
mkdir -p ~/.copilot
```

### Essential Slash Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all commands |
| `/model` | Select AI model |
| `/login` | Authenticate |
| `/logout` | Log out |
| `/context` | Show token usage |
| `/compact` | Compress history |
| `/diff` | Review changes |
| `/review` | Code review agent |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Shift+Tab` | Cycle modes (Interactive/Plan/Autopilot) |
| `Ctrl+T` | Toggle reasoning display |
| `Ctrl+C` | Cancel operation |
| `Ctrl+D` | Shutdown |
| `!command` | Run shell command directly |
| `@file` | Reference a file |

---

## Configure Git

### Set Global Configuration

```bash
# Set your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Configure line endings for cross-platform
git config --global core.autocrlf input

# Enable helpful colors
git config --global color.ui auto

# Set default editor
git config --global core.editor "code --wait"

# Configure credential helper
git config --global credential.helper store
```

### Useful Git Aliases

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --all"
```

### SSH Key Setup (Recommended)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: Settings → SSH Keys → New SSH Key
```

---

## VS Code Integration

### Install VS Code (Windows Side)

Download from: https://code.visualstudio.com/

### Install WSL Extension

1. Open VS Code
2. Install extension: **"WSL"** (ms-vscode-remote.remote-wsl)

### Open Projects from WSL

```bash
# From WSL terminal
cd ~/projects/myproject
code .

# This opens VS Code connected to WSL
```

### Recommended Extensions for WSL

Install these in VS Code (they run in WSL):

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **ESLint** (dbaeumer.vscode-eslint)
- **Prettier** (esbenp.prettier-vscode)
- **GitLens** (eamodio.gitlens)
- **GitHub Copilot** (GitHub.copilot)

### VS Code Settings for WSL

Add to settings.json (`Ctrl+,` → Open Settings JSON):

```json
{
    "remote.WSL.fileWatcher.polling": false,
    "terminal.integrated.defaultProfile.linux": "bash",
    "files.watcherExclude": {
        "**/node_modules/**": true,
        "**/.git/objects/**": true,
        "**/dist/**": true
    }
}
```

---

## Verification Checklist

Run this verification script to confirm everything is installed:

```bash
echo "=== Development Environment Verification ==="
echo ""

echo "1. WSL Version:"
cat /etc/os-release | grep PRETTY_NAME
echo ""

echo "2. Python:"
python --version
pip --version
echo ""

echo "3. Node.js and npm:"
node --version
npm --version
echo ""

echo "4. Azure CLI:"
az --version | head -1
echo ""

echo "5. GitHub CLI:"
gh --version
echo ""

echo "6. GitHub Copilot CLI:"
copilot --version 2>/dev/null || echo "Run 'copilot' to verify"
echo ""

echo "7. Git:"
git --version
echo ""

echo "8. Essential Tools:"
which curl wget jq tree htop
echo ""

echo "=== Verification Complete ==="
```

### Expected Output

```
=== Development Environment Verification ===

1. WSL Version:
PRETTY_NAME="Ubuntu 22.04.x LTS"

2. Python:
Python 3.12.x
pip 24.x.x

3. Node.js and npm:
v20.x.x
10.x.x

4. Azure CLI:
azure-cli 2.x.x

5. GitHub CLI:
gh version 2.x.x

6. GitHub Copilot CLI:
x.x.x

7. Git:
git version 2.x.x

8. Essential Tools:
/usr/bin/curl /usr/bin/wget /usr/bin/jq /usr/bin/tree /usr/bin/htop

=== Verification Complete ===
```

---

## Quick Reference

### WSL Commands (PowerShell)

| Command | Description |
|---------|-------------|
| `wsl` | Enter default distro |
| `wsl --list -v` | List distros with versions |
| `wsl --shutdown` | Shutdown all WSL instances |
| `wsl --update` | Update WSL |

### File System Locations

| Description | Linux Path | Windows Path |
|-------------|------------|--------------|
| Linux home | `~` or `/home/user` | `\\wsl$\Ubuntu\home\user` |
| Windows C: | `/mnt/c` | `C:\` |
| Projects (recommended) | `~/projects` | `\\wsl$\Ubuntu\home\user\projects` |

### Performance Best Practice

> **Always store projects in the Linux filesystem** (`~/projects/`) for optimal performance. Avoid working from `/mnt/c/`.

### Common Workflows

**Start Copilot CLI in a project:**
```bash
cd ~/projects/myproject
copilot
```

**Use Plan Mode for complex tasks:**
```
Press Shift+Tab to enter Plan mode
Describe your requirements
Review the plan
Shift+Tab back to Interactive mode to implement
```

**Reference files in prompts:**
```
Explain what @src/main.py does
Fix the bug in @lib/utils.js
```

**Run shell commands directly:**
```
!git status
!npm test
!az account show
```

---

## Next Steps

1. **Create your first project:**
   ```bash
   mkdir -p ~/projects/hello-world
   cd ~/projects/hello-world
   copilot
   # Ask: "Create a simple Python web server"
   ```

2. **Explore Copilot CLI features:**
   - Try different modes with `Shift+Tab`
   - Use `/help` to see all commands
   - Check `/model` for available AI models

3. **Connect to Azure:**
   ```bash
   az login
   az account list --output table
   ```

4. **Clone a repository and start coding:**
   ```bash
   cd ~/projects
   gh repo clone owner/repo
   cd repo
   code .
   ```

---

## Troubleshooting

### WSL Won't Start
```powershell
wsl --shutdown
wsl --update
# Restart computer if needed
```

### Network Issues in WSL
```bash
# Check connectivity
ping google.com

# Reset WSL networking
# In PowerShell:
wsl --shutdown
# Then restart WSL
```

### Azure CLI Login Issues
```bash
# Use device code if browser doesn't open
az login --use-device-code

# Clear cached tokens
az logout
az account clear
az login
```

### GitHub CLI Authentication Issues
```bash
# Re-authenticate
gh auth logout
gh auth login
```

### Copilot CLI Not Found
```bash
# Reinstall with npm
npm install -g @github/copilot

# Check npm global path is in PATH
npm config get prefix
# Add to ~/.bashrc if needed:
# export PATH="$HOME/.npm-global/bin:$PATH"
```

---

## Additional Resources

- [WSL Documentation](https://docs.microsoft.com/en-us/windows/wsl/)
- [VS Code Remote Development](https://code.visualstudio.com/docs/remote/wsl)
- [Azure CLI Documentation](https://docs.microsoft.com/en-us/cli/azure/)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [GitHub Copilot CLI Documentation](https://docs.github.com/copilot)

---

*Happy coding with your complete WSL development environment! 🚀*
