# Task 4 — Organize the Mess (The Files You Forgot)

**Student:** Muhammad Waleed-ur-Rehman  
**AI Tool Used:** ChatGPT  
**Project Type:** Safe file analysis and copy-only organization

## 1. Problem Statement

My selected folder had accumulated documents, screenshots, installers, downloads, duplicate files, and files with unclear names. It had become difficult to understand what the folder contained and which files were safe to keep, archive, or review.

The goal was to use AI as a client—not as a coder—to design a safe process that would identify duplicate files, large files, old files, screenshots, installers, file types, and empty folders without damaging the original data.

## 2. Safety Approach

The project follows this order:

1. Make a complete backup copy of the selected folder.
2. Run the scanner only on the backup copy.
3. Generate a dry-run report.
4. Review every proposed copy operation.
5. Approve the operation using an exact approval phrase.
6. Copy files into a new `_Organized_Output` folder.
7. Keep all original files unchanged.
8. Verify the output through file counts and manual spot checks.

The scripts do not delete original files.

## 3. Files in This Project

- `organize_files_dry_run_4.py` — scans the backup folder and generates reports.
- `execute_copy_plan_4.py` — copies files into categorized folders only after approval.
- `prompts_4.md` — initial and improved prompts.
- `results_4/` — generated CSV and JSON reports.
- `screenshots_4/` — screenshots showing backup, dry run, reports, and final output.

## 4. How to Run

### Step A — Create a Backup

Example:

```text
Original folder: C:\Users\YourName\Downloads_4
Backup folder:   C:\Users\YourName\Downloads_Backup
```

Work only on `Downloads_Backup`.

### Step B — Run the Dry Scan

From the Task 4 project folder:

```bash
python organize_files_dry_run_4.py "C:\Users\YourName\Downloads_Backup" --reports-dir results_4
```

Optional settings:

```bash
python organize_files_dry_run_4.py "C:\Users\YourName\Downloads_Backup" --large-mb 500 --old-days 365 --reports-dir results_4
```

### Step C — Review the Reports

Review:

- `results_4/summary.json`
- `results_4/file_inventory.csv`
- `results_4/duplicate_names.csv`
- `results_4/duplicate_contents.csv`
- `results_4/large_files.csv`
- `results_4/old_files.csv`
- `results_4/installers.csv`
- `results_4/screenshots.csv`
- `results_4/empty_folders.csv`
- `results_4/proposed_operations.json`
- `results_4/execution_log.json`
- `results_4/file_type_summary.csv`
- `results_4/category_summary.csv`

The dry-run script does not move, rename, overwrite, or delete files.

### Step D — Approve and Execute

Only after reviewing the full plan:

```bash
python execute_copy_plan_4.py results_4/proposed_operations.json --approval "I APPROVE THE COPY PLAN"
```

The script copies files into:

```text
Downloads_Backup\_Organized_Output\
├── Documents
├── Images
├── Screenshots
├── Videos
├── Audio
├── Archives
├── Installers
└── Other
```

When two files have the same destination name, the script creates a unique name such as `_1`, `_2`, and so on. It does not overwrite files.

## 5. Verification

I verified the project by:

- Comparing the number of scanned files with the backup folder.
- Reviewing duplicate hashes in `duplicate_contents.csv`.
- Opening sample files in each output category.
- Confirming the original backup folder remained intact.
- Checking `execution_log.json`.
- Confirming that the scripts reported zero deleted and zero modified original files.

## 6. Evidence to Add

Add screenshots showing:

1. Original folder and backup copy.
2. Dry-run terminal output.
3. `summary.json`.
4. `duplicate_contents.csv`.
5. `proposed_operations.json`.
6. Organized output folders.
7. Spot-check of selected files.
8. `execution_log.json`.

## 7. Final Result

- Total files scanned: `35`
- Total folder size: `0.0 GB`
- Duplicate-name entries: `0`
- Duplicate-content entries: `12`
- Potential duplicate space: `0.0 GB`
- Large files: `0`
- Old files: `0`
- Screenshots: `5`
- Installers: `3`
- Empty folders: `4`
- Original files modified: `0`
- Original files deleted: `0`

## 8. What Worked

The dry-run approach produced a clear inventory before any file operation occurred. SHA-256 hashing helped identify files with identical contents even when their names were different. The category-based output made the folder easier to review.

## 9. Problems Faced

Potential issues included permission-restricted files, very large files taking longer to hash, files with the same name but different contents, and unclear filenames that could not be classified confidently.

These risks were controlled through backup-first processing, dry-run reports, manual approval, copy-only organization, unique output names, and an execution log.

## 10. What I Learned

AI-assisted file organization is useful only when strong safety controls are applied. A backup, dry run, complete operation plan, approval gate, non-destructive copying, and verification are essential whenever code is allowed to interact with real files.
