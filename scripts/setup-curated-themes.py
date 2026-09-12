#!/usr/bin/env python3
"""
Curated 3-Theme Setup for Multiple IDEs (macOS)

Configures supported IDEs to use a minimalist 3-theme palette:
  - light themes: Calmppuccin Latte (vs)
  - dark themes: Calmppuccin Macchiato (vs-dark)
  - high contrast themes: Light High Contrast (hc-light)

Removes redundant built-in themes and variants, and clears extension caches.
Supports: Antigravity IDE, VS Code, Cursor, Windsurf.

Target OS: macOS
Usage:
  python3 setup-curated-themes.py --ide antigravity
  python3 setup-curated-themes.py --ide all
  python3 setup-curated-themes.py --ide antigravity --restore
"""

import argparse
import glob
import json
import os
import shutil
import sys
from typing import Dict, List, Optional

BUILTIN_THEME_FOLDERS = [
    "theme-defaults",
    "theme-abyss",
    "theme-kimbie-dark",
    "theme-monokai",
    "theme-monokai-dimmed",
    "theme-quietlight",
    "theme-red",
    "theme-solarized-dark",
    "theme-solarized-light",
    "theme-synthwave",
    "theme-tokyo-night",
    "theme-tomorrow-night-blue",
]

IDE_REGISTRY: Dict[str, Dict[str, str]] = {
    "antigravity": {
        "name": "Antigravity IDE",
        "app_dir": "/Applications/Antigravity IDE.app/Contents/Resources/app/extensions",
        "user_ext_dir": os.path.expanduser("~/.antigravity-ide/extensions"),
        "cache_dir": os.path.expanduser(
            "~/Library/Application Support/Antigravity IDE/CachedProfilesData/__default__profile__"
        ),
    },
    "vscode": {
        "name": "Visual Studio Code",
        "app_dir": "/Applications/Visual Studio Code.app/Contents/Resources/app/extensions",
        "user_ext_dir": os.path.expanduser("~/.vscode/extensions"),
        "cache_dir": os.path.expanduser(
            "~/Library/Application Support/Code/CachedProfilesData/__default__profile__"
        ),
    },
    "cursor": {
        "name": "Cursor",
        "app_dir": "/Applications/Cursor.app/Contents/Resources/app/extensions",
        "user_ext_dir": os.path.expanduser("~/.cursor/extensions"),
        "cache_dir": os.path.expanduser(
            "~/Library/Application Support/Cursor/CachedProfilesData/__default__profile__"
        ),
    },
    "windsurf": {
        "name": "Windsurf",
        "app_dir": "/Applications/Windsurf.app/Contents/Resources/app/extensions",
        "user_ext_dir": os.path.expanduser("~/.windsurf/extensions"),
        "cache_dir": os.path.expanduser(
            "~/Library/Application Support/Windsurf/CachedProfilesData/__default__profile__"
        ),
    },
}


def find_calmppuccin_dir(user_ext_dir: str) -> Optional[str]:
    if not os.path.isdir(user_ext_dir):
        return None
    matches = glob.glob(os.path.join(user_ext_dir, "kenan-salar.calmppuccin-vscode*"))
    return matches[0] if matches else None


def backup_file(path: str) -> str:
    bak_path = f"{path}.bak"
    if os.path.exists(path) and not os.path.exists(bak_path):
        shutil.copyfile(path, bak_path)
        print(f"    [Backup] {os.path.basename(path)} -> {os.path.basename(bak_path)}")
    return bak_path


def restore_file(path: str) -> bool:
    bak_path = f"{path}.bak"
    if os.path.exists(bak_path):
        shutil.copyfile(bak_path, path)
        print(f"    [Restored] {os.path.basename(path)}")
        return True
    return False


def clear_caches(cache_dir: str):
    if not os.path.isdir(cache_dir):
        return
    for fname in ["extensions.builtin.cache", "extensions.user.cache"]:
        target = os.path.join(cache_dir, fname)
        if os.path.exists(target):
            os.remove(target)
            print(f"    [Cache Cleared] {fname}")


