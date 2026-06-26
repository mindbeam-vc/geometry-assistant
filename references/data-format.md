# geometryData 格式参考

```json
{
  "problemText": "题目文字",
  "solids": [{
    "id": "polyhedron",
    "vertices": [{ "id": "A", "pos": [0, 0, 0], "label": "A" }],
    "edges": [{ "id": "AB", "v1": "A", "v2": "B", "dashed": false }],
    "faces": [{ "id": "ABCD", "vertices": ["A","B","C","D"], "color": "#e8e8e8" }]
  }],
  "conditions": [
    { "id": "c1", "type": "parallel", "text": "AD∥BC", "targets": { "lineA": "DA", "lineB": "BC" }, "highlightColor": "#339af0" },
    { "id": "c2", "type": "equal-length", "text": "AB=CD=AD=1", "targets": { "segments": ["AB","CD","DA"] }, "value": 1, "highlightColor": "#51cf66" },
    { "id": "c3", "type": "length", "text": "BC=2", "targets": { "segment": "BC" }, "value": 2, "highlightColor": "#51cf66" },
    { "id": "c4", "type": "midpoint", "text": "G为BC中点", "targets": { "vertex": "G" }, "highlightColor": "#cc5de8" },
    { "id": "c5", "type": "perpendicular", "text": "面ADFE⊥面ADCB", "targets": { "faceA": "ADFE", "faceB": "ABCD" }, "highlightColor": "#ff6b6b" }
  ],
  "solutionSteps": [
    { "title": "步骤名", "theorem": "所用定理", "highlights": ["A","BC"], "annotations": [] }
  ]
}
```

## targets 字段说明

| condition type | targets 必填 |
|---|---|
| midpoint | `{ vertex: "G" }` |
| perpendicular (面面垂直) | `{ faceA, faceB }` |
| perpendicular (线线垂直) | `{ segment, line2, face }` |
| parallel | `{ lineA, lineB }` |
| length | `{ segment }`, `value` |
| equal-length | `{ segments: [...] }` |
| angle / right-angle | `{ vertex, sides: [...] }` |
