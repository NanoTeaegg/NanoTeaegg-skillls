---
name: ui-design
description: 把 PRD、UX 和技术方案里已经明确的"做什么、用户怎么用、目标平台是什么"翻译成"某一个目标平台的界面应该长什么样、视觉规则怎么统一、组件状态怎么规范",产出或维护 UI 设计规范文档。当用户说"帮我定 UI 规范""视觉设计怎么做""把 UX 转成 UI 规范""设计系统怎么定义""颜色/字体/间距/圆角/阴影怎么定""组件规范怎么写""按钮、表单、表格、弹窗状态怎么统一""这个 Web 后台/iOS App/Android App/小程序界面风格怎么定""帮我写 UI_SPEC/DESIGN_SYSTEM""前端实现前先定一份界面规范"时就触发本 skill。必须先读取 docs/PRD.md、docs/UX.md 和 docs/TECH_DESIGN.md(若存在),从上游文档和用户当前请求中判断单一目标平台:Web 就只写 Web UI 规范,iOS 就只写 iOS UI 规范,Android 就只写 Android UI 规范,不要默认把所有平台规则一次性展开。若多个平台都在范围内但用户没指定本次目标平台,先问用户选择一个。使用 assets/ui-spec-template.md 和 assets/design-token-template.md 作为结构化输出骨架,再按 references/platform-*.md 读取对应平台规则。不做功能需求定义(PRD),不重新设计用户流程/信息架构(UX),不做技术栈/组件库选型(dev-kickoff),不写前端代码,不输出 Figma 文件或图片设计稿。
version: v0.2
---

# UI 设计规范

把已经明确的产品需求、交互方案和目标平台,转换成一份能指导设计稿、前端实现和界面评审的 UI 规范。这个 skill 回答的是:**某一个目标平台上的界面视觉与组件规则如何统一**。

## 核心原则

- 先读 `docs/PRD.md`、`docs/UX.md`、`docs/TECH_DESIGN.md`(若存在),再写 UI 规范。
- 先判断目标平台,再选择模板和 reference。不要把 Web、iOS、Android、小程序、桌面端规则混在一份默认输出里。
- Design Tokens 的分类、标题层级和默认值从 `assets/design-token-template.md` 读取,不要每次临时发明 token 结构。
- 平台差异从 `references/platform-*.md` 读取;只读本次目标平台对应文件。
- 输出中文文档,不写前端代码,不选择组件库,不重写 UX 流程。

## 文件职责

- `assets/ui-spec-template.md`: `docs/UI_SPEC.md` 的结构化骨架,包含一级/二级标题模块。
- `assets/design-token-template.md`: token 分类、字段、默认值和填写规则。
- `references/platform-web.md`: Web / Web 后台 / SaaS 的 UI 规范重点。
- `references/platform-ios.md`: iOS App 的 UI 规范重点。
- `references/platform-android.md`: Android App 的 UI 规范重点。
- `references/checklist.md`: 产出前自检清单。

## 何时触发哪条路径

先判断 `docs/UI_SPEC.md` 是否已存在:

- **不存在** -> 走「新建 UI 规范」流程。
- **已存在**,且用户在调整视觉风格、token、组件规范、目标平台或页面 UI 规则 -> 走「UI 规范变更」流程。

## 新建 UI 规范流程

### Step 1. 读取上游文档

按顺序检查并读取:

1. `docs/PRD.md`:产品定位、目标用户、核心场景、业务优先级。
2. `docs/UX.md`:页面结构、用户流程、状态清单、空态/错误态/加载态。
3. `docs/TECH_DESIGN.md`:目标平台、端范围、前端技术约束、已定组件库或系统能力。只把它当作平台和实现约束,不要在本 skill 里重新选型。

如果上游文档不存在,不要卡住;根据用户当前描述继续,但在「开放问题与假设」里说明本 UI 规范尚未经过对应上游文档对齐。

### Step 2. 判断目标平台

从用户当前请求和 `docs/TECH_DESIGN.md` 判断本次只服务一个目标平台:

- **Web / Web 后台 / SaaS / 管理端 / 浏览器** -> 读取 `references/platform-web.md`。
- **iOS / iPhone / iPad / App Store / SwiftUI/UIKit** -> 读取 `references/platform-ios.md`。
- **Android / Material / Google Play / Kotlin/Compose** -> 读取 `references/platform-android.md`。

