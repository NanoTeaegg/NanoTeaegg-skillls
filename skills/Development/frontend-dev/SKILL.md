---
name: frontend-dev
description: 前端实现 skill——按 UI_SPEC/UX/TECH_DESIGN 已明确的规范，写出可运行的界面代码（Web/iOS/Android）。当用户要把设计文档/界面规范落地为代码、修改/验收已有界面时触发。不含需求变更（→ requirements-definition）、交互/视觉规范定义（→ ux-design/webui-design-system）、架构选型（→ dev-kickoff）。
version: v0.3
---

# 前端实现(Frontend Dev)

把已经明确的界面规范、交互方案和技术文档，转换成真实可运行的前端代码。这个 skill 回答的是：**某一个目标平台上的界面，按文档规定应该怎么写出来，写完后如何验证它对齐了规范**。

## 为什么需要这一步

UI_SPEC、UX、TECH_DESIGN 三份文档共同构成了"代码应该是什么样"的事实源。没有这一步，开发者要么自己猜设计意图、要么反复和设计/产品来回确认，是重大沟通成本和返工来源。Frontend-dev skill 的核心价值是：**把文档里的规定直接翻译成代码**，出现分歧时先对齐文档而不是对齐个人习惯，不能确定时问用户而不是猜。

## 何时走哪条路径

先判断目标文件是否已存在：

- **不存在** → 走「新建前端代码」流程
- **已存在**，用户要修改页面/组件/样式/交互 → 走「修改迭代」流程

## 新建前端代码流程

### 第 1 步：读取上游文档

按顺序检查并读取（有则读，无则跳过并记录）：

1. `docs/UI_SPEC.md`（或平台化变体 `UI_SPEC.web.md` / `UI_SPEC.ios.md` / `UI_SPEC.android.md`）：Design Token、组件规范、状态样式、响应式策略、可访问性要求。**这是最重要的实现依据。**
2. `docs/UX.md`：用户流程、界面状态清单（正常/加载/空/错误/禁用）、交互反馈逻辑、边界情况。
3. `docs/TECH_DESIGN.md`：目标平台、技术栈、组件库、路由方案、已定架构约束。
4. `docs/PRD.md`：核心场景和验收标准（按需参考，不重复读已覆盖的内容）。

如果 UI_SPEC 不存在，不要自行发明视觉规则——告诉用户"还没有 UI_SPEC.md，建议先用 webui-design-system skill 产出一份，或者你把关键视觉决策告诉我，我记录下来后继续"，等确认后再写代码。

### 第 2 步：判断目标平台 & 技术栈

从 TECH_DESIGN 或用户当前请求中明确：

- **Web**：读 `references/platform-web.md`，确认框架（React / Vue / Next.js / 纯 HTML 等）、样式方案（CSS Modules / Tailwind / styled-components）、组件库（如 shadcn/ui、Ant Design、Element Plus）。
- **iOS**：读 `references/platform-ios.md`，确认 SwiftUI 还是 UIKit、导航栈、状态管理方案。
- **Android**：读 `references/platform-android.md`，确认 Compose 还是 XML、导航组件、主题方案。

如果平台不明确，先问用户，不要输出跨平台混合代码。

### 第 3 步：澄清歧义（仅在必要时）

上游文档通常已经覆盖了大多数决策。只在以下情况下向用户确认：

- UI_SPEC 和 UX 对同一个状态描述有矛盾
- 文档未覆盖、但对实现有影响的决策（例如空态显示策略、动效是否需要、某个边界情况的处理方式）
- 用户要求的功能超出了文档范围

**一次问 2-3 个问题，不要出长列表。等用户回答后再动笔写代码。**

### 第 4 步：写前端代码

按照上游文档的规定逐步实现：

**Token 对齐（Web 优先关注）**
- 颜色、字体、间距、圆角、阴影必须从 UI_SPEC 的 Design Token 读取，不要硬编码 hex 或 px 值。
- CSS 变量在项目入口统一声明，组件内引用变量名而非数值。

