# Tutorial 4.3: Skills

---

## Concept

### What are Skills?

**Skills** are pre-built, specialized capabilities that combine multiple tools and prompts for specific tasks. Think of them as expert modes that Copilot can activate for particular workflows—they package domain knowledge, tool orchestration, and specialized prompting into reusable capabilities.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              WHAT IS A SKILL?                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  A Skill is NOT just a tool—it's a complete workflow package:               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │   ┌─────────────┐   ┌─────────────┐   ┌─────────────────────────┐  │   │
│  │   │   TOOLS     │ + │   PROMPTS   │ + │  DOMAIN KNOWLEDGE       │  │   │
│  │   │             │   │             │   │                         │  │   │
│  │   │ • MCP tools │   │ • System    │   │ • Failure patterns      │  │   │
│  │   │ • CLI tools │   │   prompts   │   │ • Best practices        │  │   │
│  │   │ • Built-ins │   │ • Templates │   │ • Error mappings        │  │   │
│  │   │             │   │ • Formats   │   │ • Domain vocabulary     │  │   │
│  │   └─────────────┘   └─────────────┘   └─────────────────────────┘  │   │
│  │                                                                     │   │
│  │                              ↓                                      │   │
│  │                                                                     │   │
│  │   ┌─────────────────────────────────────────────────────────────┐  │   │
│  │   │              SPECIALIZED BEHAVIOR                            │  │   │
│  │   │                                                              │  │   │
│  │   │  • Knows how to sequence tool calls                         │  │   │
│  │   │  • Understands domain-specific error messages               │  │   │
│  │   │  • Follows established workflows                            │  │   │
│  │   │  • Provides structured, consistent output                   │  │   │
│  │   └─────────────────────────────────────────────────────────────┘  │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Skills vs. Tools vs. MCP Servers

Understanding the hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HIERARCHY OF CAPABILITIES                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  MCP Server                 Tool                      Skill                 │
│  ──────────                 ────                      ─────                 │
│                                                                             │
│  ┌────────────┐        ┌────────────┐          ┌────────────────────┐      │
│  │ Azure MCP  │───────▶│ list_vms   │          │                    │      │
│  │            │        │ get_metrics│          │  ado-pipeline-     │      │
│  └────────────┘        │ query_logs │          │  analyzer          │      │
│                        └────────────┘          │                    │      │
│  ┌────────────┐        ┌────────────┐          │  Uses tools from:  │      │
│  │ ADO MCP    │───────▶│ get_build  │─────────▶│  • ADO MCP         │      │
│  │            │        │ list_runs  │          │  • Bluebird MCP    │      │
│  └────────────┘        │ get_logs   │          │  • Built-in tools  │      │
│                        └────────────┘          │                    │      │
│  ┌────────────┐        ┌────────────┐          │  Adds:             │      │
│  │ Bluebird   │───────▶│search_code │─────────▶│  • Failure pattern │      │
│  │            │        │code_history│          │    recognition     │      │
│  └────────────┘        └────────────┘          │  • Fix suggestions │      │
│                                                │  • Root cause flow │      │
│  Provides            Atomic                    │                    │      │
│  connectivity        operations                └────────────────────┘      │
│                                                                             │
│                                                Complete workflow            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

| Level | What It Is | Example |
|-------|------------|---------|
| **MCP Server** | Connection to an external system | Azure DevOps MCP |
| **Tool** | Single atomic operation | `get_pipeline_run`, `search_code` |
| **Skill** | Multi-tool workflow with expertise | `ado-pipeline-analyzer` |

---

### Skill Categories

Skills are organized into functional categories:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SKILL CATEGORIES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  🔧 ADO PIPELINE SKILLS                                              │   │
│  │  ─────────────────────────────────────────────────────────────────   │   │
│  │  ado-pipeline-analyzer    Analyze pipeline runs and failures         │   │
│  │  ado-log-investigator     Deep dive into pipeline logs               │   │
│  │  ado-artifact-analyzer    Examine build artifacts and outputs        │   │
│  │  ado-pipeline-trigger     Queue and manage pipeline runs             │   │
│  │  ado-pipeline-definition  Understand pipeline YAML structure         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  📋 ADO WORK ITEM SKILLS                                             │   │
│  │  ─────────────────────────────────────────────────────────────────   │   │
│  │  ado-bug-filer            Create well-structured bug reports         │   │
│  │  ado-pr-feedback          Process and apply PR comments              │   │
│  │  ado-repo-navigator       Browse repos with branch awareness         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  💼 WORKPLACE INTELLIGENCE SKILLS                                    │   │
│  │  ─────────────────────────────────────────────────────────────────   │   │
│  │  workiq                   Query M365 for emails, meetings, docs      │   │
│  │  daily-outlook-triage     Summarize inbox and calendar               │   │
│  │  channel-digest           Summarize Teams channel activity           │   │
│  │  action-item-extractor    Extract action items from meetings         │   │
│  │  meeting-cost-calculator  Analyze meeting time investment            │   │
│  │  org-chart                Display organizational hierarchy           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  🔍 CODE ANALYSIS SKILLS                                             │   │
│  │  ─────────────────────────────────────────────────────────────────   │   │
│  │  code-review              Review staged/unstaged changes             │   │
│  │  agent-learner            Capture reusable investigation knowledge   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  ⚙️  BUILT-IN SKILLS                                                  │   │
│  │  ─────────────────────────────────────────────────────────────────   │   │
│  │  customize-cloud-agent    Configure Copilot cloud agent environment  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete Skills Reference

