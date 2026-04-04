#!/usr/bin/env python3
"""插入 / 删除飞书电子表格的行或列。

lark-cli 没有内置 v2 dimension_range API shortcut，本脚本封装这些操作。

Usage:
    python sheets_dimension.py insert <token> <sheet_id> --major-dimension ROWS --start 2 --end 5
    python sheets_dimension.py delete <token> <sheet_id> --major-dimension COLUMNS --start 3 --end 4
"""
import argparse
import json
import subprocess
import sys

V2 = "/open-apis/sheets/v2/spreadsheets"
IDENTITIES = ("user", "bot", "auto")
FORMATS = ("json", "ndjson", "table", "csv", "pretty")
DIMENSIONS = ("ROWS", "COLUMNS")


def cli(*args: str) -> int:
    return subprocess.run(["lark-cli", *args]).returncode


def cmd_insert(a: argparse.Namespace) -> int:
    data = {
        "dimension": {
            "sheetId": a.sheet_id,
            "majorDimension": a.major_dimension,
            "startIndex": a.start,
            "endIndex": a.end,
        },
        "inheritStyle": a.inherit_style,
    }
    cmd = ["api", "POST", f"{V2}/{a.token}/insert_dimension_range",
           "--as", a.identity, "--format", a.fmt,
           "--data", json.dumps(data, ensure_ascii=False)]
    if a.dry_run:
        cmd.append("--dry-run")
    return cli(*cmd)


def cmd_delete(a: argparse.Namespace) -> int:
    data = {
        "dimension": {
            "sheetId": a.sheet_id,
            "majorDimension": a.major_dimension,
            "startIndex": a.start,
            "endIndex": a.end,
        }
    }
    cmd = ["api", "DELETE", f"{V2}/{a.token}/dimension_range",
           "--as", a.identity, "--format", a.fmt,
           "--data", json.dumps(data, ensure_ascii=False)]
    if a.dry_run:
        cmd.append("--dry-run")
    return cli(*cmd)


def add_common(p):
    p.add_argument("token", help="spreadsheet token")
    p.add_argument("sheet_id", help="sheet ID")
    p.add_argument("--major-dimension", required=True, choices=DIMENSIONS,
                   help="ROWS 或 COLUMNS")
    p.add_argument("--start", type=int, required=True,
                   help="起始索引（0-based，inclusive）")
    p.add_argument("--end", type=int, required=True,
                   help="结束索引（0-based，exclusive）")
    p.add_argument("--as", dest="identity", default="user", choices=IDENTITIES)
    p.add_argument("--format", dest="fmt", default="json", choices=FORMATS)
    p.add_argument("--dry-run", action="store_true")


def main() -> int:
    ap = argparse.ArgumentParser(description="插入 / 删除飞书电子表格的行或列")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("insert", help="插入行或列")
    add_common(p)
    p.add_argument("--inherit-style", choices=("BEFORE", "AFTER"), default="BEFORE",
                   help="继承样式方向（默认 BEFORE）")
    p.set_defaults(func=cmd_insert)

    p = sub.add_parser("delete", help="删除行或列")
    add_common(p)
    p.set_defaults(func=cmd_delete)

    args = ap.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
