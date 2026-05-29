# Android UI 规范参考

适用于 Android App（Material Design 3，Android 12+）、Android 平板。

---

## 平台重点

- **Material 3（M3）**：2022 年后的 Android 设计标准，引入 Dynamic Color（壁纸取色）和 Color Role 体系。
- **触控 + Ripple**：所有可点击元素必须有 Ripple 反馈，这是 Android 用户的强烈预期。
- **系统导航**：Gesture Navigation（Android 10+）为默认，内容不能占用底部边缘手势区域。
- **深色模式**：系统级强制，必须定义 Light/Dark 两套 Color Scheme，无法单独关闭。
- **屏幕密度**：设计以 dp（密度无关像素）为单位，图片资源需提供多密度或使用 Vector。

---

## Token 体系：Material 3 Color Roles

M3 废弃了直接定义颜色值的方式，改为定义**色彩角色（Color Role）**，由 Seed Color 通过算法生成完整 palette。

**核心色彩角色（规范中必须定义 Light/Dark 两套）**：

```
Primary Roles（主色）：
  primary           主要按钮/高亮背景
  onPrimary         primary 上的内容色（通常白）
  primaryContainer  低强调容器背景（比 primary 浅）
  onPrimaryContainer primaryContainer 上的内容色

Secondary Roles（次色）：
  secondary         次要操作/筛选 Chip 等
  onSecondary
  secondaryContainer
  onSecondaryContainer

Error Roles（错误）：
  error
  onError
  errorContainer
  onErrorContainer

Surface Roles（背景/层级）：
  surface           卡片、Sheet、Dialog 背景
  surfaceVariant    稍深的背景变体（如输入框背景）
  onSurface         surface 上的主文字
  onSurfaceVariant  surface 上的次文字
  outline           边框/分割线（中等强调）
  outlineVariant    轻边框/分割线（低强调）
  background        页面背景（通常等同于 surface）
  onBackground      页面背景上的文字

Inverse（反色，用于 Snackbar 等）：
  inverseSurface
  inverseOnSurface
  inversePrimary

典型亮色 Seed 示例（primary=#6750A4 紫色）：
  primary #6750A4  onPrimary #FFFFFF
  primaryContainer #EADDFF  onPrimaryContainer #21005D
  surface #FFFBFE  onSurface #1C1B1F
  surfaceVariant #E7E0EC  onSurfaceVariant #49454F
  outline #79747E  outlineVariant #CAC4D0

自定义品牌色：通过 Material Theme Builder 生成完整 palette
→ https://m3.material.io/theme-builder
```

---

## 字体

M3 推荐字体层级（以 dp 为单位）：

```
displayLarge   57sp / Regular     — 首屏巨型标题
displayMedium  45sp / Regular
displaySmall   36sp / Regular
headlineLarge  32sp / Regular
headlineMedium 28sp / Regular
headlineSmall  24sp / Regular
titleLarge     22sp / Regular     — 页面标题、Dialog 标题
titleMedium    16sp / Medium
titleSmall     14sp / Medium
bodyLarge      16sp / Regular     — 主要正文
bodyMedium     14sp / Regular     — 次要正文（常用）
bodySmall      12sp / Regular     — 说明文字
labelLarge     14sp / Medium      — 按钮文字
labelMedium    12sp / Medium
labelSmall     11sp / Medium

中文字体推荐：
  Noto Sans SC（可直接使用）
  系统回退：HarmonyOS Sans（华为）/ MIUI 字体（小米）等品牌自带
```

---

## 间距与尺寸

```
8dp 栅格：4 / 8 / 12 / 16 / 24 / 32 / 48 / 64dp

触控目标最小：48×48dp（M3 规范）

常用组件尺寸：
  Button 高度        40dp（filled）
  TextField 高度     56dp（filled）/ 56dp（outlined）
  Top App Bar        64dp（small）
  Bottom Navigation  80dp
  FAB                56dp（standard）/ 40dp（small）/ 96dp（large）
  List Item（单行）   56dp；双行 72dp；三行 88dp
  Navigation Rail    80dp 宽
  Chip               32dp 高
```

---

## 组件状态矩阵（M3 State Layer）

M3 用"State Layer"叠加色来表达状态，比直接改背景色更优雅：

