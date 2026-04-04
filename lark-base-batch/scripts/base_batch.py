#!/usr/bin/env python3
"""飞书多维表格批量记录操作：创建、更新、删除。

lark-cli 的 +record-upsert/+record-delete 一次只能处理一条记录，
本脚本封装 batch API，支持自动分片（每片最多 500 条）。

Usage:
    python base_batch.py create <app_token> <table_id> --json '[{...},{...}]'
    python base_batch.py update <app_token> <table_id> --json '[{"record_id":"rec_xxx","fields":{...}}]'
    python base_batch.py delete <app_token> <table_id> --json '["rec_xxx","rec_yyy"]'
    python base_batch.py <cmd>  <app_token> <table_id> --file records.json
"""
import argparse
import json
import subprocess
import sys
import time

BATCH_SIZE = 500
BATCH_DELAY_MS = 200
IDENTITIES = ("user", "bot", "auto")
FORMATS = ("json", "ndjson", "table", "csv", "pretty")

BASE_V1 = "/open-apis/bitable/v1/apps"


def cli(*args: str) -> int:
    return subprocess.run(["lark-cli", *args]).returncode


def load_data(a: argparse.Namespace) -> list:
    if a.file:
        with open(a.file, encoding="utf-8") as f:
            data = json.load(f)
    elif a.json:
        data = json.loads(a.json)
    else:
        raise RuntimeError("必须指定 --json 或 --file")
    if not isinstance(data, list):
        raise RuntimeError(f"输入必须是 JSON 数组，当前类型: {type(data).__name__}")
    return data


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# ── commands ─────────────────────────────────────────────────────────

def cmd_create(a: argparse.Namespace) -> int:
    records = load_data(a)
    # 简写格式：[{field:value}] → [{"fields":{field:value}}]
    wrapped = []
    for r in records:
        if "fields" in r:
            wrapped.append(r)
        else:
            wrapped.append({"fields": r})

    total = len(wrapped)
    print(f"批量创建 {total} 条记录（分片大小 {BATCH_SIZE}）", file=sys.stderr)

    failed = 0
    for i, batch in enumerate(chunks(wrapped, BATCH_SIZE)):
        if i > 0:
            time.sleep(BATCH_DELAY_MS / 1000)
        data = json.dumps({"records": batch}, ensure_ascii=False)
        cmd = ["api", "POST",
               f"{BASE_V1}/{a.app_token}/tables/{a.table_id}/records/batch_create",
               "--as", a.identity, "--format", a.fmt, "--data", data]
        if a.dry_run:
            cmd.append("--dry-run")
        print(f"  片 {i + 1}: {len(batch)} 条", file=sys.stderr)
        rc = cli(*cmd)
        if rc != 0:
            failed += len(batch)
    if failed:
        print(f"失败 {failed}/{total} 条", file=sys.stderr)
        return 1
    return 0


def cmd_update(a: argparse.Namespace) -> int:
    records = load_data(a)
    for r in records:
        if "record_id" not in r or "fields" not in r:
            raise RuntimeError(f"每条记录必须包含 record_id 和 fields: {json.dumps(r, ensure_ascii=False)}")

    total = len(records)
    print(f"批量更新 {total} 条记录", file=sys.stderr)

    failed = 0
    for i, batch in enumerate(chunks(records, BATCH_SIZE)):
        if i > 0:
            time.sleep(BATCH_DELAY_MS / 1000)
        data = json.dumps({"records": batch}, ensure_ascii=False)
        cmd = ["api", "POST",
               f"{BASE_V1}/{a.app_token}/tables/{a.table_id}/records/batch_update",
               "--as", a.identity, "--format", a.fmt, "--data", data]
        if a.dry_run:
            cmd.append("--dry-run")
        print(f"  片 {i + 1}: {len(batch)} 条", file=sys.stderr)
        rc = cli(*cmd)
        if rc != 0:
            failed += len(batch)
    if failed:
        print(f"失败 {failed}/{total} 条", file=sys.stderr)
        return 1
    return 0


def cmd_delete(a: argparse.Namespace) -> int:
    record_ids = load_data(a)
    for rid in record_ids:
        if not isinstance(rid, str):
            raise RuntimeError(f"delete 输入必须是 record_id 字符串数组，got: {type(rid).__name__}")

    total = len(record_ids)
    print(f"批量删除 {total} 条记录", file=sys.stderr)

    failed = 0
    for i, batch in enumerate(chunks(record_ids, BATCH_SIZE)):
        if i > 0:
            time.sleep(BATCH_DELAY_MS / 1000)
        data = json.dumps({"records": batch}, ensure_ascii=False)
        cmd = ["api", "POST",
               f"{BASE_V1}/{a.app_token}/tables/{a.table_id}/records/batch_delete",
               "--as", a.identity, "--format", a.fmt, "--data", data]
        if a.dry_run:
            cmd.append("--dry-run")
        print(f"  片 {i + 1}: {len(batch)} 条", file=sys.stderr)
        rc = cli(*cmd)
        if rc != 0:
            failed += len(batch)
    if failed:
        print(f"失败 {failed}/{total} 条", file=sys.stderr)
        return 1
    return 0


# ── CLI ──────────────────────────────────────────────────────────────

def add_common(p):
    p.add_argument("app_token", help="Base app token")
    p.add_argument("table_id", help="表 ID")
    p.add_argument("--json", default=None, help="JSON 数组字符串")
    p.add_argument("--file", default=None, help="JSON 文件路径")
    p.add_argument("--as", dest="identity", default="user", choices=IDENTITIES)
    p.add_argument("--format", dest="fmt", default="json", choices=FORMATS)
    p.add_argument("--dry-run", action="store_true")


def main() -> int:
    ap = argparse.ArgumentParser(description="飞书多维表格批量记录操作")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("create", help="批量创建记录")
    add_common(p)
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("update", help="批量更新记录")
    add_common(p)
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("delete", help="批量删除记录")
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
