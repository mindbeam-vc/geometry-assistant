# Geometry Assistant — 立体几何 3D 可视化辅导工具

将立体几何题目数据渲染为交互式 3D 场景。适合高中数学立体几何辅导场景。输入 JSON 格式的几何数据，输出自包含 HTML，双击浏览器即可查看可旋转/缩放的 3D 图形。

作为 CLI 工具，可被任何 AI 编程助手（Codex、Claude Code、Cursor、Copilot Chat 等）通过 shell 调用，也可安装为 Python 包在脚本中直接使用其 API。

## 功能特性

- **交互式 3D 渲染** — 基于 Three.js，支持旋转/缩放/平移查看几何体
- **已知条件高亮** — 点击条件项高亮对应点、线、面、直角标记
- **渐进式解题展示** — 辅助线、投影点、坐标轴等构造随解题步骤逐步出现
- **自包含 HTML** — 生成的文件双击浏览器即可打开，无需安装任何软件
- **数据校验** — 内置验证器，生成前自动检查数据正确性

## 安装（选一种）

### Codex

如果用的是 Codex，直接安装 skill：

```bash
codex skill install https://github.com/mindbeam-vc/geometry-assistant
```

### 其他 AI 工具（Claude Code、Cursor 等）

先让 AI 帮你装好命令行工具：

> 帮我用 pip 安装 geometry-assistant：
> `pip install git+https://github.com/mindbeam-vc/geometry-assistant.git`

装好后，AI 就能自动调用 `geometry-assistant` 命令画图了。

## 怎么用

1. 把题目发给 AI（粘贴题目文字，或者上传题目图片）
2. 加上这句提示词
3. AI 会解题、画图、输出一个 HTML 文件，双击打开就能看

### 提示词

```text
使用高中数学知识解答本题，并使用 geometry-assistant 画出 3D 图形。按原题小问拆分，初始只显示已知结构，辅助构造和坐标轴随步骤逐步显示，输出前校验。
```

### 示例

**发给 AI（题目图片 + 下面这段文字）：**

> 使用高中数学知识解答本题，并使用 geometry-assistant 画出 3D 图形。按原题小问拆分，初始只显示已知结构，辅助构造和坐标轴随步骤逐步显示，输出前校验。

**AI 会：**

1. 识别图片中的几何体和已知条件
2. 构建 3D 模型（顶点、棱边、面）
3. 在初始图形中展示题面直接给出的结构，画直角标记
4. 辅助点、辅助线、投影、平面角、坐标轴等随解题步骤逐步出现
5. 校验数据后输出可双击打开的 HTML

最终得到一个能旋转缩放、点击条件高亮、逐步展开解题过程的 3D 页面。

## 参考：数据格式与 CLI 命令

> 以下内容供想深入使用的同学参考，正常使用不需要看。

### 命令行用法

```bash
pip install git+https://github.com/mindbeam-vc/geometry-assistant.git
geometry-assistant problem.json --output output.html
```

### 数据格式

详细说明见 [references/data-format.md](references/data-format.md)。

**坐标系**：顶点 `pos: [x, z, y]`（y 轴为高度），网格平面 y=-1。顶点用大写字母 A–Z，边用两端点字母拼接（如 `"AB"`）。

**已知条件类型**：

| 类型 | 说明 | 示例 |
|------|------|------|
| `perpendicular` | 垂直 | PD ⊥ 底面 ABCD |
| `parallel` | 平行 | AD ∥ BC |
| `length` | 线段长度 | BC = 2 |
| `equal-length` | 多线段等长 | AB = CD = AD |
| `midpoint` | 中点 | G 为 BC 中点 |
| `angle` | 角度 | ∠ABC = 60° |
| `right-angle` | 直角 | ∠ABC = 90° |

## 依赖

- **浏览器** — 支持 WebGL（Chrome、Edge、Firefox 均可）
- **网络** — 首次加载需访问 Three.js CDN
- 如果 AI 工具需要：Python 3.8+（装 CLI 时自动处理）

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

