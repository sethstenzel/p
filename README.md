# p — Path Alias Utility

A stupidly simple path aliasing utility for windows.

This utility lets you create short alias names for long paths and quickly:

- Open the directory in Explorer
- Open in VS Code
- Open a terminal in that directory
- Change your shell's working directory (`-cd`)
- Fuzzy-search aliases
- List all stored aliases

Aliases are stored in a simple JSON file: **`p.json`**.

---

## 🚀 Features

### 🔧 Manage Aliases

| Command | Description |
|--------|-------------|
| `p add` | Interactive alias creation |
| `p add <alias> <path>` | Add alias non-interactively |
| `p <alias>` | Print the stored path |
| `p <alias> -delete` | Delete an alias |

### 📂 Path Actions

| Command | Description |
|---------|-------------|
| `p <alias> -e` | Open folder in Explorer |
| `p <alias> -code` | Open folder in VS Code |
| `p <alias> -t` | Open a new terminal (cmd) in that folder |

### 📍 Changing the Current Directory

| Shell | Behavior |
|-------|----------|
| **CMD.exe** | `p <alias> -cd` changes the working directory |
| **PowerShell** | `p <alias> -cd` needs to be piped into `\| cd` |

### 🔍 Fuzzy Search

If you type a name that **is not an exact alias**, fuzzy search kicks in:
