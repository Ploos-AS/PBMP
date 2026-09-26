#!/usr/bin/env python3
"""Minimal PBMP/1 M0 Unix-socket endpoint for conformance self-tests."""

import argparse
import json
import os
import socket

RESULTS = {
    "pbmp.info": {
        "version": 1,
        "implementation": {"name": "pbmp-reference-endpoint", "version": "M0"}
    },
    "capabilities.list": {"capabilities": []},
    "bot.info": {
        "bot": {
            "id": "reference",
            "implementation": {"name": "pbmp-reference-endpoint", "version": "M0"},
            "state": "running"
        }
    },
    "networks.list": {"networks": []}
}


def handle(conn):
    data = b""
    while b"\n" not in data and len(data) < 4096:
        chunk = conn.recv(4096 - len(data))
        if not chunk:
            break
        data += chunk
    try:
        if not data.endswith(b"\n") or data.count(b"\n") != 1:
            raise ValueError("invalid framing")
        req = json.loads(data.decode("utf-8"))
        method = req.get("method")
        if req.get("pbmp") != 1 or req.get("type") != "request" or not isinstance(req.get("id"), str):
            raise ValueError("invalid request")
        if method not in RESULTS:
            response = {
                "pbmp": 1, "type": "response", "id": req["id"], "ok": False,
                "error": {"code": "not_supported", "message": "method not supported"}
            }
        else:
            response = {
                "pbmp": 1, "type": "response", "id": req["id"], "ok": True,
                "result": RESULTS[method]
            }
    except Exception as exc:
        response = {
            "pbmp": 1, "type": "response", "id": "invalid", "ok": False,
            "error": {"code": "invalid_request", "message": str(exc)}
        }
    conn.sendall((json.dumps(response, separators=(",", ":")) + "\n").encode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--socket", required=True)
    parser.add_argument("--requests", type=int, default=4)
    args = parser.parse_args()

    try:
        os.unlink(args.socket)
    except FileNotFoundError:
        pass

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(args.socket)
        server.listen()
        for _ in range(args.requests):
            conn, _ = server.accept()
            with conn:
                handle(conn)

    os.unlink(args.socket)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