| 状态 | State Layer 不透明度 | 颜色来源 |
|---|---|---|
| **default** | 0% | — |
| **hovered**（外接鼠标/平板） | 8% | onSurface / onPrimary |
| **focused** | 12% | onSurface / primary |
| **pressed / ripple** | 12% | onSurface（ripple 动画） |
| **dragged** | 16% | onSurface |
| **disabled** | 38% 透明度的 onSurface | container 也降至 12% onSurface |

**在 UI 规范中**，不需要写 State Layer 百分比，而要定义：
- 哪些状态视觉上需要区分（hover 在纯触控设备上不显示）
- disabled 态是只改透明度还是需要额外灰色文案提示
- loading 态 button 是否替换为 CircularProgressIndicator

---

## 布局规则

**一级导航（根据内容和使用场景选一）**
- Bottom Navigation Bar：4-5 个 destination，手机端首选
- Navigation Rail：平板/可折叠设备，左侧窄栏（80dp）
- Navigation Drawer：内容分类多时，从左侧滑出

**内容布局**
- 手机端内容区边距：16dp（标准）
- 平板端内容区边距：24dp（≥600dp 屏宽），内容区不超过 840dp
- 卡片网格（grid）：手机 1 列；平板 2 列或 3 列
- 不要把手机布局直接拉伸到平板——至少加内容边距和多列

**Bottom Sheet**
- Standard（不遮挡主内容）vs Modal（遮挡）需明确区分
- Drag handle 可见时允许用户拖拽展开/收起

---

## 深色模式策略

- **Surface 层级**（Surface Tones）：M3 用 primary 色叠加在 surface 上区分层级，elevation 越高颜色越浅
  - elevation 0：surface（最暗）
  - elevation 1：surface + 5% primary overlay
  - elevation 2：surface + 8% primary overlay
  - elevation 3：surface + 11% primary overlay
  - elevation 4：surface + 12% primary overlay
  - elevation 5：surface + 14% primary overlay
- 图标：Material Symbols 自动适配；自定义图标需 `tintColor` 来源于 `onSurface`
- Ripple 颜色：深色模式下 ripple 用 `onSurface` 的浅色，不用白色硬编码

---

## 常用组件规范要点

### Button（Filled / Outlined / Text / Elevated / Tonal）
- 优先级：Filled > Tonal > Elevated > Outlined > Text
- 同屏不应出现多个 Filled 按钮（主操作唯一）
- 危险操作：用 `errorContainer`/`error` 色，不是普通 `primary`

### Text Field（Filled vs Outlined）
- Filled：视觉更重，适合表单集中区域
- Outlined：视觉更轻，适合单行搜索、独立输入
- 错误态：`error` 色边框 + 支持性文本说明（不只靠颜色）

### Snackbar
- 自动消失（4-10s），不要替代 Dialog 用于确认
- 不要遮挡底部主操作按钮或 Navigation Bar
- 深色模式下 Snackbar 用 `inverseSurface`

### FAB（Floating Action Button）
- 同屏最多 1 个主 FAB
- 用于页面最重要的单一操作（如"新建"）
- 进入详情页时 FAB 应消失（或变为不同操作）

---

## 视觉风格参考

查阅 `references/design-systems/` 时，以下品牌在移动端设计上有参考价值：

| 风格 | 参考 |
|---|---|
| 金融/支付 | `revolut` `wise` `coinbase` |
| 消费/社交 | `airbnb` `spotify` `pinterest` |
| 企业级 | `ibm` `hashicorp` |

若品牌库无合适参考，使用 `references/mobile-inspiration.md` 中的搜索方法。

---

## 可访问性红线

- 触控目标 ≥ 48×48dp
- 所有自定义视图设置 `contentDescription`（Compose：`Modifier.semantics`）
- 错误态必须有文案，不只靠红色边框
- 动效克制：低端设备（< 4GB RAM）动画要能降级，避免卡顿
- 对比度：正文文字 ≥ 4.5:1（参考 onSurface vs surface）

---

## Android 禁区

- 不要写 Web hover 表格规则
- 不要写 iOS Tab Bar / Navigation Bar 专属行为
- 不要在 UI_SPEC 里输出 Kotlin/Compose/XML 代码
- 不要用 M2（Material Design 2）的旧色彩模型来描述 M3 项目
- 不要把所有状态都用"改背景颜色"实现——M3 推荐 State Layer 叠加
