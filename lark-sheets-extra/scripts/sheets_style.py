#!/usr/bin/env python3
"""设置飞书电子表格单元格样式。

lark-cli 没有内置 v2 style API shortcut，本脚本提供友好的命令行接口。

Usage:
    python sheets_style.py <token> <sheet_id> <range> [style flags...]

Examples:
    python sheets_style.py shtcnXXX abc123 A1:C1 --bold --h-align CENTER
    python sheets_style.py shtcnXXX abc123 A1:D1 --bg-color "#4A90D9" --font-size 14
    python sheets_style.py shtcnXXX abc123 A1:D10 --border all --border-color "#000000"
"""
import argparse
import json
import subprocess
import sys

V2 = "/open-apis/sheets/v2/spreadsheets"
IDENTITIES = ("user", "bot", "auto")
FORMATS = ("json", "ndjson", "table", "csv", "pretty")
H_ALIGNS = ("LEFT", "CENTER", "RIGHT")
V_ALIGNS = ("TOP", "MIDDLE", "BOTTOM")
WRAP_STRATEGIES = ("OVERFLOW", "CLIP", "WRAP")
BORDER_POSITIONS = ("top", "bottom", "left", "right", "all")


def cli(*args: str) -> int:
    return subprocess.run(["lark-cli", *args]).returncode


def qualify(sheet_id: str, cell_range: str) -> str:
    return cell_range if "!" in cell_range else f"{sheet_id}!{cell_range}"


def parse_color(hex_color: str) -> str:
    return hex_color.lstrip("#")


def build_style(a: argparse.Namespace) -> dict:
    s: dict = {}

    font: dict = {}
    if a.bold is not None:
        font["bold"] = a.bold
    if a.italic is not None:
        font["italic"] = a.italic
    if a.font_size is not None:
        font["fontSize"] = a.font_size
    if a.font_color is not None:
        font["color"] = parse_color(a.font_color)
    if font:
        s["font"] = font

    if a.h_align:
        s["hAlign"] = a.h_align
    if a.v_align:
        s["vAlign"] = a.v_align
    if a.wrap:
        s["wrapStrategy"] = a.wrap
    if a.bg_color:
        s["backgroundColor"] = parse_color(a.bg_color)

    if a.border:
        border_color = parse_color(a.border_color) if a.border_color else "000000"
        border_style = a.border_style or "FULL"
        b = {"borderType": border_style, "color": border_color}
        positions = a.border
        if "all" in positions:
            positions = ["top", "bottom", "left", "right"]
        for pos in positions:
            s[f"border{pos.capitalize()}"] = b

    return s


def main() -> int:
    ap = argparse.ArgumentParser(description="设置飞书电子表格单元格样式")
    ap.add_argument("token", help="spreadsheet token")
    ap.add_argument("sheet_id", help="sheet ID")
    ap.add_argument("range", help="cell range, e.g. A1:C3")
    ap.add_argument("--as", dest="identity", default="user", choices=IDENTITIES)
    ap.add_argument("--format", dest="fmt", default="json", choices=FORMATS)
    ap.add_argument("--dry-run", action="store_true")

    ap.add_argument("--bold", action="store_true", default=None)
    ap.add_argument("--no-bold", dest="bold", action="store_false")
    ap.add_argument("--italic", action="store_true", default=None)
    ap.add_argument("--no-italic", dest="italic", action="store_false")
    ap.add_argument("--font-size", type=int, default=None, help="字号 (pt)")
    ap.add_argument("--font-color", default=None, help="字体颜色 hex, e.g. #FF0000")

    ap.add_argument("--h-align", choices=H_ALIGNS, default=None)
    ap.add_argument("--v-align", choices=V_ALIGNS, default=None)
    ap.add_argument("--wrap", choices=WRAP_STRATEGIES, default=None)
    ap.add_argument("--bg-color", default=None, help="背景颜色 hex")

    ap.add_argument("--border", nargs="+", choices=BORDER_POSITIONS, default=None,
                    help="边框位置: top bottom left right all")
    ap.add_argument("--border-color", default=None, help="边框颜色 hex")
    ap.add_argument("--border-style", default=None, help="边框样式: FULL, DASHED, DOTTED")

    args = ap.parse_args()

    style = build_style(args)
    if not style:
        print("error: 未指定任何样式参数", file=sys.stderr)
        return 1

    data = {
        "appendStyle": {
            "range": qualify(args.sheet_id, args.range),
            "style": style,
        }
    }
    cmd = ["api", "PUT", f"{V2}/{args.token}/style",
           "--as", args.identity, "--format", args.fmt,
           "--data", json.dumps(data, ensure_ascii=False)]
    if args.dry_run:
        cmd.append("--dry-run")
    return cli(*cmd)


if __name__ == "__main__":
    sys.exit(main())