def setup_ide(target_key: str, config: Dict[str, str]):
    ide_name = config["name"]
    app_dir = config["app_dir"]
    user_ext_dir = config["user_ext_dir"]
    cache_dir = config["cache_dir"]

    print(f"\n--- Setting up {ide_name} ({target_key}) ---")

    if not os.path.isdir(app_dir):
        print(f"  [Skip] Application bundle not found at: {app_dir}")
        return

    calm_dir = find_calmppuccin_dir(user_ext_dir)
    if not calm_dir:
        print(f"  [Warning] Calmppuccin extension not found in {user_ext_dir}.")
        print("  Please install extension 'kenan-salar.calmppuccin-vscode' first.")
        return

    print(f"  Found Calmppuccin extension: {os.path.basename(calm_dir)}")

    # Ensure Light High Contrast theme definition exists
    hc_source = os.path.join(app_dir, "theme-defaults", "themes", "hc_light.json")
    hc_dest = os.path.join(calm_dir, "themes", "light-high-contrast-color-theme.json")

    if not os.path.exists(hc_dest) and os.path.exists(hc_source):
        shutil.copyfile(hc_source, hc_dest)
        print("    [Copied] hc_light.json -> light-high-contrast-color-theme.json")

    # Update Calmppuccin package.json to only expose 3 curated themes
    calm_pkg = os.path.join(calm_dir, "package.json")
    backup_file(calm_pkg)

    with open(calm_pkg, "r", encoding="utf-8") as f:
        calm_data = json.load(f)

    calm_data.setdefault("contributes", {})["themes"] = [
        {
            "id": "calmppuccin-latte",
            "label": "Calmppuccin Latte",
            "uiTheme": "vs",
            "path": "./themes/calmppuccin-latte-color-theme.json",
        },
        {
            "id": "calmppuccin-macchiato",
            "label": "Calmppuccin Macchiato",
            "uiTheme": "vs-dark",
            "path": "./themes/calmppuccin-macchiato-color-theme.json",
        },
        {
            "id": "Default High Contrast Light",
            "label": "Light High Contrast",
            "uiTheme": "hc-light",
            "path": "./themes/light-high-contrast-color-theme.json",
        },
    ]

    with open(calm_pkg, "w", encoding="utf-8") as f:
        json.dump(calm_data, f, indent=2)
    print("    [Updated] Calmppuccin package.json (3 curated themes)")

    # Empty unused built-in theme manifests
    for folder in BUILTIN_THEME_FOLDERS:
        pkg_path = os.path.join(app_dir, folder, "package.json")
        if os.path.exists(pkg_path):
            backup_file(pkg_path)
            with open(pkg_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "contributes" in data and "themes" in data["contributes"]:
                data["contributes"]["themes"] = []
                with open(pkg_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                print(f"    [Emptied] {folder}")

    # Clear manifest caches
    clear_caches(cache_dir)
    print(f"  [Done] {ide_name} configured successfully.")


def restore_ide(target_key: str, config: Dict[str, str]):
    ide_name = config["name"]
    app_dir = config["app_dir"]
    user_ext_dir = config["user_ext_dir"]
    cache_dir = config["cache_dir"]

    print(f"\n--- Restoring {ide_name} ({target_key}) ---")

    calm_dir = find_calmppuccin_dir(user_ext_dir)
    if calm_dir:
        calm_pkg = os.path.join(calm_dir, "package.json")
        restore_file(calm_pkg)

    if os.path.isdir(app_dir):
        for folder in BUILTIN_THEME_FOLDERS:
            pkg_path = os.path.join(app_dir, folder, "package.json")
            restore_file(pkg_path)

    clear_caches(cache_dir)
    print(f"  [Done] {ide_name} restored to original themes.")


def main():
    parser = argparse.ArgumentParser(
        description="Configure curated 3-theme setup for Antigravity IDE, VS Code, Cursor, Windsurf on macOS."
    )
    parser.add_argument(
        "--ide",
        choices=["antigravity", "vscode", "cursor", "windsurf", "all"],
        default="antigravity",
        help="Target IDE to configure (default: antigravity)",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore original themes from backups",
    )

    args = parser.parse_args()

    targets: List[str] = (
        list(IDE_REGISTRY.keys()) if args.ide == "all" else [args.ide]
    )

    action = restore_ide if args.restore else setup_ide
    for key in targets:
        action(key, IDE_REGISTRY[key])

    print("\nAll operations completed. Please reload your editor (Cmd + Shift + R).")


if __name__ == "__main__":
    main()
