# IDE Configs

Centralized, modular development environment toolkit across Antigravity IDE, VS Code, Cursor, and Windsurf on macOS.

[![Platform: macOS](https://img.shields.io/badge/platform-macOS-black?style=flat-square&logo=apple)](https://apple.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Editors](https://img.shields.io/badge/editors-Antigravity%20%7C%20VS%20Code%20%7C%20Cursor%20%7C%20Windsurf-orange?style=flat-square)](#directory-map)

---

## Overview

**IDE Configs** provides a clean, unified, and reproducible configuration foundation for modern code editors on macOS. It eliminates repetitive machine setup while enforcing consistent ergonomics, standardized code formatting, and a distraction-free aesthetic.

### Highlights
- **Curated 3-Theme Minimalist Palette:** Strips default theme clutter down to exactly one theme per slot: Light (`Calmppuccin Latte`), Dark (`Calmppuccin Macchiato`), and High Contrast (`Light High Contrast`).
- **Unified Ergonomics:** Standardizes right-side primary sidebar, top activity bar, Cascadia Code with ligatures, and conflict-free save-action pipelines across all editors.
- **Modular Architecture:** Shared conventions live under `common/`, while editor-specific customizations remain isolated in `ides/<editor>/`.
- **Safe Separation of Concerns:** Public repository clean of credentials, personal emails, or private paths. Machine-specific overrides use `settings.local.json` (gitignored).

> **Platform Note:** Designed and tested for macOS (Apple Silicon, macOS Sonoma / Sequoia). File paths follow macOS standards (`/Applications/*.app`, `~/Library/Application Support/...`).

---

## Directory Map

Use this directory map to navigate directly to the relevant module. Keep modifications strictly confined to the targeted module.

| Domain / Concern | Target Path | Description |
| :--- | :--- | :--- |
| **New Machine Setup** | [`docs/new-machine-setup.md`](docs/new-machine-setup.md) | 1-minute workstation bootstrap guide |
| **Theme & Palette** | [`common/themes/`](common/themes/) | 3-theme minimalist palette, picker trimming, and theme docs |
| **Keybindings (Lean)** | [`common/keybindings.json`](common/keybindings.json) | Shared window reload shortcut (`Cmd+Shift+R`) |
| **Common Extensions** | [`common/extensions.json`](common/extensions.json) | 13 shared core extensions recommendation |
| **Code Formatting & Linting** | [`common/formatting.json`](common/formatting.json) | Shared Prettier configs, ESLint fix-on-save, fonts, and tab sizes |
| **Git & GitLens Zen Mode** | [`common/git.json`](common/git.json) | Shared Git ergonomics & zero-bloat inline line blame |
| **Search Exclusions** | [`common/search-exclude.json`](common/search-exclude.json) | Build artifact (`dist`, `.next`, `node_modules`) search ignores |
| **Tab Labels (Next.js)** | [`common/nextjs-custom-labels.json`](common/nextjs-custom-labels.json) | Next.js App Router tab naming patterns (`${dirname} - ${filename}`) |
| **Antigravity IDE** | [`ides/antigravity/`](ides/antigravity/) | Antigravity settings & 19 curated extensions |
| **VS Code** | [`ides/vscode/`](ides/vscode/) | VS Code settings & 18 curated extensions |
| **Cursor** | [`ides/cursor/`](ides/cursor/) | Cursor settings & 18 curated extensions |
| **Windsurf** | [`ides/windsurf/`](ides/windsurf/) | Windsurf settings & 15 curated extensions |
| **Automation Scripts** | [`scripts/`](scripts/) | CLI utilities for automated IDE setup (`setup-ide.py`) and themes (`setup-curated-themes.py`) |

---

## Scope Isolation Rules

When modifying or extending this repository:
1. **Targeted Edits:** Always navigate directly to the corresponding module in the table above. For example, when updating theme rules, only edit `common/themes/` or `scripts/setup-curated-themes.py`. Do not modify unrelated editor settings.
2. **Credential Safety:** Never commit API keys, personal emails, or private connection strings. Store local overrides in `settings.local.json` (gitignored).

---

## Quick Start (macOS)

### 1. Clone the Repository
```bash
git clone https://github.com/tcdtist/ide-configs.git
cd ide-configs
```

### 2. Automated 1-Minute IDE Setup
Run `scripts/setup-ide.py` to sync preferences, install curated extensions, and apply lean keybindings:

```bash
# Configure Antigravity IDE (default)
python3 scripts/setup-ide.py --ide antigravity

# Or configure all detected IDEs
python3 scripts/setup-ide.py --ide all

# Preview without making changes
python3 scripts/setup-ide.py --ide all --dry-run
```

> See [New Machine Setup Guide](docs/new-machine-setup.md) for full options and flags.

### 3. (Optional) Apply Curated 3-Theme Minimalist Palette
```bash
python3 scripts/setup-curated-themes.py --ide antigravity
```

### 4. Reload Your Editor
Press `Cmd + Shift + R` (or `Cmd + Shift + P` -> `Developer: Reload Window`).

### To Restore Default Themes:
```bash
python3 scripts/setup-curated-themes.py --ide antigravity --restore
```

---

## License

This project is licensed under the [MIT License](LICENSE).
