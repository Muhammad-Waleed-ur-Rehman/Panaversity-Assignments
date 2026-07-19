# Task 5 — Audit a Skill Before Trusting It

## Skill audited
I audited an example skill from the official skills directory.
npx skills add https://github.com/claude-office-skills/skills --skill email-drafter

## Safety assessment
The skill appears safe as it only writes or summarizes text and does not ask for credentials, send data externally, or modify account settings.

## Verdict
I would trust as it stays within text generation and approved read-only access, and it does not request sensitive data.

## Why this matters
A good safety audit checks what the skill touches, whether it uses external services, and whether it could expose private information.
