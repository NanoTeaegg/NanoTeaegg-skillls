#!/usr/bin/env python3
"""lint_tokens.py — 让设计系统「可约束」。

扫描业务代码，查出绕过设计系统的写法:裸 hex 颜色、裸动效时长/缓动。让「业务代码
只能用 token / 组件」这条约束从一句话变成能跑、能进 CI 的检查。

设计系统自身的源（design-system/ 下的 tokens.css / components.css / preview.*）
是 token 的定义处，默认跳过。

用法:
    python3 lint_tokens.py src/                      # 扫描业务代码目录
    python3 lint_tokens.py src/ --check-px           # 额外查裸 px（默认关，噪声大）
    python3 lint_tokens.py src/ --exclude dist build # 追加排除目录

退出码非 0 表示发现违规，可接 CI。无第三方依赖。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

EXTS = {".css", ".scss", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".html", ".svelte"}
DEFAULT_EXCLUDE = {"node_modules", ".git", "dist", "build", "design-system", ".next", "out"}

HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
MS_RE = re.compile(r"(?<![\w-])\d+ms\b")
BEZIER_RE = re.compile(r"cubic-bezier\s*\(")
PX_RE = re.compile(r"(?<![\w-])\d+px\b")

# hex 出现在这些上下文里通常是注释/示例/sourcemap，放过以降噪
SKIP_LINE_HINTS = ("sourcemappingurl", "eslint", "// token", "/* token")


def iter_files(root: Path, exclude: set[str]):
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if any(part in exclude for part in p.parts):
            continue
        if p.suffix.lower() in EXTS:
            yield p


def scan_file(path: Path, check_px: bool) -> list[tuple[int, str, str]]:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if any(h in low for h in SKIP_LINE_HINTS):
            continue
        for m in HEX_RE.finditer(line):
            findings.append((i, "裸 hex 颜色，应用 var(--color-*)", m.group(0)))
        for m in MS_RE.finditer(line):
            findings.append((i, "裸动效时长，应用 var(--motion-duration-*)", m.group(0)))
        if BEZIER_RE.search(line):
            findings.append((i, "裸缓动曲线，应用 var(--ease-*)", "cubic-bezier(...)"))
        if check_px:
            for m in PX_RE.finditer(line):
                findings.append((i, "裸 px，建议用 var(--space-*)/--radius-*", m.group(0)))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="扫描业务代码里绕过设计系统的裸值")
    ap.add_argument("path", help="业务代码目录或文件")
    ap.add_argument("--check-px", action="store_true", help="额外检查裸 px（噪声大，默认关）")
    ap.add_argument("--exclude", nargs="*", default=[], help="追加排除目录名")
    args = ap.parse_args()

    root = Path(args.path)
    exclude = DEFAULT_EXCLUDE | set(args.exclude)
    files = [root] if root.is_file() else list(iter_files(root, exclude))

    total = 0
    for f in files:
        findings = scan_file(f, args.check_px)
        if findings:
            print(f"\n{f}")
            for line_no, reason, snippet in findings:
                print(f"  {f}:{line_no}  {reason}  →  {snippet}")
            total += len(findings)

    print(f"\n共 {total} 处可能绕过设计系统的写法。")
    if total:
        print("修复方向:改用 tokens.css 的 var(--*) 或 components.css 的 .ds-* class。")
        return 1
    print("✓ 未发现裸值，业务代码符合设计系统约束。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
