"""CAD Studio revision helper v2.0: native saveCopy() snapshots and project state.

Run from the FreeCAD Python interpreter. FreeCAD is not imported, a `doc` object
is passed by the caller. No shell/network/FreeCAD preferences access.
This helper does NOT intercept arbitrary mutating calls. The caller must call
checkpoint() before/after each logical mutation.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import json
import os
import tempfile
import uuid
import zipfile


def _utcstamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")


def _project_root(root: str | Path) -> Path:
    path = Path(root).expanduser().resolve()
    allowed = Path('/projects').resolve()
    if path == allowed or allowed not in path.parents:
        raise ValueError('project_root must be a directory under /projects')
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open('r', encoding='utf-8') as fh:
        return json.load(fh)


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix='.' + path.name + '.', suffix='.tmp', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            json.dump(value, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write('\n')
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            Path(temp_name).unlink(missing_ok=True)
        except Exception:
            pass
        raise


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def lightweight_fingerprint(doc: Any) -> str:
    """Heuristic change signal, NOT a cryptographic proof of all CAD properties."""
    objects = []
    for obj in getattr(doc, 'Objects', []):
        row = {
            'name': str(getattr(obj, 'Name', '')),
            'label': str(getattr(obj, 'Label', '')),
            'type': str(getattr(obj, 'TypeId', '')),
            'placement': str(getattr(obj, 'Placement', '')),
        }
        try:
            shape = getattr(obj, 'Shape', None)
            if shape is not None:
                box = getattr(shape, 'BoundBox', None)
                if box is not None:
                    row['bbox'] = [round(float(getattr(box, x)), 6) for x in
                                   ('XMin', 'YMin', 'ZMin', 'XMax', 'YMax', 'ZMax')]
                row['volume'] = round(float(getattr(shape, 'Volume', 0)), 6)
        except Exception:
            row['shape_unavailable'] = True
        objects.append(row)
    raw = json.dumps({'doc': str(getattr(doc, 'Name', '')), 'objects': objects},
                     ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()


def checkpoint(doc: Any, project_root: str | Path, phase: str, note: str = '') -> dict:
    """Make a verified FCStd copy and append one revision journal entry.

    `phase`: 'before' or 'after'. Raises on snapshot failure; caller must NOT
    mutate a valuable document if the 'before' snapshot failed.
    """
    if doc is None:
        raise ValueError('No active FreeCAD document')
    if phase not in ('before', 'after'):
        raise ValueError("phase must be 'before' or 'after'")
    root = _project_root(project_root)
    revisions = root / 'revisions'
    revisions.mkdir(parents=True, exist_ok=True)
    rev_id = f'{_utcstamp()}-{uuid.uuid4().hex[:8]}-{phase}'
    destination = revisions / (rev_id + '.FCStd')
    if destination.exists():
        raise FileExistsError(destination)

    # FreeCAD App::Document.saveCopy leaves the current document's FileName unchanged.
    doc.saveCopy(str(destination))
    if not destination.is_file() or destination.stat().st_size == 0:
        raise RuntimeError('FreeCAD saveCopy did not create a nonempty snapshot')
    try:
        with zipfile.ZipFile(destination, 'r') as archive:
            invalid = archive.testzip()
            if invalid is not None:
                raise RuntimeError(f'FCStd ZIP integrity failed at {invalid}')
    except Exception as exc:
        raise RuntimeError('Snapshot is not a valid FCStd ZIP archive') from exc

    entry = {
        'revision_id': rev_id,
        'created_utc': datetime.now(timezone.utc).isoformat(),
        'phase': phase,
        'note': str(note),
        'document_name': str(getattr(doc, 'Name', '')),
        'document_file': str(getattr(doc, 'FileName', '')),
        'object_count': len(getattr(doc, 'Objects', [])),
        'lightweight_fingerprint': lightweight_fingerprint(doc),
        'relative_file': str(destination.relative_to(root)),
        'size_bytes': destination.stat().st_size,
        'sha256': _sha256(destination),
    }
    log_path = root / 'revision_log.json'
    journal = _read_json(log_path, {'schema': 1, 'revisions': []})
    if not isinstance(journal, dict) or not isinstance(journal.get('revisions'), list):
        raise ValueError('Invalid revision_log.json — refusing to overwrite')
    journal['revisions'].append(entry)
    _atomic_json(log_path, journal)
    return entry


def read_project_state(project_root: str | Path) -> dict:
    root = _project_root(project_root)
    state = _read_json(root / 'project_state.json', {'schema': 1, 'facts': {}, 'decisions': [], 'open_questions': []})
    if not isinstance(state, dict):
        raise ValueError('Invalid project state')
    return state


def update_project_state(project_root: str | Path, patch: dict) -> dict:
    """Top-level merge of supplied project facts/decisions; no arbitrary files."""
    if not isinstance(patch, dict):
        raise TypeError('patch must be a dictionary')
    root = _project_root(project_root)
    state = read_project_state(root)
    state.update(patch)
    state['updated_utc'] = datetime.now(timezone.utc).isoformat()
    _atomic_json(root / 'project_state.json', state)
    return state


def quick_status(doc: Any, project_root: str | Path) -> dict:
    """Lightweight consistency check only; cannot detect every external edit."""
    root = _project_root(project_root)
    log = _read_json(root / 'revision_log.json', {'schema': 1, 'revisions': []})
    last = log.get('revisions', [])[-1] if log.get('revisions') else None
    result = {'document_present': doc is not None, 'last_revision': last}
    if doc is None:
        return result
    result['document_name'] = str(getattr(doc, 'Name', ''))
    result['object_count'] = len(getattr(doc, 'Objects', []))
    result['lightweight_fingerprint'] = lightweight_fingerprint(doc)
    result['matches_last_snapshot_heuristically'] = bool(
        last and last.get('document_name') == result['document_name']
        and last.get('lightweight_fingerprint') == result['lightweight_fingerprint']
    )
    return result
