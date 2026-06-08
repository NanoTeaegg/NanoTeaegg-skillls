---
name: webui-design-system
description: webui-design-system skill——为 Web 项目建立可观测、可预览、可约束的设计系统，保持整个项目 UI 一致。产出 tokens.css（值的事实源）+ components.css 组件库 + preview.html 文档站（引用并渲染真实 token 与真实组件）+ 精简 UI_SPEC 契约 + diff/lint 脚本。当用户要定或改 Web 界面视觉规则、Design Token（颜色/字体/间距/圆角/阴影/动效）、组件规范与状态、设计系统文档站点，或只要项目有任何 UI 变更需要保持整体一致时触发。只做 Web 端；不含原生 iOS/Android、功能需求（→requirements-definition）、交互流程（→ux-design）、页面/landing 视觉设计与落地（→web-design）、业务页面代码实现（→frontend-dev）、技术/数据库选型（→dev-kickoff/database）。
version: v0.7
---

# Web 设计系统（webui-design-system）

为一个 **Web 项目**建立一套**可约束、可观测、可预览**的设计系统，保持整个项目 UI 一致。只要项目有 UI 变更，就用这个 skill 同步设计系统，而不是一次性输出界面就完事。

设计推演（为什么是现在这套格式）见 `RATIONALE.md`。

## 核心模型:三类事实源，各管一层

一个完整设计系统是三层，本 skill 只「拥有」前两层的实现，第三层归项目组件代码:

| 层 | 事实源 | 约束力来源 |
|---|---|---|
| **Token 层**（色/字/间距/圆角/阴影/动效） | `design-system/tokens.css` | 业务代码 `import` 它、用 `var(--*)` → **自动引力** |
| **组件规范层**（API/状态/行为编排） | `docs/UI_SPEC.md` + `design-system/components.css` 的 `.ds-*` | 业务页面复用 class + lint 校验 |
| **组件实现层**（能跑的页面） | 项目业务代码 | 本 skill 不写，只约束 |

`preview.html` 是**观测窗**，不是法律:它**引用** tokens.css/components.css 渲染真实 token 与真实组件，**绝不重画**——所以它永远等于真实组件、不漂移。它的职责是让人肉眼验收和追溯变更，不产生任何约束力。

## 核心原则

- 先读 `docs/PRD.md`、`docs/UX.md`、`docs/TECH_DESIGN.md`（若存在），再写设计系统。
- 只做 Web。出现原生 iOS/Android 需求时，归属另一个 skill，不要在这里混写。
- `docs/UI_SPEC.md` 是给 AI 读的工程契约:短、硬、结构化。不写"高级感/现代"这类不可执行的描述。
- Token 分类、字段、代码映射从 `assets/design-token-template.md` 读取，不临时发明结构。
- **token 是急性子，组件是慢性子**:token 前置定义；组件碰到再建、守约定、第二次复用才回收进 components.css（见「组件回收工作流」）。
- 三类产物（tokens.css / components.css / preview.html）+ UI_SPEC 任何时候一起改，保持同一事实源。
- 允许做 UI 层技术/组件库映射（CSS Variables / Tailwind token / shadcn variant），不扩展到后端、状态管理、数据库、部署。
- 不写业务页面代码，不重写 UX 流程。

## 文件职责

**模板（assets/）**
- `ui-spec-template.md`: 精简 `docs/UI_SPEC.md` 契约骨架（含「基础 UI 约定」「组件回收」「变更记录」）。
- `design-token-template.md`: token 分类、字段、默认值、代码映射（动效含 duration + ease）。
- `components-starter.css`: 组件库起步种子（Button/Field/Tag/Card），复制为项目 `components.css` 再扩展。
- `preview-shell/`: 文档站**固定外壳**——专业度由它兜底。
  - `preview.css` / `preview.js`: 工具外壳，**verbatim 复制**进项目 design-system/，不要手改。负责 chrome、色板+对比度徽章+复制 hex、间距/圆角/阴影标尺、代码块、主题切换、scrollspy。
  - `preview.template.html`: 文档站骨架，复制后只填 manifest（token 清单）和组件 demo。

**Web 规范参考（按需读取）**
- `references/platform-web.md`: token 区间、组件状态矩阵、暗色策略、布局、可访问性红线。

**视觉方向参考（按需读取）**
- `references/style-seeds.md`: 气质关键词 → token 方向速查。
- `references/design-systems/INDEX.md` + `{brand}.md`: 真实品牌设计规范索引（按需读对应品牌，禁止全量加载）。

**脚本（scripts/）**
- `crawl_website.py` / `extract_design_tokens.py`: 竞品参考提取（"做成像 XX"且无预置品牌时）。
- `diff_tokens.py`: 对比两版 tokens.css/components.css → 生成变更 changelog（**变更可观测**）。
- `lint_tokens.py`: 扫描业务代码里的裸 hex/px/ms 与绕过组件库的自写样式（**约束校验**）。

**质量**
- `references/checklist.md`: 产出前自检。

## 固定输出

每次新建或变更设计系统，交付:

1. **AI 契约**: `docs/UI_SPEC.md`（用 `ui-spec-template.md` 结构）。
2. **值源**: `design-system/tokens.css`（`:root` CSS 变量，含 motion token；有暗色则含切换选择器）。
3. **组件库**: `design-system/components.css`（`.ds-*`，只消费 token；有交互再加 `components.js`）。
4. **文档站**: `design-system/preview.html` + `preview.css` + `preview.js`（外壳 verbatim 复制）。

如果项目已有前端应用且希望预览嵌入项目，可改为内部 `/design-system` 路由 import 真实组件（Storybook 式）；静态 preview.html 与路由二选一，逻辑一致:都渲染真实组件、不重画。

