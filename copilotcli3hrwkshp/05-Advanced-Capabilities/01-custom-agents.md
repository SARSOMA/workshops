# Tutorial 5.1: Custom Agents

## Introduction

Custom agents are specialized versions of Copilot tailored for specific tasks, coding conventions, or workflows. This tutorial shows you how to create and use them.

## Understanding Agents

### Built-in Sub-Agents

Copilot CLI includes these default agents:

| Agent | Description | When Used |
|-------|-------------|-----------|
| **Explore** | Quick codebase analysis | Finding code, understanding structure |
| **Task** | Command execution | Running tests, builds |
| **General-purpose** | Complex multi-step tasks | Large implementations |
| **Code-review** | Analyze changes | Reviewing PRs, diffs |

### Custom Agents Extend This

You can create agents that:
- Follow your team's coding standards
- Specialize in specific domains
- Use particular tools or approaches
- Apply custom instructions

---

## Agent Profile Structure

Agents are defined in Markdown files:

```markdown
---
name: my-agent
description: Description of what this agent does
tools:
  - file-operations
  - shell
  - git
---

# Agent Instructions

Your detailed instructions here...
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier |
| `description` | Yes | What the agent does |
| `tools` | No | Available tools (defaults to all) |
| `model` | No | Specific model to use |

---

## Agent Locations

### User-Level Agents

Location: `~/.copilot/agents/`

Available in all projects:

```
~/.copilot/agents/
├── security-reviewer.md
├── documentation-writer.md
└── performance-optimizer.md
```

### Repository-Level Agents

Location: `.github/agents/`

Available only in this repository:

```
my-project/
└── .github/
    └── agents/
        ├── api-designer.md
        └── test-generator.md
```

### Organization-Level Agents

Location: `/.github-private/agents/` in your organization

Available to all repos in the organization.

### Precedence

```
System/Built-in > Repository > Organization > User
```

If names conflict, higher precedence wins.

---

## Creating Your First Agent

### Example: Code Reviewer Agent

Create `~/.copilot/agents/strict-reviewer.md`:

```markdown
---
name: strict-reviewer
description: Performs strict code reviews with security and performance focus
tools:
  - file-operations
  - shell
---

# Strict Code Reviewer

You are a senior software engineer performing thorough code reviews.

## Review Criteria

When reviewing code, always check for:

### Security
- SQL injection vulnerabilities
- XSS vulnerabilities  
- Sensitive data exposure
- Proper input validation
- Authentication/authorization issues

### Performance
- N+1 query problems
- Unnecessary re-renders (React)
- Missing caching opportunities
- Large bundle sizes
- Memory leaks

### Code Quality
- DRY violations
- SOLID principles adherence
- Error handling completeness
- Test coverage
- Documentation

## Response Format

Structure your review as:

