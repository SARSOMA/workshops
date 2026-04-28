# Tutorial 2.1: Architecture & Configuration

---

## Concept

### The Agentic Loop

Copilot CLI operates as an **autonomous agent** that continuously cycles through four phases to accomplish your tasks:

```
┌─────────────────────────────────────────────────────────────────────┐
│                        THE AGENTIC LOOP                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │
│    │   UNDERSTAND │─────►│     PLAN     │─────►│   EXECUTE    │    │
│    │              │      │              │      │              │    │
│    │ • Parse input│      │ • Choose     │      │ • Run tools  │    │
│    │ • Read files │      │   tools      │      │ • Edit files │    │
│    │ • Get context│      │ • Sequence   │      │ • Call APIs  │    │
│    └──────────────┘      │   steps      │      └──────────────┘    │
│           ▲              └──────────────┘              │            │
│           │                                            │            │
│           │              ┌──────────────┐              │            │
│           └──────────────│    VERIFY    │◄─────────────┘            │
│                          │              │                           │
│              Re-enter    │ • Check      │   Success?                │
│              loop if     │   results    │   ────────►  Done!        │
│              needed      │ • Validate   │                           │
│                          │ • Iterate    │                           │
│                          └──────────────┘                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Phase Details

| Phase | What Happens | Internal Actions | You See |
|-------|--------------|------------------|---------|
| **Understand** | Parses your request and gathers context | Reads `@`-referenced files, checks git status, scans directory structure, loads instructions files | Brief pause while context loads |
| **Plan** | Determines the strategy and tools needed | Selects from available tools (bash, file edit, GitHub API, MCP), orders steps logically | May show thinking or approach |
| **Execute** | Performs the planned actions | Runs shell commands, edits files, creates PRs, queries MCP servers | **Asks for approval** (unless auto mode) |
| **Verify** | Validates results and decides next steps | Checks command exit codes, reads modified files, runs tests if appropriate | Shows results, may iterate |

#### How the Loop Handles Complexity

For simple requests, the loop runs once:
```
You: "What branch am I on?"
→ Understand (read git) → Plan (run git branch) → Execute → Verify → Done
```

For complex tasks, the loop **iterates multiple times**:
```
You: "Fix the failing tests in auth.py"
→ Understand (read test output, auth.py)
→ Plan (identify fix needed)
→ Execute (edit file)
→ Verify (run tests again) → Tests still fail?
→ Re-enter: Understand (new error) → Plan (different fix) → Execute → Verify → ✓ Pass!
```

#### Key Behaviors

- **Context Accumulation**: Each loop iteration adds to the agent's understanding
- **Self-Correction**: Failed executions trigger re-planning with new information
- **Tool Chaining**: Multiple tools can be orchestrated in a single plan
- **Approval Gates**: You control when execution happens (configurable via modes)

#### Where the LLM is Called

The LLM (Claude/GPT-4) is invoked at **multiple points** throughout the agentic loop:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     LLM CALLS IN THE AGENTIC LOOP                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐                                                    │
│  │  UNDERSTAND │  🤖 LLM CALL #1: Intent Classification            │
│  │             │     • "What is the user asking for?"               │
│  │             │     • "What context do I need to gather?"          │
│  └──────┬──────┘                                                    │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                    │
│  │    PLAN     │  🤖 LLM CALL #2: Strategy & Tool Selection        │
│  │             │     • "Which tools should I use?"                  │
│  │             │     • "In what order? What parameters?"            │
│  │             │     • "What's my step-by-step approach?"           │
│  └──────┬──────┘                                                    │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                    │
│  │   EXECUTE   │  🤖 LLM CALL #3: Tool Invocation (per tool)       │
│  │             │     • "Generate the bash command"                  │
│  │             │     • "Generate the code edit"                     │
│  │             │     • "Format the API request"                     │
│  └──────┬──────┘                                                    │
│         │                                                           │
│         ▼                                                           │
│  ┌─────────────┐                                                    │
│  │   VERIFY    │  🤖 LLM CALL #4: Result Interpretation            │
│  │             │     • "Did this succeed or fail?"                  │
│  │             │     • "Is the task complete?"                      │
│  │             │     • "What should I do next?"                     │
│  └─────────────┘                                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

| Phase | LLM Call Purpose | Input to LLM | Output from LLM |
|-------|------------------|--------------|-----------------|
| **Understand** | Intent classification | Your prompt + system instructions + loaded context | Parsed intent, required context sources |
| **Plan** | Strategy formation | Intent + all gathered context (files, git, MCP data) | Ordered list of tool calls with parameters |
| **Execute** | Tool call generation | Plan step + relevant context | Actual command/code/API call to run |
| **Verify** | Result interpretation | Tool output + original goal | Success/failure assessment, next action |

#### LLM Call Frequency

A single user request can trigger **many LLM calls**:

```
Example: "Add error handling to the API endpoint"

