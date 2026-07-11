# Prompts Used — Task 4

## Initial Prompt

I have made a complete backup copy of a genuinely messy folder from my computer. I will work only on the backup.

Act as my file-organization consultant. My definition of clean is:

- Identify duplicate filenames.
- Identify files with identical contents even when filenames differ.
- Flag files larger than 500 MB.
- Group files by type.
- Identify screenshots.
- Identify installers.
- Identify files not modified for more than one year.
- Identify empty folders.

Safety requirement:

Do not delete, move, rename, overwrite, or modify anything.

Show me the full plan first, including every file you would move, delete, or rename, and wait for my approval before touching anything.

## Improved Prompt — Dry Run

Create a Python dry-run scanner for my backup folder.

Requirements:

- Scan all files recursively.
- Produce a complete file inventory.
- Detect duplicate filenames.
- Detect identical file contents using SHA-256.
- Flag files at or above 500 MB.
- Flag files not modified for at least 365 days.
- Identify screenshots using filename keywords.
- Identify installer files.
- Identify empty folders.
- Count files by extension and category.
- Generate CSV reports and a JSON summary.
- Generate a complete proposed-operations file.
- Do not move, copy, rename, overwrite, modify, or delete any file.
- Clearly print that no file operations were performed.

## Improved Prompt — Approved Execution

Create a separate execution script that reads the reviewed proposed-operations JSON file.

Safety requirements:

- Require the exact approval phrase: “I APPROVE THE COPY PLAN”.
- Perform copy operations only.
- Create a new `_Organized_Output` folder.
- Never delete, rename, move, or modify originals.
- Never overwrite an existing destination file.
- Add a numeric suffix where destination names conflict.
- Save a complete execution log.
- Report how many files were copied, skipped, or failed.
- Report zero original files deleted and zero original files modified.

## Prompt Iteration Explanation

The initial prompt described the business problem and safety expectations. The improved dry-run prompt converted the requirements into a verifiable report-only workflow. The final prompt added a formal approval gate and limited execution to copy-only operations.
