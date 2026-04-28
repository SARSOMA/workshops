# Tutorial 4.4: Custom Agents

---

## Concept

### What are Custom Agents?

**Custom Agents** are user-defined personas with specialized instructions, tool access, and behavior. They extend Copilot CLI's capabilities for specific workflows or team needs.

```
┌─────────────────────────────────────────────────────┐
│                  CUSTOM AGENTS                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Agent = Instructions + Tools + Personality         │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  "security-reviewer" Agent                   │   │
│  │  ├── Focus: Security vulnerabilities        │   │
│  │  ├── Tools: Code search, ADO, GitHub        │   │
│  │  └── Style: Thorough, conservative          │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Agent Configuration

Agents are defined in `.github/copilot-agents.yaml` or `~/.copilot/agents/`:

```yaml
# .github/copilot-agents.yaml
agents:
  security-reviewer:
    description: "Reviews code for security vulnerabilities"
    instructions: |
      You are a security-focused code reviewer.
      - Look for SQL injection, XSS, CSRF vulnerabilities
      - Check for hardcoded credentials
      - Verify input validation
      - Recommend security best practices
    tools:
      - github
      - bluebird
      - code-review

  docs-writer:
    description: "Technical documentation specialist"
    instructions: |
      You are a technical writer.
      - Write clear, concise documentation
      - Include code examples
      - Follow Microsoft style guide
    tools:
      - github
      - filesystem
```

### Agent Capabilities

| Feature | Description |
|---------|-------------|
| **Instructions** | Persona, focus area, behavior guidelines |
| **Tools** | Which MCP tools the agent can use |
| **Style** | Communication style and approach |
| **Restrictions** | What the agent should avoid |

### Using Agents

1. **List available agents:**
   ```
   /agents
   ```

2. **Switch to an agent:**
   ```
   /agent security-reviewer
   ```

3. **Return to default:**
   ```
   /agent default
   ```

### Built-in Agent Types

| Agent | Purpose |
|-------|---------|
| `explore` | Fast codebase exploration |
| `task` | Execute commands with summary |
| `rubber-duck` | Critique plans and implementations |
| `code-review` | High-signal code review |

---

## Practice

### Exercise 1: List Available Agents

```
/agents
```

Or ask:

```
What agents do you have available?
```

### Exercise 2: Use Built-in Agents

Try the rubber-duck agent for plan critique:

```
As a rubber-duck reviewer, critique this plan:
I want to add user authentication using JWT tokens stored in localStorage.
```

Try the explore agent:

```
Using the explore agent, help me understand the project structure of SARSOMA/akri
```

### Exercise 3: Create a Custom Agent

1. **Create the agents file:**
   ```
   Create a .github/copilot-agents.yaml file with a "performance-optimizer" agent
   that focuses on finding and fixing performance issues in code.
   ```

2. **Review the generated configuration**

3. **Test the agent:**
   ```
   /agent performance-optimizer
   ```

   Then:
   ```
   Review @src/main.py for performance issues
   ```

### Exercise 4: Create a Practical Agent Using MCPs

Create an agent that leverages multiple MCPs:

```
Create a custom agent called "incident-responder" that:
1. Can analyze ADO pipeline failures
2. Search code for related issues
3. Check work items for related bugs
4. File new bugs if needed

Include instructions for thorough incident investigation.
```

### Exercise 5: Team-Specific Agent

Design an agent for your team's workflow:

```
Create a custom agent for [your team's common task].
For example, if you do a lot of PR reviews, create a "team-reviewer" 
agent with your team's specific coding standards and review checklist.
```

---

## Q&A

### Question 1

Where are custom agents defined?

A) `~/.copilot/mcp.json`  
B) `.github/copilot-agents.yaml` or `~/.copilot/agents/`  
C) `package.json`  
D) `.copilot/agents.json`  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Custom agents are defined in `.github/copilot-agents.yaml` for repository-level agents, or in `~/.copilot/agents/` for user-level agents.

</details>

---

### Question 2

What components make up a custom agent?

A) Only custom prompts  
B) Instructions, tools, and personality/style  
C) Just MCP server connections  
D) Programming code and functions  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

A custom agent consists of instructions (persona, focus area, behavior guidelines), tools (which MCP tools it can use), and personality/style (communication approach, restrictions).

</details>

---

### Question 3

Which command switches to a custom agent?

A) `/use agent-name`  
B) `/switch agent-name`  
C) `/agent agent-name`  
D) `/mode agent-name`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Use `/agent agent-name` to switch to a custom agent, and `/agent default` to return to the default behavior.

</details>

---

### Question 4

What is the rubber-duck agent best used for?

A) Executing code automatically  
B) Critiquing plans and implementations before execution  
C) Creating documentation  
D) Managing Git branches  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

The rubber-duck agent provides constructive feedback on plans and implementations, helping catch bugs, logic errors, and design flaws before you execute them. It's like a code review for your approach.

</details>

---

## Summary: MCP + Skills + Agents

You've now learned the complete extensibility stack:

```
┌─────────────────────────────────────────────────────┐
│            EXTENSIBILITY STACK                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  Custom Agents (Highest level)               │   │
│  │  - Personas with specialized behavior        │   │
│  └─────────────────────────────────────────────┘   │
│                      ▼                              │
│  ┌─────────────────────────────────────────────┐   │
│  │  Skills (Middle level)                       │   │
│  │  - Pre-built workflows combining tools       │   │
│  └─────────────────────────────────────────────┘   │
│                      ▼                              │
│  ┌─────────────────────────────────────────────┐   │
│  │  MCP Servers (Foundation)                    │   │
│  │  - External system connections               │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Next Steps

Continue to [Section 5: End-to-End Workflows](../05-End-to-End-Workflows/README.md) to apply everything with a real project.
