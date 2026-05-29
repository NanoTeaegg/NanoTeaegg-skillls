#!/usr/bin/env python3
"""Platform-neutral quality checks for skill eval outputs.

This script does not run Claude, Cursor, or Codex. It grades artifacts already
produced by the current agent, so the same checks can be reused across agents.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


def grader_module_name(skill_name: str) -> str:
    return skill_name.replace("-", "_")


def load_grader(skill_name: str):
    module_name = grader_module_name(skill_name)
    grader_path = Path(__file__).resolve().parent / "graders" / f"{module_name}.py"
    if not grader_path.exists():
        raise SystemExit(
            f"No quality grader found for skill `{skill_name}`.\n"
            f"Expected: {grader_path}\n"
            "Add a grader module with a grade(eval_item, outputs_dir) function."
        )

    spec = importlib.util.spec_from_file_location(f"skill_quality_grader_{module_name}", grader_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load grader module: {grader_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "grade"):
        raise SystemExit(f"Grader module {grader_path} must define grade(eval_item, outputs_dir).")

    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade platform-neutral skill eval outputs.")
    parser.add_argument("--evals", required=True, help="Path to evals.json")
    parser.add_argument("--outputs-dir", required=True, help="Directory containing eval output folders")
    parser.add_argument("--output", default=None, help="Optional path for JSON grading results")
    args = parser.parse_args()

    evals_path = Path(args.evals)
    outputs_dir = Path(args.outputs_dir)
    eval_spec = json.loads(evals_path.read_text(encoding="utf-8"))
    skill_name = eval_spec["skill_name"]
    grader = load_grader(skill_name)

    results = []
    for item in eval_spec["evals"]:
        grading = grader.grade(item, outputs_dir)
        results.append({
            "eval_id": item["id"],
            "prompt": item["prompt"],
            "expected_output": item["expected_output"],
            **grading,
        })

    passed = sum(1 for result in results if result["passed"])
    report = {
        "skill_name": skill_name,
        "summary": {
            "passed": passed,
            "failed": len(results) - passed,
            "total": len(results),
        },
        "results": results,
    }

    output_text = json.dumps(report, ensure_ascii=False, indent=2)
    print(output_text)

    if args.output:
        Path(args.output).write_text(output_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
