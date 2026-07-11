from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

INSTALLER_EXTENSIONS = {".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"}
ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz"}
DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".wmv", ".webm"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg"}

SCREENSHOT_KEYWORDS = ("screenshot", "screen shot", "snipping", "snip")


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def write_csv(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    name = path.name.lower()

    if any(keyword in name for keyword in SCREENSHOT_KEYWORDS) and suffix in IMAGE_EXTENSIONS:
        return "Screenshots"
    if suffix in DOCUMENT_EXTENSIONS:
        return "Documents"
    if suffix in IMAGE_EXTENSIONS:
        return "Images"
    if suffix in VIDEO_EXTENSIONS:
        return "Videos"
    if suffix in AUDIO_EXTENSIONS:
        return "Audio"
    if suffix in ARCHIVE_EXTENSIONS:
        return "Archives"
    if suffix in INSTALLER_EXTENSIONS:
        return "Installers"
    return "Other"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Safe dry-run folder scanner. It never moves, deletes, renames, or overwrites files."
    )
    parser.add_argument("folder", help="Path to the BACKUP COPY of the folder to scan.")
    parser.add_argument(
        "--large-mb",
        type=int,
        default=500,
        help="Flag files at or above this size in MB. Default: 500.",
    )
    parser.add_argument(
        "--old-days",
        type=int,
        default=365,
        help="Flag files not modified within this many days. Default: 365.",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory where CSV and JSON reports will be saved.",
    )
    args = parser.parse_args()

    root = Path(args.folder).expanduser().resolve()
    reports_dir = Path(args.reports_dir).expanduser().resolve()
    reports_dir.mkdir(parents=True, exist_ok=True)

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Folder does not exist or is not a directory: {root}")

    files = list(iter_files(root))
    now = datetime.now().timestamp()
    large_bytes = args.large_mb * 1024 * 1024
    old_seconds = args.old_days * 24 * 60 * 60

    name_groups: dict[str, list[Path]] = defaultdict(list)
    size_groups: dict[int, list[Path]] = defaultdict(list)
    extension_counts = Counter()
    category_counts = Counter()

    inventory_rows = []
    large_rows = []
    old_rows = []
    installer_rows = []
    screenshot_rows = []

    total_size = 0

    for path in files:
        stat = path.stat()
        size = stat.st_size
        total_size += size
        suffix = path.suffix.lower() or "[no extension]"
        category = classify_file(path)

        name_groups[path.name.lower()].append(path)
        size_groups[size].append(path)
        extension_counts[suffix] += 1
        category_counts[category] += 1

        modified = datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds")
        relative = str(path.relative_to(root))

        inventory_rows.append([
            relative,
            path.name,
            suffix,
            category,
            size,
            round(size / (1024 * 1024), 2),
            modified,
        ])

        if size >= large_bytes:
            large_rows.append([relative, size, round(size / (1024 * 1024), 2), modified])

        if now - stat.st_mtime >= old_seconds:
            old_rows.append([relative, round((now - stat.st_mtime) / 86400), modified])

        if path.suffix.lower() in INSTALLER_EXTENSIONS:
            installer_rows.append([relative, round(size / (1024 * 1024), 2), modified])

        if category == "Screenshots":
            screenshot_rows.append([relative, round(size / (1024 * 1024), 2), modified])

    duplicate_name_rows = []
    for _, grouped in sorted(name_groups.items()):
        if len(grouped) > 1:
            for path in grouped:
                duplicate_name_rows.append([
                    path.name,
                    str(path.relative_to(root)),
                    path.stat().st_size,
                ])

    duplicate_content_rows = []
    duplicate_content_bytes = 0
    for size, grouped in size_groups.items():
        if len(grouped) < 2:
            continue

        hash_groups: dict[str, list[Path]] = defaultdict(list)
        for path in grouped:
            try:
                hash_groups[sha256_file(path)].append(path)
            except (OSError, PermissionError) as exc:
                duplicate_content_rows.append([
                    "ERROR",
                    str(path.relative_to(root)),
                    size,
                    str(exc),
                ])

        for digest, matches in hash_groups.items():
            if len(matches) > 1:
                duplicate_content_bytes += size * (len(matches) - 1)
                for path in matches:
                    duplicate_content_rows.append([
                        digest,
                        str(path.relative_to(root)),
                        size,
                        "",
                    ])

    empty_folder_rows = []
    for folder in root.rglob("*"):
        if folder.is_dir():
            try:
                if not any(folder.iterdir()):
                    empty_folder_rows.append([str(folder.relative_to(root))])
            except PermissionError:
                empty_folder_rows.append([str(folder.relative_to(root)) + " [permission denied]"])

    proposed_operations = []
    for path in files:
        category = classify_file(path)
        proposed_operations.append({
            "operation": "COPY",
            "source": str(path),
            "destination": str(root / "_Organized_Output" / category / path.name),
            "status": "PLANNED_ONLY",
        })

    write_csv(
        reports_dir / "file_inventory.csv",
        ["relative_path", "filename", "extension", "category", "size_bytes", "size_mb", "modified_at"],
        inventory_rows,
    )
    write_csv(
        reports_dir / "duplicate_names.csv",
        ["filename", "relative_path", "size_bytes"],
        duplicate_name_rows,
    )
    write_csv(
        reports_dir / "duplicate_contents.csv",
        ["sha256", "relative_path", "size_bytes", "notes"],
        duplicate_content_rows,
    )
    write_csv(
        reports_dir / "large_files.csv",
        ["relative_path", "size_bytes", "size_mb", "modified_at"],
        large_rows,
    )
    write_csv(
        reports_dir / "old_files.csv",
        ["relative_path", "age_days", "modified_at"],
        old_rows,
    )
    write_csv(
        reports_dir / "installers.csv",
        ["relative_path", "size_mb", "modified_at"],
        installer_rows,
    )
    write_csv(
        reports_dir / "screenshots.csv",
        ["relative_path", "size_mb", "modified_at"],
        screenshot_rows,
    )
    write_csv(
        reports_dir / "empty_folders.csv",
        ["relative_path"],
        empty_folder_rows,
    )
    write_csv(
        reports_dir / "file_type_summary.csv",
        ["extension", "count"],
        [[extension, count] for extension, count in extension_counts.most_common()],
    )
    write_csv(
        reports_dir / "category_summary.csv",
        ["category", "count"],
        [[category, count] for category, count in category_counts.most_common()],
    )

    with (reports_dir / "proposed_operations.json").open("w", encoding="utf-8") as handle:
        json.dump(proposed_operations, handle, indent=2)

    summary = {
        "scanned_folder": str(root),
        "scan_time": datetime.now().isoformat(timespec="seconds"),
        "total_files": len(files),
        "total_size_bytes": total_size,
        "total_size_gb": round(total_size / (1024 ** 3), 3),
        "duplicate_name_entries": len(duplicate_name_rows),
        "duplicate_content_entries": len([r for r in duplicate_content_rows if r[0] != "ERROR"]),
        "potential_duplicate_space_bytes": duplicate_content_bytes,
        "potential_duplicate_space_gb": round(duplicate_content_bytes / (1024 ** 3), 3),
        "large_files": len(large_rows),
        "old_files": len(old_rows),
        "installers": len(installer_rows),
        "screenshots": len(screenshot_rows),
        "empty_folders": len(empty_folder_rows),
        "files_modified": 0,
        "files_moved": 0,
        "files_deleted": 0,
        "dry_run_only": True,
    }

    with (reports_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print("\nDRY RUN COMPLETE")
    print("=" * 60)
    print(f"Folder scanned: {root}")
    print(f"Total files: {summary['total_files']}")
    print(f"Total size: {summary['total_size_gb']} GB")
    print(f"Duplicate-name entries: {summary['duplicate_name_entries']}")
    print(f"Duplicate-content entries: {summary['duplicate_content_entries']}")
    print(f"Potential duplicate space: {summary['potential_duplicate_space_gb']} GB")
    print(f"Large files: {summary['large_files']}")
    print(f"Old files: {summary['old_files']}")
    print(f"Installers: {summary['installers']}")
    print(f"Screenshots: {summary['screenshots']}")
    print(f"Empty folders: {summary['empty_folders']}")
    print("\nNo files were moved, renamed, overwritten, or deleted.")
    print(f"Review the reports in: {reports_dir}")
    print("Do not run the organizer until proposed_operations.json has been reviewed.")


if __name__ == "__main__":
    main()
