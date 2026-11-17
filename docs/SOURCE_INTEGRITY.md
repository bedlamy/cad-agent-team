# Source integrity and public redaction

- The v1 and v2 package manifests were checked against the extracted source files during archive preparation.
- The v2 helper and its test are preserved under `versioning/v2/`; the same files are retained in the v2 historical package.
- The v3 Coordinator prompt is preserved exactly as recovered; its SHA-256 matches the later reported hash.
- The v3 Analyst/Builder/Reviewer prompt texts were not available as files; only their reported SHA-256 values are retained in `docs/AGENTS_AND_PROMPTS.md`. Do not reconstruct them from hashes.
- The six Skills and references are preserved individually, with import ZIPs under `skills/v0.1/import_zips/`.
- Public source ZIPs are rebuilt from sanitized extracted files; see `source-archives/README.md`. They are not byte-identical to private source archives.
- The raw Coordinator execution export and customer CAD input were omitted from the public release. Aggregate statistics and behavior findings are preserved in the anonymized incident summary.
- The offline `versioning/v2/test_revision.py` was executed against the archived helper and passed. This validates the packaged helper's fake-document test only, not the installed helper or live FreeCAD runtime.
