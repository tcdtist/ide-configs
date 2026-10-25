# New Machine Setup Guide (1-Minute Bootstrap)

Rapid, automated setup guide for developers and AI Coding Agents setting up a new macOS workstation with unified ergonomics across Antigravity IDE, VS Code, Cursor, and Windsurf/Devin.

---

## 1. Prerequisites

- **macOS** (Apple Silicon or Intel, macOS 14+ recommended)
- **Python 3** (`python3 --version`)
- Target IDE(s) installed under `/Applications`:
  - [Antigravity IDE](https://antigravity.google)
  - [Visual Studio Code](https://code.visualstudio.com)
  - [Cursor](https://cursor.com)
  - [Windsurf / Devin](https://codeium.com/windsurf)

---

## 2. One-Minute Fast Track

### Step 1: Clone Repository
```bash
git clone git@github.com-tcdtist:tcdtist/ide-configs.git ~/dev/me/ide-configs
cd ~/dev/me/ide-configs
```

### Step 2: Run Unified Setup Script
Run [`scripts/setup-ide.py`](../scripts/setup-ide.py) to configure editor preferences and install curated extensions in one command:

```bash
# Setup Antigravity IDE (default)
python3 scripts/setup-ide.py --ide antigravity

# Or setup all detected IDEs simultaneously
python3 scripts/setup-ide.py --ide all

# Preview actions without making changes
python3 scripts/setup-ide.py --ide all --dry-run
```

#### Selective Setup Options:
```bash
# Only sync settings.json and keybindings.json (skip extension installation)
python3 scripts/setup-ide.py --ide all --skip-extensions

# Only install extensions (skip preferences)
python3 scripts/setup-ide.py --ide all --skip-configs

# Force reinstall and overwrite configurations
python3 scripts/setup-ide.py --ide all --force
```

### Step 3: (Optional) Apply Curated 3-Theme Minimalist Palette
For Antigravity IDE or editors using the 3-slot theme system:
```bash
python3 scripts/setup-curated-themes.py --ide antigravity
```

### Step 4: Reload Your Editor
Press `Cmd + Shift + R` (or `Cmd + Shift + P` -> `Developer: Reload Window`).

---

## 3. What Gets Configured

### Unified Ergonomics:
- **Primary Sidebar:** Right side (`"workbench.sideBar.location": "right"`) to avoid UI jitter when opening file trees or agent chats.
- **Activity Bar:** Top activity bar (`"workbench.activityBar.location": "top"`) across all editors for maximum vertical code view.
- **Font & Formatting:** Cascadia Code (13px, font ligatures enabled), Prettier on save, ESLint autofix.
- **Git Blame (Zen Mode):** Subtle, non-intrusive inline blame at the end of active lines via GitLens.
- **Keybindings:** Lean, agent-friendly shortcuts (`Cmd + Shift + R` for window reload; manual git commit hotkeys removed as AI Agents manage commits).

### Extension Curations:
| IDE Target | Curated Count | Extensions Manifest |
| :--- | :---: | :--- |
| **Common (All IDEs)** | 13 | [`common/extensions.json`](../common/extensions.json) |
| **Antigravity IDE** | 19 | [`ides/antigravity/extensions.json`](../ides/antigravity/extensions.json) |
| **VS Code** | 18 | [`ides/vscode/extensions.json`](../ides/vscode/extensions.json) |
| **Cursor** | 18 | [`ides/cursor/extensions.json`](../ides/cursor/extensions.json) |
| **Windsurf / Devin** | 15 | [`ides/windsurf/extensions.json`](../ides/windsurf/extensions.json) |

---

## 4. Verification & Health Check

Verify that configurations and extensions are active:
```bash
# Check installed extensions
code --list-extensions
cursor --list-extensions
antigravity-ide --list-extensions
windsurf --list-extensions
```
