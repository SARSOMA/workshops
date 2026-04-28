# Section 2: Core Concepts

## Overview

This section covers how GitHub Copilot CLI works internally — its architecture, configuration system, and how it builds context. Understanding these concepts helps you use Copilot CLI more effectively.

## Learning Objectives

By the end of this section, you will be able to:
- Explain the Copilot CLI architecture and agentic loop
- Describe the configuration hierarchy
- Understand how Copilot builds and utilizes context
- Know where configuration files are stored

## Duration

**10 minutes**

## Tutorials

| Tutorial | Description |
|----------|-------------|
| [2.1 Architecture & Configuration](./01-architecture-config.md) | Concept + Practice + Q&A |

## Prerequisites

- Completed Section 1
- Working Copilot CLI installation

## Key Takeaways

- Copilot CLI uses an agentic loop: Understand → Plan → Execute → Verify
- Configuration flows: CLI flags → Environment → Repository → User → Organization
- Context is automatically built from your directory tree and can be manually enhanced
