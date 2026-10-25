# Editor-Specific Configurations (`ides/`)

This directory contains tailored configuration files (`settings.json`, `extensions.json`) for each supported editor. Shared keybindings live centrally under [`common/keybindings.json`](../common/keybindings.json).

## Supported Editors & macOS Paths

| Editor | Directory | Settings Path on macOS | Extensions Manifest |
| :--- | :--- | :--- | :--- |
| **Antigravity IDE** | [`antigravity/`](antigravity/) | `~/Library/Application Support/Antigravity IDE/User/` | 19 extensions |
| **VS Code** | [`vscode/`](vscode/) | `~/Library/Application Support/Code/User/` | 18 extensions |
| **Cursor** | [`cursor/`](cursor/) | `~/Library/Application Support/Cursor/User/` | 18 extensions |
| **Windsurf** | [`windsurf/`](windsurf/) | `~/Library/Application Support/Windsurf/User/` | 15 extensions |

---

## Automated Deployment

To sync settings and install curated extensions automatically, use:

```bash
# Setup Antigravity IDE (default)
python3 scripts/setup-ide.py --ide antigravity

# Or setup all detected IDEs
python3 scripts/setup-ide.py --ide all
```

---

## Private Overrides (`settings.local.json`)

To configure machine-specific, sensitive, or personal settings without polluting public git tracking:
- Create `settings.local.json` in your local IDE User configuration folder.
- `*.local.json` is globally ignored by `.gitignore`.

---

## Agent Guidance
When an agent is requested to modify editor settings:
- Identify the target editor from the prompt (Antigravity, Cursor, VS Code, Windsurf).
- Only mutate the corresponding `ides/<editor>/` subdirectory.
- Preserve common rules defined in `../common/`.
