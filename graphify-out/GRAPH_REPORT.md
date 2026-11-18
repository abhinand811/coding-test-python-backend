# Graph Report - coding-test-python-backend  (2026-11-18)

## Corpus Check
- 7 files · ~1,349 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 1 file(s) not represented in the graph (top: (none) 1)

## Summary
- 36 nodes · 29 edges · 9 communities (6 shown, 3 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `dba0879f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Coding Test — Workspace Rules
- Clean Code Standards
- AGENTS.md — Project Guidelines for AI Agents
- AI Prompt Log — Coding Test
- Testing Standards
- coding-test-python-backend

## God Nodes (most connected - your core abstractions)
1. `Clean Code Standards` - 6 edges
2. `AGENTS.md — Project Guidelines for AI Agents` - 6 edges
3. `coding-test-python-backend` - 5 edges
4. `Coding Test — Workspace Rules` - 5 edges
5. `AI Prompt Log — Coding Test` - 4 edges
6. `Testing Standards` - 4 edges
7. `Knowledge Graph (Graphify)` - 2 edges
8. `Running the Application` - 1 edges
9. `Running Tests` - 1 edges
10. `Update Command` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (9 total, 3 thin omitted)

### Community 0 - "Coding Test — Workspace Rules"
Cohesion: 0.33
Nodes (5): 1. Prompt Logging, 2. Workflow, 3. Code Quality, 4. README, Coding Test — Workspace Rules

### Community 1 - "Clean Code Standards"
Cohesion: 0.33
Nodes (6): Async, Clean Code Standards, Error Handling, Pydantic Models, Route Handlers (keep them thin), Type Hints

### Community 2 - "AGENTS.md — Project Guidelines for AI Agents"
Cohesion: 0.40
Nodes (4): AGENTS.md — Project Guidelines for AI Agents, General Rules, Repository Layout, Stack

### Community 3 - "AI Prompt Log — Coding Test"
Cohesion: 0.40
Nodes (4): AI Prompt Log — Coding Test, Prompt 1, Prompt 2, Prompt 3

### Community 4 - "Testing Standards"
Cohesion: 0.50
Nodes (4): Naming, Rules, Setup, Testing Standards

### Community 5 - "coding-test-python-backend"
Cohesion: 0.29
Nodes (6): coding-test-python-backend, Design Decisions, Knowledge Graph (Graphify), Running Tests, Running the Application, Update Command

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AGENTS.md — Project Guidelines for AI Agents` connect `AGENTS.md — Project Guidelines for AI Agents` to `Clean Code Standards`, `Testing Standards`?**
  _High betweenness centrality (0.118) - this node is a cross-community bridge._
- **Why does `Clean Code Standards` connect `Clean Code Standards` to `AGENTS.md — Project Guidelines for AI Agents`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `Testing Standards` connect `Testing Standards` to `AGENTS.md — Project Guidelines for AI Agents`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._