"""Quality grader for the webui-design-system skill (Web-only design system).

校验四类事实源是否齐备且符合新模型:
- docs/UI_SPEC.md      精简契约（含基础 UI 约定、组件库、动效、变更记录…）
- design-system/tokens.css       值源（含 motion token）
- design-system/components.css   组件库（.ds-* class）
- design-system/preview.html     文档站（引用 tokens.css/components.css，用外壳渲染真实组件）
"""

from __future__ import annotations

from pathlib import Path


REQUIRED_UI_TERMS = [
    "工程映射",
    "Design Tokens",
    "颜色",
    "字体",
    "间距",
    "圆角",
    "动效",
    "基础 UI 约定",
    "组件",
    "状态",
    "AI 落地约束",
    "文档站",
    "可访问性",
    "变更记录",
]

# 只做 Web：出现这些原生平台词视为跑偏
NATIVE_DRIFT_TERMS = [
    "SwiftUI", "UIKit", "Navigation Bar", "Tab Bar", "VoiceOver",
    "Material 3", "Theme.kt", "Snackbar", "FAB", "Jetpack Compose", "Kotlin",
]

IMPLEMENTATION_DRIFT_TERMS = [
    "useState", "useEffect", "npm install", "CREATE TABLE", "ALTER TABLE",
    "Prisma", "Drizzle", "axios",
]

UX_REWRITE_TERMS = ["用户流程图", "信息架构图", "用户旅程"]


def _find(outputs_dir: Path, eval_id: int, rel_candidates: list[str], glob: str) -> Path | None:
    for rel in rel_candidates:
        p = outputs_dir / f"eval-{eval_id}" / "outputs" / rel
        if p.exists():
            return p
    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/{glob}"))
    return matches[0] if matches else None


def find_ui_spec(outputs_dir: Path, eval_id: int) -> Path | None:
    return _find(
        outputs_dir, eval_id,
        ["docs/UI_SPEC.md", "docs/UI_SPEC.web.md", "UI_SPEC.md"],
        "docs/UI_SPEC*.md",
    )


def find_tokens(outputs_dir: Path, eval_id: int) -> Path | None:
    return _find(outputs_dir, eval_id, ["design-system/tokens.css"], "design-system/**/tokens.css")


def find_components(outputs_dir: Path, eval_id: int) -> Path | None:
    return _find(outputs_dir, eval_id, ["design-system/components.css"], "design-system/**/components.css")


def find_preview(outputs_dir: Path, eval_id: int) -> Path | None:
    return _find(outputs_dir, eval_id, ["design-system/preview.html"], "design-system/**/preview.html")


