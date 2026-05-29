"""Cursor trigger eval backend.

Cursor skill invocation telemetry is not currently exposed in a
platform-neutral way in this repository. This backend records the limitation so
the shared trigger report format remains usable without overstating evidence.
"""

from __future__ import annotations


def run(config: dict) -> dict:
    results = []
    for item in config["eval_items"]:
        results.append({
            "query": item["query"],
            "should_trigger": bool(item["should_trigger"]),
            "did_trigger": None,
            "passed": None,
            "evidence": "No Cursor skill invocation trace is available to this low-cost backend.",
            "notes": "Run in Cursor with observable skill-use evidence, or add a Cursor backend that can read reliable invocation telemetry.",
        })

    return {
        "platform": "cursor",
        "skill_name": config["skill_name"],
        "mode": "limited-trigger-check",
        "confidence": "limited",
        "summary": {
            "total": len(results),
            "parsed": 0,
            "passed": 0,
            "failed": 0,
            "unknown": len(results),
            "should_trigger_hit_rate": None,
            "should_not_trigger_avoid_rate": None,
        },
        "results": results,
        "notes": "This is a structured limitation report, not proof of Cursor automatic trigger behavior.",
    }
