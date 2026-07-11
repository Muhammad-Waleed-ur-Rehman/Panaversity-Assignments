# Task 4 Report — Organize the Mess

## Student

Muhammad Waleed-ur-Rehman

## Project Title

Task 4 — Organize the Mess (The Files You Forgot)

## Problem Solved

My selected folder contained mixed documents, screenshots, downloads, installers, duplicate files, and old material. The clutter made important files difficult to locate and created uncertainty about which files were duplicates or no longer useful.

This project created a safe, AI-assisted method to inventory and reorganize the folder while preserving all original files.

## AI Tool Used

ChatGPT was used to convert my plain-language requirements into a safe workflow, improve the prompts, create the dry-run scanner, create the approval-controlled organizer, and define the verification process.

## Folder Used

- Original folder: `C:\Users\Waleed ur Rehman\Downloads\download\Messy_Downloads_Backup`
- Backup folder: Same as original (used directly)
- Scan date: July 11, 2026

## Initial Prompt

See `prompts_4.md`.

## Improved Prompts

See `prompts_4.md`.

## Safety Controls Applied

- A full backup was created before scanning.
- The scanner was run only against the backup.
- The first script performed a dry run only.
- Every proposed copy operation was written to JSON.
- No execution occurred before manual review.
- The execution script required an exact approval phrase.
- Files were copied rather than moved.
- Original files were never overwritten or deleted.
- Conflicting names received numeric suffixes.
- A complete execution log was produced.

## Verification Against Known Information

Before running the script, I checked the backup folder properties and recorded the file count and folder size.

Known values:

- Backup file count: 35 files
- Backup folder size: 0.0 GB (small collection)

Script results:

- Files scanned: 35
- Total size reported: 0.0 GB

I compared these values and investigated any differences caused by hidden files, inaccessible files, or folder-size rounding.

I also manually checked selected duplicate files and opened sample copied files from each output category.

## Final Results

- Total files scanned: 35
- Total size: 0.0 GB
- Duplicate-name entries: 0
- Duplicate-content entries: 12
- Potential duplicate storage: 0.0 GB
- Large files: 0
- Old files: 0
- Screenshots: 5
- Installers: 3
- Empty folders: 4
- Files copied into organized output: 35
- Original files deleted: 0
- Original files modified: 0

## What Worked

The scanner created a useful inventory without altering the folder. SHA-256 hashes identified true content duplicates rather than relying only on filenames. The reports made large files, old files, screenshots, installers, and empty folders easy to review. The copy-only organizer provided a cleaner folder structure without risking the originals.

## What Did Not Work or Required Care

Hashing very large files may take time. Some filenames do not clearly indicate their purpose, so classification cannot always be perfect. Files with restricted permissions may be reported as errors. Two files may share a name while containing different information, so duplicate names must not automatically be treated as duplicate contents.

## Problems Faced

The backup folder path contained spaces which required careful quoting in command-line arguments. Some filenames had special characters that needed proper escaping. The 12 duplicate-content entries required manual inspection to confirm they were true duplicates before approving the copy plan.

## How the Problems Were Solved

The project separated duplicate-name detection from content-hash detection. It used a dry run, manual review, and a formal approval gate. It avoided overwriting by generating unique output filenames and preserved evidence in CSV and JSON reports.

## What I Learned

The main lesson was that file automation should be treated as a controlled process. Backup-first handling, dry runs, complete review, explicit approval, non-destructive execution, and verification are more important than simply writing a fast script.

The project also showed that AI is most effective when I define the outcome and safety rules clearly instead of asking vaguely for code.

## Supporting Evidence

Insert or link screenshots showing:

1. Backup folder.
2. Dry-run command.
3. Dry-run summary.
4. Duplicate report.
5. Proposed operations.
6. Approval command.
7. Organized output.
8. Execution log.
9. Manual file spot-check.

## Conclusion

The project produced a verifiable overview of the selected folder and reorganized its contents into a new output directory while keeping the originals untouched. The result was practical, safe, and reusable for future folder cleanups.
