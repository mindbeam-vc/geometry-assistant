---
name: geometry-assistant
description: Use when rendering high-school solid-geometry problem data into an interactive 3D standalone HTML artifact with known-condition highlights, step-by-step constructions, faces, polygons, line-plane angles, or dihedral angles.
metadata:
  short-description: 立体几何 3D 自包含 HTML 可视化
---

# Geometry Assistant

## 技术方案

SELF_CONTAINED_HTML_ONLY：本 skill 只交付自包含 HTML 文件。生成结果必须能直接作为一个 .html 文件交给用户打开，不能要求用户启动服务端，不能把 http://localhost:8080 作为预览或交付地址。

已淘汰的 localhost/--serve 方案只保留在 archive/legacy-localhost-preview.md 中作为历史记录，不属于当前工作流。遇到浏览器已经打开 localhost 页面时，不要沿用该页面判断结果；应重新生成 HTML 文件并让用户打开该文件。

## 标准流程

1. 构建 geometryData JSON，格式见 references/data-format.md。
2. 写入临时 JSON 文件。
3. 运行 python scripts/deploy.py <json文件路径> --output <输出html路径>，或 pip 安装后运行 geometry-assistant <json文件路径> -o <输出html路径>。
4. 交付输出的 .html 文件路径。不要启动本地服务器。
5. 交付前必须验证：validator 通过、HTML 中已嵌入 window.__GEOMETRY_DATA__、module script 语法通过 node --check。

## 数据构建要点

- 坐标使用 pos: [x, z, y]，第三个坐标是竖直高度。
- 顶点 ID 用大写字母；边 ID 用两端点拼接，如 AB、PA。
- 面 ID 用顶点顺序拼接，如 ABC、PAB、PAM。
- conditions 只放题目直接给出的已知条件。
- 用户手动添加的标注不需要反向更新题目已知条件。
- 题目已知长度可用 valueText、displayValue、label 或 exactValue 提供精确显示，例如 2√2、sqrt(2)/2、3/4。

## 高亮规则

- 选中的面、多边形、线面角、面面角，对应面或多边形必须高亮。
- 面高亮统一使用半透明柔和蓝色，避免橙色或强饱和色。
- solutionSteps[].highlights 可混用顶点、边、面 ID。
- 若步骤文字中提到已有 face ID，例如 PAM、PAC，也应纳入高亮，避免二面角说明中漏高亮两个面。
- length 和 equal-length 已知条件应在线段中点显示题目给出的精确长度标签；只限题目已知条件。

## 解题展示边界

- 初始图只展示题面直接给出的结构。
- 辅助点、投影线、垂线、平面角、坐标轴等随 solutionSteps 逐步显示。
- 线面角、二面角、截面平面角等默认属于解题构造，不应放进全局 conditions，除非题面已明确给出对应辅助对象。
- 多问问题必须使用 parts 或 questionParts，并为每个 part 指定 stepIds 和 conditionIds。
- 每个 solutionSteps[].theorem 必须写出必要证明、计算或构造过程，不能只写定理名。

## 坐标系规则

- 使用坐标法、法向量、平面方程、向量夹角公式或点到平面距离公式的步骤，必须同步显示 x/y/z 坐标轴。
- 坐标轴使用 renderMode: "axis" 和 auxiliary: true。
- 轴端点使用 axisEndpoint: true 和 label: ""，不要显示成普通几何点。

## 垂直与直角标记

- 题面已知条件出现垂直、直角或 90° 时，图上必须画 L 形直角标记。
- 这些标记属于已知条件注记，点击对应条件时显示，不要作为新推导塞进步骤。

## 运行后注意

- 生成的 HTML 不依赖本地 Node 服务端。
- 页面仍通过 importmap 加载 Three.js CDN，打开 HTML 时需要能访问对应 CDN。
- 可在浏览器控制台调用 window.__debugVertices() 调试几何点。
