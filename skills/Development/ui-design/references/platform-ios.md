# iOS UI 规范参考

适用于 iPhone App、iPad App（iOS 16+，遵循 Apple HIG）。

---

## 平台重点

- **触控优先**：没有 hover，所有状态反馈靠 press/focus/selection。
- **系统语义**：Navigation Bar、Tab Bar、Sheet、List、Alert 是用户已经学会的范式，不要无故替换成自定义控件。
- **安全区（Safe Area）**：底部 Home Indicator、顶部刘海/灵动岛区域必须尊重，内容不能溢出。
- **Dynamic Type**：系统字体大小由用户控制，UI 规范需说明是否支持缩放或写明豁免理由。
- **深色模式**：iOS 深色模式是系统级强制，必须定义 Light/Dark 两套颜色，无法单独关闭。

---

## Token 默认值区间（iOS 产品 UI 参考）

```
系统色（直接用，无需定义 token）：
  Primary Action    systemBlue (#007AFF)
  Destructive       systemRed  (#FF3B30)
  Success           systemGreen (#34C759)
  Warning           systemOrange (#FF9500)
  Label（主文字）    label / #000000(亮) / #FFFFFF(暗)
  SecondaryLabel    secondaryLabel / #3C3C43@60%(亮) / #EBEBF5@60%(暗)
  TertiaryLabel     tertiaryLabel / #3C3C43@30%(亮)
  Separator         separator / #3C3C4349(亮) / #54545899(暗)
  systemBackground  #FFFFFF(亮) / #000000(暗)
  secondaryBackground #F2F2F7(亮) / #1C1C1E(暗)
  tertiaryBackground #FFFFFF(亮) / #2C2C2E(暗)

自定义主色（品牌色，叠加在系统色上）：
  推荐范围：同 Web，但避免与系统红/绿/橙撞色造成语义混乱
  定义两个变体：light mode hex + dark mode hex
  品牌色不能仅靠数值硬编码——Asset Catalog Color Set 分层定义

触控目标最小尺寸：44×44pt（等效 px 依屏幕密度）

字体（SF Pro 系统字体层级）：
  largeTitle  34pt  Regular
  title1      28pt  Regular
  title2      22pt  Regular
  title3      20pt  Regular
  headline    17pt  Semibold
  body        17pt  Regular（正文首选）
  callout     16pt  Regular
  subheadline 15pt  Regular
  footnote    13pt  Regular
  caption1    12pt  Regular
  caption2    11pt  Regular

自定义字体：注册到 Info.plist，SwiftUI 中用 .custom("FontName", size: ..., relativeTo: .body)

圆角（iOS 风格偏大）：
  系统默认卡片/Sheet  continuousCornerRadius≈13pt（使用 .continuous RoundedCorners）
  按钮小圆角          8-10pt
  Pill 按钮            radius = height/2
  大卡片/封面         16-20pt

间距（8pt 栅格）：
  xs=4  sm=8  md=16  lg=20  xl=24  2xl=32  3xl=48

阴影（iOS 偏轻/少用）：
  列表行 shadow 通常为 none（用 separator 分隔）
  浮层/Card  0 2px 8px rgba(0,0,0,0.12)
  深色模式改为 border 而非阴影
```

---

## 组件状态矩阵（iOS）

iOS 没有 hover，状态简化为：

| 状态 | 触发条件 | 视觉规则 |
|---|---|---|
| **default** | 正常显示 | 完整样式 |
| **highlighted/pressed** | 手指按压瞬间 | opacity 降至 0.5（系统默认）或背景变色 |
| **selected** | 已选中（Tab/checkbox/item） | 主色填充 / 主色文字 |
| **disabled** | 不可操作 | opacity 0.4，移除 tap gesture |
| **loading** | 异步等待 | ActivityIndicator / ProgressView，按钮显示 spinner |
| **focused**（iPadOS/外接键盘） | 键盘 Tab 导航 | 系统 focus ring，不要覆盖 |

