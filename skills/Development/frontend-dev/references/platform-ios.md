# iOS 前端实现规范

适用于 SwiftUI 和 UIKit，针对 iPhone/iPad App Store 应用。

## Token 对接

- UI_SPEC 里定义的颜色 token 在 Xcode Asset Catalog 中创建对应 Color Set，支持 Light/Dark 两套。
- 不在代码里写 `Color(hex: "#1677ff")`，用 `Color("primary")` 或 `Color.primary`（Asset Catalog 命名与 UI_SPEC token 一致）。
- 字体：如 UI_SPEC 指定自定义字体，注册到项目 Info.plist；否则用系统 SF Pro，通过 `Font.system(size:weight:design:)` 控制。

## SwiftUI 关键规则

- **状态驱动**：每个 View 的显示态由 `@State`/`@Binding`/`@ObservedObject` 的数据驱动，不手动操作 UI 元素。
- **组件状态**：按钮的 `disabled`/`loading`/`pressed` 状态用 `.disabled()` modifier + 自定义 ButtonStyle 实现，不用透明度技巧。
- **安全区**：用 `.safeAreaInset()` 或 `safeAreaPadding`，不用写死数值。
- **动态字体（Dynamic Type）**：文本用 `.font(.body)` / `.font(.headline)` 等语义字号，不写死 `.system(size: 16)`；除非 UI_SPEC 明确不支持动态字体。

## UIKit 关键规则

- Auto Layout 为主，SnapKit/Anchors 均可；不用 frame 赋值布局。
- 色彩用 `UIColor(named:)` 从 Asset Catalog 读取，支持 `traitCollection` 深色模式切换。
- 复杂列表用 `UICollectionView` + Diffable Data Source，避免 `reloadData()` 引起闪烁。

## 交互 & 动效

- 轻交互（按钮弹簧）用 `withAnimation(.spring())` / `UIView.animate(withDuration:)`。
- 滚动联动、复杂转场在 UI_SPEC 里明确了档位才实现，不自行添加。
- `UIFeedbackGenerator` 用于触觉反馈（按钮点击/成功/错误），配合 UX.md 的反馈设计。

## 可访问性

- 所有自定义控件设置 `accessibilityLabel` 和 `accessibilityHint`。
- 图标按钮（无文字）必须有 `accessibilityLabel`。
- 颜色对比度满足 WCAG AA（4.5:1 文本，3:1 大文本/UI 组件）。
- VoiceOver 逻辑顺序与视觉顺序一致（SwiftUI 用 `.accessibilitySortPriority()`）。

## 常见坑

- `LazyVStack`/`LazyHStack` 的 item 不要放太重的 View 初始化逻辑，会首屏卡。
- SwiftUI sheet 和 fullScreenCover 的 `isPresented` 绑定来自父视图，不在子视图里 dismiss 自身（除非用 `@Environment(\.dismiss)`）。
- UIKit 的 `viewDidAppear` 不要做 layout 计算，用 `viewDidLayoutSubviews`。

## 验收清单

- [ ] 颜色来自 Asset Catalog Color Set，支持 Dark Mode
- [ ] 自定义字体已注册，或系统字体按语义使用
- [ ] 按钮所有状态（normal/disabled/loading/pressed）均有样式
- [ ] 安全区处理正确（没有内容被刘海/Home Bar 遮挡）
- [ ] Dynamic Type 未写死字号（或 UI_SPEC 明确豁免）
- [ ] VoiceOver label 在所有自定义控件上设置
- [ ] UX.md 中所有状态（加载/空/错误）均有对应实现
- [ ] 深色模式外观正确（如 UI_SPEC 支持）
