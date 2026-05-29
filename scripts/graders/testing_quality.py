"""Quality grader for the testing-quality skill."""

from __future__ import annotations

from pathlib import Path


REQUIRED_TEST_PLAN_TERMS = [
    "TEST_PLAN",
    "验收标准映射",
    "自动化测试",
    "测试代码",
    "单元",
    "集成",
    "E2E",
    "质量门禁",
    "运行命令",
    "测试结果",
    "边界",
    "非目标",
    "开放问题",
    "变更记录",
]

BUSINESS_IMPL_DRIFT_TERMS = [
    "实现业务逻辑",
    "修改业务代码",
    "修复生产代码",
]

TEST_FILE_PATTERNS = [
    "**/*.spec.ts",
    "**/*.test.ts",
    "**/*Tests.swift",
    "**/*UITests.swift",
    "**/*Test.kt",
    "**/*Test.java",
    "**/test_*.py",
    "**/*_test.go",
]


def find_test_plan(outputs_dir: Path, eval_id: int) -> Path | None:
    candidates = [
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "TEST_PLAN.md",
        outputs_dir / f"eval-{eval_id}" / "docs" / "TEST_PLAN.md",
        outputs_dir / str(eval_id) / "outputs" / "docs" / "TEST_PLAN.md",
        outputs_dir / str(eval_id) / "docs" / "TEST_PLAN.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/docs/TEST_PLAN.md"))
    return matches[0] if matches else None


def find_generated_tests(eval_root: Path) -> list[Path]:
    matches: list[Path] = []
    for pattern in TEST_FILE_PATTERNS:
        matches.extend(eval_root.glob(pattern))
    return sorted({path for path in matches if path.is_file()})


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    test_plan_path = find_test_plan(outputs_dir, eval_item["id"])
    checks = []

    if test_plan_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [
                {
                    "text": "writes docs/TEST_PLAN.md",
                    "passed": False,
                    "evidence": "No docs/TEST_PLAN.md found under the eval output directory.",
                }
            ],
        }

    eval_root = test_plan_path.parents[1] if test_plan_path.parent.name == "docs" else test_plan_path.parent
    text = test_plan_path.read_text(encoding="utf-8")
    checks.append({
        "text": "writes docs/TEST_PLAN.md",
        "passed": True,
        "evidence": str(test_plan_path),
    })

    missing_terms = [term for term in REQUIRED_TEST_PLAN_TERMS if term not in text]
    checks.append({
        "text": "includes core testing-quality sections",
        "passed": not missing_terms,
        "evidence": "Missing terms: " + ", ".join(missing_terms) if missing_terms else "All required terms found.",
    })

    generated_tests = find_generated_tests(eval_root)
    checks.append({
        "text": "generates at least one automated test code artifact",
        "passed": bool(generated_tests),
        "evidence": "\n".join(str(path) for path in generated_tests) if generated_tests else "No test code files found.",
    })

    drift_terms = [term for term in BUSINESS_IMPL_DRIFT_TERMS if term in text]
    checks.append({
        "text": "states that it does not modify business implementation code",
        "passed": "不修改业务实现代码" in text or "不改业务实现代码" in text,
        "evidence": "Boundary found." if ("不修改业务实现代码" in text or "不改业务实现代码" in text) else "Missing explicit implementation boundary.",
    })
    checks.append({
        "text": "does not claim to implement production business logic",
        "passed": not drift_terms,
        "evidence": "Implementation drift terms found: " + ", ".join(drift_terms) if drift_terms else "No business implementation drift terms found.",
    })

    prompt = eval_item.get("prompt", "")
    if "iOS" in prompt or "Android" in prompt:
        mobile_terms = ["iOS", "Android", "XCUITest", "Espresso"]
        missing_mobile_terms = [term for term in mobile_terms if term not in text]
        checks.append({
            "text": "separates iOS and Android mobile testing strategy",
            "passed": not missing_mobile_terms,
            "evidence": "Missing mobile terms: " + ", ".join(missing_mobile_terms) if missing_mobile_terms else "Mobile strategy terms found.",
        })

    if "Playwright" in prompt or "Next.js" in prompt:
        web_terms = ["Web", "Playwright", "E2E"]
        missing_web_terms = [term for term in web_terms if term not in text]
        checks.append({
            "text": "includes Web/Playwright E2E strategy when requested",
            "passed": not missing_web_terms,
            "evidence": "Missing Web terms: " + ", ".join(missing_web_terms) if missing_web_terms else "Web strategy terms found.",
        })

    return {
        "artifact": str(test_plan_path),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