**SwiftUI 按钮五态定义模板**
```
ButtonStyle:
  default:     background = primaryColor, foreground = white
  pressed:     background = primaryColor.opacity(0.85), scale = 0.97
  disabled:    background = primaryColor.opacity(0.4)
  loading:     显示 ProgressView，按钮 .disabled(true)
  destructive: background = systemRed
```

---

## 布局规则

**iPhone 导航范式**
- 一级入口：底部 Tab Bar（4-5 个 tab，系统 UITabBar 或 SwiftUI TabView）
- 页面间：Navigation Stack（push/pop）
- 编辑/表单：Sheet（modal，不是 push，保留返回语义）
- 确认操作：Alert（系统级）或 ActionSheet（选项多时）

**内容密度（iPhone）**
- List 行高建议 ≥44pt；带副标题行 ≥56pt
- 卡片之间水平边距 16pt；卡片内容 padding 16pt
- 全面屏底部按钮：固定在安全区上方 16pt，不要 fixed to safeArea.bottom=0

**iPad 适配（如范围内）**
- 需单独说明：Split View（UISplitViewController / NavigationSplitView）
- 是否支持多窗口（Scene）
- Keyboard + Pointer（鼠标/触控板）可访问性

---

## 深色模式策略

- **所有颜色必须使用 Asset Catalog Color Set**，分别定义 Light/Dark variant
- 不能用 `Color(hex:)` 硬编码——系统切换深色时不会自动反转
- 语义色：优先用 `Color(.label)` 等系统 semantic color，不受硬编码色影响
- 图标：SF Symbols 自动适配深浅，自定义图标需提供两套或用 template rendering

---

## 常用组件规范要点

### Navigation Bar
- 标题：Large Title（首屏滚动收缩）/ Inline Title（子页面）
- 右侧操作：最多 2 个 BarButtonItem，过多时用"..."菜单
- Back 按钮文字：通常显示上一级标题，规范中说明是否自定义

### Tab Bar
- 图标：SF Symbols 优先；自定义图标提供 filled + outlined 两态
- 角标（Badge）：数字徽标不超过 3 位（99+），颜色用系统红
- 隐藏规则：Tab Bar 何时隐藏（进入详情页时）需在规范中明确

### List / 表单
- 分组：Grouped List（设置页风格）/ Plain List（内容列表）
- 滑动操作：Trailing swipe（删除/归档）/ Leading swipe（标记已读）
- 占位：空态必须有插图 + 标题 + 引导按钮（不能只留白）

### Sheet
- Detent：.medium（半屏）/ .large（全屏），iOS 16+ 支持 custom detent
- 关闭方式：拖拽关闭（默认）+ 明确的"关闭/取消"按钮（规范中说明）

---

## 视觉风格参考

iOS 产品 UI 参考时，优先查 `references/design-systems/` 中的移动端友好品牌：

| 风格方向 | 参考 |
|---|---|
| 极简效率 | `linear.app`（有 iOS App）|
| 金融/支付 | `revolut` `wise` |
| 消费/社交 | `spotify` `airbnb` `pinterest` |
| AI 产品 | `claude` `elevenlabs` |

若品牌库中无合适参考，使用 `references/mobile-inspiration.md` 中的 WebSearch 方法获取截图。

---

## 可访问性红线

- 所有自定义控件必须设置 `accessibilityLabel`（无文字的图标按钮必须）
- 触控目标 ≥ 44×44pt
- 语义色不能只靠颜色区分状态（错误态必须有文案）
- 支持 Dynamic Type 或在规范中明确豁免理由
- VoiceOver 阅读顺序与视觉顺序一致

---

## iOS 禁区

- 不要写桌面端 hover 规则
- 不要写 Android Material 专属组件（Snackbar、FAB 等）
- 不要在 UI_SPEC 里输出 SwiftUI/UIKit 代码
- 不要把 Web 管理后台的表格密度照搬到 iOS
- 不要自定义返回手势（系统手势不可被覆盖或静默拦截）
