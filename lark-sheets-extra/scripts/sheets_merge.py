#!/usr/bin/env python3
"""合并 / 取消合并飞书电子表格单元格。

lark-cli 没有内置 merge_cells / unmerge_cells shortcut（v2 API），
本脚本通过 `lark-cli api` 封装这些操作。

Usage:
    python sheets_merge.py merge  <token> <sheet_id> <range> [--merge-type MERGE_ALL]
    python sheets_merge.py unmerge <token> <sheet_id> <range>
    python sheets_merge.py test   [--title "My Test"] [--unmerge-after]
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime

MERGE_TYPES = ("MERGE_ALL", "MERGE_ROWS", "MERGE_COLUMNS")
FORMATS = ("json", "ndjson", "table", "csv", "pretty")
IDENTITIES = ("user", "bot", "auto")

V2 = "/open-apis/sheets/v2/spreadsheets"


def cli(*args: str) -> int:
    return subprocess.run(["lark-cli", *args]).returncode


def cli_json(*args: str) -> dict:
    r = subprocess.run(["lark-cli", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or "lark-cli failed")
    return json.loads(r.stdout)


def qualify(sheet_id: str, cell_range: str) -> str:
    """Ensure range is fully qualified: <sheet_id>!A1:C3."""
    return cell_range if "!" in cell_range else f"{sheet_id}!{cell_range}"


# ── commands ─────────────────────────────────────────────────────────

def cmd_merge(a: argparse.Namespace) -> int:
    data = {"range": qualify(a.sheet_id, a.range), "mergeType": a.merge_type}
    cmd = ["api", "POST", f"{V2}/{a.token}/merge_cells",
           "--as", a.identity, "--format", a.fmt,
           "--data", json.dumps(data, ensure_ascii=False)]
    if a.dry_run:
        cmd.append("--dry-run")
    return cli(*cmd)


def cmd_unmerge(a: argparse.Namespace) -> int:
    data = {"range": qualify(a.sheet_id, a.range)}
    cmd = ["api", "POST", f"{V2}/{a.token}/unmerge_cells",
           "--as", a.identity, "--format", a.fmt,
           "--data", json.dumps(data, ensure_ascii=False)]
    if a.dry_run:
        cmd.append("--dry-run")
    return cli(*cmd)


def cmd_test(a: argparse.Namespace) -> int:
    title = a.title or f"Merge Test {datetime.now():%Y-%m-%d %H:%M:%S}"

    # 1. create spreadsheet
    resp = cli_json("api", "POST", "/open-apis/sheets/v3/spreadsheets",
                    "--as", a.identity, "--format", "json",
                    "--data", json.dumps({"title": title}, ensure_ascii=False))
    token = (resp.get("data", {}).get("spreadsheet", {}).get("spreadsheet_token")
             or resp.get("data", {}).get("spreadsheetToken"))
    if not token:
        raise RuntimeError(f"no token in response: {json.dumps(resp, ensure_ascii=False)}")

    # 2. resolve first sheet id
    if a.sheet_id:
        sid = a.sheet_id
    else:
        info = cli_json("api", "GET",
                        f"/open-apis/sheets/v3/spreadsheets/{token}/sheets/query",
                        "--as", a.identity, "--format", "json")
        sheets = info.get("data", {}).get("sheets", [])
        if isinstance(sheets, dict):
            sheets = [sheets]
        if not sheets:
            raise RuntimeError(f"no sheets found: {json.dumps(info, ensure_ascii=False)}")
        sid = sheets[0].get("sheet_id") or sheets[0].get("sheetId")
        if not sid:
            raise RuntimeError(f"no sheet_id: {json.dumps(sheets[0], ensure_ascii=False)}")

    # 3. write sample data
    values = a.values or '[["合并测试","",""],["姓名","部门","状态"],["小敬","OpenClaw","OK"],["图图","Owner","OK"]]'
    rc = cli("sheets", "+write", "--spreadsheet-token", token,
             "--sheet-id", sid, "--range", a.write_range, "--values", values,
             "--as", a.identity)
    if rc != 0:
        return rc

    # 4. merge
    data = {"range": qualify(sid, a.merge_range), "mergeType": a.merge_type}
    rc = cli("api", "POST", f"{V2}/{token}/merge_cells",
             "--as", a.identity, "--format", a.fmt,
             "--data", json.dumps(data, ensure_ascii=False))
    if rc != 0:
        return rc

    # 5. optional unmerge
    if a.unmerge_after:
        udata = {"range": qualify(sid, a.merge_range)}
        rc = cli("api", "POST", f"{V2}/{token}/unmerge_cells",
                 "--as", a.identity, "--format", a.fmt,
                 "--data", json.dumps(udata, ensure_ascii=False))
        if rc != 0:
            return rc

    print(json.dumps({
        "title": title, "spreadsheet_token": token, "sheet_id": sid,
        "write_range": qualify(sid, a.write_range),
        "merge_range": qualify(sid, a.merge_range),
        "unmerge_after": a.unmerge_after,
    }, ensure_ascii=False, indent=2))
    return 0


# ── CLI ──────────────────────────────────────────────────────────────

def add_common(p, *, need_range=True):
    p.add_argument("token", help="spreadsheet token")
    p.add_argument("sheet_id", help="sheet ID")
    if need_range:
        p.add_argument("range", help="cell range, e.g. A1:C3")
    p.add_argument("--as", dest="identity", default="user", choices=IDENTITIES)
    p.add_argument("--format", dest="fmt", default="json", choices=FORMATS)
    p.add_argument("--dry-run", action="store_true")


def main() -> int:
    ap = argparse.ArgumentParser(description="合并 / 取消合并飞书电子表格单元格")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("merge", help="合并单元格")
    add_common(p)
    p.add_argument("--merge-type", default="MERGE_ALL", choices=MERGE_TYPES)
    p.set_defaults(func=cmd_merge)

    p = sub.add_parser("unmerge", help="取消合并")
    add_common(p)
    p.set_defaults(func=cmd_unmerge)

    p = sub.add_parser("test", help="创建表格 → 写入 → 合并（端到端测试）")
    p.add_argument("--title", default=None)
    p.add_argument("--sheet-id", default=None)
    p.add_argument("--write-range", default="A1:C4")
    p.add_argument("--merge-range", default="A1:C1")
    p.add_argument("--merge-type", default="MERGE_ALL", choices=MERGE_TYPES)
    p.add_argument("--values", default=None)
    p.add_argument("--unmerge-after", action="store_true")
    p.add_argument("--as", dest="identity", default="user", choices=IDENTITIES)
    p.add_argument("--format", dest="fmt", default="json", choices=FORMATS)
    p.set_defaults(func=cmd_test)

    args = ap.parse_args()
    try:
        return args.func(args)
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
