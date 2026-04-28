# Tutorial 5.3: Programmatic Usage

## Introduction

Copilot CLI can be used programmatically—in scripts, CI/CD pipelines, and automation workflows. This tutorial covers non-interactive usage patterns.

## Command-Line Interface

### Basic Programmatic Usage

```bash
copilot -p "Your prompt here"
copilot --prompt "Your prompt here"
```

The CLI processes the prompt and exits.

### Example: Quick Code Generation

```bash
copilot -p "Create a hello world function in Python" > hello.py
```

---

## Essential Flags

### Prompt Flags

| Flag | Description |
|------|-------------|
| `-p, --prompt` | The prompt to execute |
| `--stdin` | Read prompt from stdin |

### Permission Flags

| Flag | Description |
|------|-------------|
| `--allow-all-tools` | Allow all tools without prompts |
| `--allow-tool='shell(cmd)'` | Allow specific tool |
| `--deny-tool='shell(cmd)'` | Deny specific tool |
| `--yolo` | Alias for --allow-all-tools |

### Model Flags

| Flag | Description |
|------|-------------|
| `--model=name` | Use specific AI model |

### Agent Flags

| Flag | Description |
|------|-------------|
| `--agent=name` | Use specific custom agent |

### Output Flags

| Flag | Description |
|------|-------------|
| `--json` | Output in JSON format |
| `--quiet` | Minimal output |

---

## Permission Patterns

### Allow Specific Commands

```bash
# Allow git commands
copilot -p "Commit my changes" --allow-tool='shell(git)'

# Allow npm
copilot -p "Install lodash" --allow-tool='shell(npm)'

# Allow multiple
copilot -p "Build and test" \
  --allow-tool='shell(npm)' \
  --allow-tool='shell(node)'
```

### Allow File Writes

```bash
copilot -p "Create a config file" --allow-tool='write'
```

### Allow Everything

```bash
copilot -p "Setup the project" --allow-all-tools
```

> ⚠️ Use with caution—allows any action without confirmation.

### Deny Dangerous Commands

```bash
copilot -p "Clean up the project" \
  --allow-all-tools \
  --deny-tool='shell(rm)'
```

---

## Script Integration

### Bash Script Example

```bash
#!/bin/bash
# automated-review.sh

# Get changed files
CHANGED_FILES=$(git diff --name-only HEAD~1)

# Review each file
for file in $CHANGED_FILES; do
  echo "Reviewing $file..."
  copilot -p "Review @$file for security issues. Output only critical findings." \
    --model=claude-sonnet-4-5 \
    --quiet
done
```

### Piping Input

```bash
# Read prompt from stdin
echo "Explain this code: $(cat app.js)" | copilot --stdin

# Pipe file for analysis
cat error.log | copilot --stdin -p "Analyze this error log"
```

### Capturing Output

```bash
# Capture to variable
RESULT=$(copilot -p "Generate a UUID" --quiet)
echo "Generated: $RESULT"

# Capture to file
copilot -p "Generate package.json for a Node.js project" > package.json
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Copilot CLI
        run: npm install -g @github/copilot

      - name: Review Changes
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          copilot -p "Review the changes in this PR for potential issues. 
                      Focus on: security, performance, and best practices.
                      Output a summary suitable for a PR comment." \
            --allow-tool='shell(git)' \
            > review.md

      - name: Post Review Comment
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review
            });
```

### Azure DevOps Pipeline Example

```yaml
trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '18.x'

  - script: npm install -g @github/copilot
    displayName: 'Install Copilot CLI'

  - script: |
      copilot -p "Generate a summary of changes since last release" \
        --allow-tool='shell(git)' \
        > release-notes.md
    displayName: 'Generate Release Notes'
    env:
      GITHUB_TOKEN: $(GITHUB_TOKEN)

  - publish: release-notes.md
    artifact: release-notes
```

---

## Automation Patterns

### Pattern 1: Batch File Processing

```bash
#!/bin/bash
# process-all.sh

for file in src/**/*.ts; do
  echo "Processing $file"
  copilot -p "Add JSDoc comments to all functions in @$file" \
    --allow-tool='write' \
    --quiet
done
```

### Pattern 2: Conditional Logic

