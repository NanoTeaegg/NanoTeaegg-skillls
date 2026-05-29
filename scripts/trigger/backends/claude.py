"""Claude Code trigger eval backend."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


RESULT_RE = re.compile(
    r"\[(?P<label>PASS|FAIL)\]\s+rate=(?P<hits>\d+)/(?P<runs>\d+)\s+expected=(?P<expected>True|False):\s+(?P<query>.+)"
)


def _base_result(item: dict) -> dict:
    return {
        "query": item["query"],
        "should_trigger": bool(item["should_trigger"]),
        "did_trigger": None,
        "passed": None,
        "evidence": "",
        "notes": "No parseable Claude trigger result was found for this query.",
    }


def _parse_results(text: str, eval_items: list[dict]) -> list[dict]:
    by_query = {item["query"]: _base_result(item) for item in eval_items}

    for line in text.splitlines():
        match = RESULT_RE.search(line.strip())
        if not match:
            continue
        query = match.group("query")
        if query not in by_query:
            continue
        hits = int(match.group("hits"))
        runs = int(match.group("runs"))
        expected = match.group("expected") == "True"
        did_trigger = hits > 0
        by_query[query].update({
            "should_trigger": expected,
            "did_trigger": did_trigger,
            "passed": did_trigger == expected,
            "evidence": f"Claude run_eval reported rate={hits}/{runs}.",
            "notes": "",
        })

    return [by_query[item["query"]] for item in eval_items]


def _summary(results: list[dict]) -> dict:
    known = [item for item in results if item["passed"] is not None]
    passed = sum(1 for item in known if item["passed"])
    should = [item for item in known if item["should_trigger"]]
    should_not = [item for item in known if not item["should_trigger"]]
    hit = sum(1 for item in should if item["did_trigger"])
    avoided = sum(1 for item in should_not if not item["did_trigger"])
    return {
        "total": len(results),
        "parsed": len(known),
        "passed": passed,
        "failed": len(known) - passed,
        "unknown": len(results) - len(known),
        "should_trigger_hit_rate": hit / len(should) if should else None,
        "should_not_trigger_avoid_rate": avoided / len(should_not) if should_not else None,
    }


def run(config: dict) -> dict:
    output_dir: Path = config["output_dir"]
    script = config["repo_root"] / "scripts" / "eval-claude-trigger-low-cost.sh"
    cmd = [
        str(script),
        str(config["eval_set_path"]),
        str(config["skill_path"]),
    ]
    if config.get("model"):
        cmd.append(str(config["model"]))

    completed = subprocess.run(
        cmd,
        cwd=config["repo_root"],
        text=True,
        capture_output=True,
        timeout=1800,
    )
    stdout_path = output_dir / "stdout.txt"
    stderr_path = output_dir / "stderr.txt"
    stdout_path.write_text(completed.stdout, encoding="utf-8")
    stderr_path.write_text(completed.stderr, encoding="utf-8")

    results = _parse_results(completed.stdout + "\n" + completed.stderr, config["eval_items"])
    report = {
        "platform": "claude",
        "skill_name": config["skill_name"],
        "mode": "runtime-trigger",
        "confidence": "high",
        "returncode": completed.returncode,
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
        "summary": _summary(results),
        "results": results,
    }
    if completed.returncode != 0:
        report["notes"] = "Claude trigger eval command failed; inspect stdout/stderr."
    return report
