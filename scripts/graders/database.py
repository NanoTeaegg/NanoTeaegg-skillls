"""Quality grader for the database skill.

The database skill owns the data-persistence layer: database product selection,
table/field/relationship/index/constraint design, and change (migration) rules.
It must NOT drift into ORM/framework/language selection, app architecture, or
concrete business/query code — those belong to dev-kickoff or the build phase.
"""

from __future__ import annotations

from pathlib import Path


REQUIRED_SCHEMA_TERMS = [
    "数据库选型",
    "数据模型",
    "字段",
    "主键",
    "索引",
    "约束",
    "外键",
    "迁移",
    "回滚",
    "命名",
    "开放问题",
    "变更",
]

# An "invariant / acceptance criterion" for a table is the schema-level analog of
# a PRD acceptance criterion. We accept any of these signals as evidence that the
# doc pinned down checkable constraints rather than just listing columns.
INVARIANT_SIGNALS = ["不变量", "唯一", "非空", "CHECK", "级联"]

# Drift = doing another skill's job. ORM/framework/language *selection* and
# concrete app code do not belong here. (Database product selection DOES, so
# Postgres/MySQL/Mongo are not drift terms.)
ORM_FRAMEWORK_DRIFT_TERMS = [
    "Prisma",
    "Drizzle",
    "SQLAlchemy",
    "Next.js",
    "React",
    "Vue",
    "SwiftUI",
]

CODE_DRIFT_TERMS = [
    "```tsx",
    "```jsx",
    "```ts\n",
    "```js\n",
    "```python",
    "```go\n",
    "function ",
    "class ",
]


def find_schema(outputs_dir: Path, eval_id: int) -> Path | None:
    candidates = [
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "SCHEMA.md",
        outputs_dir / f"eval-{eval_id}" / "docs" / "SCHEMA.md",
        outputs_dir / str(eval_id) / "outputs" / "docs" / "SCHEMA.md",
        outputs_dir / str(eval_id) / "docs" / "SCHEMA.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/docs/SCHEMA.md"))
    return matches[0] if matches else None


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    schema_path = find_schema(outputs_dir, eval_item["id"])
    checks = []

    if schema_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [
                {
                    "text": "writes docs/SCHEMA.md",
                    "passed": False,
                    "evidence": "No docs/SCHEMA.md found under the eval output directory.",
                }
            ],
        }

    text = schema_path.read_text(encoding="utf-8")
    checks.append({
        "text": "writes docs/SCHEMA.md",
        "passed": True,
        "evidence": str(schema_path),
    })

    missing_terms = [term for term in REQUIRED_SCHEMA_TERMS if term not in text]
    checks.append({
        "text": "includes core schema sections (selection, model, fields, keys, indexes, constraints, migration/change)",
        "passed": not missing_terms,
        "evidence": "Missing terms: " + ", ".join(missing_terms) if missing_terms else "All required terms found.",
    })

    found_invariants = [sig for sig in INVARIANT_SIGNALS if sig in text]
    checks.append({
        "text": "pins down checkable table constraints / invariants (schema-level acceptance criteria)",
        "passed": bool(found_invariants),
        "evidence": "Invariant signals found: " + ", ".join(found_invariants) if found_invariants else "No constraint/invariant signals (唯一/非空/CHECK/级联/不变量) found.",
    })

    orm_drift = [term for term in ORM_FRAMEWORK_DRIFT_TERMS if term in text]
    checks.append({
        "text": "does not drift into ORM/framework/language selection (dev-kickoff's job)",
        "passed": not orm_drift,
        "evidence": "ORM/framework selection terms found: " + ", ".join(orm_drift) if orm_drift else "No ORM/framework selection drift terms found.",
    })

    code_drift = [term for term in CODE_DRIFT_TERMS if term in text]
    checks.append({
        "text": "does not include concrete business/query code implementation",
        "passed": not code_drift,
        "evidence": "Code implementation terms found: " + ", ".join(code_drift) if code_drift else "No business-code drift terms found.",
    })

    return {
        "artifact": str(schema_path),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
