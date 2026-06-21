#!/usr/bin/env python3
"""
notify.py — 按负责人发送待办通知（飞书 IM / 邮件）

用法：
  python3 notify.py --config config.yaml --todos /tmp/todos.json \
    --meeting-title "产品讨论会" --minutes-url "https://..."
"""

import argparse
import json
import smtplib
import subprocess
import sys
import tempfile
from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import yaml


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def group_by_owner(todos):
    groups = defaultdict(list)
    for todo in todos:
        groups[todo["owner"]].append(todo)
    return groups


def format_im_message(owner, todos, meeting_title, minutes_url):
    lines = [f"Hi {owner}，以下是「{meeting_title}」会后你的待办事项：\n"]
    for i, todo in enumerate(todos, 1):
        lines.append(f"{i}. {todo['title']}")
        lines.append(f"   截止：{todo.get('due_date', '待定')}")
        lines.append(f"   完成标准：{todo.get('deliverable', '')}")
        if todo.get("reviewer"):
            lines.append(f"   验收人：{todo['reviewer']}")
        if todo.get("collaborators"):
            lines.append(f"   协同方：{todo['collaborators']}")
        lines.append("")
    if minutes_url:
        lines.append(f"会议纪要：{minutes_url}")
    return "\n".join(lines)


def format_email_html(owner, todos, meeting_title, minutes_url):
    template_path = Path(__file__).parent.parent / "templates" / "email_todo.html"
    if not template_path.exists():
        return format_email_html_inline(owner, todos, meeting_title, minutes_url)
    template = template_path.read_text(encoding="utf-8")
    rows = ""
    for i, todo in enumerate(todos, 1):
        rows += f"""
        <tr style="border-bottom:1px solid #e8e8e8;">
          <td style="padding:12px 8px;color:#666;font-size:14px;width:30px;vertical-align:top;">{i:02d}</td>
          <td style="padding:12px 8px;">
            <div style="font-size:15px;color:#1a1a1a;font-weight:500;">{todo['title']}</div>
            <div style="font-size:13px;color:#888;margin-top:4px;">
              截止 {todo.get('due_date', '待定')} | {todo.get('deliverable', '')}，{todo.get('reviewer', '')}确认
            </div>
          </td>
        </tr>"""
    return (template
            .replace("{{owner}}", owner)
            .replace("{{meeting_title}}", meeting_title)
            .replace("{{todo_rows}}", rows)
            .replace("{{minutes_url}}", minutes_url or "#"))


def format_email_html_inline(owner, todos, meeting_title, minutes_url):
    rows = ""
    for i, todo in enumerate(todos, 1):
        rows += f"""
        <tr style="border-bottom:1px solid #e8e8e8;">
          <td style="padding:12px 8px;color:#666;font-size:14px;width:30px;vertical-align:top;">{i:02d}</td>
          <td style="padding:12px 8px;">
            <div style="font-size:15px;color:#1a1a1a;font-weight:500;">{todo['title']}</div>
            <div style="font-size:13px;color:#888;margin-top:4px;">
              截止 {todo.get('due_date', '待定')} | {todo.get('deliverable', '')}，{todo.get('reviewer', '')}确认
            </div>
          </td>
        </tr>"""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Microsoft YaHei',sans-serif;margin:0;padding:20px;background:#f5f5f5;">
<div style="max-width:600px;margin:0 auto;background:#fff;padding:32px;">
  <h2 style="font-size:18px;color:#1a1a1a;margin:0 0 8px;">会后待办确认</h2>
  <p style="font-size:14px;color:#888;margin:0 0 24px;">{owner} | {meeting_title}</p>
  <table style="width:100%;border-collapse:collapse;">{rows}</table>
  <div style="margin-top:24px;padding-top:16px;border-top:1px solid #e8e8e8;">
    <a href="{minutes_url or '#'}" style="color:#045e81;font-size:14px;">查看会议纪要</a>
  </div>
</div>
</body></html>"""


def send_feishu_im(profile, open_id, message):
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(message)
        tmp_path = f.name
    try:
        cmd = [
            "lark-cli", "--profile", profile,
            "im", "+messages-send", "--as", "bot",
            "--user-id", open_id,
            "--text", message,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def send_email(config, to_email, owner, html_body, meeting_title):
    smtp_cfg = config["notification"]["email"]
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"会后待办确认 | {meeting_title}"
    msg["From"] = f"{smtp_cfg.get('sender_name', '会议助手')} <{smtp_cfg['smtp_user']}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    try:
        with smtplib.SMTP_SSL(smtp_cfg["smtp_host"], smtp_cfg["smtp_port"]) as server:
            server.login(smtp_cfg["smtp_user"], smtp_cfg["smtp_pass"])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"email error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Send todo notifications")
    parser.add_argument("--config", required=True, help="Path to config.yaml")
    parser.add_argument("--todos", required=True, help="Path to todos JSON file")
    parser.add_argument("--meeting-title", required=True, help="Meeting title")
    parser.add_argument("--minutes-url", default="", help="Minutes document URL")
    args = parser.parse_args()

    config = load_config(args.config)
    with open(args.todos, "r", encoding="utf-8") as f:
        todos = json.load(f)

    groups = group_by_owner(todos)
    profile = config["feishu"].get("profile", "default")
    im_cfg = config.get("notification", {}).get("feishu_im", {})
    email_cfg = config.get("notification", {}).get("email", {})

    im_enabled = im_cfg.get("enabled", False)
    email_enabled = email_cfg.get("enabled", False)

    if not im_enabled and not email_enabled:
        print("warning: no notification channel enabled in config", file=sys.stderr)
        sys.exit(0)

    im_contacts = im_cfg.get("contacts", {}) or {}
    email_contacts = email_cfg.get("contacts", {}) or {}

    for owner, owner_todos in groups.items():
        sent = False

        if im_enabled and owner in im_contacts:
            message = format_im_message(owner, owner_todos, args.meeting_title, args.minutes_url)
            if send_feishu_im(profile, im_contacts[owner], message):
                print(f"  IM sent to {owner}")
                sent = True
            else:
                print(f"  IM FAILED for {owner}", file=sys.stderr)

        if email_enabled and owner in email_contacts:
            html = format_email_html(owner, owner_todos, args.meeting_title, args.minutes_url)
            if send_email(config, email_contacts[owner], owner, html, args.meeting_title):
                print(f"  Email sent to {owner}")
                sent = True
            else:
                print(f"  Email FAILED for {owner}", file=sys.stderr)

        if not sent:
            print(f"  WARNING: {owner} has no contact configured, skipped", file=sys.stderr)

    print(f"\nDone: notified {len(groups)} people")


if __name__ == "__main__":
    main()
