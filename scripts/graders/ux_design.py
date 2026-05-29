"""Quality grader for the ux-design skill."""

from __future__ import annotations

from pathlib import Path


REQUIRED_UX_TERMS = [
    "用户",
    "流程",
    "信息架构",
    "状态",
    "验收标准",
    "边界",
    "非目标",
    "开放问题",
    "变更记录",
]

# Terms that indicate the doc has drifted into visual design territory
VISUAL_DRIFT_TERMS = [
    "主色调",
    "字体大小",
    "font-size",
    "颜色方案",
    "color:",
    "border-radius",
    "Figma",
    "设计稿",
    "视觉规范",
]

# Terms that indicate the doc has drifted into implementation territory
IMPL_DRIFT_TERMS = [
    "React",
    "Vue",
    "Next.js",
    "Prisma",
    "Drizzle",
    "数据库表",
    "CREATE TABLE",
    "技术栈",
    "组件库",
    "useState",
    "useEffect",
]


def find_ux_doc(outputs_dir: Path, eval_id: int) -> Path | None:
    candidates = [
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "UX.md",
        outputs_dir / f"eval-{eval_id}" / "docs" / "UX.md",
        outputs_dir / str(eval_id) / "outputs" / "docs" / "UX.md",
        outputs_dir / str(eval_id) / "docs" / "UX.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/docs/UX.md"))
    return matches[0] if matches else None


def _content_section(text: str) -> str:
    """Return only the main content portion of the UX doc, excluding the
    '边界与非目标' section (and everything after it).  Terms that appear in
    the boundary section are expected — they describe what we deliberately
    omit — so we must not flag them as drift."""
    boundary_markers = ["## 6.", "## 6 ", "边界与非目标", "边界：", "边界:"]
    for marker in boundary_markers:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx]
    return text


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    ux_path = find_ux_doc(outputs_dir, eval_item["id"])
    checks = []

    if ux_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [
                {
                    "text": "writes docs/UX.md",
                    "passed": False,
                    "evidence": "No docs/UX.md found under the eval output directory.",
                }
            ],
        }

    text = ux_path.read_text(encoding="utf-8")
    content = _content_section(text)

    checks.append({
        "text": "writes docs/UX.md",
        "passed": True,
        "evidence": str(ux_path),
    })

    missing_terms = [term for term in REQUIRED_UX_TERMS if term not in text]
    checks.append({
        "text": "includes core UX sections (flows, IA, states, acceptance criteria, boundaries)",
        "passed": not missing_terms,
        "evidence": "Missing terms: " + ", ".join(missing_terms) if missing_terms else "All required terms found.",
    })

    # Only check the content sections — the boundary section legitimately names
    # these terms to explain what the skill does NOT cover.
    visual_drift = [term for term in VISUAL_DRIFT_TERMS if term in content]
    checks.append({
        "text": "stays at interaction level without drifting into visual/brand design",
        "passed": not visual_drift,
        "evidence": "Visual design terms found: " + ", ".join(visual_drift) if visual_drift else "No visual design drift terms found.",
    })

    impl_drift = [term for term in IMPL_DRIFT_TERMS if term in content]
    checks.append({
        "text": "stays at interaction level without drifting into implementation details",
        "passed": not impl_drift,
        "evidence": "Implementation terms found: " + ", ".join(impl_drift) if impl_drift else "No implementation drift terms found.",
    })

    # Check for acceptance criteria — at least one concrete verifiable statement
    has_acceptance_criteria = "验收标准" in text and (
        "用户点击" in text or "点击" in text or "输入" in text or "提交" in text
    )
    checks.append({
        "text": "includes at least one concrete verifiable acceptance criterion",
        "passed": has_acceptance_criteria,
        "evidence": "Found concrete acceptance criteria." if has_acceptance_criteria else "No concrete acceptance criteria found (needs specific user action + system response descriptions).",
    })

    return {
        "artifact": str(ux_path),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
