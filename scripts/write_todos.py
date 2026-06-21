#!/usr/bin/env python3
"""
write_todos.py — 把待办写入飞书多维表格

用法：
  python3 write_todos.py --config config.yaml --todos /tmp/todos.json

待办 JSON 格式：
[
  {
    "id": "M1-01",
    "title": "完成竞品分析报告",
    "owner": "张三",
    "due_date": "2026-07-01",
    "deliverable": "竞品分析 PPT",
    "reviewer": "李总",
    "collaborators": "王五",
    "source_meeting": "2026-06-28 产品讨论会"
  }
]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone

import yaml


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_lark_cli(args, profile=None):
    cmd = ["lark-cli"]
    if profile:
        cmd.extend(["--profile", profile])
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print(f"lark-cli error: {result.stderr}", file=sys.stderr)
        return None
    raw = result.stdout
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError) as e:
        print(f"JSON parse error: {e}\nraw output: {raw}", file=sys.stderr)
        return None


def date_to_timestamp_ms(date_str):
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            dt = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    print(f"warning: cannot parse date '{date_str}', skipping", file=sys.stderr)
    return None


def fetch_existing_records(profile, base_token, table_id):
    resp = run_lark_cli(
        ["base", "+record-list", "--as", "user",
         "--base-token", base_token,
         "--table-id", table_id,
         "--page-size", "200"],
        profile=profile,
    )
    if not resp or "data" not in resp:
        return {}
    items = resp["data"].get("items", [])
    index = {}
    for item in items:
        fields = item.get("fields", {})
        todo_id = None
        for key in ("ID", "id", "编号"):
            val = fields.get(key)
            if val:
                if isinstance(val, list):
                    todo_id = val[0].get("text", "") if val else ""
                else:
                    todo_id = str(val)
                break
        if todo_id:
            index[todo_id] = item["record_id"]
    return index


def upsert_todo(profile, base_token, table_id, todo, record_id=None):
    fields = {
        "ID": todo["id"],
        "待办事项": todo["title"],
        "负责人": todo["owner"],
        "完成标准": f"{todo['deliverable']}，{todo['reviewer']}确认",
        "协同方": todo.get("collaborators", ""),
        "来源会议": todo.get("source_meeting", ""),
        "状态": "待确认",
    }
    due_ts = date_to_timestamp_ms(todo.get("due_date", ""))
    if due_ts:
        fields["截止日期"] = due_ts

    args = [
        "base", "+record-upsert", "--as", "user",
        "--base-token", base_token,
        "--table-id", table_id,
        "--json", json.dumps(fields, ensure_ascii=False),
    ]
    if record_id:
        args.extend(["--record-id", record_id])

    resp = run_lark_cli(args, profile=profile)
    return resp is not None


def main():
    parser = argparse.ArgumentParser(description="Write meeting todos to Feishu bitable")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--todos", required=True, help="Path to todos JSON file")
    args = parser.parse_args()

    config = load_config(args.config)
    with open(args.todos, "r", encoding="utf-8") as f:
        todos = json.load(f)

    feishu = config["feishu"]
    profile = feishu.get("profile", "default")
    base_token = feishu["bitable"]["base_token"]
    table_id = feishu["bitable"]["table_id"]

    if not base_token or not table_id:
        print("error: bitable base_token or table_id not configured", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching existing records from bitable...")
    existing = fetch_existing_records(profile, base_token, table_id)
    print(f"Found {len(existing)} existing records")

    success_count = 0
    for todo in todos:
        record_id = existing.get(todo["id"])
        action = "updating" if record_id else "creating"
        print(f"  {action}: {todo['id']} - {todo['title']}")
        if upsert_todo(profile, base_token, table_id, todo, record_id):
            success_count += 1
        else:
            print(f"  FAILED: {todo['id']}", file=sys.stderr)

    print(f"\nDone: {success_count}/{len(todos)} todos written to bitable")
    if success_count < len(todos):
        sys.exit(1)


if __name__ == "__main__":
    main()