| Skill | Category | Purpose | Key Capabilities |
|-------|----------|---------|------------------|
| `ado-pipeline-analyzer` | Pipeline | Analyze pipeline runs and failures | Fetch run details, identify failure points, suggest fixes |
| `ado-log-investigator` | Pipeline | Deep investigation of pipeline logs | Trace errors to source, compare retry attempts |
| `ado-artifact-analyzer` | Pipeline | Examine build artifacts | Analyze test results, logs, deployment outputs |
| `ado-pipeline-trigger` | Pipeline | Queue and manage pipeline runs | Trigger builds, pass parameters |
| `ado-pipeline-definition` | Pipeline | Understand pipeline YAML | Read templates, map steps to scripts |
| `ado-bug-filer` | Work Items | Create structured bug reports | File bugs with investigation evidence |
| `ado-pr-feedback` | Work Items | Process PR review comments | Apply suggestions, resolve comments |
| `ado-repo-navigator` | Work Items | Browse repos with branch awareness | Read files at specific branches/commits |
| `workiq` | Workplace | Query M365 Copilot | Search emails, meetings, documents, Teams |
| `daily-outlook-triage` | Workplace | Daily inbox/calendar summary | Prioritize emails and meetings |
| `channel-digest` | Workplace | Teams channel summary | Key discussions, decisions, mentions |
| `action-item-extractor` | Workplace | Extract meeting action items | Owners, deadlines, priorities |
| `meeting-cost-calculator` | Workplace | Analyze meeting time | Hours spent, most expensive meetings |
| `org-chart` | Workplace | Display org hierarchy | Manager, peers, direct reports |
| `channel-audit` | Workplace | Audit Teams channels | Find inactive channels, recommend cleanup |
| `site-explorer` | Workplace | Browse SharePoint | Sites, lists, document libraries |
| `multi-plan-search` | Workplace | Search Planner tasks | Cross-plan task discovery |
| `email-analytics` | Workplace | Email pattern analysis | Volume trends, top senders, response times |
| `code-review` | Code | Review code changes | Analyze diffs, find bugs, suggest improvements |
| `agent-learner` | Code | Capture investigation knowledge | Store patterns for future investigations |
| `customize-cloud-agent` | Built-in | Configure cloud agent | Setup steps, runners, dependencies |

---

### How Skills Work Internally

When a skill is invoked, here's what happens:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SKILL EXECUTION FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    User Request                                                             │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  1. SKILL MATCHING                                                   │   │
│  │     • Copilot analyzes the request                                   │   │
│  │     • Matches against available skill descriptions                   │   │
│  │     • Selects most appropriate skill (or none)                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  2. SKILL ACTIVATION                                                 │   │
│  │     • Skill's system prompts are loaded                              │   │
│  │     • Domain knowledge becomes available                             │   │
│  │     • Tool preferences are set                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  3. ORCHESTRATED EXECUTION                                           │   │
│  │     • Skill determines tool sequence                                 │   │
│  │     • Calls tools with domain-aware parameters                       │   │
│  │     • Interprets results with specialized knowledge                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  4. STRUCTURED OUTPUT                                                │   │
│  │     • Results formatted per skill's template                         │   │
│  │     • Domain-specific recommendations included                       │   │
│  │     • Next steps suggested based on patterns                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Example: Pipeline Analyzer Skill in Action

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ado-pipeline-analyzer WORKFLOW                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  User: "Why did the CI pipeline fail?"                                      │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 1: Get Pipeline Context                                        │   │
│  │  └── Tool: azure-devops-pipelines_get_builds                         │   │
│  │      └── Gets recent builds for the repository                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 2: Identify Failed Run                                         │   │
│  │  └── Tool: azure-devops-pipelines_get_build_status                   │   │
│  │      └── Finds the failed build, gets failure stage                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 3: Fetch Logs                                                  │   │
│  │  └── Tool: azure-devops-pipelines_get_build_log                      │   │
│  │      └── Retrieves logs from failed stage/job                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 4: Analyze with Domain Knowledge                               │   │
│  │  └── Skill applies pattern recognition:                              │   │
│  │      • "npm ERR!" → dependency issue                                 │   │
│  │      • "ENOSPC" → disk space                                         │   │
│  │      • "exit code 137" → OOM killed                                  │   │
│  │      • "certificate has expired" → cert renewal needed               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 5: Find Related Code (optional)                                │   │
│  │  └── Tool: bluebird-mcp-aio-search_code                              │   │
│  │      └── Searches for code related to the failure                    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                   │
│         ▼                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Step 6: Generate Structured Report                                  │   │
│  │  • Summary: What failed and why                                      │   │
│  │  • Root cause: Specific error and pattern match                      │   │
│  │  • Recommendation: How to fix it                                     │   │
│  │  • Related: Links to code, docs, similar issues                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Skill Invocation Methods

Skills can be activated in multiple ways:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INVOKING SKILLS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. AUTOMATIC (Implicit)                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Just describe what you need—Copilot activates the relevant skill:          │
│                                                                             │
│    "Why did my pipeline fail?"                                              │
│         └── Activates: ado-pipeline-analyzer                                │
│                                                                             │
│    "What did Sarah say about the launch date?"                              │
│         └── Activates: workiq                                               │
│                                                                             │
│    "Review my changes before I commit"                                      │
│         └── Activates: code-review                                          │
│                                                                             │
│  2. EXPLICIT (By Name)                                                      │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  Mention the skill by name for precise control:                             │
│                                                                             │
│    "Use the ado-log-investigator skill to trace this error"                 │
│                                                                             │
│    "Invoke workiq to find emails about the budget"                          │
│                                                                             │
│    "Use code-review to analyze just the auth module changes"                │
│                                                                             │
│  3. VIA SKILL TOOL                                                          │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                             │
│  The CLI has a skill invocation tool for programmatic activation:           │
│                                                                             │
│    The agent calls: skill(skill: "ado-pipeline-analyzer")                   │
│                                                                             │
│    This loads the skill's context and capabilities immediately.             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### When Skills Activate Automatically

Copilot matches your request against skill descriptions. Here are trigger patterns:

| Trigger Phrases | Skill Activated |
|-----------------|-----------------|
| "pipeline failed", "build error", "CI broken" | `ado-pipeline-analyzer` |
| "trace the error", "where did this log come from" | `ado-log-investigator` |
| "file a bug", "create a work item for this" | `ado-bug-filer` |
| "address PR comments", "fix the review feedback" | `ado-pr-feedback` |
| "what did [person] say", "find emails about" | `workiq` |
| "meetings today", "what's on my calendar" | `daily-outlook-triage` |
| "summarize the Teams channel" | `channel-digest` |
| "review my changes", "check this code" | `code-review` |
| "org chart for", "who reports to" | `org-chart` |

---

## Practice

### Exercise 1: Discover Available Skills

**Step 1**: List skills available in your environment:

```
What skills do you have available?
```

Or more specifically:

```
List all the ADO-related skills you have
```

**Step 2**: Get details about a specific skill:

```
Tell me about the ado-pipeline-analyzer skill. What can it do?
```

```
What tools does the workiq skill use?
```

### Exercise 2: Pipeline Analysis Skill

> **Requires**: ADO MCP configured with access to a project with pipelines

**Step 1**: Analyze a recent pipeline run:

```
Analyze the most recent pipeline run in project "MyProject"
```

**Step 2**: Investigate a specific failure:

```
Why did build #12345 fail? Use the pipeline analyzer skill.
```

**Step 3**: Compare runs:

```
Compare the failed build #12345 with the last successful build. What changed?
```

**Step 4**: Deep log investigation (uses `ado-log-investigator`):

```
Trace the "connection refused" error in build #12345 back to its source
```

**What the skill does**:
- Fetches pipeline run details and status
- Retrieves and parses build logs
- Identifies failure patterns (OOM, timeout, dependency errors)
- Suggests specific fixes based on error type
- Links to related code when possible

### Exercise 3: Bug Filing Skill

> **Requires**: ADO MCP configured with work item write permissions

**Step 1**: File a bug from investigation:

```
File a bug for the authentication timeout issue we just investigated.
Include the stack trace and reproduction steps.
```

**Step 2**: Create a bug with specific details:

```
Use ado-bug-filer to create a bug:
- Title: Login fails intermittently under load
- Area: Backend/Authentication
- Priority: 2
- Include the log evidence from build #12345
```

**What the skill does**:
- Creates structured bug reports with proper fields
- Attaches evidence from previous investigation
- Sets appropriate area path, priority, and tags
- Links to related pipeline runs or commits

### Exercise 4: WorkIQ Skill

> **Requires**: WorkIQ MCP configured, EULA accepted

**Step 1**: Query about communications:

```
What did my manager say about priorities this week?
```

**Step 2**: Find meeting context:

