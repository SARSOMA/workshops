# Tutorial 5.2: Skills & Automation

## Introduction

Skills extend Copilot CLI's capabilities with reusable instructions, scripts, and resources. They're perfect for automating repetitive tasks and ensuring consistency.

## What are Skills?

Skills are packages that provide:
- **Instructions**: How to perform a task
- **Scripts**: Executable code to run
- **Resources**: Templates, schemas, reference data
- **Tools**: Custom tool definitions

---

## Managing Skills

### View Available Skills

```
/skills
```

Shows:
- Installed skills
- Skill status
- Available actions

### Skill Locations

```
~/.copilot/skills/           # User skills
.github/skills/              # Repository skills
```

---

## Skill Structure

A skill is a directory with specific files:

```
my-skill/
├── skill.yaml          # Skill definition (required)
├── instructions.md     # Instructions for Copilot
├── scripts/            # Executable scripts
│   ├── setup.sh
│   └── generate.js
├── templates/          # File templates
│   └── component.tsx.template
└── resources/          # Reference data
    └── schema.json
```

### skill.yaml

```yaml
name: react-component-generator
description: Generate React components following team conventions
version: 1.0.0

resources:
  - templates/component.tsx.template
  - templates/component.test.tsx.template
  - resources/prop-types.json

scripts:
  - name: generate
    command: node scripts/generate.js
    description: Generate a new React component

instructions:
  file: instructions.md
```

---

## Creating a Simple Skill

### Example: React Component Generator

Create directory structure:
```bash
mkdir -p ~/.copilot/skills/react-generator/templates
mkdir -p ~/.copilot/skills/react-generator/scripts
```

### 1. Create skill.yaml

```yaml
# ~/.copilot/skills/react-generator/skill.yaml
name: react-generator
description: Generate React components with tests and styles
version: 1.0.0

resources:
  - templates/component.tsx.template
  - templates/component.test.tsx.template
  - templates/component.module.css.template

instructions:
  file: instructions.md
```

### 2. Create instructions.md

```markdown
# React Component Generator

Use this skill to generate React components following our conventions.

## Usage

When asked to generate a React component, follow these steps:

1. Use the component template from templates/component.tsx.template
2. Replace placeholders:
   - {{ComponentName}}: PascalCase component name
   - {{componentName}}: camelCase version
   - {{props}}: TypeScript props interface

3. Generate corresponding test file from templates/component.test.tsx.template

4. Generate CSS module from templates/component.module.css.template

## Conventions

- Functional components only
- Use TypeScript
- Props interface named {ComponentName}Props
- Export as default
- CSS Modules for styling
```

### 3. Create Templates

**templates/component.tsx.template:**
```tsx
import React from 'react';
import styles from './{{ComponentName}}.module.css';

export interface {{ComponentName}}Props {
  {{props}}
}

export default function {{ComponentName}}({ {{destructuredProps}} }: {{ComponentName}}Props) {
  return (
    <div className={styles.container}>
      {/* Component content */}
    </div>
  );
}
```

**templates/component.test.tsx.template:**
```tsx
import { render, screen } from '@testing-library/react';
import {{ComponentName}} from './{{ComponentName}}';

describe('{{ComponentName}}', () => {
  it('renders without crashing', () => {
    render(<{{ComponentName}} />);
  });
});
```

**templates/component.module.css.template:**
```css
.container {
  /* Add styles */
}
```

---

## Using Skills

### Reference in Prompts

```
Using the react-generator skill, create a UserProfile component 
with name and email props
```

### Invoke via /skills

```
/skills
```

Select the skill from the list.

---

## Advanced Skill Features

### Scripts

Add executable scripts for automation:

