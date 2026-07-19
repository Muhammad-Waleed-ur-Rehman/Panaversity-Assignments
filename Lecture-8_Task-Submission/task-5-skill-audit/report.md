# Task 5 Report

## Project title and what it does
Skill Safety Audit — this project reviews whether a skill is safe to trust by checking what it touches and whether it requests sensitive information.

## AI tools and apps used
- AI assistant Claude.ai
- Official skills directory example from Skills.sh

## Prompts used and how they were refined
- Prompt used: “Explain what this skill does and flag any sensitive actions it might take.”
- Refinement: I focused the prompt on privacy, external access, and permission concerns.

## How I tested or verified it worked
I asked the AI to explain the skill in plain English and evaluate whether it could contact external services or handle sensitive data.

## What worked, what did not, and problems faced
- Worked well: the skill explanation was clear and easy to assess.
- Problem faced: the main challenge was judging safety without reading code, so I had to rely on plain-language behavior.

## Safety assessment and verdict
The skill appears safe if it only writes or summarizes text and does not ask for credentials, send data externally, or modify account settings. I would trust it if it stays within text generation and approved read-only access and does not request sensitive data.
