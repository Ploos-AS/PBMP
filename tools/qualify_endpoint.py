#!/usr/bin/env python3
"""Run PBMP/1 M0 qualification against a local Unix-domain JSONL endpoint."""

import argparse
import json
import pathlib
import socket
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from validate_vectors import validate_envelope, validate_required_result

METHODS = ("pbmp.info", "capabilities.list", "bot.info", "networks.list")


def request(sock_path, method, ident):
    message = {"pbmp": 1, "type": "request", "id": ident, "method": method, "params": {}}
    wire = (json.dumps(message, separators=(",", ":")) + "\n").encode("utf-8")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(5.0)
        sock.connect(sock_path)
        sock.sendall(wire)
        sock.shutdown(socket.SHUT_WR)
        data = b""
        while b"\n" not in data:
            chunk = sock.recv(16384 - len(data))
            if not chunk:
                break
            data += chunk
            if len(data) >= 16384:
                raise ValueError("response exceeds local transport limit")
    if not data.endswith(b"\n") or data.count(b"\n") != 1:
        raise ValueError("endpoint must return exactly one newline-terminated response")
    obj = json.loads(data.decode("utf-8"))
    validate_envelope(obj)
    if obj["type"] != "response" or obj["id"] != ident:
        raise ValueError("response type/id mismatch")
    if not obj["ok"]:
        raise ValueError("required method returned error")
    validate_required_result(method, obj["result"])
    return obj["result"]


def git_revision(root):
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return "unknown"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", required=True, help="Unix-domain socket path")
    parser.add_argument("--implementation-name", required=True)
    parser.add_argument("--implementation-version", required=True)
    parser.add_argument("--output", default="pbmp-conformance-report.json")
    args = parser.parse_args()

    results = {}
    failures = []
    for index, method in enumerate(METHODS, 1):
        try:
            request(args.socket, method, f"pbmp-m0-{index}")
            results[method] = "pass"
        except Exception as exc:
            results[method] = "fail"
            failures.append(f"{method}: {exc}")

    root = pathlib.Path(__file__).resolve().parents[1]
    report = {
        "pbmp": 1,
        "profile": "M0",
        "implementation": {"name": args.implementation_name, "version": args.implementation_version},
        "suite": {"revision": git_revision(root)},
        "result": "pass" if not failures else "fail",
        "required_methods": results,
        "capabilities_tested": {}
    }
    pathlib.Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for failure in failures:
        print("FAIL:", failure, file=sys.stderr)
    print(f"Wrote {args.output}: {report['result'].upper()}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
