# PBMP/1 M0 conformance reports

A PBMP implementation MAY publish a machine-readable conformance report after running the PBMP qualification suite.

The report is evidence about a particular implementation version tested against a particular suite revision. It is not a permanent certification and MUST NOT be reused for a different implementation version without rerunning qualification.

## Required fields

- `pbmp`: protocol major version; M0 reports use `1`.
- `profile`: conformance profile; currently `M0`.
- `implementation.name` and `implementation.version`: identity of the tested implementation.
- `suite.revision`: immutable PBMP suite revision, normally a Git commit SHA or release tag.
- `result`: overall `pass` or `fail`.
- `required_methods`: individual results for every PBMP/1 M0 required method.
- `capabilities_tested`: optional results for advertised optional capabilities that were actually exercised.

An overall `pass` requires every required M0 method to pass. Optional capabilities do not affect M0 conformance unless a future profile explicitly requires them.

Reports MUST NOT contain credentials, authentication tokens, private keys, raw configuration secrets, or private management endpoints.

## Local endpoint qualification runner

`tools/qualify_endpoint.py` exercises the PBMP/1 M0 required methods against the local Unix-domain JSONL transport profile and writes a conformance report.

Example:

```sh
python3 tools/qualify_endpoint.py \\
  --socket /run/example/pbmp.sock \\
  --implementation-name example-bot \\
  --implementation-version 0.1.0 \\
  --output pbmp-conformance-report.json
```

The runner opens a fresh local stream connection for each request, sends exactly one newline-terminated request, requires exactly one newline-terminated response, verifies the echoed request ID, and applies the required-method semantic checks. It exits non-zero if any required method fails.

The implementation name and version supplied to the runner identify the artifact being qualified; automated integrations SHOULD obtain these values from their build/release metadata rather than mutable runtime configuration.

## Pinning the qualification suite

Consumer repositories SHOULD pin PBMP qualification to an immutable PBMP Git commit or release tag. A moving branch such as `main` MUST NOT be used as the recorded `suite.revision` for a published qualification result.

A consumer CI job SHOULD check out the pinned PBMP revision, start the implementation under test with its local PBMP endpoint enabled, run `tools/qualify_endpoint.py`, and archive the resulting JSON report. Updating the pinned PBMP revision is an explicit requalification event.

This rule keeps historical PASS reports reproducible even as PBMP gains new optional capabilities, stronger tests, or future profiles.
