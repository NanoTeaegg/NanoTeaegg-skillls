# 移动端 UI 视觉灵感获取指南

iOS 和 Android App 无法用爬虫直接抓取，但可以通过以下方法获取高质量视觉参考。

**重要限制**：移动端参考只能用于气质判断和风格灵感，不能反推出精确 token 数值。提取到的颜色/尺寸仅作参考，必须经过人工确认后写入 UI_SPEC。

---

## 方法一：Mobbin（首选）

Mobbin 是最全的移动端 UI 截图库，覆盖 iOS/Android/Web 三端，按行业和功能分类。

**使用方式（WebSearch）**：

```
WebSearch: site:mobbin.com "[产品名]" OR "[功能] app UI"
WebSearch: mobbin [行业类型] app design [交互场景]
```

**示例查询**：
- `mobbin fintech app onboarding dark mode`
- `mobbin health app dashboard iOS`
- `mobbin ecommerce checkout flow android`

**可以从截图中提取的信息**：
- 整体色调（暖/冷/中性）和主色方向
- 信息密度（紧凑/宽松）
- 圆角风格（小/大/圆润）
- 导航模式（Tab Bar / 抽屉 / 全屏）
- 空态/加载态风格

---

## 方法二：官方截图（App Store / Google Play）

官方应用商店截图由 App 团队精心设计，最能代表品牌视觉意图。

**使用方式（WebSearch）**：

```
WebSearch: "[品牌名] app store screenshots iOS 2024"
WebSearch: "[品牌名] google play screenshots android UI"
WebSearch: site:apps.apple.com "[品牌名]"
```

**注意**：App Store 截图可能是营销图（经过美化），不一定等于真实 UI。查找时优先找功能截图而非 Banner 式宣传图。

---

## 方法三：品牌设计博客/Dribbble（气质参考）

当需要了解某产品的整体设计语言时，设计团队有时会发布 Case Study。

**使用方式（WebSearch）**：

```
WebSearch: "[品牌名] design system case study mobile"
WebSearch: "[品牌名] iOS app redesign dribbble"
WebSearch: "[品牌名] UI kit figma community"
```

---

## 方法四：品牌库预置（最快）

先检查 `references/design-systems/` 是否已有对应品牌预置文件。部分预置文件包含移动端规范（如 Revolut、Wise、Airbnb、Spotify）。

查看索引：`references/design-systems/INDEX.md`

---

## 结果记录格式

获取到参考截图/描述后，记录以下信息（用于后续访谈确认）：

```
参考来源：[Mobbin/App Store/品牌库 - 具体 URL 或品牌名]
气质描述：[1-2 句话描述整体感受]
主色方向：[颜色描述，如"深蓝+白+少量橙色强调"]
圆角印象：[小/中/大，对应约 4/8/16px]
信息密度：[紧凑/标准/宽松]
导航模式：[底部 Tab / 侧边栏 / 无固定导航]
特殊元素：[如"大量使用卡片""暗色背景""插图占比高"]
可信度：[低/中/高——截图越官方、越近期越高]
```

---

## 重要声明

- 搜索到的截图**不能直接作为精确 token 数值**（像素级提取不可靠）
- 颜色只能描述色调方向，不能直接用取色器的数值
- 一定要在访谈环节向用户确认："我找到的参考是这个风格，方向对吗？"
- 移动端 UI 规范的最终 token 值来源于：品牌色板（官网/品牌手册）+ 平台 reference 区间 + 用户访谈确认
