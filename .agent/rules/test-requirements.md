---
trigger: always_on
---

# Coding Test — Workspace Rules

## 1. Prompt Logging
After every user prompt, append an entry to `prompt.md` **before doing any work**:

```
## Prompt N
**Prompt:** <exact user wording, never paraphrased>
**Helped with:** <one line>
```

- N is the next sequential integer (count existing `## Prompt` headings + 1).
- Never backfill, reorder, or edit past entries.
- Use the user's exact words verbatim.

## 2. Workflow
1. Write a brief plan (2–5 bullet points) before writing any code.
2. Make one small, focused change at a time.
3. Run `pytest` after every change; fix failures before moving on.

## 3. Code Quality
- No failing tests at any commit point.
- No dead code or commented-out blocks.
- Validate all inputs with Pydantic; never let raw exceptions escape a handler.
- Add every new dependency to `requirements.txt`.

## 4. README
Keep the bottom of `README.md` current with:
- How to run the app (`uvicorn` command).
- How to run tests (`pytest` command).
- A short **Design Decisions** section explaining non-obvious choices.
