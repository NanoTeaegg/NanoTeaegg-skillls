"""Quality grader for the dev-kickoff skill."""

from __future__ import annotations

from pathlib import Path


REQUIRED_TECH_TERMS = [
    "TECH_DESIGN",
    "Android",
    "iOS",
    "Web",
    "Windows",
    "技术栈",
    "架构",
    "模块",
    "关键技术决策",
    "风险",
    "边界",
    "非目标",
    "开放问题",
    "变更记录",
]

DATABASE_DETAIL_TERMS = [
    "CREATE TABLE",
    "ALTER TABLE",
    "字段类型",
    "索引名",
]

CODE_DRIFT_TERMS = [
    "```tsx",
    "```jsx",
    "```ts",
    "```js",
    "```python",
    "function ",
    "class ",
]


def find_tech_design(outputs_dir: Path, eval_id: int) -> Path | None:
    candidates = [
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "TECH_DESIGN.md",
        outputs_dir / f"eval-{eval_id}" / "docs" / "TECH_DESIGN.md",
        outputs_dir / str(eval_id) / "outputs" / "docs" / "TECH_DESIGN.md",
        outputs_dir / str(eval_id) / "docs" / "TECH_DESIGN.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/docs/TECH_DESIGN.md"))
    return matches[0] if matches else None


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    tech_path = find_tech_design(outputs_dir, eval_item["id"])
    checks = []

    if tech_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [
                {
                    "text": "writes docs/TECH_DESIGN.md",
                    "passed": False,
                    "evidence": "No docs/TECH_DESIGN.md found under the eval output directory.",
                }
            ],
        }

    text = tech_path.read_text(encoding="utf-8")
    checks.append({
        "text": "writes docs/TECH_DESIGN.md",
        "passed": True,
        "evidence": str(tech_path),
    })

    missing_terms = [term for term in REQUIRED_TECH_TERMS if term not in text]
    checks.append({
        "text": "includes core technical-design sections",
        "passed": not missing_terms,
        "evidence": "Missing terms: " + ", ".join(missing_terms) if missing_terms else "All required terms found.",
    })

    platform_mentions = {
        "Android app": "Android" in text and ("app" in text or "应用" in text),
        "iOS app": "iOS" in text and ("app" in text or "应用" in text),
        "Web": "Web" in text or "网页" in text,
        "Windows 应用": "Windows" in text and "应用" in text,
    }
    missing_platforms = [name for name, found in platform_mentions.items() if not found]
    checks.append({
        "text": "separates Android, iOS, Web, and Windows platform decisions",
        "passed": not missing_platforms,
        "evidence": "Missing platform coverage: " + ", ".join(missing_platforms) if missing_platforms else "All target platform sections found.",
    })

    database_drift = [term for term in DATABASE_DETAIL_TERMS if term in text]
    checks.append({
        "text": "does not drift into database table/field/index design",
        "passed": not database_drift,
        "evidence": "Database detail terms found: " + ", ".join(database_drift) if database_drift else "No database-detail drift terms found.",
    })

    code_drift = [term for term in CODE_DRIFT_TERMS if term in text]
    checks.append({
        "text": "does not include concrete business-code implementation",
        "passed": not code_drift,
        "evidence": "Code implementation terms found: " + ", ".join(code_drift) if code_drift else "No code implementation drift terms found.",
    })

    return {
        "artifact": str(tech_path),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