def _content_section(text: str) -> str:
    """Drop boundary / non-goal sections where adjacent-domain terms are expected."""
    for marker in ["## 10.", "非目标与边界", "边界与非目标", "## 边界"]:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx]
    return text


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    eval_id = eval_item["id"]
    ui_path = find_ui_spec(outputs_dir, eval_id)
    tokens_path = find_tokens(outputs_dir, eval_id)
    comp_path = find_components(outputs_dir, eval_id)
    preview_path = find_preview(outputs_dir, eval_id)
    checks = []

    if ui_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [{"text": "writes docs/UI_SPEC.md", "passed": False,
                        "evidence": "No docs/UI_SPEC.md found under the eval output directory."}],
        }

    text = ui_path.read_text(encoding="utf-8")
    content = _content_section(text)

    checks.append({"text": "writes docs/UI_SPEC.md", "passed": True, "evidence": str(ui_path)})

    # tokens.css + motion token
    tokens_ok = tokens_path is not None
    tokens_ev = str(tokens_path) if tokens_path else "No design-system/tokens.css found."
    checks.append({"text": "writes design-system/tokens.css", "passed": tokens_ok, "evidence": tokens_ev})
    if tokens_path:
        tcss = tokens_path.read_text(encoding="utf-8", errors="replace")
        base_ok = all(t in tcss for t in ["--color", "--space", "--radius"])
        motion_ok = ("--motion-duration" in tcss) or ("--ease" in tcss)
        checks.append({"text": "tokens.css has color/space/radius + motion tokens",
                       "passed": base_ok and motion_ok,
                       "evidence": ("base=" + str(base_ok) + ", motion=" + str(motion_ok))})

    # components.css with .ds-* classes
    comp_ok = comp_path is not None and ".ds-" in comp_path.read_text(encoding="utf-8", errors="replace")
    checks.append({"text": "writes design-system/components.css with .ds-* classes",
                   "passed": comp_ok,
                   "evidence": str(comp_path) if comp_path else "No design-system/components.css found."})

    # preview references tokens.css + components.css and uses the shell (renders real components)
    if preview_path is not None:
        ptext = preview_path.read_text(encoding="utf-8", errors="replace")
        refs_ok = ("tokens.css" in ptext) and ("components.css" in ptext)
        shell_ok = ("ph-manifest" in ptext) or ("ph-app" in ptext) or ("preview.js" in ptext)
        real_ok = ".ds-" in ptext  # 渲染真实组件 class，而不是重画
        checks.append({"text": "preview.html references tokens.css + components.css", "passed": refs_ok,
                       "evidence": "refs tokens.css & components.css" if refs_ok else "missing source links"})
        checks.append({"text": "preview.html uses the doc-site shell and renders real components",
                       "passed": shell_ok and real_ok,
                       "evidence": ("shell=" + str(shell_ok) + ", real .ds-*=" + str(real_ok))})
    else:
        checks.append({"text": "writes design-system/preview.html", "passed": False,
                       "evidence": "No design-system/preview.html found."})

    # UI_SPEC required sections
    missing = [t for t in REQUIRED_UI_TERMS if t not in text]
    checks.append({"text": "UI_SPEC includes core sections (tokens/基础约定/组件/动效/变更记录…)",
                   "passed": not missing,
                   "evidence": ("Missing: " + ", ".join(missing)) if missing else "All required terms found."})

    # web vocabulary present
    web_terms = [t for t in ["Web", "CSS", "hover", "focus", "响应式"] if t in text]
    checks.append({"text": "covers Web platform vocabulary", "passed": len(web_terms) >= 3,
                   "evidence": "Found: " + ", ".join(web_terms)})

    # component + state coverage
    comp_terms = [t for t in ["按钮", "Button", "表单", "Field", "Tag", "卡片", "弹窗", "Toast"] if t in text]
    checks.append({"text": "covers common component specifications", "passed": len(comp_terms) >= 3,
                   "evidence": "Found: " + ", ".join(comp_terms)})
    state_terms = [t for t in ["hover", "focus", "disabled", "loading", "空态", "错误"] if t in text]
    checks.append({"text": "covers visual states", "passed": len(state_terms) >= 3,
                   "evidence": "Found: " + ", ".join(state_terms)})

    # no native drift
    native = [t for t in NATIVE_DRIFT_TERMS if t in content]
    checks.append({"text": "stays Web-only (no native iOS/Android rules)", "passed": not native,
                   "evidence": ("Native terms: " + ", ".join(native)) if native else "No native drift."})

    impl = [t for t in IMPLEMENTATION_DRIFT_TERMS if t in content]
    checks.append({"text": "does not drift into frontend code / DB / ORM", "passed": not impl,
                   "evidence": ("Found: " + ", ".join(impl)) if impl else "No implementation drift."})

    uxd = [t for t in UX_REWRITE_TERMS if t in content]
    checks.append({"text": "does not rewrite UX flows", "passed": not uxd,
                   "evidence": ("Found: " + ", ".join(uxd)) if uxd else "No UX rewrite drift."})

    return {
        "artifact": str(ui_path),
        "passed": all(c["passed"] for c in checks),
        "checks": checks,
    }
