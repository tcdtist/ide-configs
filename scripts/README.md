# Automation Scripts (`scripts/`)

This directory contains standalone automation scripts for configuring and maintaining editors.

## 1. `setup-curated-themes.py`

Configures supported IDEs on macOS to use the curated 3-theme minimalist palette.

### Capabilities:
- Trims extra Calmppuccin variants from `package.json`.
- Empties unused built-in theme manifests with automatic `.bak` backups.
- Clears manifest caches in `CachedProfilesData` to force immediate editor reload.
- Provides `--restore` to revert all modifications from backups.

### Usage:
```bash
# Configure Antigravity IDE (default)
python3 scripts/setup-curated-themes.py --ide antigravity

# Configure all detected IDEs
python3 scripts/setup-curated-themes.py --ide all

# Target a specific editor
python3 scripts/setup-curated-themes.py --ide vscode
python3 scripts/setup-curated-themes.py --ide cursor
python3 scripts/setup-curated-themes.py --ide windsurf

# Restore original themes from backups
python3 scripts/setup-curated-themes.py --ide antigravity --restore
```

---

## Agent Guidance
When an agent is requested to modify script behavior or theme automation:
- Confine edits to `scripts/setup-curated-themes.py`.
- Do not modify configuration files in `ides/` or `common/` unless explicitly instructed.
