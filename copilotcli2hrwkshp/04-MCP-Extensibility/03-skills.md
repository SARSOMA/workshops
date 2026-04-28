# Tutorial 4.3: Skills

---

## Concept

### What are Skills?

**Skills** are pre-built, specialized capabilities that combine multiple tools and prompts for specific tasks. They're like expert modes that Copilot can activate for particular workflows.

```
┌─────────────────────────────────────────────────────┐
│                    SKILLS                            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Skill = Tools + Prompts + Specialized Knowledge    │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │  "ado-pipeline-analyzer" Skill               │   │
│  │  ├── ADO MCP tools                          │   │
│  │  ├── Pipeline-specific prompts              │   │
│  │  └── Failure pattern knowledge              │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Available Skills

Skills are context-aware and activate automatically or can be invoked explicitly:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `ado-pipeline-analyzer` | Analyze ADO pipeline failures | Debugging build/deploy issues |
| `ado-bug-filer` | Create ADO bugs with details | Filing bugs from investigations |
| `ado-pr-feedback` | Process PR review comments | Addressing PR feedback |
| `ado-log-investigator` | Deep dive into pipeline logs | Tracing error sources |
| `workiq` | Microsoft 365 intelligence | Finding emails, meetings, docs |
| `code-review` | Comprehensive code review | Reviewing changes |

### How Skills Work

1. **Automatic Activation**: Copilot detects when a skill is relevant
2. **Manual Invocation**: You can explicitly request a skill
3. **Combined Tools**: Skills coordinate multiple MCP tools
4. **Specialized Prompts**: Skills include domain expertise

### Skill Invocation

Skills can be invoked:
- **Implicitly**: Copilot activates based on your request
- **Explicitly**: Use `/skill` command or mention the skill name

---

## Practice

### Exercise 1: Discover Available Skills

Ask Copilot about available skills:

```
What skills do you have available?
```

```
/help skills
```

### Exercise 2: Use Pipeline Analyzer Skill (if ADO configured)

If you have ADO MCP configured, try:

```
Analyze the latest pipeline run in [project]/[pipeline-name]
```

The `ado-pipeline-analyzer` skill will:
1. Fetch pipeline run details
2. Identify failure points
3. Analyze logs
4. Suggest fixes

### Exercise 3: Use WorkIQ Skill (if configured)

If WorkIQ is configured, try:

```
What are the top priorities from my manager this week?
```

```
Summarize the emails about [project] from the last 3 days
```

### Exercise 4: Use Code Review Skill

The code review skill works with local changes:

1. **Make some changes in your practice project**

2. **Request a code review:**
   ```
   Review my pending changes using the code-review skill
   ```

   Or simply:
   ```
   /review
   ```

### Exercise 5: Combining Skills

Try a task that might use multiple skills:

```
I need to understand why yesterday's deployment failed.
Check the pipeline, find any related bugs or work items,
and summarize what emails were sent about it.
```

---

## Q&A

### Question 1

What is a Skill in GitHub Copilot CLI?

A) A programming language Copilot can write  
B) A pre-built capability combining tools and specialized knowledge  
C) A certification level for users  
D) A type of MCP server  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

A Skill is a pre-built, specialized capability that combines multiple tools, prompts, and domain-specific knowledge for particular workflows. Skills make Copilot more effective at specific tasks.

</details>

---

### Question 2

How can Skills be activated?

A) Only manually via `/skill` command  
B) Only automatically by Copilot  
C) Both automatically (context-aware) and manually  
D) They must be enabled in config first  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Skills can be activated both automatically (Copilot detects when they're relevant) and manually (using `/skill` or mentioning the skill name).

</details>

---

### Question 3

Which skill would you use to investigate a pipeline failure?

A) `workiq`  
B) `code-review`  
C) `ado-pipeline-analyzer`  
D) `bluebird-search`  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

The `ado-pipeline-analyzer` skill is specifically designed for analyzing Azure DevOps pipeline failures. It fetches run details, identifies failure points, analyzes logs, and suggests fixes.

</details>

---

## Next Steps

Continue to [Tutorial 4.4: Custom Agents](./04-custom-agents.md) to create your own specialized agents.
