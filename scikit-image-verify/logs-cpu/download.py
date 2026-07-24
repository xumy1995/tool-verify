#!/usr/bin/env python3

import os
import re
import subprocess

LOG_FILE = "missing_file_v3.txt"

pattern = re.compile(
    r"Downloading file '(.+?)' from '(.+?)' to '(.+?)'\."
)

with open(LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        m = pattern.search(line)
        if not m:
            continue

        relative_path, url, _ = m.groups()

        dst = relative_path

        os.makedirs(os.path.dirname(dst), exist_ok=True)

        if os.path.exists(dst):
            print(f"[Skip] {dst}")
            continue

        print(f"[Download] {url}")
        print(f"           -> {dst}")

        result = subprocess.run(
            [
                "curl",
                "-L",              # 跟随重定向
                "--fail",          # HTTP错误返回非0
                "--retry", "3",    # 重试3次
                "--retry-delay", "2",
                "-o", dst,
                url,
            ]
        )

        if result.returncode == 0:
            print("[OK]\n")
        else:
            print(f"[FAILED] {url}\n")