LLM Call 1: Understand intent → "User wants try/catch added"
LLM Call 2: Plan approach → "Read file, identify function, edit code, run tests"
LLM Call 3: Execute read → (tool runs, no LLM needed for read)
LLM Call 4: Execute edit → Generate the actual code changes
LLM Call 5: Verify edit → "Code looks correct, now run tests"
LLM Call 6: Execute test → Generate test command
LLM Call 7: Verify test → "Tests pass, task complete"

Total: 7 LLM calls for one user request
```

> 💡 **Why this matters**: Understanding LLM call frequency helps you:
> - Estimate response times (more calls = longer wait)
> - Understand why complex tasks take longer
> - Appreciate the value of clear, specific prompts (fewer iterations needed)

### Configuration Hierarchy

Configuration is **layered** — higher priority settings override lower ones:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION HIERARCHY                          │
│                    (Highest to Lowest Priority)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 1. CLI FLAGS                              [HIGHEST PRIORITY] │   │
│  │    copilot --model gpt-4 --no-auto-approve                   │   │
│  │    • Overrides everything for this session                   │   │
│  │    • Useful for one-off changes                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 2. ENVIRONMENT VARIABLES                                     │   │
│  │    COPILOT_MODEL=gpt-4                                       │   │
│  │    GITHUB_TOKEN=ghp_xxx                                      │   │
│  │    • Set in shell profile or CI/CD                           │   │
│  │    • Good for machine-level defaults                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 3. REPOSITORY CONFIG                                         │   │
│  │    .github/copilot-instructions.md                           │   │
│  │    .github/mcp.json                                          │   │
│  │    • Shared with team via git                                │   │
│  │    • Project-specific standards and tools                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 4. USER CONFIG                                               │   │
│  │    ~/.copilot/copilot-instructions.md                        │   │
│  │    ~/.copilot/mcp.json                                       │   │
│  │    • Personal preferences across all projects                │   │
│  │    • Your MCP servers, preferred model, etc.                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ 5. ORGANIZATION CONFIG                    [LOWEST PRIORITY]  │   │
│  │    Set by GitHub org admins                                  │   │
│  │    • Enterprise policies, allowed models                     │   │
│  │    • Cannot be overridden by users (enforced)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Configuration Merge Behavior

| Setting Type | Merge Behavior | Example |
|--------------|----------------|---------|
| **Scalar values** (model, flags) | Higher priority wins | CLI `--model gpt-4` beats env `COPILOT_MODEL=claude` |
| **Instructions** | Concatenated (all apply) | Repo + User instructions both included in prompts |
| **MCP servers** | Merged by name | User + Repo MCPs both available; same name = repo wins |
| **Org policies** | Enforced (cannot override) | If org disables a model, you can't use it |

### Key Configuration Files

| File/Location | Purpose | Scope |
|---------------|---------|-------|
| `.github/copilot-instructions.md` | Repository-specific instructions | Shared with team |
| `~/.copilot/copilot-instructions.md` | Personal instructions | All your projects |
| `~/.copilot/mcp.json` | MCP server configuration | All your projects |
| `.github/mcp.json` | Project MCP servers | Shared with team |
| `~/.copilot/lsp-config.json` | LSP server configuration | All your projects |

#### Instructions File Format

```markdown
# ~/.copilot/copilot-instructions.md or .github/copilot-instructions.md

## Coding Standards
- Use TypeScript strict mode
- Prefer functional programming patterns
- Always add JSDoc comments to public functions

## Project Context
- This is a React 18 application
- We use Zustand for state management
- API calls go through src/api/client.ts

## Testing
- Use Vitest for unit tests
- Aim for 80% code coverage
- Mock external APIs in tests
```

### How Context is Built

The agent builds context **progressively** from multiple sources:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CONTEXT ASSEMBLY                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐                                                │
│  │ 1. ALWAYS       │  System prompts, org policies, user           │
│  │    INCLUDED     │  instructions, repo instructions               │
│  └────────┬────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │ 2. AUTO-LOADED  │  Current directory tree, git status,          │
│  │                 │  branch info, recent file changes              │
│  └────────┬────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │ 3. ON-DEMAND    │  @file references, @url fetches,               │
│  │                 │  MCP queries, GitHub API calls                 │
│  └────────┬────────┘                                                │
│           │                                                         │
│           ▼                                                         │
│  ┌─────────────────┐                                                │
│  │ 4. ACCUMULATED  │  Previous conversation turns,                  │
│  │                 │  tool outputs, checkpoints                     │
│  └─────────────────┘                                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

| Source | What's Included | When Loaded |
|--------|-----------------|-------------|
| **Always Included** | System prompts, instructions files, org policies | Session start |
| **Auto-Loaded** | Directory tree (truncated), git status, branch, recent changes | Each prompt |
| **On-Demand** | `@file` contents, `@url` pages, MCP data, GitHub issues/PRs | When referenced |
| **Accumulated** | Conversation history, tool outputs, your feedback | Throughout session |

### Context Window Management

The LLM has a **finite context window** — all information must fit:

```
┌─────────────────────────────────────────────────────────────────────┐
│                  CONTEXT WINDOW (e.g., 128K-200K tokens)            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────┐  │
│  │    System    │ │    Your      │ │  Conversation │ │  Response │  │
│  │   Prompts    │+│   Context    │+│    History    │+│   Space   │  │
│  │   (~10%)     │ │   (varies)   │ │   (grows)     │ │  (~20%)   │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────┘  │
│                                                                     │
│  ════════════════════════════════════════════════════════════════  │
│  0%                                                           100%  │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  WHAT HAPPENS WHEN CONTEXT FILLS UP:                                │
│                                                                     │
│  1. Auto-compaction: Older conversation turns summarized            │
│  2. Prioritization: Recent/relevant content kept, old dropped       │
│  3. Truncation: Large files may be partially loaded                 │
│  4. Memory loss: Agent may "forget" early conversation details      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### Context Optimization Strategies

