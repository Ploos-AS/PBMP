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
