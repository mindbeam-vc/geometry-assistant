# Geometry Assistant

Geometry Assistant 将立体几何题目的 geometryData JSON 渲染为交互式 3D 场景，输出一个可直接打开的自包含 HTML 文件。适合高中数学立体几何辅导：已知条件高亮、精确长度标注、逐步显示辅助构造、面/线面角/面面角高亮。

## 技术方案

SELF_CONTAINED_HTML_ONLY：当前唯一交付方案是自包含 HTML。

- 用户拿到的是一个 .html 文件，直接用浏览器打开。
- 不要求用户启动服务端。
- 不使用 localhost:8080 作为预览或交付地址。
- 旧 localhost/--serve 方案已淘汰，只在 archive/legacy-localhost-preview.md 中保留历史说明。

## 安装

```bash
pip install git+https://github.com/mindbeam-vc/geometry-assistant.git
```

Codex skill 使用时，可安装本仓库 skill；生成图形时仍以输出 HTML 文件为准。

## 使用

```bash
geometry-assistant problem.json --output output.html
```

或者在仓库内直接运行兼容脚本：

```bash
python scripts/deploy.py problem.json --output output.html
```

命令会校验 geometryData，并生成自包含 HTML。生成后打开 output.html 即可查看 3D 场景。

## 面向 AI 的提示词

```text
使用高中数学知识解答本题，并使用 geometry-assistant 输出一个自包含 HTML 3D 图形。按原题小问拆分；初始图只显示题面直接给出的结构；辅助构造、坐标轴、线面角和二面角相关面随步骤逐步显示；题目已知长度用精确值标注；输出前运行校验。
```

## 数据要点

- 坐标：pos: [x, z, y]，第三个坐标是竖直高度。
- 顶点 ID：大写字母，如 A、B、P。
- 边 ID：两端点拼接，如 AB、PA。
- 面 ID：顶点拼接，如 ABC、PAB、PAM。
- 已知长度：可用 valueText/displayValue/label/exactValue 显示无理数或分数。
- conditions 只放题目直接给出的已知条件；辅助构造放 solutionSteps。

详细格式见 references/data-format.md。

## 高亮与标注

- 选中面、多边形、线面角、面面角时，对应面使用半透明柔和蓝色高亮。
- 二面角步骤中提到的两个面，例如 PAM 与 PAC，会跟随步骤高亮。
- length 与 equal-length 已知条件会在线段中点显示题目给出的精确长度标签。

## 项目结构

```text
geometry-assistant/
  pyproject.toml
  SKILL.md
  README.md
  archive/
    legacy-localhost-preview.md
  assets/
    template.html
  references/
    data-format.md
  scripts/
    deploy.py
  src/geometry_assistant/
    core.py
    cli.py
    assets/template.html
```

## 依赖

- Python 3.8+
- 支持 WebGL 的浏览器
- 首次加载页面需访问 Three.js CDN

## 许可证

MIT
