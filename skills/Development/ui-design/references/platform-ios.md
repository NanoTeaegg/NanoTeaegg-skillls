# iOS UI 规范参考

适用于 iPhone、iPad、iOS App。

## 平台重点

- 遵循 iOS 用户对导航、手势、系统控件和安全区域的预期。
- 触控优先,控件尺寸、手势反馈和页面转场比桌面信息密度更重要。
- 尽量使用系统语义:Navigation Bar、Tab Bar、Sheet、List、Form、Swipe Action。
- iPad 需要单独说明分栏、弹窗和横竖屏适配。

## 布局规则

- iPhone 常用底部 Tab 承载一级入口,Navigation Bar 承载页面标题和少量操作。
- 复杂编辑任务可使用分步页面或 Sheet,不要照搬 Web 大表单。
- 列表页强调触控行高、分组、搜索和滑动操作。
- 详情页主操作可固定在底部安全区上方。
- iPad 可用 Split View 或双栏布局,但仍要保持触控尺寸。

## iOS 组件清单

至少按需覆盖:

- Navigation Bar、Tab Bar、Toolbar。
- Button、Icon Button、Destructive Action。
- List、Grouped List、Card。
- Form、Picker、Date Picker、Search。
- Sheet、Alert、Action Sheet。
- Toast 替代方案:轻提示、Banner 或页面内状态。
- Empty State、Error State、Loading。

## iOS 可访问性

- 触控目标建议不小于 44 等效尺寸。
- 支持动态字体或至少说明字体缩放策略。
- VoiceOver 标签要能描述按钮和状态。
- 状态不能只靠颜色表达。

## iOS 禁区

- 不要写 Web 表格密度、桌面 hover 规则或键盘快捷键优先的模式。
- 不要写 Android Material 专属组件。
- 不要输出 SwiftUI/UIKit 代码。
