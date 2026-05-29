# Android UI 规范参考

适用于 Android App、Android 平板、Material 风格移动应用。

## 平台重点

- 遵循 Android 用户对返回、系统导航、Material 组件、触控反馈的预期。
- 使用 Material 语义描述组件和状态,但不要替技术方案选 Compose/XML/MDC。
- 移动端以触控、可读性、离线/弱网状态和系统反馈为重点。

## 布局规则

- 一级入口可用 Navigation Bar、Navigation Rail 或 Drawer,根据屏幕尺寸选择。
- 列表页使用触控友好的 row/card,支持搜索、筛选、空态和错误态。
- 主操作可使用显眼按钮或 Floating Action Button,但同屏不要堆多个主操作。
- 平板端可使用双栏或导航 rail,不要简单拉伸手机布局。

## Android 组件清单

至少按需覆盖:

- Top App Bar、Navigation Bar、Navigation Rail、Drawer。
- Button、Icon Button、FAB、Segmented Button。
- Text Field、Select、Date Picker、Search。
- List、Card、Chip、Tabs。
- Dialog、Bottom Sheet、Snackbar。
- Empty State、Error State、Loading。

## Android 可访问性

- 触控目标建议不小于 48 等效尺寸。
- 状态要有 content description 或可读文本承载。
- Snackbar 不应遮挡底部主操作。
- 动效要克制,避免影响低端设备。

## Android 禁区

- 不要写 Web hover 表格规则。
- 不要写 iOS 专属 Navigation Bar / Tab Bar 行为。
- 不要输出 Kotlin/Compose/XML 代码。