**组件实现**
- 按 UI_SPEC 中「用途 → 结构 → 变体 → 状态」的顺序实现，每个变体和状态都要覆盖。
- 状态样式（hover / focus / active / disabled / loading / error）不能只实现 default 态。
- 先实现文档中明确定义的组件，再处理文档没有覆盖的边界组合。

**UX 状态逻辑**
- UX.md 里的状态清单是必须实现的验收条件：正常态、加载态、空态、错误态、禁用态逐一落地。
- 错误处理、边界情况和非常规路径按 UX 文档实现，不要只处理 happy path。

**响应式 & 平台规则**
- Web：按 UI_SPEC 定义的断点实现响应式，移动端触摸目标 ≥ 44×44px，无横向溢出。
- iOS：遵循 SafeArea、Dynamic Type、深色模式（若 UI_SPEC 有定义）。
- Android：遵循 Material 主题、适配不同屏幕密度、处理系统手势区域。

**可访问性（按 UI_SPEC 要求）**
- 键盘 focus 必须可见且不被 hover 样式覆盖（Web）。
- 错误态不只靠颜色，必须有文案提示。
- 图片和图标有 alt / contentDescription。

### 第 5 步：自审与验收

代码写完后，对照以下清单自审，不满足的就地修：

- 读 `references/platform-{web|ios|android}.md` 的验收清单逐项检查。
- 所有 UI_SPEC 中的 Design Token 都正确引用（无硬编码）。
- UX.md 里所有状态都有对应实现。
- 响应式在最小断点和桌面端都无明显问题。
- 如果文档定义了动效档位（L1/L2/L3），对应交互已实现。

完成后告诉用户：实现了哪些页面/组件、哪些文档规定已对齐、哪里有开放问题或文档需要补充，以及建议用 testing-quality skill 做验收测试。

## 修改迭代流程

当目标文件已存在，用户要修改样式、交互、组件或页面时：

1. **先读现有代码**，理解当前实现，再动手——不在没读全的情况下改。
2. **读对应的上游文档变更**：如果是 UI_SPEC 改了颜色/token，就读 UI_SPEC 最新版；如果是 UX 改了流程，就读 UX 最新版。
3. **精准修改对应部分**，保持已有代码风格一致，不要顺手重构无关代码。
4. **评估改动影响范围**：改 token 会影响引用该 token 的所有组件；改导航逻辑会影响所有依赖该路由的页面——在回复里说明影响范围。
5. 如果修改让代码和文档产生了新的分歧（比如 UX 文档还没更新），记录到开放问题里，而不是把文档当作错的那个。

## 文档与代码的分歧处理

遇到代码实现和文档规定有矛盾时，优先级顺序：

```
UI_SPEC.md > UX.md > TECH_DESIGN.md > 个人判断
```

1. UI_SPEC 说 primary 按钮背景是 `--color-primary`，代码不要用 `#1677ff`，即使视觉上一样。
2. UX 说空态显示「暂无数据」插图 + 引导文案，不能只用一行灰色文字。
3. 如果文档规定和技术约束真的有冲突，**告诉用户**，而不是悄悄取一个折中。

## 边界：这个 skill 不做什么

- ❌ 修改产品功能范围 → requirements-definition
- ❌ 重新设计用户流程或信息架构 → ux-design
- ❌ 调整 Design Token、修改视觉规范 → webui-design-system
- ❌ 数据库表结构、字段设计 → database
- ❌ 后端 API 实现、服务端业务逻辑 → 后端开发
- ❌ 架构选型、技术栈决策 → dev-kickoff

如果用户在写代码过程中发现 UX 流程有问题，先记录、继续实现当前文档版本，然后建议用 ux-design 更新文档，而不是在代码里绕开文档规定。

## 参考文件

| 文件 | 内容 | 何时读 |
|------|------|--------|
| `references/platform-web.md` | Web 实现规范、验收清单、常见坑 | 目标平台是 Web 时 |
| `references/platform-ios.md` | iOS 实现规范、SwiftUI/UIKit 要点、验收清单 | 目标平台是 iOS 时 |
| `references/platform-android.md` | Android 实现规范、Compose/XML 要点、验收清单 | 目标平台是 Android 时 |
