#!/usr/bin/env python3
"""
check_setup.py — 检查 Meeting to Action 的环境是否就绪

用法：
  python3 check_setup.py --config config.yaml
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    msg = f"  [{status}] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return ok


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    print("Meeting to Action — Setup Check\n")
    all_ok = True

    all_ok &= check("Python 3.8+",
                     sys.version_info >= (3, 8),
                     f"found {sys.version.split()[0]}")

    all_ok &= check("PyYAML installed", HAS_YAML,
                     "pip install pyyaml" if not HAS_YAML else "")

    lark_path = shutil.which("lark-cli")
    all_ok &= check("lark-cli installed",
                     lark_path is not None,
                     "npm install -g lark-cli" if not lark_path else lark_path)

    if lark_path:
        result = subprocess.run(["lark-cli", "profile", "list"],
                                capture_output=True, text=True, timeout=10)
        has_profile = result.returncode == 0 and "name" in result.stdout.lower()
        all_ok &= check("lark-cli profile configured", has_profile,
                         "run: lark-cli profile add" if not has_profile else "")

    config_path = Path(args.config)
    has_config = config_path.exists()
    all_ok &= check("config.yaml exists", has_config,
                     "cp config.example.yaml config.yaml" if not has_config else "")

    if has_config and HAS_YAML:
        with open(config_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        feishu = cfg.get("feishu", {})
        bt = feishu.get("bitable", {})

        all_ok &= check("doc_folder_token configured",
                         bool(feishu.get("doc_folder_token")))
        all_ok &= check("bitable base_token configured",
                         bool(bt.get("base_token")))
        all_ok &= check("bitable table_id configured",
                         bool(bt.get("table_id")))

        notif = cfg.get("notification", {})
        im_on = notif.get("feishu_im", {}).get("enabled", False)
        email_on = notif.get("email", {}).get("enabled", False)
        all_ok &= check("at least one notification channel",
                         im_on or email_on,
                         "enable feishu_im or email in config" if not (im_on or email_on) else "")

        if im_on:
            contacts = notif.get("feishu_im", {}).get("contacts", {}) or {}
            all_ok &= check("feishu_im contacts configured",
                             len(contacts) > 0,
                             "add name: open_id pairs")
        if email_on:
            email_cfg = notif.get("email", {})
            all_ok &= check("SMTP host configured",
                             bool(email_cfg.get("smtp_host")))
            contacts = email_cfg.get("contacts", {}) or {}
            all_ok &= check("email contacts configured",
                             len(contacts) > 0)

    print()
    if all_ok:
        print("All checks passed. Ready to go!")
    else:
        print("Some checks failed. Fix the issues above and re-run.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
