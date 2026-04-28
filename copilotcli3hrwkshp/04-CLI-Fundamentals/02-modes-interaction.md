# Tutorial 4.2: Modes & Interaction Patterns

## Introduction

Copilot CLI offers multiple modes for different tasks. Understanding when and how to use each mode makes you more effective.

## Available Modes

```
┌─────────────────────────────────────────────────────────────────┐
│                     MODE COMPARISON                              │
├─────────────────────────────────────────────────────────────────┤
│  INTERACTIVE (Default)                                          │
│  • Turn-by-turn conversation                                    │
│  • Immediate execution with approval                            │
│  • Best for: Exploration, Q&A, quick tasks                      │
├─────────────────────────────────────────────────────────────────┤
│  PLAN MODE                                                      │
│  • Collaborative planning before coding                         │
│  • Clarifying questions and structured plans                    │
│  • Best for: Complex features, multi-step tasks                 │
├─────────────────────────────────────────────────────────────────┤
│  AUTOPILOT (Experimental)                                       │
│  • Autonomous execution                                         │
│  • Continues until task completion                              │
│  • Best for: Routine tasks, confident implementations           │
└─────────────────────────────────────────────────────────────────┘
```

### Switching Modes

Press `Shift+Tab` to cycle through modes:

```
Interactive → Plan → Autopilot → Interactive → ...
```

The current mode is shown in the status bar.

---

## Interactive Mode (Default)

### Characteristics

- Standard conversation flow
- Each prompt gets a response
- Tool use requires approval
- Full control at every step

### When to Use

- Exploring a codebase
- Asking questions
- Quick fixes
- Learning how Copilot approaches problems

### Example Session

```
You: Explain the authentication flow in this project

Copilot: [Reads files, explains the flow]

You: Can you suggest improvements?

Copilot: [Analyzes and suggests improvements]

You: Implement the first suggestion

Copilot: [Asks for approval, makes changes]
```

### Steering the Conversation

You can add messages while Copilot is thinking:

```
You: Refactor the user service

[Copilot starts working]

You: Actually, use async/await instead of promises

[Copilot incorporates your feedback]
```

---

## Plan Mode

### Characteristics

- Planning before implementation
- Asks clarifying questions
- Creates structured plans
- Waits for approval before coding

### Entering Plan Mode

Method 1: Press `Shift+Tab` to cycle to Plan mode

Method 2: Use the `/plan` command:
```
/plan Create a REST API for user management
```

Method 3: Start prompt with plan intent:
```
[PLAN] Create a REST API for user management
```

### When to Use

- Complex multi-step implementations
- Uncertain requirements
- Tasks where mistakes are costly
- Team collaboration (share the plan)

### Example Session

```
[PLAN] Create a user authentication system with JWT

Copilot: I'll help you create a user authentication system. 
Let me ask a few clarifying questions:

1. Which JWT library do you prefer?
   - jsonwebtoken (most common)
   - jose (modern)
   
2. Do you need refresh tokens?
   - Yes, with rotation
   - Yes, simple
   - No, just access tokens

3. Where should tokens be stored client-side?
   - HTTP-only cookies
   - localStorage
   - sessionStorage

You: 1. jsonwebtoken, 2. Yes with rotation, 3. HTTP-only cookies

Copilot: Here's my implementation plan:

## Authentication System Plan

### 1. User Model Setup
- Add password hash field
- Add refreshToken field
- Create User model in @src/models/User.js

### 2. Auth Routes
- POST /auth/register
- POST /auth/login
- POST /auth/refresh
- POST /auth/logout

[... detailed plan continues ...]

Should I proceed with implementation?

You: Yes, start with the User model

Copilot: [Switches to implementation mode]
```

### Plan Mode Benefits

1. **Catches misunderstandings early** - Before any code is written
2. **Creates documentation** - Plan serves as implementation record
3. **Enables collaboration** - Share plan with team
4. **Prevents scope creep** - Clear boundaries defined upfront

---

## Autopilot Mode (Experimental)

### Enabling Experimental Features

First, enable experimental mode:
```
/experimental
```

Or launch with flag:
```bash
copilot --experimental
```

### Characteristics

- Autonomous task execution
- Continues without confirmation
- Completes multi-step tasks
- Minimal interruption

### When to Use

- Well-defined routine tasks
- High confidence implementations
- Batch operations
- When you trust the approach

