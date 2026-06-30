# Geometry Assistant — 立体几何 3D 可视化辅导工具

将立体几何题目数据渲染为交互式 3D 场景。适合高中数学立体几何辅导场景。输入 JSON 格式的几何数据，输出自包含 HTML，双击浏览器即可查看可旋转/缩放的 3D 图形。

作为 CLI 工具，可被任何 AI 编程助手（Codex、Claude Code、Cursor、Copilot Chat 等）通过 shell 调用，也可安装为 Python 包在脚本中直接使用其 API。

## 功能特性

- **交互式 3D 渲染** — 基于 Three.js，支持旋转/缩放/平移查看几何体
- **已知条件高亮** — 点击条件项即可高亮对应的点、线、面、直角标记
- **渐进式解题展示** — 解题步骤逐步显示辅助线、投影点、坐标轴等构造
- **自包含 HTML 输出** — 生成的 HTML 文件可直接在浏览器打开，无需本地服务器
- **数据校验** — 内置验证器检测顶点引用、边重复、坐标系配置等常见问题
- **AI 工具集成** — 纯 CLI 设计，任何 AI 编程助手均可通过 shell 调用；附带 Codex skill 定义文件（SKILL.md）

## 快速开始


### 0. pip 安装（推荐）

```bash
pip install git+https://github.com/mindbeam-vc/geometry-assistant.git
```

安装后，全局可用 `geometry-assistant` 命令：
```bash
geometry-assistant problem.json --output pyramid.html
```



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

## AI 工具集成

本工具通过标准 CLI 接口设计，任何 AI 编程助手均可直接调用：

```bash
geometry-assistant problem.json --output output.html
```

- **Codex** — 仓库内含 `SKILL.md`，可用 `codex skill install https://github.com/mindbeam-vc/geometry-assistant` 安装为技能
- **Claude Code / Cursor / Copilot Chat** — pip 安装后，直接在对话中让 AI 构建 `geometryData` JSON 并执行 `geometry-assistant` 命令
- **任意脚本** — 可作为 Python 库使用：`from geometry_assistant import build_standalone_html, validate_geometry_data`



## 提示词指南（面向高中生）

将立体几何题目交给 AI 生成 3D 图形，只需在提示词中说清三件事：**几何体长什么样**、**已知哪些条件**、**要证/求什么**。AI 会自动构建 `geometryData` JSON 并调用本工具输出可交互的 HTML。

### 提示词怎么写

按下面模板填空即可——把题目原文和图形描述替换成你手头的题。

```text
使用 geometry-assistant 为下面的立体几何题画 3D 图。

题目原文：
（粘贴题目原文，含图描述）

要求：
1. 按原题小问编号（如（1）（2））拆分步骤，不要多拆也不要少拆
2. 初始图形只展示题目主干直接给出的结构和条件
3. 只在某个小问中出现的条件（如"若 M 为 AC 中点"）不要放到全局已知条件，应随该小问的解题步骤逐步显示
4. 辅助点、辅助线、投影、垂足、平面角、坐标系随着解题步骤逐步出现，不要一次性全画出来
5. 如果用坐标法、法向量、平面方程，在对应步骤画出 x/y/z 坐标轴（z 轴向上）
6. 题面中的垂直/直角条件必须画 L 形直角标记
7. 输出 HTML 前先校验 geometryData，报错则修复后重新生成

完成后给出 HTML 文件路径，并简要说明哪些是初始已知、哪些是逐步构造的。
```

### 简化版

如果只是快速查看图形结构，用短版：

```text
用 geometry-assistant 把这道立体几何题画成 3D 图。按原题小问拆分，初始只显示已知结构，辅助构造和坐标轴随步骤逐步显示，输出前校验。
```

### 写提示词要注意什么

| 要点 | 说明 |
|------|------|
| **给图** | 如果题目有配图，截图贴给 AI 或描述图形结构（谁是谁的底面、侧棱、顶点位置） |
| **按原作答步骤拆分** | 原题有几个小问就拆几个，不要为了配合作图多拆，也不要因为步骤多就合并 |
| **初始只给已知** | 让学生先看到题目原样，再跟随解题逐步看到辅助线和构造——保护独立思考 |
| **垂直标直角** | 题面有 PD⊥底面 或 ∠ABC=90° 时明确要求画直角标记，AI 会处理但提醒更好 |
| **坐标轴随步骤出现** | 不要一开始就画坐标系，在首次用坐标法/向量法的步骤才显示 x/y/z 轴 |
| **校验后再交付** | 要求 AI 生成后运行校验，报错就改，避免拿到的图有问题 |

### 示例：完整对话

**你的消息：**

> 用 geometry-assistant 画这道题：
>
> 如图，在四棱锥 P-ABCD 中，底面 ABCD 是边长为 2 的正方形，PD⊥底面 ABCD，PD=2，E 为 PC 中点。
> （1）求证：PA∥平面 BDE；
> （2）求二面角 E-BD-C 的余弦值。

AI 会：
1. 构建四棱锥的顶点坐标和棱边
2. 把 PD⊥底面 作为初始已知条件，画出直角标记
3. E 为 PC 中点随（1）的步骤出现
4. 证明线面平行时高亮 PA 和平面 BDE
5. 求二面角时在步骤中构造平面角、显示辅助线
6. 校验 geometryData 后输出可打开的 HTML

最终你会得到一个能旋转缩放、点击条件高亮、逐步展开解题过程的 3D 页面。
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
│   └── template.html            # Three.js 渲染模板
├── references/
│   └── data-format.md           # 数据格式详细说明
├── scripts/
│   └── deploy.py                # 薄封装（无需 pip 安装可直接运行）
└── src/
    └── geometry_assistant/      # Python 包
        ├── __init__.py
        ├── core.py              # 核心逻辑（校验 + HTML 生成）
        ├── cli.py               # CLI 入口
        └── assets/
            └── template.html    # 捆绑模板
```
