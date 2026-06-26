# Geometry Assistant — 立体几何 3D 可视化辅导工具

将立体几何题目数据渲染为交互式 3D 场景。适合高中数学立体几何辅导场景，支持几何体可视化、已知条件高亮、解题步骤标注。

## 功能特性

- **交互式 3D 渲染** — 基于 Three.js，支持旋转/缩放/平移查看几何体
- **已知条件高亮** — 点击条件项即可高亮对应的点、线、面、直角标记
- **渐进式解题展示** — 解题步骤逐步显示辅助线、投影点、坐标轴等构造
- **自包含 HTML 输出** — 生成的 HTML 文件可直接在浏览器打开，无需本地服务器
- **数据校验** — 内置验证器检测顶点引用、边重复、坐标系配置等常见问题
- **Codex Skill 集成** — 可作为 Codex 技能使用，通过自然语言描述自动构建几何场景

## 快速开始


### 0. pip 安装（推荐）

```bash
pip install git+https://github.com/mindbeam-vc/geometry-assistant.git
```

安装后，全局可用 `geometry-assistant` 命令：
```bash
geometry-assistant problem.json --output pyramid.html
```

也支持 Codex skill 直接使用（无需 pip 安装），见下方。

### 1. 编写几何数据 JSON

```json
{
  "problemText": "如图，在四棱锥 P-ABCD 中，底面 ABCD 为正方形...",
  "solids": [{
    "id": "pyramid",
    "vertices": [
      { "id": "A", "pos": [0, 0, 0], "label": "A" },
      { "id": "B", "pos": [2, 0, 0], "label": "B" },
      { "id": "C", "pos": [2, 0, 2], "label": "C" },
      { "id": "D", "pos": [0, 0, 2], "label": "D" },
      { "id": "P", "pos": [1, 1.5, 1], "label": "P" }
    ],
    "edges": [
      { "id": "AB", "v1": "A", "v2": "B" },
      { "id": "BC", "v1": "B", "v2": "C" },
      { "id": "CD", "v1": "C", "v2": "D" },
      { "id": "DA", "v1": "D", "v2": "A" },
      { "id": "PA", "v1": "P", "v2": "A" },
      { "id": "PB", "v1": "P", "v2": "B" },
      { "id": "PC", "v1": "P", "v2": "C" },
      { "id": "PD", "v1": "P", "v2": "D" }
    ],
    "faces": [
      { "id": "ABCD", "vertices": ["A","B","C","D"], "color": "#e8e8e8" },
      { "id": "PAB", "vertices": ["P","A","B"], "color": "#d0ebff" },
      { "id": "PBC", "vertices": ["P","B","C"], "color": "#d0ebff" },
      { "id": "PCD", "vertices": ["P","C","D"], "color": "#d0ebff" },
      { "id": "PDA", "vertices": ["P","D","A"], "color": "#d0ebff" }
    ]
  }],
  "conditions": [
    {
      "id": "c1", "type": "perpendicular",
      "text": "PD \u22a5 \u5e95\u9762 ABCD",
      "targets": { "segment": "PD", "face": "ABCD" },
      "highlightColor": "#ff6b6b"
    }
  ],
  "solutionSteps": [
    {
      "title": "\u8bc1\u660e PD \u22a5 AC",
      "theorem": "\u7ebf\u9762\u5782\u76f4\u5b9a\u4e49",
      "highlights": ["PD", "AC"],
      "annotations": []
    }
  ]
}
```

### 2. 生成 HTML

```bash
python scripts/deploy.py problem.json --output pyramid.html
```

### 3. 浏览器打开

直接双击 `pyramid.html` 即可查看交互式 3D 场景。

> 如需本地 HTTP 服务器预览，追加 `--serve` 参数。

## 数据格式

详细格式说明见 [references/data-format.md](references/data-format.md)。

### 坐标系约定

- 顶点坐标使用 `pos: [x, z, y]`（Three.js 中 y 轴为高度轴）
- 网格平面位于 y = -1，顶点应位于网格平面上方
- 顶点 ID 使用大写字母 A–Z，边 ID 为两端点字母拼接（如 `"AB"`）

### 已知条件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `perpendicular` | 线线垂直 / 线面垂直 / 面面垂直 | PD \u22a5 \u5e95\u9762 ABCD |
| `parallel` | 线线平行 / 面面平行 | AD \u2225 BC |
| `length` | 线段长度 | BC = 2 |
| `equal-length` | 多线段等长 | AB = CD = AD = 1 |
| `midpoint` | 中点 | G \u4e3a BC \u4e2d\u70b9 |
| `angle` | 角度 | \u2220ABC = 60\u00b0 |
| `right-angle` | 直角 | \u2220ABC = 90\u00b0 |

### 解题步骤

每个 `solutionSteps` 条目包含：
- `title` — 步骤标题
- `theorem` — 所用定理
- `highlights` — 高亮的点/边 ID 列表
- `annotations` — 文字标注

## 作为 Codex Skill 使用

本仓库可直接安装为 Codex 几何辅导技能：

```bash
codex skill install https://github.com/<your-username>/geometry-assistant
```

安装后在 Codex 中描述立体几何题目，模型会自动构建 `geometryData` JSON 并调用 `deploy.py` 生成交互式 3D 图形。

## 依赖

- **Python 3.8+** — 用于运行 `deploy.py` 脚本
- **Node.js** — 仅在 `--serve` 模式下需要（用于本地 HTTP 服务器）
- **浏览器** — 支持 WebGL 的现代浏览器（Chrome、Edge、Firefox）
- **网络** — 首次加载 HTML 时需要访问 Three.js CDN（unpkg）

## 许可证

[MIT](LICENSE)

## 项目结构

```
geometry-assistant/
├── pyproject.toml               # pip 包配置（支持 pip install）
├── SKILL.md                     # Codex 技能定义
├── README.md
├── LICENSE
├── .gitignore
├── assets/
│   └── template.html            # Three.js 渲染模板（Codex skill 用）
├── references/
│   └── data-format.md           # 数据格式详细说明
├── scripts/
│   └── deploy.py                # 薄封装（向后兼容 Codex skill）
└── src/
    └── geometry_assistant/      # Python 包
        ├── __init__.py
        ├── core.py              # 核心逻辑（校验 + HTML 生成）
        ├── cli.py               # CLI 入口
        └── assets/
            └── template.html    # 捆绑模板（pip 安装用）
```
