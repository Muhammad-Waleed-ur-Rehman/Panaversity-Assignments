from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


APPROVAL_PHRASE = "I APPROVE THE COPY PLAN"


def unique_destination(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Approval-gated organizer. Copies files into a new output folder and never deletes originals."
    )
    parser.add_argument(
        "operations_file",
        help="Path to proposed_operations.json created by organize_files_dry_run_4.py.",
    )
    parser.add_argument(
        "--approval",
        required=True,
        help=f'Exact approval phrase required: "{APPROVAL_PHRASE}"',
    )
    args = parser.parse_args()

    if args.approval != APPROVAL_PHRASE:
        raise SystemExit(
            "Approval phrase did not match. No files were copied.\n"
            f'Use exactly: --approval "{APPROVAL_PHRASE}"'
        )

    operations_path = Path(args.operations_file).expanduser().resolve()
    if not operations_path.exists():
        raise SystemExit(f"Operations file not found: {operations_path}")

    with operations_path.open("r", encoding="utf-8") as handle:
        operations = json.load(handle)

    log_rows = []
    copied = 0
    skipped = 0
    failed = 0

    for operation in operations:
        source = Path(operation["source"])
        destination = Path(operation["destination"])

        if operation.get("operation") != "COPY":
            skipped += 1
            log_rows.append({
                "source": str(source),
                "destination": str(destination),
                "status": "SKIPPED_UNSUPPORTED_OPERATION",
            })
            continue

        if not source.exists() or not source.is_file():
            failed += 1
            log_rows.append({
                "source": str(source),
                "destination": str(destination),
                "status": "FAILED_SOURCE_MISSING",
            })
            continue

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            final_destination = unique_destination(destination)
            shutil.copy2(source, final_destination)
            copied += 1
            log_rows.append({
                "source": str(source),
                "destination": str(final_destination),
                "status": "COPIED",
            })
        except Exception as exc:
            failed += 1
            log_rows.append({
                "source": str(source),
                "destination": str(destination),
                "status": f"FAILED: {exc}",
            })

    log_path = operations_path.parent / "execution_log.json"
    with log_path.open("w", encoding="utf-8") as handle:
        json.dump({
            "executed_at": datetime.now().isoformat(timespec="seconds"),
            "copied": copied,
            "skipped": skipped,
            "failed": failed,
            "originals_deleted": 0,
            "originals_modified": 0,
            "operations": log_rows,
        }, handle, indent=2)

    print("\nCOPY-ONLY ORGANIZATION COMPLETE")
    print("=" * 60)
    print(f"Files copied: {copied}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")
    print("Original files deleted: 0")
    print("Original files modified: 0")
    print(f"Execution log: {log_path}")


if __name__ == "__main__":
    main()
