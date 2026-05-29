# Web 前端实现规范

适用于 Web 后台、SaaS 工作台、Landing Page、C 端应用、浏览器应用。

## Token 与样式

- **所有颜色必须通过 CSS 变量引用**，UI_SPEC 里的 token 名原样用，不转成硬编码 hex。
  ```css
  /* ✅ */ background-color: var(--color-primary);
  /* ❌ */ background-color: #1677ff;
  ```
- CSS 变量在 `:root` 统一声明，组件文件不重复定义同名变量。
- 间距、圆角、阴影、字体也走 token，不用魔法数字。

## 组件状态

- 每个交互元素必须有 `hover`、`focus`、`active`、`disabled` 样式，不能只有 default。
- `focus-visible` 优于 `focus`（避免鼠标点击时出现键盘 focus 环）。
- `disabled` 状态：`pointer-events: none` + 降低透明度，不要只去掉 cursor。

## 响应式

- 断点从 UI_SPEC 读取；如果 UI_SPEC 未定义，默认：mobile ≤ 767px，tablet 768-1199px，desktop ≥ 1200px。
- 移动端所有可点击目标 ≥ 44×44px（包括图标按钮）。
- 不能有横向溢出（`overflow-x: hidden` 不算解决，是掩盖问题）。
- 表格在移动端降级为摘要卡片或横向滚动容器，不照搬桌面表格。

## 可访问性

- `<img>` 有 `alt`；装饰性图片用 `alt=""`。
- 表单 `<input>` 与 `<label>` 关联（`for` / `aria-labelledby`）。
- 错误信息不只靠红色，必须有字段级文案。
- 键盘 Tab 顺序与视觉阅读顺序一致。
- 模态框打开时焦点进入弹窗，关闭后焦点回到触发元素。

## 动效实现

- L1（精致静态）：`transition` 用 `ease-out`，时长 150-200ms，hover/enter 场景。
- L2（流畅交互）：`IntersectionObserver` 触发入场动画；导航滚动态用 scroll listener + `requestAnimationFrame`。
- L3（沉浸）：GSAP/ScrollTrigger，单页 pin ≤ 2 处；WebGL 场景 ≤ 1 个，不可见时暂停。
- **必须实现 `prefers-reduced-motion` 降级**：L2/L3 动效检测到该媒体查询时还原为静态或 opacity 淡入。

## 常见坑

- `z-index` 不用超过 1000 的随意数字，建立层级变量（`--z-modal: 300`）。
- 不用 `!important` 覆盖第三方组件库样式，用 CSS Modules scoping 或更高优先级选择器。
- 图片避免纯色块占位；loading 骨架屏比色块好，真实图片比骨架屏好。
- 异步数据请求：加载态、错误态、空态、正常态四态都实现，不只写正常态。

## 验收清单

- [ ] 所有颜色来自 CSS 变量，零硬编码 hex
- [ ] 组件所有状态（hover/focus/active/disabled）均有样式
- [ ] 移动端 ≤ 767px 无横向溢出，触摸目标 ≥ 44×44px
- [ ] 桌面端和移动端布局都正确
- [ ] `prefers-reduced-motion` 降级（如有 L2/L3 动效）
- [ ] 图片有 alt，表单有 label 关联
- [ ] 错误态有文案提示，不只靠颜色
- [ ] UX.md 中所有状态（加载/空/错误）均有对应实现
