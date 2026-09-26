#!/usr/bin/env python3
"""PBMP/1 M0 conformance-vector validator."""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
VECTORS = ROOT / "test-vectors"

REQUIRED_METHODS = {"pbmp.info", "capabilities.list", "bot.info", "networks.list"}


def load_one(path):
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    if len(lines) != 1:
        raise ValueError("vector must contain exactly one JSON line")
    return json.loads(lines[0])


def validate_envelope(obj):
    if not isinstance(obj, dict):
        raise ValueError("message must be an object")
    if obj.get("pbmp") != 1:
        raise ValueError("pbmp must equal 1")
    typ = obj.get("type")
    if typ not in {"request", "response", "event"}:
        raise ValueError("invalid or missing type")
    if typ in {"request", "response"} and not isinstance(obj.get("id"), str):
        raise ValueError("request/response id must be a string")
    if typ == "request":
        if not isinstance(obj.get("method"), str) or not obj["method"]:
            raise ValueError("request method must be a non-empty string")
        if "params" in obj and not isinstance(obj["params"], dict):
            raise ValueError("request params must be an object")
    elif typ == "response":
        if not isinstance(obj.get("ok"), bool):
            raise ValueError("response ok must be boolean")
        if obj["ok"] and "result" not in obj:
            raise ValueError("successful response must contain result")
        if not obj["ok"] and not isinstance(obj.get("error"), dict):
            raise ValueError("failed response must contain error object")
    else:
        if not isinstance(obj.get("event"), str) or not obj["event"]:
            raise ValueError("event name must be a non-empty string")


def main():
    failures = []

    for path in sorted((VECTORS / "valid").glob("*.jsonl")):
        try:
            validate_envelope(load_one(path))
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: expected valid: {exc}")

    for path in sorted((VECTORS / "invalid").glob("*.jsonl")):
        try:
            validate_envelope(load_one(path))
        except Exception:
            continue
        failures.append(f"{path.relative_to(ROOT)}: expected rejection")

    methods = set()
    for path in sorted((VECTORS / "methods").glob("*.request.jsonl")):
        try:
            obj = load_one(path)
            validate_envelope(obj)
            methods.add(obj["method"])
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: invalid method request: {exc}")

    missing = REQUIRED_METHODS - methods
    if missing:
        failures.append("missing required method vectors: " + ", ".join(sorted(missing)))

    for path in sorted((VECTORS / "methods").glob("*.response.jsonl")):
        try:
            validate_envelope(load_one(path))
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: invalid method response: {exc}")

    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1

    print("PASS: PBMP/1 M0 conformance vectors")
    return 0


if __name__ == "__main__":
    sys.exit(main())
