# Tutorial 5.1: Project Setup

---

## Concept

### The Akri Project

**[Akri](https://github.com/SARSOMA/akri)** is a Kubernetes resource interface for the edge that enables discovering and using leaf devices. For this workshop, we'll use it as a real-world codebase to practice Copilot CLI workflows.

### Why a Real Project?

- **Realistic complexity**: Not a toy example
- **Unfamiliar codebase**: Simulates joining a new team
- **Public repo**: Anyone can view and contribute
- **Good structure**: Well-organized code to explore

### What We'll Do

1. Clone the repository
2. Explore the project structure
3. Understand key components
4. Identify areas for improvement

---

## Practice

### Exercise 1: Clone the Repository

1. **Create a workshop directory:**
   ```bash
   mkdir -p ~/workshop-projects
   cd ~/workshop-projects
   ```

2. **Clone the akri repository:**
   ```bash
   git clone https://github.com/SARSOMA/akri.git
   cd akri
   ```

3. **Launch Copilot CLI:**
   ```bash
   copilot
   ```

4. **Trust the directory** when prompted

### Exercise 2: Understand Project Structure

Ask Copilot to explain the project:

```
What is this project about? Give me a high-level overview.
```

```
Show me the project structure and explain the main directories
```

```
What programming languages and frameworks are used?
```

### Exercise 3: Explore Key Components

Dive deeper into specific areas:

```
Explain the architecture of this project. What are the main components?
```

```
Show me @README.md and summarize the key points
```

```
What are the main entry points for the application?
```

### Exercise 4: Find Documentation

```
Where is the documentation located? Summarize what's available.
```

```
Are there any contributing guidelines? What should I know before making changes?
```

### Exercise 5: Check Project Health

```
Show me recent commits - what has been happening in this project?
```

```
Are there any open issues that would be good for a first-time contributor?
```

```
What does the CI/CD pipeline look like?
```

### Exercise 6: Identify Code Patterns

```
What coding conventions does this project follow?
```

```
Show me an example of how tests are structured in this project
```

```
What error handling patterns are used?
```

---

## Q&A

### Question 1

What is the first thing you should do when exploring a new codebase with Copilot CLI?

A) Start making changes immediately  
B) Ask for a high-level overview and project structure  
C) Run all the tests  
D) Delete unnecessary files  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

When exploring a new codebase, start by asking for a high-level overview and understanding the project structure. This gives you context before diving into specific files or making changes.

</details>

---

### Question 2

Why is using a real, unfamiliar codebase good practice?

A) It's easier than toy examples  
B) It simulates the real experience of joining a new team or project  
C) It has fewer bugs  
D) It's faster to understand  

<details>
<summary>Click to reveal answer</summary>

**Answer: B**

Using a real, unfamiliar codebase simulates the actual experience of joining a new team or contributing to an open source project. This is more valuable practice than working with simple examples you already understand.

</details>

---

## Key Prompts Reference

Save these for future use:

| Goal | Prompt |
|------|--------|
| Overview | "What is this project about?" |
| Structure | "Show me the project structure" |
| Architecture | "Explain the architecture" |
| Entry points | "What are the main entry points?" |
| Conventions | "What coding conventions are used?" |
| Contributing | "How do I contribute to this project?" |
| Recent activity | "Show me recent commits" |

---

## Next Steps

Continue to [Tutorial 5.2: Making Changes](./02-making-changes.md) to implement a small change in the project.