```bash
#!/bin/bash
# smart-fix.sh

# Run tests first
if ! npm test; then
  echo "Tests failed, asking Copilot to fix..."
  copilot -p "The tests are failing. Fix the issues." \
    --allow-all-tools
  
  # Run tests again
  npm test
fi
```

### Pattern 3: Report Generation

```bash
#!/bin/bash
# daily-report.sh

copilot -p "Generate a daily report including:
1. Git commits in the last 24 hours
2. Open PRs and their status
3. Any failing CI pipelines
Format as markdown." \
  --allow-tool='shell(git)' \
  --allow-tool='github' \
  > reports/daily-$(date +%Y-%m-%d).md
```

---

## Hooks

Hooks allow you to run custom scripts at key points:

### Hook Types

| Hook | When It Runs |
|------|--------------|
| `pre-tool` | Before a tool is executed |
| `post-tool` | After a tool completes |
| `pre-response` | Before Copilot responds |
| `post-response` | After Copilot responds |

### Configuring Hooks

In `~/.copilot/hooks.json`:

```json
{
  "hooks": {
    "pre-tool": {
      "shell": "bash ~/.copilot/hooks/pre-shell.sh"
    },
    "post-response": {
      "all": "bash ~/.copilot/hooks/log-response.sh"
    }
  }
}
```

### Example Hook: Audit Logging

**~/.copilot/hooks/log-response.sh:**
```bash
#!/bin/bash
# Log all Copilot responses for audit

TIMESTAMP=$(date -Iseconds)
LOG_FILE="$HOME/.copilot/audit.log"

echo "[$TIMESTAMP] Response received" >> "$LOG_FILE"
```

---

## Environment Variables

### Authentication

```bash
export GITHUB_TOKEN="ghp_xxxxx"
# or
export GH_TOKEN="ghp_xxxxx"
```

### Custom Model Provider

```bash
export COPILOT_PROVIDER_BASE_URL="https://api.openai.com/v1"
export COPILOT_PROVIDER_API_KEY="sk-xxxxx"
export COPILOT_PROVIDER_MODEL="gpt-4"
```

### Configuration Directory

```bash
export COPILOT_HOME="/custom/path/.copilot"
```

---

## Exercise: Programmatic Usage

### Exercise 5.3.1: Simple Script

Create a script that generates a README:

```bash
#!/bin/bash
# generate-readme.sh

copilot -p "Generate a README.md for this project based on:
- package.json or similar config
- Source file structure
- Any existing documentation

Make it professional and comprehensive." \
  --allow-tool='shell(cat)' \
  > README.md

echo "README.md generated!"
```

### Exercise 5.3.2: Batch Operation

Create a script to add type hints to Python files:

```bash
#!/bin/bash

for file in *.py; do
  echo "Adding type hints to $file"
  copilot -p "Add type hints to all functions in @$file. 
              Keep all existing functionality." \
    --allow-tool='write' \
    --quiet
done
```

### Exercise 5.3.3: CI Integration

Design a CI job that:
1. Installs Copilot CLI
2. Reviews PR changes
3. Posts findings as a comment

---

## Safety Considerations

### 1. Be Specific with Permissions

```bash
# Too permissive
copilot -p "Clean up" --allow-all-tools

# Better
copilot -p "Remove .log files" --allow-tool='shell(rm)'
```

### 2. Use Deny for Dangerous Commands

```bash
copilot -p "Organize the project" \
  --allow-all-tools \
  --deny-tool='shell(rm -rf)' \
  --deny-tool='shell(git push --force)'
```

### 3. Run in Isolated Environments

For CI/CD:
- Use containers
- Limit network access
- Restrict file system access

### 4. Review Before Production

Test scripts locally before adding to CI/CD pipelines.

---

## Key Takeaways

1. **Use `-p` for single prompts** without interactive mode
2. **Control permissions** with `--allow-tool` and `--deny-tool`
3. **Pipe input/output** for shell integration
4. **CI/CD ready** with proper authentication
5. **Hooks extend** with custom scripts
6. **Safety first** - be specific with permissions

---

## Next Section

Continue to [Section 6: MCP Extensibility](../06-MCP-Extensibility/README.md) for integrating external systems.
