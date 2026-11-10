#!/usr/bin/env python3
"""Write themes/kanagawa-<variant> (aerc stylesets) from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]

# Lines without colors: they set attributes only.
FIXED = [
    "*.default=true",
    "*.normal=true",
    "title.reverse=true",
    "header.bold=true",
    "*error.bold=true",
    "statusline*.default=true",
    "msglist_unread.bold=true",
    "dirlist_unread.bold=true",
    "completion_pill.reverse=true",
    "selector_focused.reverse=true",
    "selector_chooser.bold=true",
]
# aerc style object -> palette role.
COLORS = {
    "default.fg": "ui.fg",
    "default.bg": "ui.bg",
    "header.fg": "syn.fun",
    "error.fg": "diag.error",
    "warning.fg": "diag.warning",
    "success.fg": "diag.ok",
    "statusline_default.fg": "ui.fg_dim",
    "statusline_default.bg": "ui.bg_m3",
    "statusline_error.fg": "diag.error",
    "statusline_error.bg": "ui.bg_m3",
    "statusline_success.fg": "diag.ok",
    "statusline_success.bg": "ui.bg_m3",
    "dirlist_default.selected.fg": "ui.fg",
    "dirlist_default.selected.bg": "ui.bg_p2",
    "dirlist_unread.fg": "syn.fun",
    "msglist_default.selected.fg": "ui.fg",
    "msglist_default.selected.bg": "ui.bg_p2",
    "msglist_unread.fg": "syn.fun",
    "msglist_read.fg": "ui.fg_dim",
    "msglist_marked.fg": "syn.constant",
    "msglist_flagged.fg": "diag.warning",
    "msglist_deleted.fg": "vcs.removed",
    "msglist_result.fg": "syn.string",
    "tab.fg": "ui.fg_dim",
    "tab.bg": "ui.bg_m3",
    "tab.selected.fg": "ui.fg",
    "tab.selected.bg": "ui.bg_p2",
    "border.fg": "ui.bg_m3",
    "border.bg": "ui.bg_m3",
}


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def theme(variant, colors):
    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/aerc", ""]
    out += FIXED + [""]
    out += [f"{k}={colors[r]}" for k, r in COLORS.items()]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v, roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