```
What was discussed in yesterday's standup meeting?
```

**Step 3**: Search across M365:

```
Find all documents and emails about the Q4 launch from the last month
```

**Step 4**: People intelligence:

```
What has the platform team been working on this sprint?
```

**What the skill does**:
- Queries Microsoft 365 Copilot for workplace data
- Searches across emails, meetings, documents, Teams
- Synthesizes information from multiple sources
- Respects access permissions (only sees what you can see)

### Exercise 5: Code Review Skill

**Step 1**: Make changes to your practice project:

```bash
# Edit a file in your project
echo "// TODO: implement authentication" >> src/auth.js
git add src/auth.js
```

**Step 2**: Request a code review:

```
Review my staged changes
```

Or be more specific:

```
Use the code-review skill to analyze my changes. 
Focus on security issues and potential bugs.
```

**Step 3**: Review unstaged changes:

```
Review all my uncommitted changes, both staged and unstaged
```

**What the skill does**:
- Analyzes staged and/or unstaged git changes
- Identifies bugs, security issues, logic errors
- Provides high signal-to-noise feedback (ignores style nits)
- Suggests specific improvements

### Exercise 6: PR Feedback Skill

> **Requires**: ADO MCP configured with an open PR that has comments

**Step 1**: Fetch PR comments:

```
Get the review comments on PR #456 in repository "backend-api"
```

**Step 2**: Apply suggested changes:

```
Apply the suggested changes from the PR review comments
```

**Step 3**: Address specific feedback:

```
Address the comment about error handling in the auth module
```

**What the skill does**:
- Fetches all comments from a PR
- Identifies actionable suggestions
- Applies code changes from suggestions
- Can resolve comments after addressing them

### Exercise 7: Multi-Skill Workflow

Try a complex task that activates multiple skills in sequence:

**Scenario 1**: Full investigation flow

```
The production deployment failed an hour ago. 
1. Find out what failed and why
2. Check if there are any related bugs already filed
3. If not, file a bug with the evidence
4. Find any emails or Teams messages about this issue
```

**Scenario 2**: Code change to deployment

```
I need to fix bug #789.
1. Show me the bug details
2. Find the related code
3. Help me implement a fix
4. Review my changes
5. Create a PR
```

**Scenario 3**: Investigation with context gathering

```
Users are reporting slow API responses.
1. Check recent pipeline deployments for changes
2. Search the codebase for the affected endpoint
3. Find any related discussions in Teams
4. Summarize what might have changed

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

### Question 4

What is the difference between a Tool and a Skill?

A) Tools are faster than Skills  
B) Skills combine multiple tools with domain knowledge and specialized prompts  
C) Tools are for code, Skills are for documentation  
D) There is no difference  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

A Tool is a single atomic operation (like `get_pipeline_run`), while a Skill combines multiple tools with specialized prompts and domain knowledge to handle complete workflows (like analyzing a pipeline failure end-to-end).

</details>

---

### Question 5

Which skill category would help you find information about what your team discussed in a Teams channel?

A) ADO Pipeline Skills  
B) Code Analysis Skills  
C) Workplace Intelligence Skills  
D) Built-in Skills  

<details>
<summary>Click to reveal answer</summary>

**Answer: C**

Workplace Intelligence Skills (like `workiq`, `channel-digest`, and `channel-audit`) integrate with Microsoft 365 to provide access to Teams messages, emails, meetings, and documents.

</details>

---

### Question 6

What happens when you say "Why did my build fail?" to Copilot CLI?

A) Copilot asks you to specify which skill to use  
B) Copilot automatically activates the `ado-pipeline-analyzer` skill  
C) Copilot searches for documentation about builds  
D) Copilot requires you to manually run the `/skill` command  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Skills activate automatically based on context. Phrases like "build failed", "pipeline error", or "CI broken" trigger the `ado-pipeline-analyzer` skill without requiring explicit invocation.

</details>

---

## Key Takeaways

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SKILLS SUMMARY                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ✓ Skills = Tools + Prompts + Domain Knowledge                              │
│                                                                             │
│  ✓ Skills provide complete workflow capabilities, not just single ops       │
│                                                                             │
│  ✓ Skills activate automatically based on your request context              │
│                                                                             │
│  ✓ You can also invoke skills explicitly by name                            │
│                                                                             │
│  ✓ Multiple skills can work together on complex tasks                       │
│                                                                             │
│  Key Skill Categories:                                                      │
│  • ADO Pipeline: Analyze, debug, trigger pipelines                          │
│  • ADO Work Items: File bugs, process PR feedback                           │
│  • Workplace Intelligence: M365 emails, meetings, Teams                     │
│  • Code Analysis: Review changes, learn from investigations                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Next Steps

Continue to [Tutorial 4.4: Custom Agents](./04-custom-agents.md) to create your own specialized agents.
