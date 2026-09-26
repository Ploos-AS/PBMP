# PBMP/1 M0 consumer qualification

This document is a template for projects implementing PBMP/1.

## CI contract

1. Pin this PBMP repository to an immutable commit SHA or release tag.
2. Build and start the implementation under test.
3. Enable its local Unix-domain PBMP JSONL endpoint.
4. Run the pinned `tools/qualify_endpoint.py` against that socket.
5. Archive `pbmp-conformance-report.json` as a CI artifact.
6. Treat a non-zero runner exit status as qualification failure.

Example command:

```sh
python3 PBMP/tools/qualify_endpoint.py \
  --socket "$PBMP_SOCKET" \
  --implementation-name "$IMPLEMENTATION_NAME" \
  --implementation-version "$IMPLEMENTATION_VERSION" \
  --output pbmp-conformance-report.json
```

The implementation MUST remain fully functional as its primary application when PBMP is disabled or unavailable. PBMP qualification proves management-protocol interoperability; it does not make PBMP a runtime dependency.
