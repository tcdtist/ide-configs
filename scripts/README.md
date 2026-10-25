# Automation Scripts (`scripts/`)

This directory contains standalone automation scripts for configuring and maintaining editors.

---

## 1. `setup-ide.py`

Automated, 1-minute configuration synchronizer and extension installer for Antigravity IDE, VS Code, Cursor, and Windsurf/Devin.

### Capabilities:
- Detects IDE binary/CLI and user application support paths automatically.
- Synchronizes `settings.json` (editor-specific) and lean `common/keybindings.json` with safety backups (`.bak`).
- Installs recommended extensions defined in `ides/<ide>/extensions.json`.
- Skips already installed extensions for instant execution.
- Supports `--dry-run`, `--skip-extensions`, `--skip-configs`, and `--force`.

### Usage:
```bash
# Setup Antigravity IDE (default)
python3 scripts/setup-ide.py --ide antigravity

# Setup all detected IDEs
python3 scripts/setup-ide.py --ide all

# Preview without applying changes
python3 scripts/setup-ide.py --ide all --dry-run

# Only sync preferences (skip extensions)
python3 scripts/setup-ide.py --ide all --skip-extensions
```

---

## 2. `setup-curated-themes.py`

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
