# Curated 3-Theme Minimalist Setup

Minimalist theme configuration for Antigravity IDE, VS Code, Cursor, and Windsurf. Each Color Theme QuickPick category holds exactly one option:

| Category | Theme Name | Archetype (`uiTheme`) | Source |
| :--- | :--- | :--- | :--- |
| **`light themes`** | **`Calmppuccin Latte`** | `vs` (Light) | `kenan-salar.calmppuccin-vscode` |
| **`dark themes`** | **`Calmppuccin Macchiato`** | `vs-dark` (Dark) | `kenan-salar.calmppuccin-vscode` |
| **`high contrast themes`** | **`Light High Contrast`** | `hc-light` (High Contrast) | Embedded default theme |

## Installation (macOS)

Run the script from the repository root:
```bash
# Configure Antigravity IDE
python3 scripts/setup-curated-themes.py --ide antigravity

# Or configure all installed editors
python3 scripts/setup-curated-themes.py --ide all
```

Reload the editor via `Cmd + Shift + R`.

## Restore Original Themes

To restore all built-in themes and original extension manifests:
```bash
python3 scripts/setup-curated-themes.py --ide antigravity --restore
```
