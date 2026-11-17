"""Offline fake-document tests; no FreeCAD dependency and no user documents."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zipfile import ZipFile
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cad_revision

class FakeDoc:
    Name = 'Sandbox'
    FileName = ''
    Objects = []
    def saveCopy(self, pathname):
        with ZipFile(pathname, 'w') as z:
            z.writestr('Document.xml', '<Document/>')

with TemporaryDirectory() as tmp:
    fake_projects = Path(tmp) / 'projects'
    fake_projects.mkdir()
    project = fake_projects / 'cad-agent-projects' / 'test'
    doc = FakeDoc()
    with patch.object(cad_revision, '_project_root', side_effect=lambda x: Path(x).resolve()):
        a = cad_revision.checkpoint(doc, project, 'before', 'test')
        b = cad_revision.checkpoint(doc, project, 'after', 'test')
        assert a['revision_id'] != b['revision_id']
        assert (project / a['relative_file']).is_file()
        assert (project / b['relative_file']).is_file()
        assert a['size_bytes'] > 0 and b['size_bytes'] > 0
        assert doc.FileName == ''
        st = cad_revision.quick_status(doc, project)
        assert st['matches_last_snapshot_heuristically']
        state = cad_revision.update_project_state(project, {'current_task': 'done'})
        assert state['current_task'] == 'done'
        assert cad_revision.read_project_state(project)['current_task'] == 'done'
print('Offline cad_revision tests: OK')