## 何时触发哪条路径

检查 `docs/UI_SPEC.md` 和 `design-system/` 是否已有 token/组件/文档站:

- **不存在** → 走「新建设计系统」。
- **已存在**，用户在调整视觉、token、组件、页面 UI 规则、文档站，或要新增/改某个 UI → 走「设计系统变更」。

## 新建设计系统流程

### Step 1. 读上游文档
按顺序读 `docs/PRD.md` → `docs/UX.md` → `docs/TECH_DESIGN.md`（若存在）。缺失不要卡住，在「开放问题与假设」说明未对齐。

### Step 2. 结构化访谈
不要凭审美直接配色。已在上游写清的不重复问，一次问 2-4 个关键问题:产品气质、目标用户与环境、信息密度、视觉偏好（主色/中性/字体/圆角/阴影）、核心组件范围、可访问性与暗色。

- 拿到气质描述后先查 `references/style-seeds.md` 匹配种子，展示 token 方向供确认。
- 用户说"做成像 XX 产品"时，先查 `references/design-systems/INDEX.md`，有预置直接读；无预置用 `scripts/crawl_website.py` 提取。

### Step 3. 读模板与 Web 参考
读 `assets/ui-spec-template.md`、`assets/design-token-template.md`、`references/platform-web.md`、`references/checklist.md`。

### Step 4. 选 UI 层实现策略
优先 CSS Variables 作底层 token；有 Tailwind 同步 token 映射；有 shadcn/Radix/Ant/MUI 只做 token + variant 映射，不另起组件系统。写进 UI_SPEC「工程映射」。

### Step 5. 产出四类产物

**tokens.css**:按 token 模板给具体值，命名与 UI_SPEC 一致，含 motion token。

**components.css**:复制 `assets/components-starter.css` 为起点，按产品 token 调整。**只放最常复用的基础组件**（Button/Field/Tag/Card），其余组件等第二次复用再回收。

**UI_SPEC.md**:
- 用模板结构。
- Design Tokens 给具体值与代码映射。
- 写「基础 UI 约定」（一页硬规则，不逐组件矩阵）。
- 「组件库」只登记已回收进 components.css 的组件，按「用途 → 变体/class → 状态 → token 依赖 → 行为动效编排 → 禁止用法」写。
- 写「AI 落地约束」「文档站验收」「可访问性」「变更记录」。

**preview.html + 外壳**:
1. 把 `preview-shell/preview.css`、`preview.js` **verbatim 复制**进 `design-system/`。
2. 复制 `preview.template.html` 为 `preview.html`，改 brand/title/版本号。
3. 在 `#ph-manifest` 里登记本项目 tokens.css 的 token 清单（颜色/字体/间距/圆角/阴影）——外壳据此自动渲染色板、对比度徽章、标尺，无需手画。
4. 组件区用真实 `.ds-*` class 渲染 demo，每个套 `.ph-demo` + `.ph-demo-canvas` + `.ph-code`。**绝不在 preview 里内联重写组件样式**（不漂移铁规则）。
5. 暗色优先的产品可加一行 `.ph-demo-canvas { background: var(--color-bg-surface); color: var(--color-text-primary); }` 让组件在真实底色上展示。

## 组件回收工作流（Lite 的核心）

小项目不前置定死组件，否则维护成本高于收益。规则:

- **第一次**需要某组件（如折叠面板）→ 直接用 token + 基础约定建在业务页面里，不写规范、不进 components.css。
- **第二次**要复用同一组件 → 把它回收:① 抽成 `components.css` 的 `.ds-*` class（消费 token）；② 有交互则行为写进 `components.js`（动效用 motion token）；③ 在 UI_SPEC「组件库」登记；④ 在 preview.html 加一段真实 demo；⑤ 在变更记录追加一行。
- 影响面大的新组件要通知维护者。

## 设计系统变更流程

UI_SPEC/tokens.css/components.css/preview.html 已存在，用户要改视觉、token、组件或页面规则时:

1. 读现有 UI_SPEC + tokens.css + components.css + preview.html，确认四者一致。
2. 读 PRD/UX/TECH_DESIGN 相关变更。
3. 变更影响评估:改主色影响按钮/链接/焦点/图表/状态色；改间距影响表格密度与移动端；改圆角/阴影影响卡片/弹窗/浮层；改 motion 影响所有过渡。
4. 组件缺口评估:复用 → 加变体 → 新增（按回收工作流）。
5. 原地同步改 tokens.css / components.css / components.js / UI_SPEC / preview.html，保持同一事实源。
6. 用 `scripts/diff_tokens.py` 对比改前改后，生成变更条目；在「变更记录」追加一行:日期、类型、内容、原因、影响范围、同步文件。
7. 提醒可用 `scripts/lint_tokens.py` 校验业务代码没有绕过设计系统。

## 边界

- 属于本 skill:Web 端视觉方向、Design Tokens、UI 层技术/组件库映射、tokens.css、components.css 组件库、组件 API/状态/行为编排规范、设计系统文档站、布局栅格、页面使用法则、响应式/移动适配、可访问性、变更可观测与约束校验。
- 不属于本 skill:功能范围、用户流程、信息架构、业务页面实现、后端/数据库/API/部署/状态管理选型、原生 iOS/Android、landing/营销页视觉设计、Figma/Sketch 稿。

- 用户要"写登录页/仪表盘业务页面" → frontend-dev。
- 用户要"做一个 landing page / 官网页面视觉" → web-design。
- 用户要"原生 App 的设计系统" → 暂不在本 skill，另起 iOS/Android skill。
- 用户问"用 shadcn 还是 Ant Design" → 只从 UI 设计系统角度给 token/variant 映射，不扩展成整体架构。
