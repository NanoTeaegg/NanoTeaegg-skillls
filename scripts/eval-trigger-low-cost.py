#!/usr/bin/env python3
"""Cross-platform low-cost skill trigger eval entrypoint.

This script provides one command shape for trigger evals, while each platform
backend records its own confidence level. Claude Code can run a real-ish
description trigger eval; Cursor and Codex currently report limited support
unless a reliable invocation signal is available in that environment.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def read_skill_name(skill_path: Path) -> str:
    text = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"')
    return skill_path.name


def default_eval_set(skill_path: Path) -> Path:
    relative = skill_path.resolve().relative_to(REPO_ROOT / "skills")
    return REPO_ROOT / "evals" / relative / "trigger-eval.json"


def default_output_dir(skill_name: str, platform: str) -> Path:
    return REPO_ROOT / "workspaces" / skill_name / platform / "trigger-eval"


def load_backend(platform: str):
    backend_path = REPO_ROOT / "scripts" / "trigger" / "backends" / f"{platform}.py"
    if not backend_path.exists():
        raise SystemExit(f"No trigger backend for platform `{platform}` at {backend_path}")

    spec = importlib.util.spec_from_file_location(f"trigger_backend_{platform}", backend_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Unable to load trigger backend: {backend_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "run"):
        raise SystemExit(f"Trigger backend {backend_path} must define run(config).")
    return module


def load_eval_set(eval_set_path: Path) -> list[dict]:
    data = json.loads(eval_set_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit("trigger-eval.json must be a JSON array of {query, should_trigger} items.")
    for item in data:
        if "query" not in item or "should_trigger" not in item:
            raise SystemExit("Each trigger eval item must include query and should_trigger.")
    return data


def run_platform(platform: str, args: argparse.Namespace, eval_items: list[dict], skill_name: str) -> dict:
    output_dir = Path(args.outputs_dir).resolve() if args.outputs_dir else default_output_dir(skill_name, platform)
    if args.platform == "all" and args.outputs_dir:
        output_dir = output_dir / platform
    output_dir.mkdir(parents=True, exist_ok=True)

    backend = load_backend(platform)
    config = {
        "repo_root": REPO_ROOT,
        "platform": platform,
        "skill_name": skill_name,
        "skill_path": Path(args.skill_path).resolve(),
        "eval_set_path": Path(args.eval_set).resolve(),
        "eval_items": eval_items,
        "output_dir": output_dir,
        "model": args.model,
    }
    report = backend.run(config)
    report_path = output_dir / "results.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "platform": platform,
        "results_path": str(report_path),
        "summary": report.get("summary", {}),
        "mode": report.get("mode"),
        "confidence": report.get("confidence"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run low-cost skill trigger evals.")
    parser.add_argument("--platform", required=True, choices=["claude", "codex", "cursor", "all"])
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--eval-set", default=None, help="Path to trigger-eval.json")
    parser.add_argument("--outputs-dir", default=None, help="Optional output directory")
    parser.add_argument("--model", default=None, help="Optional platform model override")
    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()
    if not (skill_path / "SKILL.md").exists():
        raise SystemExit(f"Skill path must contain SKILL.md: {skill_path}")

    if args.eval_set is None:
        args.eval_set = str(default_eval_set(skill_path))
    eval_set_path = Path(args.eval_set).resolve()
    if not eval_set_path.exists():
        raise SystemExit(f"Trigger eval set not found: {eval_set_path}")

    skill_name = read_skill_name(skill_path)
    eval_items = load_eval_set(eval_set_path)
    platforms = ["claude", "codex", "cursor"] if args.platform == "all" else [args.platform]
    reports = [run_platform(platform, args, eval_items, skill_name) for platform in platforms]

    output = {
        "skill_name": skill_name,
        "skill_path": str(skill_path),
        "eval_set": str(eval_set_path),
        "reports": reports,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
