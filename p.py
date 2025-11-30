#!/usr/bin/env python
import json
import os
import sys
import subprocess

# Path to p.json (same directory as this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "p.json")


def load_aliases():
    if not os.path.exists(DB_PATH):
        return {}
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_aliases(aliases):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(aliases, f, indent=2)


def print_help():
    print("")
    print("P - PATH ALIAS TOOL (Python version)")
    print("------------------------------------")
    print("")
    print("Usage:")
    print("  p add                        # interactive")
    print("  p add <alias> <path>         # non-interactive")
    print("")
    print("  p <alias>                    # print mapped path")
    print("  p <alias> -e                 # open in Explorer")
    print("  p <alias> -code              # open in VS Code")
    print("  p <alias> -t                 # open in terminal (new cmd window)")
    print("  p <alias> -delete            # delete alias")
    print("  p <alias> --print-path       # internal (used by wrapper)")
    print("")
    print("  p -list                      # list all aliases")
    print("  p <text>                     # fuzzy search: list aliases containing <text>")
    print("")
    print("Examples:")
    print("  p add nvim-conf %userprofile%\\AppData\\Local\\nvim")
    print("  p nvim-conf -e")
    print("  p vim                        # fuzzy search (matches nvim-conf, etc.)")
    print("")


def print_list(aliases=None):
    if aliases is None:
        aliases = load_aliases()

    if not aliases:
        print("No aliases stored.")
        return

    print("")
    print("Stored Aliases")
    print("--------------")

    for alias in sorted(aliases.keys(), key=lambda x: x.lower()):
        path = aliases[alias]
        print(f"{alias:<20}  {path}")

    print("")


def print_fuzzy_matches(query, aliases):
    q = query.lower()
    matches = {a: p for a, p in aliases.items() if q in a.lower()}

    if not matches:
        print(f'Alias "{query}" not found.')
        return

    print("")
    print(f'Matches for "{query}":')
    print("---------------------")
    for alias in sorted(matches.keys(), key=lambda x: x.lower()):
        print(f"{alias:<20}  {matches[alias]}")
    print("")


def cmd_add(args):
    aliases = load_aliases()

    if len(args) >= 2:
        alias = args[0]
        path = " ".join(args[1:])
    else:
        alias = input("Enter alias name: ").strip()
        path = input("Enter full path: ").strip()

    if not alias or not path:
        print("Alias and path cannot be empty.")
        return

    path = os.path.expandvars(path)
    aliases[alias] = path
    save_aliases(aliases)
    print(f'Saved alias "{alias}" -> "{path}"')


def cmd_for_alias(alias, action):
    aliases = load_aliases()
    path = aliases.get(alias)

    # No exact match
    if not path:
        # If no action flag -> treat as fuzzy search
        if action is None:
            print_fuzzy_matches(alias, aliases)
        else:
            # For actions (-e, -code, -t, --print-path, etc.) require exact match
            print(f'Alias "{alias}" not found.')
        return

    # Exact match: proceed with normal actions
    path = os.path.expandvars(path)

    if action is None:
        # Default: print path
        print(path)
        return

    action = action.lower()

    if action == "-e":
        # Open in Explorer
        subprocess.Popen(["explorer", path])

    elif action == "-code":
        # Open in VS Code
        subprocess.Popen(["code", path])

    elif action == "-t":
        # Open a new cmd window starting in this directory
        subprocess.Popen([
            "cmd",
            "/K",
            f'cd /d "{path}"'
        ])

    elif action == "-delete":
        if alias in aliases:
            del aliases[alias]
            save_aliases(aliases)
            print(f'Deleted alias "{alias}".')
        else:
            print(f'Alias "{alias}" not found.')

    elif action == "--print-path":
        # Internal use: batch wrapper uses this for -cd
        print(path)

    else:
        print(f"Unknown action: {action}")
        print("Try: -e, -code, -t, -delete")


def main(argv):
    if len(argv) == 0:
        print_help()
        return

    cmd = argv[0]

    # Help flags
    if cmd in ("help", "-help", "--help", "/?"):
        print_help()
        return

    # List aliases
    if cmd.lower() == "-list":
        print_list()
        return

    # Add command
    if cmd == "add":
        cmd_add(argv[1:])
        return

    # Otherwise: treat first arg as alias or fuzzy query
    alias = cmd
    action = argv[1] if len(argv) > 1 else None
    cmd_for_alias(alias, action)


if __name__ == "__main__":
    main(sys.argv[1:])
