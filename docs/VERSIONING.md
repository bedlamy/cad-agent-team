# CAD project versioning

## Intended structure

```text
<CAD_WORKSPACE>/<project-slug>/
  project_state.json
  revision_log.json
  revisions/
    <UTC>-<id>-before.FCStd
    <UTC>-<id>-after.FCStd
```

`project_state.json` stores current project/document identity, last confirmed revision, parameters, accepted facts/decisions, constraints, hypotheses, open questions and next step. `revision_log.json` records revision phase, label, document, path, timestamp, SHA-256, object count and fingerprint.

## Helper source

Exact v2 package source is in `versioning/v2/cad_revision.py`; test is `versioning/v2/test_revision.py`. Preferred install path reported on VM: `<CAD_AGENT_HOME>/bin/cad_revision.py`.

Known helper functions from v2 prompt examples: `checkpoint()`, `read_project_state()`, `update_project_state()`, `quick_status()`. Confirm the live helper source/API before relying on exact signatures.

## Safety contract

- before checkpoint must succeed before mutation;
- after checkpoint must succeed before next mutation;
- never delete old revisions;
- do not change active document FileName or close/reopen the working document as a routine check;
- preserve original STEP/FCStd sources;
- revision snapshot is not proof of geometric correctness;
- helper relies on agents following the workflow; it is not a technical mutation gateway.

## Reported tests

### `team-v2-scratch`

Reported before/after FCStd snapshots passed ZIP integrity and SHA-256 checks; `doc.FileName` did not change; `project_state.json` updated.

### `team-v2-final-acceptance`

Reported test: source model 10×20×30 mm, volume 6000; modified model 12×20×35 mm, volume 8400; Shape valid; four revisions; acceptance report created.

### XYZ Calibration Cube

Historical handoff 16 Nov said the cube could not be written to `<CAD_WORKSPACE>` and files remained in `<TEMP_DIR>`. The later 17 Nov Coordinator export lists `/projects/xyz-calibration-cube-test/revision_log.json`, `project_state.json`, and four revision files. This indicates progress after the older handoff, but the directory is `/projects/xyz-calibration-cube-test` — outside the declared `<CAD_WORKSPACE>` root. Current permissions and intended project-root policy need verification.

## Important unknowns

- live helper may differ from the v2 archived source;
- current Workspace ACL/GID and bind mounts;
- whether the XYZ cube project was deliberately moved outside the target root;
- whether all active Builder mutations currently enforce the checkpoint contract.
