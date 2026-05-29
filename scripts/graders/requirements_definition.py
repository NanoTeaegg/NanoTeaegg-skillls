"""Quality grader for the requirements-definition skill."""

from __future__ import annotations

from pathlib import Path


REQUIRED_PRD_TERMS = [
    "背景",
    "目标",
    "用户",
    "功能",
    "验收标准",
    "范围",
    "非目标",
    "开放问题",
    "变更记录",
]

TECH_DRIFT_TERMS = [
    "技术栈",
    "架构设计",
    "数据库表",
    "API 接口",
    "React",
    "Next.js",
    "Prisma",
    "Drizzle",
]


def find_prd(outputs_dir: Path, eval_id: int) -> Path | None:
    candidates = [
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "PRD.md",
        outputs_dir / f"eval-{eval_id}" / "docs" / "PRD.md",
        outputs_dir / str(eval_id) / "outputs" / "docs" / "PRD.md",
        outputs_dir / str(eval_id) / "docs" / "PRD.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/docs/PRD.md"))
    return matches[0] if matches else None


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    prd_path = find_prd(outputs_dir, eval_item["id"])
    checks = []

    if prd_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [
                {
                    "text": "writes docs/PRD.md",
                    "passed": False,
                    "evidence": "No docs/PRD.md found under the eval output directory.",
                }
            ],
        }

    text = prd_path.read_text(encoding="utf-8")
    checks.append({
        "text": "writes docs/PRD.md",
        "passed": True,
        "evidence": str(prd_path),
    })

    missing_terms = [term for term in REQUIRED_PRD_TERMS if term not in text]
    checks.append({
        "text": "includes core PRD sections and acceptance criteria",
        "passed": not missing_terms,
        "evidence": "Missing terms: " + ", ".join(missing_terms) if missing_terms else "All required terms found.",
    })

    drift_terms = [term for term in TECH_DRIFT_TERMS if term in text]
    checks.append({
        "text": "stays at requirements level without drifting into implementation",
        "passed": not drift_terms,
        "evidence": "Implementation terms found: " + ", ".join(drift_terms) if drift_terms else "No implementation drift terms found.",
    })

    return {
        "artifact": str(prd_path),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
