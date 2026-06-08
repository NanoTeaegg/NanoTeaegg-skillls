# Design Token 与代码映射模板

Design Tokens 要表达"语义角色 + 推荐值/规则 + 使用场景 + 代码映射",不要只罗列颜色或尺寸。以下分类和标题结构应在 UI_SPEC 和设计系统代码中保持一致。

## Token 输出字段

| 字段 | 说明 |
|---|---|
| Token | 语义化名称,优先用 `color-bg-page`、`space-4` 这类稳定名称 |
| 值 | 平台值,如 hex/rem/px/pt/dp/sp |
| 用途 | 允许使用的组件或场景 |
| 代码映射 | Web CSS variable / Tailwind key / Swift/Kotlin 常量 |
| 禁止用法 | 避免 token 被误用 |

## 代码映射规则

- Web:每个 token 至少映射到 CSS variable,例如 `--color-primary`;使用 Tailwind 时同步映射到 `colors.primary` 或等效 key。
- iOS:每个 token 映射到 `DesignTokens` 静态常量或 Asset Catalog semantic color 名称。
- Android:颜色优先映射到 Material 3 Color Role 或 `DesignTokens` Kotlin object。
- HTML 文档站点必须读取或内嵌同一套 token,不能出现与代码文件不一致的临时值。
- 颜色、字体、间距、圆角/阴影 token 必须在文档站点中有独立章节,每个章节包含 token 表格、视觉样本、使用规则和代码展示。

## 颜色 Tokens

| Token | 推荐值/规则 | 用途 | 代码映射 | 禁止用法 |
|---|---|---|---|---|
| `color-bg-page` | 页面底色,通常为浅灰/深灰/系统背景 | 页面背景 | `--color-bg-page` | 不用于卡片正文底色 |
| `color-bg-surface` | 卡片、表格、弹窗底色 | 内容容器 | `--color-bg-surface` | 不要过度依赖阴影 |
| `color-text-primary` | 最高对比正文色 | 标题、主要数字、正文 | `--color-text-primary` | 不用于禁用态 |
| `color-text-secondary` | 中等对比文字色 | 注释、辅助说明 | `--color-text-secondary` | 不承载关键信息 |
| `color-border-subtle` | 低对比分隔线 | 表格、输入、卡片 | `--color-border-subtle` | 不作为 focus ring |
| `color-primary` | 产品主色 | 主按钮、链接、选中态、焦点态 | `--color-primary` | 不要和危险色接近 |
| `color-success` | 成功语义色 | 成功、启用、增长 | `--color-success` | 不只靠颜色表达 |
| `color-warning` | 警告语义色 | 待处理、风险提醒 | `--color-warning` | 避免与主色冲突 |
| `color-danger` | 危险语义色 | 删除、取消、错误 | `--color-danger` | 高风险动作专用 |
| `color-chart-1..8` | 低饱和可区分色组 | 图表系列 | `--color-chart-*` | 不跨语义复用 |

## 文字 Tokens

| Token | 推荐值/规则 | 用途 | 代码映射 | 禁止用法 |
|---|---|---|---|---|
| `font-family-base` | 平台默认优先,必要时用品牌字体 | 正文 | `--font-family-base` | 不破坏平台习惯 |
| `font-size-page-title` | Web 常用 20-24;移动端跟随平台标题层级 | 页面标题 | `--font-size-page-title` | 不用于卡片内小标题 |
| `font-size-section-title` | 16-18 | 区块标题 | `--font-size-section-title` | 不用于正文 |
| `font-size-body` | 14-16 | 正文 | `--font-size-body` | 不用于弱提示 |
| `font-size-caption` | 12-13 | 辅助说明 | `--font-size-caption` | 不承载核心操作 |
| `line-height-base` | 1.4-1.6 | 正文 | `--line-height-base` | 不用于按钮高度 |
| `font-weight-strong` | 600/700 或平台等效值 | 强调 | `--font-weight-strong` | 避免整页过粗 |

## 间距与布局 Tokens

| Token | 推荐值/规则 | 用途 | 注意事项 |
|---|---|---|---|
| `space-1` | 4 等效 | 极近元素 | 少量使用 |
| `space-2` | 8 等效 | 控件内部/小间距 | 高频使用 |
| `space-3` | 12 等效 | 表单、列表内部 | 高频使用 |
| `space-4` | 16 等效 | 区块内标准间距 | 默认基准 |
| `space-6` | 24 等效 | 区块间距 | 页面组织 |
| `space-8` | 32 等效 | 大区块间距 | 营销/低频页可用 |
| `content-max-width` | 按平台和信息密度定义 | 主内容宽度 | 后台不宜过窄 |

## 圆角、边框与阴影 Tokens

| Token | 推荐值/规则 | 用途 | 注意事项 |
|---|---|---|---|
| `radius-sm` | 4 等效 | 输入、标签、小按钮 | 工具型界面常用 |
| `radius-md` | 8 等效 | 卡片、弹窗、标准按钮 | 默认圆角 |
| `radius-lg` | 12-16 等效 | 移动端卡片或低频容器 | 后台慎用 |
| `border-width-default` | 1 等效 | 输入、表格、分隔线 | 比阴影更稳定 |
| `shadow-popover` | 轻量浮层阴影 | Popover、菜单 | 不用于所有卡片 |
| `shadow-modal` | 中等浮层阴影 | 弹窗 | 暗色模式需克制 |

## 层级与动效 Tokens

动效是设计系统的一等公民:组件的**行为/动效**（折叠展开、Toast 进出场、hover 反馈）必须只引用这里的 duration 和 ease token，业务/组件代码里不准裸写 `ms` 或 `cubic-bezier(...)`。动效的「编排」（先展开后淡入、谁先谁后）写在 UI_SPEC 组件规范里，不是 token。

| Token | 推荐值/规则 | 用途 | 注意事项 |
|---|---|---|---|
| `layer-dropdown` | 高于页面内容 | 菜单、选择器 | 不遮挡关键提示 |
| `layer-sticky` | 高于滚动内容 | 固定表头/工具栏 | 与弹窗分开 |
| `layer-modal` | 高于全部页面层 | 弹窗 | 只用于阻断式任务 |
| `motion-duration-fast` | 100-150ms | hover、focus、轻反馈 | 高频交互 |
| `motion-duration-medium` | 180-250ms | 折叠、弹窗、抽屉、局部切换 | 避免拖慢效率 |
| `motion-duration-slow` | 280-360ms | 大面积转场、loading | 少量使用 |
| `ease-standard` | `cubic-bezier(.2,0,0,1)` | 默认进出场 | 统一缓动入口 |
| `ease-emphasized` | `cubic-bezier(.3,0,0,1)` | 需要强调的进场 | 关键反馈 |
| `ease-exit` | `cubic-bezier(.4,0,1,1)` | 退出 / 收起 | 退出更快更利落 |

## 图标与数据可视化 Tokens

| Token | 推荐值/规则 | 用途 | 注意事项 |
|---|---|---|---|
| `icon-size-sm/md/lg` | 16/20/24 等效 | 按钮、导航、空态 | 与文字基线对齐 |
| `icon-stroke` | 1.5-2 等效 | 线性图标 | 保持统一风格 |
| `chart-grid` | 低对比网格线 | 图表辅助线 | 不抢主数据 |
| `chart-positive/negative` | 与语义色一致 | 增长/下降 | 加文字或符号辅助 |
