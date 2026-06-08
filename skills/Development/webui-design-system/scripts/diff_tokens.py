#!/usr/bin/env python3
"""diff_tokens.py — 让设计系统「变更可观测」。

对比两版 tokens.css / components.css，输出人类可读的变更清单（新增 / 删除 / 改值 /
组件增删），可直接粘进 UI_SPEC 的「变更记录」。结构化源进 git 后，配合本脚本，任何
UI 变更都能被追溯，而不依赖手写记忆。

用法:
    # token 值的变更
    python3 diff_tokens.py OLD/tokens.css NEW/tokens.css

    # 组件库的增删
    python3 diff_tokens.py OLD/components.css NEW/components.css --mode components

    # 用 git 取旧版（无需手动 checkout）
    python3 diff_tokens.py --git HEAD design-system/tokens.css

无第三方依赖。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

VAR_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;}]+?)\s*[;}]")
CLASS_RE = re.compile(r"\.(ds-[A-Za-z0-9_-]+)")


def read_source(path: str, git_ref: str | None) -> str:
    if git_ref:
        try:
            return subprocess.check_output(
                ["git", "show", f"{git_ref}:{path}"], text=True, stderr=subprocess.DEVNULL
            )
        except subprocess.CalledProcessError:
            return ""  # 文件在该版本不存在 → 视为全新
    return Path(path).read_text(encoding="utf-8")


def parse_vars(css: str) -> dict[str, str]:
    # 优先只取 :root 块的 canonical 值，避免被 [data-theme] 等主题覆盖块干扰。
    root_match = re.search(r":root\s*\{(.*?)\}", css, re.DOTALL)
    scope = root_match.group(1) if root_match else css
    out: dict[str, str] = {}
    for name, value in VAR_RE.findall(scope):
        out[name] = re.sub(r"\s+", " ", value.strip())
    return out


def parse_classes(css: str) -> set[str]:
    return set(CLASS_RE.findall(css))


def diff_vars(old: dict[str, str], new: dict[str, str]) -> list[str]:
    lines = []
    added = [k for k in new if k not in old]
    removed = [k for k in old if k not in new]
    changed = [k for k in new if k in old and new[k] != old[k]]
    if added:
        lines.append("### 新增 token")
        lines += [f"- `{k}`: `{new[k]}`" for k in added]
    if changed:
        lines.append("### 改值 token")
        lines += [f"- `{k}`: `{old[k]}` → `{new[k]}`" for k in changed]
    if removed:
        lines.append("### 删除 token")
        lines += [f"- `{k}`（原 `{old[k]}`）" for k in removed]
    if not (added or changed or removed):
        lines.append("_无 token 变更_")
    return lines


def diff_classes(old: set[str], new: set[str]) -> list[str]:
    lines = []
    added = sorted(new - old)
    removed = sorted(old - new)
    if added:
        lines.append("### 新增组件 class")
        lines += [f"- `.{k}`" for k in added]
    if removed:
        lines.append("### 删除组件 class")
        lines += [f"- `.{k}`" for k in removed]
    if not (added or removed):
        lines.append("_无组件增删（class 级）_")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="对比两版设计系统源，输出变更清单")
    ap.add_argument("old", help="旧版文件路径（--git 时为该 ref 下的路径）")
    ap.add_argument("new", help="新版文件路径")
    ap.add_argument("--git", metavar="REF", help="把 old 当作 git ref 下的路径取出")
    ap.add_argument("--mode", choices=["tokens", "components", "auto"], default="auto")
    args = ap.parse_args()

    old_src = read_source(args.old, args.git)
    new_src = read_source(args.new, None)

    mode = args.mode
    if mode == "auto":
        mode = "components" if "components" in Path(args.new).name else "tokens"

    print(f"# 变更清单 ({mode})")
    print(f"- 旧: {('git ' + args.git + ':' if args.git else '') + args.old}")
    print(f"- 新: {args.new}\n")

    if mode == "components":
        for line in diff_classes(parse_classes(old_src), parse_classes(new_src)):
            print(line)
        print()
    # 组件文件里通常也含 token 引用变化，token 模式或 components 都额外跑一遍 var 对比
    for line in diff_vars(parse_vars(old_src), parse_vars(new_src)):
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