### Safety Considerations

Even in Autopilot:
- Tools still require initial approval
- You can interrupt with `Ctrl+C`
- Changes are trackable with `/diff`
- Use `/rewind` to undo if needed

### Example Session

```
[Autopilot] Add unit tests for all functions in @src/utils/

Copilot: 
✓ Analyzing utils directory
✓ Found 5 files with 23 functions
✓ Creating tests/utils/helpers.test.js
✓ Creating tests/utils/validators.test.js
✓ Creating tests/utils/formatters.test.js
✓ Running tests... 23/23 passing

Task complete. Created 3 test files covering 23 functions.
```

---

## Interaction Patterns

### Pattern 1: Iterative Refinement

Start broad, then refine:

```
Turn 1: Create a React component for user profiles
Turn 2: Add loading state
Turn 3: Add error handling
Turn 4: Add TypeScript types
Turn 5: Add unit tests
```

### Pattern 2: Plan Then Execute

Use Plan mode for design, then switch:

```
[PLAN] Design a caching layer

[Review and approve plan]

[Switch to Interactive with Shift+Tab]

Let's implement step 1 of the plan
```

### Pattern 3: Exploratory Development

Use `/ask` for side questions:

```
/ask What's the best approach for caching in Node.js?

[Read the answer, doesn't affect main conversation]

Now implement caching using Redis following the pattern in @src/cache/
```

### Pattern 4: Batch Operations

Use Autopilot for repetitive tasks:

```
[Autopilot] Update all import statements in @src/ from CommonJS to ES modules
```

---

## Inline Feedback

### During Tool Approval

When you reject a tool, provide feedback:

```
Copilot wants to run: rm -rf node_modules && npm install

[Press Esc]

You: Don't delete node_modules. Just run npm update for outdated packages.

[Copilot adjusts approach]
```

### During Generation

Add clarifications while Copilot works:

```
Copilot: [Generating a service class]

You: Add dependency injection for the database connection

[Copilot incorporates this in the current generation]
```

---

## Exercise: Mode Mastery

### Exercise 4.2.1: Interactive Mode

1. Start in Interactive mode (default)
2. Ask: "What testing frameworks are commonly used with Node.js?"
3. Follow up: "Which one would you recommend for a REST API?"
4. Ask to see an example test

### Exercise 4.2.2: Plan Mode

1. Switch to Plan mode: `Shift+Tab`
2. Enter: "Create a file upload feature"
3. Answer the clarifying questions
4. Review the generated plan
5. Approve or request changes

### Exercise 4.2.3: Mode Comparison

Try the same task in different modes:

**Task:** Add input validation to a form

**Interactive Mode:**
```
Add email validation to the contact form in @src/components/ContactForm.jsx
```

**Plan Mode:**
```
[PLAN] Add comprehensive input validation to the contact form
```

Compare:
- Which gave more thorough results?
- Which was faster?
- When would you use each?

---

## Mode Selection Guide

```
┌─────────────────────────────────────────────────────────────────┐
│                    WHICH MODE SHOULD I USE?                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  START                                                          │
│    │                                                            │
│    ▼                                                            │
│  Is the task well-defined?                                      │
│    │                                                            │
│    ├─── No ──► Is it complex?                                   │
│    │             │                                              │
│    │             ├─── Yes ──► PLAN MODE                         │
│    │             │            (Clarify first)                   │
│    │             │                                              │
│    │             └─── No ──► INTERACTIVE                        │
│    │                         (Explore together)                 │
│    │                                                            │
│    └─── Yes ──► Is it routine/repetitive?                       │
│                   │                                             │
│                   ├─── Yes ──► AUTOPILOT                        │
│                   │            (Let it run)                     │
│                   │                                             │
│                   └─── No ──► Do you want full control?         │
│                                  │                              │
│                                  ├─── Yes ──► INTERACTIVE       │
│                                  │                              │
│                                  └─── No ──► AUTOPILOT          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Interactive** is default—good for exploration and control
2. **Plan Mode** prevents mistakes on complex tasks
3. **Autopilot** speeds up routine work (experimental)
4. **Switch freely** with `Shift+Tab`
5. **Provide inline feedback** to steer any mode
6. **Choose based on confidence** and task complexity

---

## Next Tutorial

Continue to [Tutorial 4.3: Terminal-First Workflows](./03-terminal-workflows.md) for practical workflow patterns.
