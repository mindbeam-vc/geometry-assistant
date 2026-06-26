#!/usr/bin/env python3
"""Build a standalone geometry-assistant HTML file from geometryData JSON.

The local HTTP server is optional and is only started with --serve.
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"
TEMPLATE = ASSETS / "template.html"
PORT = 8080
NODE = r"C:\Users\xiaN\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
OUT_DIR = Path(tempfile.gettempdir()) / "geometry_skill"
DEFAULT_OUT_FILE = OUT_DIR / "index.html"
ALLOWED_EDGE_RENDER_MODES = {"auxiliary", "axis"}
COORDINATE_KEYWORDS = ("\u5efa\u5750\u6807\u7cfb", "\u5750\u6807\u7cfb", "\u5750\u6807\u6cd5", "\u7a7a\u95f4\u76f4\u89d2\u5750\u6807\u7cfb")
DERIVED_KEYWORDS = ("\u4f5c", "\u5782\u8db3", "\u6295\u5f71", "\u8f85\u52a9", "\u4e2d\u70b9", "\u4ea4\u4e8e", "\u5750\u6807\u7cfb")
INITIAL_STEP_KEYS = ("\u5df2\u77e5", "\u521d\u59cb", "\u52a0\u8f7d", "\u89c2\u5bdf")


def _is_aux_entity(entity):
    return bool(entity.get("auxiliary") or entity.get("constructionOnly") or entity.get("axisEndpoint") or entity.get("renderMode") == "auxiliary")


def _step_text(step):
    return "\n".join(str(step.get(key, "")) for key in ("title", "subtitle", "theorem", "note"))


def _collect_geometry(geom_data):
    vertices = {}
    edges = {}
    faces = {}
    duplicate_pairs = []
    edge_pairs = {}
    for solid in geom_data.get("solids", []):
        solid_id = solid.get("id", "<solid>")
        for vertex in solid.get("vertices", []):
            vertex_id = vertex.get("id")
            if vertex_id:
                vertices[vertex_id] = vertex
        for face in solid.get("faces", []):
            face_id = face.get("id")
            if face_id:
                faces[face_id] = face
        for edge in solid.get("edges", []):
            edge_id = edge.get("id")
            if edge_id:
                edges[edge_id] = edge
            pair = tuple(sorted((edge.get("v1", ""), edge.get("v2", ""))))
            if pair[0] and pair[1]:
                previous = edge_pairs.get(pair)
                if previous:
                    duplicate_pairs.append((previous, edge_id or "<edge>", pair, solid_id))
                else:
                    edge_pairs[pair] = edge_id or "<edge>"
    return vertices, edges, faces, duplicate_pairs


def _collect_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _collect_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _collect_strings(child)


def _known_initial_ids(geom_data):
    known = set()
    for condition in geom_data.get("conditions", []):
        for value in _collect_strings(condition.get("targets", {})):
            known.add(value)
        for key in ("target", "line", "plane"):
            value = condition.get(key)
            if isinstance(value, str):
                known.add(value)
    for step in geom_data.get("solutionSteps", []):
        text = _step_text(step)
        if any(key in text for key in INITIAL_STEP_KEYS):
            known.update(step.get("highlights", []))
    return known


def validate_geometry_data(geom_data):
    """Fail fast on data patterns that repeatedly caused misleading 3D scenes."""
    errors = []
    vertices, edges, faces, duplicate_pairs = _collect_geometry(geom_data)
    known_initial = _known_initial_ids(geom_data)

    for previous, current, pair, solid_id in duplicate_pairs:
        errors.append(f"duplicate edge in {solid_id}: {previous} and {current} both connect {pair[0]}-{pair[1]}")

    for edge_id, edge in edges.items():
        render_mode = edge.get("renderMode")
        if render_mode and render_mode not in ALLOWED_EDGE_RENDER_MODES:
            errors.append(f"edge {edge_id} has invalid renderMode {render_mode!r}; use dashed/hidden/auxiliary/axis semantics instead")
        for key in ("v1", "v2"):
            vertex_id = edge.get(key)
            if vertex_id not in vertices:
                errors.append(f"edge {edge_id} references missing vertex {vertex_id!r}")
        if render_mode == "axis":
            if not edge.get("auxiliary"):
                errors.append(f"coordinate axis edge {edge_id} must be auxiliary")
            if edge.get("axisLabel") not in {"x", "y", "z"}:
                errors.append(f"coordinate axis edge {edge_id} must declare axisLabel x/y/z")
            endpoint = vertices.get(edge.get("v2"))
            if endpoint and not endpoint.get("axisEndpoint"):
                errors.append(f"coordinate axis edge {edge_id} should point to a hidden axisEndpoint vertex")

    for vertex_id, vertex in vertices.items():
        if vertex.get("axisEndpoint") and vertex.get("label"):
            errors.append(f"axis endpoint vertex {vertex_id} must not have a visible label")

    for face_id, face in faces.items():
        for vertex_id in face.get("vertices", []):
            if vertex_id not in vertices:
                errors.append(f"face {face_id} references missing vertex {vertex_id!r}")

    highlighted_ids = set()
    axis_edge_ids = {edge_id for edge_id, edge in edges.items() if edge.get("renderMode") == "axis"}
    axis_labels = {edge.get("axisLabel") for edge in edges.values() if edge.get("renderMode") == "axis"}
    for step in geom_data.get("solutionSteps", []):
        text = _step_text(step)
        highlights = set(step.get("highlights", []))
        highlighted_ids.update(highlights)
        if any(keyword in text for keyword in COORDINATE_KEYWORDS):
            if axis_labels != {"x", "y", "z"}:
                errors.append(f"coordinate step {step.get('id', '<step>')} needs x/y/z coordinate axis edges")
            if axis_edge_ids and not (axis_edge_ids & highlights):
                errors.append(f"coordinate step {step.get('id', '<step>')} must reveal coordinate axis edges in highlights")
        if any(keyword in text for keyword in DERIVED_KEYWORDS):
            for item_id in highlights:
                vertex = vertices.get(item_id)
                edge = edges.get(item_id)
                if vertex and item_id not in known_initial and not _is_aux_entity(vertex):
                    errors.append(f"derived point {item_id} in step {step.get('id', '<step>')} must be auxiliary")
                if edge and item_id not in known_initial:
                    endpoints = (edge.get("v1"), edge.get("v2"))
                    uses_aux_endpoint = any(_is_aux_entity(vertices.get(vertex_id, {})) for vertex_id in endpoints)
                    if (uses_aux_endpoint or edge.get("renderMode") == "auxiliary") and not _is_aux_entity(edge):
                        errors.append(f"derived edge {item_id} in step {step.get('id', '<step>')} must be auxiliary")

    for entity_id, entity in {**vertices, **edges}.items():
        if _is_aux_entity(entity) and entity.get("renderMode") != "axis" and entity_id not in highlighted_ids:
            errors.append(f"auxiliary entity {entity_id} is never revealed by a solution step")

    for condition in geom_data.get("conditions", []):
        for key in ("target", "line", "plane"):
            value = condition.get(key)
            if isinstance(value, str) and value not in vertices and value not in edges and value not in faces:
                errors.append(f"condition {condition.get('id', '<condition>')} references missing {key} {value!r}")
        if condition.get("type") in {"perpendicular", "right-angle"}:
            targets = condition.get("targets", {})
            marker_target = condition.get("target") or condition.get("line") or targets.get("segment") or targets.get("vertex")
            if not marker_target:
                errors.append(f"condition {condition.get('id', '<condition>')} needs a target/line for an L marker")

    if errors:
        raise ValueError("geometryData validation failed:\n- " + "\n- ".join(errors))



def build_standalone_html(template_text, geom_data):
    data_json = json.dumps(geom_data, ensure_ascii=False, separators=(",", ":"))
    embedded = f"<script>window.__GEOMETRY_DATA__={data_json};</script>\n"
    if "window.__GEOMETRY_DATA__" not in template_text:
        template_text = template_text.replace("<script type=\"module\">", embedded + "<script type=\"module\">", 1)

    standalone_boot = """if (window.__GEOMETRY_DATA__) {
  init(window.__GEOMETRY_DATA__);
  const statusHint = document.getElementById('status-hint');
  if (statusHint) statusHint.textContent = '已加载自包含题目数据';
} else {
  loadCurrentProblem();
}"""
    if "loadCurrentProblem();" in template_text:
        template_text = template_text.replace("loadCurrentProblem();", standalone_boot, 1)
    else:
        marker = "init(geometryData);"
        template_text = template_text.replace(marker, "init(window.__GEOMETRY_DATA__ || geometryData);", 1)

    return template_text.replace('fetch("problems/current.json", { cache: "no-store" })', 'fetch("__standalone_disabled_current.json", { cache: "no-store" })')


def ensure_port_free():
    try:
        subprocess.run(
            "taskkill /F /IM node.exe",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
    except Exception:
        pass
    time.sleep(0.5)


def start_server(serve_dir):
    server_js = serve_dir / "server.js"
    server_js.write_text(
        'const h=require("http"),fs=require("fs"),p=require("path");'
        'const s=h.createServer((r,res)=>{'
        'let fp=r.url==="/"?"/index.html":r.url;'
        'fp=p.join(__dirname,fp);'
        'fs.readFile(fp,(e,d)=>{if(e){res.writeHead(404);res.end("404")}else{'
        'const t={".html":"text/html",".js":"text/javascript",".css":"text/css"};'
        'res.writeHead(200,{"Content-Type":t[p.extname(fp)]||"text/plain"});'
        'res.end(d)}})});'
        f's.listen({PORT},"127.0.0.1",()=>console.log("server ready"));',
        encoding="utf-8",
    )
    subprocess.Popen(
        [NODE, str(server_js)],
        cwd=str(serve_dir),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Export geometryData as a standalone HTML page.")
    parser.add_argument("json_file", help="Path to geometryData JSON")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUT_FILE), help="Output HTML path")
    parser.add_argument("--serve", action="store_true", help="Optionally start a local HTTP preview server")
    return parser.parse_args()


def main():
    args = parse_args()
    data_file = Path(args.json_file)
    if not data_file.exists():
        print(f"JSON file does not exist: {data_file}", file=sys.stderr)
        sys.exit(1)

    with data_file.open("r", encoding="utf-8-sig") as f:
        geom_data = json.load(f)

    try:
        validate_geometry_data(geom_data)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

    with TEMPLATE.open("r", encoding="utf-8") as f:
        template = f.read()

    out_file = Path(args.output)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(build_standalone_html(template, geom_data), encoding="utf-8")

    if args.serve:
        ensure_port_free()
        start_server(out_file.parent)
        print(f"http://localhost:{PORT}")
    else:
        print(str(out_file.resolve()))


if __name__ == "__main__":
    main()