1. **Critical Issues** (must fix before merge)
2. **Warnings** (should address)
3. **Suggestions** (nice to have)
4. **Positive Notes** (what's done well)

## Tone

Be constructive and educational. Explain why issues are problems
and how to fix them. Acknowledge good practices.
```

### Example: TypeScript Expert Agent

Create `.github/agents/typescript-expert.md`:

```markdown
---
name: typescript-expert
description: TypeScript specialist following strict typing practices
tools:
  - file-operations
  - shell
  - lsp
---

# TypeScript Expert

You are a TypeScript expert who values type safety above all else.

## Principles

1. **Strict mode always** - Enable all strict checks
2. **No `any`** - Use `unknown` and type guards instead
3. **Explicit returns** - Always declare return types
4. **Discriminated unions** - Prefer over optional fields
5. **Const assertions** - Use `as const` for literals

## Patterns

When writing TypeScript:

### Prefer interfaces for objects
```typescript
interface User {
  id: string;
  name: string;
}
```

### Use type guards
```typescript
function isUser(value: unknown): value is User {
  return typeof value === 'object' && value !== null && 'id' in value;
}
```

### Avoid any, use unknown
```typescript
// Bad
function parse(data: any) { ... }

// Good
function parse(data: unknown) {
  if (isValidData(data)) { ... }
}
```

## When generating code

- Add JSDoc comments for public APIs
- Include type annotations on all parameters
- Define return types explicitly
- Create interfaces in a separate types file
```

---

## Using Custom Agents

### Method 1: Agent Browser

```
/agent
```

Shows a picker with all available agents.

### Method 2: Direct Reference

In your prompt:
```
Use the strict-reviewer agent to review my changes
```

Copilot infers which agent you want.

### Method 3: Command-Line Flag

```bash
copilot --agent=strict-reviewer --prompt "Review my changes"
```

### Method 4: Let Copilot Delegate

Copilot automatically delegates to appropriate agents:
```
Review my code changes
```

May automatically invoke code-review or your custom reviewer.

---

## Advanced Agent Configuration

### Restricting Tools

```markdown
---
name: safe-analyst
description: Read-only code analysis
tools:
  - file-operations-readonly
  - search
---
```

This agent cannot modify files.

### Specifying Model

```markdown
---
name: complex-architect
description: Complex architectural analysis
model: claude-opus-4
---
```

Uses a more capable (and expensive) model.

### Adding Examples

```markdown
# Documentation Writer

## Example Output

When documenting a function, format like this:

\`\`\`typescript
/**
 * Calculates the total price including tax.
 * 
 * @param subtotal - The pre-tax amount
 * @param taxRate - The tax rate as a decimal (e.g., 0.07 for 7%)
 * @returns The total price including tax
 * 
 * @example
 * const total = calculateTotal(100, 0.07);
 * console.log(total); // 107
 */
function calculateTotal(subtotal: number, taxRate: number): number {
  return subtotal * (1 + taxRate);
}
\`\`\`
```

---

## Exercise: Create Custom Agents

### Exercise 5.1.1: Create a Review Agent

1. Create `~/.copilot/agents/my-reviewer.md`:

```markdown
---
name: my-reviewer
description: Reviews code for my specific project standards
---

# My Code Reviewer

Review code for:
- Consistent naming conventions
- Proper error handling
- Performance considerations

Always be constructive in feedback.
```

2. Launch Copilot CLI
3. Test: `Use my-reviewer to check @src/index.js`

### Exercise 5.1.2: Create a Domain Expert

Create an agent for your specific domain:

Examples:
- `react-expert.md` - React best practices
- `api-designer.md` - REST API design
- `sql-optimizer.md` - Database query optimization
- `security-auditor.md` - Security analysis

### Exercise 5.1.3: Repository-Specific Agent

1. In your project, create `.github/agents/project-guide.md`:

```markdown
---
name: project-guide
description: Knows this project's specific conventions
---

# Project Guide

This project uses:
- [Your framework]
- [Your patterns]
- [Your conventions]

When generating code, follow these patterns from:
- @src/services/example.js (service pattern)
- @src/components/Example.jsx (component pattern)
```

2. Commit and push
3. Test the agent in your project

---

## Best Practices

### 1. Be Specific About Standards

❌ Vague:
```markdown
Write good code.
```

✅ Specific:
```markdown
Follow these conventions:
- Use 2-space indentation
- Prefer const over let
- Use async/await over callbacks
```

### 2. Include Examples

Show, don't just tell:
```markdown
## Error Handling Example

Always wrap async operations:
\`\`\`javascript
try {
  const result = await fetchData();
  return result;
} catch (error) {
  logger.error('Fetch failed', { error });
  throw new ApplicationError('Data unavailable', error);
}
\`\`\`
```

### 3. Define Response Format

```markdown
## Response Format

Always structure responses as:
1. Summary of changes
2. Files modified (with line numbers)
3. Testing suggestions
4. Documentation updates needed
```

### 4. Set Boundaries

```markdown
## Scope

This agent handles:
- Frontend React components
- CSS/styling
- Client-side state

This agent does NOT handle:
- Backend APIs
- Database operations
- Infrastructure
```

---

## Key Takeaways

1. **Agents specialize Copilot** for specific tasks
2. **Three levels**: User, Repository, Organization
3. **Markdown format** with optional frontmatter
4. **Invoke directly** or let Copilot delegate
5. **Include examples** for best results
6. **Restrict tools** for safety when needed

---

## Next Tutorial

Continue to [Tutorial 5.2: Skills & Automation](./02-skills-automation.md) for building reusable skills.
