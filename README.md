# Backup Planner

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Preview and apply safe incremental file backups with JSON manifests and optional SHA-256 verification.

## Safety-first behavior

- Preview-only by default.
- Never deletes source files.
- Never deletes extra files already present in the destination.
- Rejects a destination placed inside the source directory.
- Can verify every copied file with SHA-256.

This tool is a file-copy helper, not a replacement for a tested disaster-recovery strategy.

## Install

```bash
git clone https://github.com/jellywong343-sys/backup-planner.git
cd backup-planner
python -m pip install -e .
```

## Usage

```bash
backup-plan ./documents D:/Backups/documents
backup-plan ./documents D:/Backups/documents --apply
backup-plan ./documents D:/Backups/documents --hash --apply --verify
backup-plan ./documents D:/Backups/documents --apply --manifest report.json
```

Use `--hash` for content-based comparison of existing files. It is slower but more thorough.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT


