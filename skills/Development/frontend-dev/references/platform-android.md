# Android 前端实现规范

适用于 Jetpack Compose 和传统 View 体系（XML + ViewBinding），针对 Google Play 应用。

## Token 对接

- UI_SPEC 里的颜色 token 在 `ui/theme/Color.kt` 统一声明，`MaterialTheme.colorScheme` 映射 Light/Dark 两套。
- 不在 Composable 里写 `Color(0xFF1677FF)`，用 `MaterialTheme.colorScheme.primary`（或自定义扩展属性）。
- 字体：自定义字体放 `res/font/`，在 `Typography.kt` 按语义层级定义；不在每个组件里单独 `fontFamily`。
- 尺寸 token 放 `ui/theme/Dimension.kt`（`val SpacingMd = 16.dp`），不写魔法数字 dp。

## Jetpack Compose 关键规则

- **单向数据流**：State 从 ViewModel 通过 `collectAsState()` / `observeAsState()` 流入，不在 Composable 里持有业务状态。
- **组件状态**：按钮的 enabled/loading 通过参数传入，不在内部自行管理。
- **副作用**：网络请求、导航用 `LaunchedEffect`；不要在 `remember` 里做有副作用的计算。
- **Modifier 顺序**：`padding` 在 `background`/`clickable` 之后，否则点击区域/背景范围会出错。

## XML + ViewBinding 关键规则

- 颜色用 `@color/primary`（`colors.xml` 里对应 Day/Night 两套）。
- 尺寸用 `@dimen/spacing_md`（`dimens.xml`），不写死数值。
- 复杂列表用 `RecyclerView` + `ListAdapter`（DiffUtil），不用 `notifyDataSetChanged()`。
- `ViewBinding` 替代 `findViewById`，生命周期内不持有 binding 引用超过 `onDestroyView`。

## 导航

- 单 Activity + Fragment/Compose Navigation，按 TECH_DESIGN 定义的路由结构实现。
- 系统手势返回（Android 13+）：如有自定义返回逻辑，注册 `OnBackPressedCallback`，不要拦截 `onBackPressed()`（已废弃）。

## 主题 & 深色模式

- `MaterialTheme` 的 `colorScheme` 分 `lightColorScheme`/`darkColorScheme` 两套，跟随系统或 UI_SPEC 的定义。
- 图标用 Vector Drawable，不用位图（支持任意密度缩放）。
- 适配不同屏幕密度：图片资源放 `drawable-mdpi/hdpi/xhdpi/xxhdpi`，或用 SVG Vector。

## 可访问性

- 所有自定义组件设置 `contentDescription`（Compose：`Modifier.semantics { contentDescription = "..." }`）。
- 纯装饰性图标：`contentDescription = null` + `Modifier.semantics { invisibleToUser() }`。
- 触摸目标 ≥ 48×48dp（Material 最小触摸目标规范）。
- TalkBack 逻辑顺序与视觉顺序一致。

## 常见坑

- Compose 的 `LazyColumn` item 里不要嵌套 `Column` 带 `verticalScroll`（两层滚动冲突）。
- `remember { mutableStateOf() }` 在 recomposition 之间保留值；`rememberSaveable` 在 Activity 重建后保留。
- ViewModel 的 `viewModelScope.launch` 里不要直接引用 Activity/Fragment/View，会内存泄漏。
- `Scaffold` 的 `contentWindowInsets` 在 Android 15+ 默认启用 edge-to-edge，确认 padding 处理正确。

## 验收清单

- [ ] 颜色来自 `MaterialTheme.colorScheme` 或 `@color/` 资源，无硬编码
- [ ] 尺寸来自 Dimension token，无魔法数字 dp
- [ ] 支持深色模式（Light/Dark colorScheme 均正确）
- [ ] 触摸目标 ≥ 48×48dp
- [ ] contentDescription 在所有自定义控件上设置
- [ ] 系统手势返回处理正确（如有自定义逻辑）
- [ ] UX.md 中所有状态（加载/空/错误/禁用）均有对应实现
- [ ] 不同屏幕密度图片资源齐全或使用 Vector
