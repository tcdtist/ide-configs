# Editor-Specific Configurations (`ides/`)

This directory contains tailored configuration files (`settings.json`, `keybindings.json`) for each supported editor.

## Supported Editors & macOS Paths

| Editor | Directory | Settings Path on macOS | Extensions Directory |
| :--- | :--- | :--- | :--- |
| **Antigravity IDE** | [`antigravity/`](antigravity/) | `~/Library/Application Support/Antigravity IDE/User/` | `~/.antigravity-ide/extensions/` |
| **VS Code** | [`vscode/`](vscode/) | `~/Library/Application Support/Code/User/` | `~/.vscode/extensions/` |
| **Cursor** | [`cursor/`](cursor/) | `~/Library/Application Support/Cursor/User/` | `~/.cursor/extensions/` |
| **Windsurf** | [`windsurf/`](windsurf/) | `~/Library/Application Support/Windsurf/User/` | `~/.windsurf/extensions/` |

---

## Private Overrides Workflow (`settings.local.json`)

To configure machine-specific, sensitive, or personal settings (such as local database connection strings or personal `git-autoconfig` identities) without polluting public git tracking:

1. Copy the example template in the target editor directory:
   ```bash
   cp ides/antigravity/settings.local.example.json ides/antigravity/settings.local.json
   ```
2. Fill in your personal credentials.
3. `settings.local.json` is automatically ignored by `.gitignore`.

---

## Agent Guidance
When an agent is requested to modify editor settings:
- Identify the target editor from the prompt (e.g., Antigravity, Cursor, VS Code, Windsurf).
- Only mutate the corresponding `ides/<editor>/` subdirectory.
- Preserve common rules defined in `../common/`.