**scripts/generate.js:**
```javascript
#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const componentName = process.argv[2];
if (!componentName) {
  console.error('Usage: generate.js <ComponentName>');
  process.exit(1);
}

// Read template
const templatePath = path.join(__dirname, '../templates/component.tsx.template');
const template = fs.readFileSync(templatePath, 'utf-8');

// Replace placeholders
const content = template
  .replace(/\{\{ComponentName\}\}/g, componentName)
  .replace(/\{\{componentName\}\}/g, componentName.charAt(0).toLowerCase() + componentName.slice(1));

// Write component
const outputPath = `./src/components/${componentName}/${componentName}.tsx`;
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, content);

console.log(`Created ${outputPath}`);
```

Reference in skill.yaml:
```yaml
scripts:
  - name: generate
    command: node scripts/generate.js
    description: Generate a component structure
    args:
      - name: componentName
        description: Name of the component
        required: true
```

### Resources

Include reference data:

**resources/api-schema.json:**
```json
{
  "endpoints": {
    "/users": {
      "methods": ["GET", "POST"],
      "auth": "required"
    },
    "/users/:id": {
      "methods": ["GET", "PUT", "DELETE"],
      "auth": "required"
    }
  }
}
```

Reference in instructions:
```markdown
When generating API clients, refer to the schema in resources/api-schema.json
for endpoint definitions.
```

---

## Practical Skill Examples

### Example 1: Database Migration Skill

```yaml
name: db-migrations
description: Generate and manage database migrations
version: 1.0.0

scripts:
  - name: create
    command: npx prisma migrate dev --name
    description: Create a new migration
  - name: run
    command: npx prisma migrate deploy
    description: Run pending migrations
  - name: status
    command: npx prisma migrate status
    description: Check migration status

instructions:
  content: |
    # Database Migration Skill
    
    When asked about database changes:
    1. Generate Prisma schema changes
    2. Run the create script to create a migration
    3. Verify the generated SQL
    4. Run the migration if approved
```

### Example 2: Documentation Generator

```yaml
name: doc-generator
description: Generate documentation from code
version: 1.0.0

resources:
  - templates/api-docs.md.template
  - templates/component-docs.md.template

instructions:
  content: |
    # Documentation Generator
    
    Generate documentation following our standards:
    
    ## For APIs
    - Include endpoint URL, method, auth requirements
    - Document request/response with examples
    - Include error codes
    
    ## For Components
    - Document props with types
    - Include usage examples
    - Note any side effects or dependencies
```

---

## Exercise: Create a Skill

### Exercise 5.2.1: Simple Skill

Create a skill for your common task:

1. Choose a repetitive task you do often
2. Create the skill structure:
   ```bash
   mkdir -p ~/.copilot/skills/my-task
   ```
3. Create `skill.yaml` and `instructions.md`
4. Test: `/skills` and select your skill

Ideas:
- Test file generator
- API endpoint scaffolding
- Documentation template
- Code review checklist

### Exercise 5.2.2: Skill with Templates

1. Add a templates directory to your skill
2. Create template files with placeholders
3. Update instructions to reference templates
4. Test the skill generates from templates

---

## Best Practices

### 1. Keep Skills Focused

Each skill should do one thing well:
- ✅ "React Component Generator"
- ✅ "API Documentation Generator"
- ❌ "General Code Helper" (too broad)

### 2. Version Your Skills

```yaml
version: 1.0.0  # Semantic versioning
```

### 3. Include Examples

In instructions.md:
```markdown
## Example

Input: "Create a UserCard component with name and avatar props"

Output:
- src/components/UserCard/UserCard.tsx
- src/components/UserCard/UserCard.test.tsx
- src/components/UserCard/UserCard.module.css
```

### 4. Document Prerequisites

```markdown
## Prerequisites

- Node.js 18+
- npm or yarn
- Project must have @testing-library/react installed
```

---

## Key Takeaways

1. **Skills package reusable automation**
2. **Structure**: skill.yaml + instructions + resources
3. **Include templates** for consistent output
4. **Add scripts** for complex automation
5. **Focus each skill** on one task
6. **Share skills** via repository or organization

---

## Next Tutorial

Continue to [Tutorial 5.3: Programmatic Usage](./03-programmatic-usage.md) for scripting with Copilot CLI.
