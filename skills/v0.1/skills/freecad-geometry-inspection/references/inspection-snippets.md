# Read-only FreeCAD Python examples

Use only on a clearly named open document; replace identifiers with confirmed values. These snippets are illustrative, not executable scripts installed on the server.

```python
import FreeCAD as App
doc = App.getDocument('ExactDocumentName')
for obj in doc.Objects:
    rec = {'Name': obj.Name, 'TypeId': obj.TypeId, 'Label': obj.Label,
           'InList': [x.Name for x in obj.InList],
           'OutList': [x.Name for x in obj.OutList]}
    if hasattr(obj, 'Shape') and not obj.Shape.isNull():
        s = obj.Shape; bb = s.BoundBox
        rec.update({'valid': s.isValid(), 'solids': len(s.Solids),
                    'volume_mm3': s.Volume, 'area_mm2': s.Area,
                    'bbox_mm': [bb.XLength, bb.YLength, bb.ZLength],
                    'min_xyz_mm': [bb.XMin, bb.YMin, bb.ZMin]})
    print(rec)
```

Sketches:
```python
for obj in doc.Objects:
    if obj.TypeId == 'Sketcher::SketchObject':
        print(obj.Name, 'geometry', len(obj.Geometry),
              'constraints', len(obj.Constraints))
        # Check availability of solver/DoF properties on this FreeCAD build.
```

Avoid `doc.recompute()` in Analyst/Reviewer. Do not parse all feature properties indiscriminately: giant trees can overwhelm the LLM and logs. Query only relevant objects.

`Shape.check()` in some FreeCAD versions returns diagnostics differently or can be expensive; don't assume a universal return schema. If unavailable, say so. For STL use independent file validation in an isolated read-only environment, not import into the user's live document.
