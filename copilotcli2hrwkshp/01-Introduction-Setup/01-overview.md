# Tutorial 1.1: Overview & First Launch

---

## Concept

### What is GitHub Copilot CLI?

GitHub Copilot CLI is a **terminal-native AI assistant** that brings AI-powered development directly to your command line. Unlike IDE-based Copilot (which focuses on code completion), Copilot CLI can:

- **Understand context**: Reads and comprehends your entire codebase
- **Take action**: Modify files, run commands, interact with GitHub
- **Learn from you**: Supports custom instructions and configuration
- **Integrate deeply**: Works with your existing Git and GitHub workflow

### Copilot CLI vs IDE Copilot

| Feature | Copilot in IDE | Copilot CLI |
|---------|---------------|-------------|
| Primary Interface | Code editor | Terminal |
| Main Use Case | Code completion | Full task automation |
| Context Source | Open files | Entire directory tree |
| Can Execute Commands | Limited | ✅ Full shell access |
| Can Modify Files | Via suggestions | ✅ Direct operations |
| GitHub API Access | Limited | ✅ Full access |

### Architecture at a Glance

Copilot CLI is built as a **layered agentic system** that connects your terminal to AI capabilities:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │   Terminal  │  │  Slash Cmds │  │ @ References │  │   Modes    │ │
│  │    Input    │  │ /help /mcp  │  │ @file @url   │  │ plan/agent │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
│  Your natural language requests, commands, and file references      │
├─────────────────────────────────────────────────────────────────────┤
│                         AGENT CORE                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │        Understand → Plan → Execute → Verify → Repeat         │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │  Context Manager  │  Tool Orchestrator  │  Session Memory    │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  The "brain" that interprets requests and coordinates actions       │
├─────────────────────────────────────────────────────────────────────┤
│                     TOOL EXECUTION LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │
│  │    Bash    │  │   File     │  │    Git     │  │    GitHub    │  │
│  │  Commands  │  │ Edit/View  │  │ Operations │  │   API Tools  │  │
│  └────────────┘  └────────────┘  └────────────┘  └──────────────┘  │
│  Built-in tools for shell commands, file ops, and GitHub access     │
├─────────────────────────────────────────────────────────────────────┤
│                     EXTENSIBILITY LAYER                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐    │
│  │  MCP Servers   │  │     Skills     │  │   Custom Agents    │    │
│  │ Azure/ADO/etc  │  │  Specialized   │  │  Domain-specific   │    │
│  └────────────────┘  └────────────────┘  └────────────────────┘    │
│  Pluggable extensions for enterprise tools and custom workflows     │
├─────────────────────────────────────────────────────────────────────┤
│                       AI MODEL LAYER                                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │   Claude Sonnet/Opus   │   GPT-4/4o   │   Model Routing      │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  LLM backbone for reasoning, code generation, and conversation      │
└─────────────────────────────────────────────────────────────────────┘
```

#### What Each Layer Does

| Layer | Key Components | What It Handles |
|-------|----------------|-----------------|
| **User Interface** | Terminal, `/commands`, `@references` | Accepts your input—natural language, slash commands, file references |
| **Agent Core** | Agentic Loop, Context Manager | Interprets intent, builds context, plans multi-step actions |
| **Tool Execution** | Bash, File, Git, GitHub tools | Runs shell commands, edits files, interacts with repos |
| **Extensibility** | MCP, Skills, Agents | Connects to Azure, ADO, and custom enterprise systems |
| **AI Model** | Claude, GPT-4 | Powers reasoning, generates code, understands context |

### Security Model

1. **Trusted Directories**: You must explicitly trust the directory where you launch Copilot CLI
2. **Tool Approval**: Every file modification or command execution requires your approval
3. **Review Before Execution**: Nothing runs without explicit consent (unless you enable auto-approve)

### Interaction Modes

| Mode | Purpose | Switch with |
|------|---------|-------------|
| **Interactive** | Default mode, step-by-step collaboration | `Shift+Tab` |
| **Plan** | Create plans before executing | `Shift+Tab` |
| **Auto** | Execute with minimal confirmations | `Shift+Tab` |

---

## Practice

### Exercise 1: Launch and Explore

1. **Create a practice directory:**
   ```bash
   mkdir ~/copilot-workshop-practice
   cd ~/copilot-workshop-practice
   ```

2. **Launch Copilot CLI:**
   ```bash
   copilot
   ```

3. **Trust the directory** when prompted

4. **Try these prompts:**

   ```
   What can you help me with?
   ```

   ```
   List your available commands
   ```

   ```
   /help
   ```

### Exercise 2: First Real Task

1. **Ask Copilot to create a file:**
   ```
   Create a simple Python hello world script
   ```

2. **Observe the approval prompt** — Copilot asks permission before creating files

3. **Approve the creation** and verify the file was created

4. **Run the script:**
   ```
   Run the hello world script you just created
   ```

### Exercise 3: Explore Context

1. **Check what Copilot knows:**
   ```
   /context
   ```

2. **Reference a file explicitly:**
   ```
   Show me @hello.py
   ```

3. **Try the diff command:**
   ```
   /diff
   ```

### Exercise 4: Exit and Resume

1. **Exit the session:**
   ```
   /exit
   ```

2. **Resume where you left off:**
   ```bash
   copilot --continue
   ```

3. **Ask about previous work:**
   ```
   What did we do in this session?
   ```

---

## Q&A

Test your understanding with these questions:

### Question 1

What makes Copilot CLI different from Copilot in your IDE?

A) Copilot CLI only works with Python  
B) Copilot CLI has full shell access and can execute commands directly  
C) Copilot CLI is faster but less accurate  
D) Copilot CLI doesn't need authentication  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Copilot CLI has full shell access, can execute commands, modify files directly, and has deep GitHub integration. IDE Copilot focuses primarily on inline code completion within files you're editing.

</details>

---

### Question 2

Why should you never launch Copilot CLI from your home directory (`~` or `%USERPROFILE%`)?

A) It runs slower from home directory  
B) It costs more premium requests  
C) The home directory contains sensitive configs and a broad range of files  
D) Copilot CLI doesn't support home directories  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

The home directory typically contains sensitive configuration files, credentials, SSH keys, and a broad range of unrelated files. Limiting Copilot's scope to specific project directories reduces security risk and improves context relevance.

</details>

---

### Question 3

What happens when Copilot wants to modify a file or run a command?

A) It modifies the file immediately  
B) It asks for explicit permission before proceeding  
C) It creates a backup first automatically  
D) It sends the change to GitHub for approval  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Copilot CLI asks for explicit permission before modifying any file or running commands. You see exactly what it wants to do and can approve, deny, or suggest an alternative approach.

</details>

---

### Question 4

How do you switch between Interactive, Plan, and Auto modes?

A) Type `/mode interactive` or `/mode plan`  
B) Press `Shift+Tab`  
C) Exit and restart with different flags  
D) Use the `/switch` command  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Press `Shift+Tab` to cycle between Interactive, Plan, and Auto modes. The current mode is shown in the prompt indicator.

</details>

---

## Next Steps

Continue to [Section 2: Core Concepts](../02-Core-Concepts/README.md) to understand how Copilot CLI works under the hood.