| Strategy | How to Do It | Why It Helps |
|----------|--------------|--------------|
| **Use `/clear`** | Start fresh between unrelated tasks | Removes irrelevant accumulated context |
| **Be specific with `@`** | `@src/auth.ts` not `@src/` | Loads only what's needed |
| **Compact when needed** | `/compact` | Summarizes history, frees context space |
| **Reference by path** | "Look at line 45 of utils.ts" | More precise than pasting code |
| **Break up large tasks** | Do in phases, `/clear` between | Prevents context overflow |

#### Signs Your Context is Getting Full

- Responses become slower
- Agent "forgets" things you mentioned earlier
- You see compaction messages
- Agent asks about things you already told it

---

## Practice

### Exercise 1: Explore Configuration Locations

1. **Check user config directory:**
   ```bash
   ls -la ~/.copilot/
   ```

2. **View MCP configuration (if it exists):**
   ```bash
   cat ~/.copilot/mcp.json
   ```

### Exercise 2: Create Repository Instructions

1. **In your practice directory, create instructions:**
   ```bash
   mkdir -p .github
   ```

2. **Ask Copilot to create the file:**
   ```
   Create a .github/copilot-instructions.md file that tells you to:
   - Always use Python 3.10+ features
   - Prefer type hints
   - Follow PEP 8 style
   ```

3. **Verify the instructions are loaded:**
   ```
   /clear
   ```
   Then ask:
   ```
   What coding standards should you follow in this project?
   ```

### Exercise 3: Context Inspection

1. **Check current context:**
   ```
   /context
   ```

2. **Create some test files:**
   ```
   Create three Python files: utils.py, main.py, and tests.py with simple placeholder content
   ```

3. **Check context again:**
   ```
   /context
   ```

4. **Reference a specific file:**
   ```
   Explain what @main.py does
   ```

### Exercise 4: Model Selection

1. **Check current model:**
   ```
   /model
   ```

2. **List available models:**
   ```
   /model list
   ```

3. **Try a different model (if available):**
   ```
   /model claude-sonnet-4
   ```

---

## Q&A

### Question 1

What is the correct priority order for Copilot CLI configuration?

A) Organization → User → Repository → Environment → CLI flags  
B) CLI flags → Environment → Repository → User → Organization  
C) Repository → User → CLI flags → Environment → Organization  
D) User → Organization → Repository → CLI flags → Environment  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

CLI flags have the highest priority, followed by environment variables, then repository config, user config, and finally organization config (lowest priority). This allows you to override broader settings with more specific ones.

</details>

---

### Question 2

Where should you place repository-specific instructions for Copilot CLI?

A) `~/.copilot/instructions.md`  
B) `.copilot/instructions.md`  
C) `.github/copilot-instructions.md`  
D) `copilot.config.json`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Repository-specific instructions go in `.github/copilot-instructions.md`. This file is read automatically when you launch Copilot CLI in that repository and is shared with your team via version control.

</details>

---

### Question 3

What happens when the context window fills up?

A) Copilot stops responding until you restart  
B) Copilot auto-compacts by removing older, less relevant context  
C) You get an error message and must use `/clear`  
D) Copilot switches to a larger model automatically  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Copilot CLI automatically compacts the context when it fills up, keeping the most relevant information and summarizing or removing older conversation details. You can manually clear context with `/clear` when switching tasks.

</details>

---

### Question 4

Which command shows you what context Copilot currently has loaded?

A) `/status`  
B) `/info`  
C) `/context`  
D) `/memory`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

The `/context` command shows what context Copilot currently has loaded, including files, conversation history, and other relevant information.

</details>

---

## Next Steps

Continue to [Section 3: CLI Fundamentals](../03-CLI-Fundamentals/README.md) to master commands, shortcuts, and workflows.