如果技术方案里有多个平台,但用户没有说本次做哪一端,先问用户选择一个,不要直接输出全平台大合集。推荐问法:

> 这份 UI 规范要先服务哪个端?Web 后台、iOS App、Android App 里选一个即可;我会只写这个平台的 UI_SPEC,其他端后续单独出。

如果用户明确要求多个平台,建议拆成多份文档,例如 `docs/UI_SPEC.web.md`、`docs/UI_SPEC.ios.md`,不要在一份文档里交叉混写平台规则。

### Step 3. 结构化访谈

不要凭个人审美直接写配色。UI 规范要服务目标用户、业务气质、平台习惯和团队实现能力。已在 PRD/UX/TECH_DESIGN 写清楚的不要重复问;一次问 2-4 个关键问题。

优先澄清:

1. 产品气质与品牌方向:稳重、效率、温暖、科技、年轻、医疗感、教育感等。
2. 目标用户与使用环境:高频专业操作、低频消费操作、移动现场操作、管理者扫视等。
3. 信息密度:紧凑、标准、宽松;只对当前目标平台判断。
4. 视觉偏好:主色、中性色、字体气质、圆角、阴影、图标风格。
5. 核心组件范围:导航、按钮、表单、表格/列表、卡片、弹窗、Toast、图表、上传、步骤条等。
6. 可访问性与模式:暗色模式、键盘可达、对比度、触控尺寸、弱网/低性能设备。

### Step 4. 读取模板与平台 reference

正式产出前读取:

- `assets/ui-spec-template.md`
- `assets/design-token-template.md`
- Step 2 确定的平台 reference
- `references/checklist.md`

只把平台 reference 中适用于当前目标平台的内容写进文档。例如目标是 Web 后台,就不要展开 iOS 导航栏、Android Material 组件或移动端底部导航规则。

### Step 5. 产出 UI_SPEC

默认写入 `docs/UI_SPEC.md`。如果用户明确要求多个平台,或已有文档已经被某个平台占用,建议写入带平台后缀的文件并说明原因,例如:

- `docs/UI_SPEC.web.md`
- `docs/UI_SPEC.ios.md`
- `docs/UI_SPEC.android.md`

产出要求:

- 使用 `assets/ui-spec-template.md` 的一级/二级标题结构。
- 使用 `assets/design-token-template.md` 的 token 分类和值域,并根据产品气质给出具体建议。
- 组件规范按「用途 -> 结构 -> 变体 -> 状态 -> 验收标准」写。
- 状态必须和 UX 对齐,但不要重写 UX 流程。
- 页面级规则只覆盖当前目标平台的关键页面。
- 可访问性写成检查项。
- 记录开放问题、假设和变更记录。

## UI 规范变更流程

当 `docs/UI_SPEC.md` 或平台化 UI_SPEC 已存在、用户要调整视觉风格、token、组件状态或页面 UI 规则时:

1. 先读现有 UI_SPEC,确认它服务的平台。
2. 同步读取 PRD/UX/TECH_DESIGN 中相关变更。
3. 如果用户要求的是另一个平台,不要把规则混进旧文档;新建或建议新建对应平台文件。
4. 原地修改对应章节,保持文档是当前平台的最新 UI 事实源。
5. 评估影响范围:改主色会影响按钮、链接、焦点、图表和状态色;改间距会影响表格密度和移动端布局。
6. 在「变更记录」表追加一行:日期、类型、内容、原因、影响范围。

## 边界

- 属于本 skill:单一目标平台的视觉方向、Design Tokens、布局栅格、组件视觉规范、页面级 UI 规则、状态样式、响应式或移动适配、可访问性检查清单。
- 不属于本 skill:功能范围、用户故事、用户流程、信息架构、交互反馈逻辑、技术栈/组件库选型、数据库设计、前端代码、Figma/Sketch 文件或图片设计稿。

如果用户要求"帮我写 React 组件"或"选 shadcn/ui 还是 Ant Design",把结论归属提示清楚:前者是开发实现,后者是 dev-kickoff。然后把工作拉回"当前目标平台的界面规则和视觉标准怎么定义"。
