# Web 设计系统契约（UI_SPEC）

精简、可执行的 AI 契约。业务代码生成时读它，人评审时读它。不写审美散文。

## 1. 文档信息

- 文档:
- 项目 / 定位:
- 状态 / 日期:
- 输入文档: （PRD / UX / TECH_DESIGN 是否存在）
- 本文档只覆盖: Web 单平台设计系统
- 明确不覆盖: 业务页面、后端/数据库、原生 iOS/Android
- 同步产物（事实源）:
  - 值源: `design-system/tokens.css`
  - 组件库: `design-system/components.css`(+ 可选 `components.js`)
  - 观测窗: `design-system/preview.html`(+ 工具外壳 `preview.css` / `preview.js`)

## 2. 工程映射

- UI 层技术选择: CSS Variables 作为底层 token；（如有 Tailwind/shadcn/Radix）只做映射，不另起组件系统。
- Token 输出格式: `:root` 暗色或浅色默认 + 切换选择器。
- 组件库策略: `.ds-*` class，业务页面只复用、不自写样式。
- 文档站点方式: 静态 `preview.html` 引用 tokens.css/components.css 渲染真实 token 与真实组件。

## 3. Design Tokens

按 `design-token-template.md` 分类，给具体值与代码映射。

### 3.1 颜色 ｜ 3.2 字体 ｜ 3.3 间距 ｜ 3.4 圆角/边框/阴影 ｜ 3.5 层级/动效 ｜ 3.6 图标/图表

（每类一张表：Token / 值 / 用途 / 代码映射 / 禁止用法。动效含 duration + ease。）

## 4. 基础 UI 约定（一页硬规则，所有页面必须遵守）

不逐组件展开，只列十几条能直接判对错的硬规则，例如：

- 只准用 `var(--token)` 和 `.ds-*` class；禁止裸 hex / px / ms / cubic-bezier。
- 同一区域只允许一个 primary 操作。
- 表单标签外置；字段级错误用行内文案，不用 Toast 替代。
- 状态（running/done/failed…）不只靠颜色，必带文字或图标。
- 所有可交互控件可键盘聚焦，focus ring 不被 hover 覆盖。
- 暗色分层用 border 建层级，不靠扩散阴影；不直接取反亮色。
- 动效只用 motion token；进出场用 `ease-standard` / `ease-exit`。

## 5. 组件库（回收制）

组件不前置定死。**第一次**需要某组件，直接按基础约定建；**第二次**要复用时，才回收进 `components.css` 并在此登记。

### 已登记组件

每个登记组件按下列结构写（保持精简）:

#### 5.x 组件名 · `.ds-xxx`

- 用途:
- 变体 / class:
- 状态: default / hover / active / focus / disabled（+ 组件特有态）
- Token 依赖:
- 行为与动效编排:（若有交互，写「触发 → 过程 → 时长/缓动 token」，实现归 `components.js`）
- 禁止用法:

## 6. 布局法则

- 页面最大宽度 / 栅格 / 断点:
- 导航结构:
- 页面密度:

## 7. AI 落地约束

- 允许: tokens.css 变量、components.css 的 `.ds-*`、motion token、文档站 demo pattern。
- 禁止: 裸值、页面内自写组件样式、复制粘贴重复样式块、未登记的临时状态色。
- 组件缺口: 优先复用 → 不足加变体 → 仍不足新增组件（第二次复用时回收）。新增影响面大的组件要通知维护者。
- 可由 `scripts/lint_tokens.py` 校验裸值/裸动效。

## 8. 设计系统文档站点验收清单

- 左侧导航分组: 全局变量 / 基础组件 / 业务组件或模式 / 规范。
- token 章节: 颜色（带对比度徽章 + 复制 hex）、字体、间距、圆角、阴影、动效。
- 组件章节: 每个组件有用途、demo（真实 class 渲染）、状态、代码、Dos and Don'ts。
- preview 引用 tokens.css/components.css，**不内联重写组件样式**（不漂移铁规则）。
- 浅/深色切换；header 显示 token 版本。

## 9. 可访问性与可用性

- 对比度: 正文 ≥ 4.5:1，UI 控件 ≥ 3:1。
- 焦点/键盘 / 状态表达 / 移动端降级:

## 10. 非目标与边界

（业务页面、后端、原生端、Figma 稿等不在范围。preview.html 是文档站，不是产品页。）

## 11. 开放问题与假设

## 12. 变更记录

| 日期 | 类型 | 内容 | 原因 | 影响范围 | 同步文件 |
|---|---|---|---|---|---|

> token/组件变更可用 `scripts/diff_tokens.py` 对比两版自动生成条目。
