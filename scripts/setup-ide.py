#!/usr/bin/env python3
"""
Automated IDE Setup & Extension Installer (macOS / Linux)

Configures supported IDEs (Antigravity IDE, VS Code, Cursor, Windsurf/Devin) by:
1. Detecting IDE application bundle and command-line interface (CLI).
2. Copying standardized settings.json (editor-specific) and common/keybindings.json.
3. Installing curated extensions defined in ides/<ide>/extensions.json via CLI.

Usage:
  python3 scripts/setup-ide.py --ide antigravity
  python3 scripts/setup-ide.py --ide all
  python3 scripts/setup-ide.py --ide vscode --dry-run
  python3 scripts/setup-ide.py --ide cursor --skip-extensions
  python3 scripts/setup-ide.py --ide windsurf --skip-configs
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from typing import Dict, List, Optional, Set, Tuple

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IDE_REGISTRY: Dict[str, Dict] = {
    "antigravity": {
        "name": "Antigravity IDE",
        "cli_candidates": [
            "antigravity-ide",
            "/Applications/Antigravity IDE.app/Contents/Resources/app/bin/antigravity-ide",
            "/Applications/Antigravity.app/Contents/Resources/app/bin/antigravity",
        ],
        "user_dir_candidates": [
            os.path.expanduser("~/Library/Application Support/Antigravity IDE/User"),
            os.path.expanduser("~/.config/Antigravity IDE/User"),
        ],
        "settings_relpath": "ides/antigravity/settings.json",
        "extensions_relpath": "ides/antigravity/extensions.json",
    },
    "vscode": {
        "name": "Visual Studio Code",
        "cli_candidates": [
            "code",
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",
        ],
        "user_dir_candidates": [
            os.path.expanduser("~/Library/Application Support/Code/User"),
            os.path.expanduser("~/.config/Code/User"),
        ],
        "settings_relpath": "ides/vscode/settings.json",
        "extensions_relpath": "ides/vscode/extensions.json",
    },
    "cursor": {
        "name": "Cursor",
        "cli_candidates": [
            "cursor",
            "/Applications/Cursor.app/Contents/Resources/app/bin/cursor",
        ],
        "user_dir_candidates": [
            os.path.expanduser("~/Library/Application Support/Cursor/User"),
            os.path.expanduser("~/.config/Cursor/User"),
        ],
        "settings_relpath": "ides/cursor/settings.json",
        "extensions_relpath": "ides/cursor/extensions.json",
    },
    "windsurf": {
        "name": "Windsurf / Devin",
        "cli_candidates": [
            "windsurf",
            os.path.expanduser("~/.codeium/windsurf/bin/windsurf"),
            "/Applications/Devin.app/Contents/Resources/app/bin/devin-desktop",
            "/Applications/Windsurf.app/Contents/Resources/app/bin/windsurf",
            "devin",
        ],
        "user_dir_candidates": [
            os.path.expanduser("~/Library/Application Support/Devin/User"),
            os.path.expanduser("~/Library/Application Support/Windsurf/User"),
            os.path.expanduser("~/.config/Windsurf/User"),
        ],
        "settings_relpath": "ides/windsurf/settings.json",
        "extensions_relpath": "ides/windsurf/extensions.json",
    },
}

COMMON_KEYBINDINGS_RELPATH = "common/keybindings.json"


def resolve_cli(candidates: List[str]) -> Optional[str]:
    """Find the first working executable path from candidates."""
    for cand in candidates:
        # Check direct command in PATH
        which_path = shutil.which(cand)
        if which_path and os.path.isfile(which_path) and os.access(which_path, os.X_OK):
            return which_path
        # Check absolute path
        expanded = os.path.expanduser(cand)
        if os.path.isfile(expanded) and os.access(expanded, os.X_OK):
            return expanded
    return None


def resolve_user_dir(candidates: List[str]) -> str:
    """Find existing user config directory or return preferred default."""
    for cand in candidates:
        if os.path.isdir(cand):
            return cand
    # Fallback to first candidate
    return candidates[0]


def backup_if_different(source_path: str, target_path: str) -> None:
    """Backup target_path to target_path.bak if target exists and differs from source."""
    if not os.path.exists(target_path):
        return
    try:
        with open(source_path, "r", encoding="utf-8") as sf, open(
            target_path, "r", encoding="utf-8"
        ) as tf:
            if sf.read() == tf.read():
                return
    except Exception:
        pass

    bak_path = f"{target_path}.bak"
    shutil.copyfile(target_path, bak_path)
    print(f"    [Backup] Saved existing config to {os.path.basename(bak_path)}")


def sync_file(source_path: str, target_path: str, dry_run: bool = False) -> bool:
    """Safely copy configuration file with backup and difference check."""
    if not os.path.isfile(source_path):
        print(f"    [Error] Source file not found: {source_path}")
        return False

    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    if dry_run:
        print(f"    [Dry-Run] Would copy {os.path.relpath(source_path, REPO_ROOT)} -> {target_path}")
        return True

    backup_if_different(source_path, target_path)
    shutil.copyfile(source_path, target_path)
    print(f"    [Synced] {os.path.basename(target_path)}")
    return True


def get_installed_extensions(cli_path: str) -> Set[str]:
    """Query currently installed extensions via IDE CLI."""
    try:
        proc = subprocess.run(
            [cli_path, "--list-extensions"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            check=False,
        )
        installed = set()
        for line in proc.stdout.splitlines():
            line = line.strip()
            if line and not line.startswith("[") and not line.startswith("("):
                installed.add(line.lower())
        return installed
    except Exception as e:
        print(f"    [Warning] Could not query installed extensions via {cli_path}: {e}")
        return set()


def setup_ide(ide_key: str, config: Dict, args: argparse.Namespace) -> Tuple[bool, str]:
    """Execute setup steps for a single IDE target."""
    name = config["name"]
    print(f"\n==================================================")
    print(f"  Target: {name} ({ide_key})")
    print(f"==================================================")

    # 1. Resolve User config directory
    user_dir = resolve_user_dir(config["user_dir_candidates"])
    print(f"  Config Directory: {user_dir}")

    # 2. Sync Configuration Files (settings.json & keybindings.json)
    if not args.skip_configs:
        print(f"\n  [1/2] Syncing Editor Preferences...")
        settings_src = os.path.join(REPO_ROOT, config["settings_relpath"])
        settings_dst = os.path.join(user_dir, "settings.json")
        sync_file(settings_src, settings_dst, dry_run=args.dry_run)

        keybindings_src = os.path.join(REPO_ROOT, COMMON_KEYBINDINGS_RELPATH)
        keybindings_dst = os.path.join(user_dir, "keybindings.json")
        sync_file(keybindings_src, keybindings_dst, dry_run=args.dry_run)
    else:
        print(f"\n  [1/2] Skipping preference sync (--skip-configs).")

    # 3. Extension Management
    if not args.skip_extensions:
        print(f"\n  [2/2] Managing Extensions...")
        cli_path = resolve_cli(config["cli_candidates"])
        if not cli_path:
            msg = (
                f"  [Warning] CLI tool not found for {name}. Checked candidates:\n"
                + "\n".join(f"    - {c}" for c in config["cli_candidates"])
                + "\n  Skipping extension installation."
            )
            print(msg)
            return True, f"{name}: Configs synced, CLI unavailable"

        print(f"  Using CLI: {cli_path}")

        extensions_file = os.path.join(REPO_ROOT, config["extensions_relpath"])
        if not os.path.isfile(extensions_file):
            print(f"  [Error] Extensions list file not found: {extensions_file}")
            return False, f"{name}: Missing extensions.json"

        with open(extensions_file, "r", encoding="utf-8") as f:
            ext_data = json.load(f)
        recommendations = ext_data.get("recommendations", [])

        print(f"  Target Extensions: {len(recommendations)}")
        installed = get_installed_extensions(cli_path) if not args.force else set()

        installed_count = 0
        skipped_count = 0
        failed_count = 0

        for ext_id in recommendations:
            if ext_id.lower() in installed and not args.force:
                print(f"    [Already Installed] {ext_id}")
                skipped_count += 1
                continue

            if args.dry_run:
                print(f"    [Dry-Run] Would install: {ext_id}")
                installed_count += 1
                continue

            print(f"    [Installing] {ext_id}...", end="", flush=True)
            cmd = [cli_path, "--install-extension", ext_id]
            if args.force:
                cmd.append("--force")

            try:
                proc = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=120,
                    check=False,
                )
                if proc.returncode == 0:
                    print(" OK")
                    installed_count += 1
                else:
                    print(f" FAILED (exit code {proc.returncode})")
                    err_msg = proc.stderr.strip() or proc.stdout.strip()
                    if err_msg:
                        print(f"      {err_msg}")
                    failed_count += 1
            except subprocess.TimeoutExpired:
                print(" TIMED OUT")
                failed_count += 1
            except Exception as e:
                print(f" ERROR: {e}")
                failed_count += 1

        summary = (
            f"{name}: {installed_count} installed, {skipped_count} up-to-date, {failed_count} failed"
        )
        print(f"\n  Result: {summary}")
        return failed_count == 0, summary
    else:
        print(f"\n  [2/2] Skipping extensions (--skip-extensions).")
        return True, f"{name}: Configs synced, extensions skipped"


def main():
    parser = argparse.ArgumentParser(
        description="Unified IDE Setup & Extension Installer for Antigravity IDE, VS Code, Cursor, Windsurf.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/setup-ide.py --ide antigravity
  python3 scripts/setup-ide.py --ide all
  python3 scripts/setup-ide.py --ide vscode --dry-run
  python3 scripts/setup-ide.py --ide cursor --skip-extensions
  python3 scripts/setup-ide.py --ide windsurf --skip-configs
        """,
    )
    parser.add_argument(
        "--ide",
        choices=["antigravity", "vscode", "cursor", "windsurf", "all"],
        default="antigravity",
        help="Target IDE to configure (default: antigravity)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the setup process without copying files or installing extensions",
    )
    parser.add_argument(
        "--skip-extensions",
        action="store_true",
        help="Skip extension installation and only synchronize settings and keybindings",
    )
    parser.add_argument(
        "--skip-configs",
        action="store_true",
        help="Skip configuration file copying and only install extensions",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force reinstallation of extensions and overwrite existing files without skipping",
    )

    args = parser.parse_args()

    targets = list(IDE_REGISTRY.keys()) if args.ide == "all" else [args.ide]

    print("==================================================")
    print(" IDE Configs & Extensions Automated Setup")
    print(f" Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print(f" Targets: {', '.join(targets)}")
    print("==================================================")

    results = []
    overall_success = True

    for key in targets:
        success, msg = setup_ide(key, IDE_REGISTRY[key], args)
        results.append(msg)
        if not success:
            overall_success = False

    print("\n==================================================")
    print(" Execution Summary")
    print("==================================================")
    for res in results:
        print(f"  * {res}")
    print("\nNext step: Reload your editor window via Cmd + Shift + R.")

    sys.exit(0 if overall_success else 1)


if __name__ == "__main__":
    main()
