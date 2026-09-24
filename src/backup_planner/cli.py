from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

@dataclass
class BackupItem:
    relative_path: str
    source: str
    destination: str
    action: str
    size: int


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def build_plan(source: Path, destination: Path, compare_hash: bool = False) -> list[BackupItem]:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    if not source.is_dir():
        raise ValueError(f"Source is not a directory: {source}")
    if source == destination or is_within(destination, source):
        raise ValueError("Destination must be outside the source directory.")
    items: list[BackupItem] = []
    for path in sorted(source.rglob("*"), key=lambda p: str(p).lower()):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(source)
        target = destination / relative
        action = "create"
        if target.exists():
            source_stat, target_stat = path.stat(), target.stat()
            same = source_stat.st_size == target_stat.st_size
            if same and compare_hash:
                same = sha256(path) == sha256(target)
            elif same:
                same = source_stat.st_mtime_ns <= target_stat.st_mtime_ns
            if same:
                continue
            action = "update"
        items.append(BackupItem(str(relative), str(path), str(target), action, path.stat().st_size))
    return items


def apply_plan(items: list[BackupItem], manifest: Path, verify: bool = False) -> dict:
    copied = 0
    total_bytes = 0
    records = []
    for item in items:
        source, target = Path(item.source), Path(item.destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        record = asdict(item)
        if verify:
            source_hash, target_hash = sha256(source), sha256(target)
            if source_hash != target_hash:
                raise IOError(f"Verification failed: {item.relative_path}")
            record["sha256"] = source_hash
        records.append(record)
        copied += 1
        total_bytes += item.size
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "copied_files": copied,
        "copied_bytes": total_bytes,
        "verified": verify,
        "items": records,
    }
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview and apply incremental file backups.")
    parser.add_argument("source")
    parser.add_argument("destination")
    parser.add_argument("--hash", action="store_true", help="Compare existing files with SHA-256")
    parser.add_argument("--apply", action="store_true", help="Copy the displayed files")
    parser.add_argument("--verify", action="store_true", help="Verify copied files with SHA-256")
    parser.add_argument("--manifest", help="Manifest path; defaults inside destination")
    args = parser.parse_args()
    source, destination = Path(args.source), Path(args.destination)
    items = build_plan(source, destination, args.hash)
    total = sum(item.size for item in items)
    for item in items:
        print(f"{item.action.upper():6} {human_size(item.size):>10}  {item.relative_path}")
    print(f"\nPlanned: {len(items)} files, {human_size(total)}")
    if not args.apply:
        print("Preview only. Add --apply to copy files. No destination files were deleted.")
        return
    manifest = Path(args.manifest) if args.manifest else destination / "backup-manifest.json"
    report = apply_plan(items, manifest, args.verify)
    print(f"Copied {report['copied_files']} files. Manifest: {manifest}")
    print("Source files and extra destination files were not deleted.")

if __name__ == "__main__":
    main()
