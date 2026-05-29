# Web UI 规范参考

适用于 Web 后台、SaaS 工作台、管理系统、浏览器应用（不含营销/展示页）。

---

## 平台重点

信息密度、扫描效率、批量操作、键盘可达是 Web 产品 UI 的核心诉求，而不是视觉冲击。

- 用户在桌面端以鼠标+键盘操作为主，hover 状态必须设计。
- 高频操作路径要最短：筛选→列表→详情→编辑，每步都要有状态反馈。
- 需要明确断点策略：管理后台通常有一个"窄桌面"降级（≤1280px），而不只是手机端。

---

## Token 默认值区间（产品 UI 参考）

以下为常见 SaaS/后台产品的 token 合理区间，选值时根据产品气质偏向两端。

```
主色（Primary）：
  科技/开发者工具  #5E6AD2 / #0070F3 / #18181B（暗）
  企业/金融       #1677FF / #2563EB（更稳重）
  医疗/健康       #0EA5E9 / #10B981（绿意信任）
  B 端中性方向    #374151 / #475569

中性灰（Neutral）：
  背景（亮）      #FAFAFA / #F5F5F5 / #F8FAFC
  背景（暗）      #09090B / #0F172A / #111827
  表面（亮）      #FFFFFF / #F0F4FF
  表面（暗）      #18181B / #1E293B
  边框（亮）      #E5E7EB / #D1D5DB
  边框（暗）      rgba(255,255,255,0.1) / #27272A

文字（亮色模式）：
  主文本          #111827 / #1A1A1A
  次文本          #6B7280 / #94A3B8
  禁用文本        #9CA3AF / #D1D5DB
文字（暗色模式）：
  主文本          #F4F4F5 / #F8FAFC
  次文本          #A1A1AA / #94A3B8

语义色：
  成功            #16A34A / #22C55E
  警告            #D97706 / #F59E0B
  错误            #DC2626 / #EF4444
  信息            #2563EB / #3B82F6

间距梯度（8pt 栅格）：
  xs=4px  sm=8px  md=16px  lg=24px  xl=32px  2xl=48px

圆角：
  小组件（badge/tag）  radius-sm: 4px
  按钮/输入框          radius-md: 6-8px
  卡片/面板           radius-lg: 12px
  模态框              radius-xl: 16px

字体（推荐）：
  中文优先  Noto Sans SC + Inter(数字/英文)
  纯英文    Inter / DM Sans / Plus Jakarta Sans
  代码      JetBrains Mono / Fira Code

字号层级：
  xs=12px  sm=13px  body=14px  md=15px  lg=16px
  h3=18px  h2=20-22px  h1=24-28px  display=32px+

行高：
  UI 元素  1.4
  正文段落 1.6
  中文正文 1.7+

阴影（产品 UI 偏轻）：
  low    0 1px 3px rgba(0,0,0,0.08)
  md     0 4px 12px rgba(0,0,0,0.12)
  high   0 8px 24px rgba(0,0,0,0.16)
  暗色模式 以 border + 轻微阴影代替，避免扩散阴影
```

---

## 组件状态矩阵

每个交互组件必须定义以下五态，并给出颜色/样式规则（不要只写 default）：

| 状态 | 触发条件 | 需要定义的样式 |
|---|---|---|
| **default** | 正常可用 | 背景、边框、文字、图标 |
| **hover** | 鼠标悬停（桌面必须） | 背景变化（通常 +10% 深/浅）|
| **active/pressed** | 点击瞬间 | 再深一档 / scale(0.98) |
| **focus** | 键盘 Tab 聚焦 | focus-ring，不能被 hover 覆盖 |
| **disabled** | 不可操作 | opacity 40-50%，cursor:not-allowed |

**额外状态（视组件定义）**

| 场景 | 需要定义 |
|---|---|
| 输入框 | error / warning / success 三态，各配行内文案色 |
| 按钮 | loading 态（spinner + 禁止重复点击）|
| 开关/复选框 | checked、indeterminate |
| 列表行 | selected、drag-over |
| 卡片/行 | 可点击时有 hover，不可点击时无 hover |

---

## 布局规则

**管理后台**
- 左侧导航 + 顶部上下文栏 + 主内容区（最常见）
- 顶部导航 + 内容区（内容型/简单 SaaS）
- 列表页：筛选区（可折叠）→ 批量操作栏 → 表格 → 分页
- 详情页：主信息 + 状态 + 操作区 → 关联信息 → 审计日志

**栅格（12 列基础）**
- 桌面 ≥1280px：边距 24-32px，列间距 16-24px
- 窄桌面 1024-1279px：边距 16px，部分面板可折叠
- 平板（<1024px）：导航收起，主内容全宽

---

## 暗色模式策略

- **背景分层**：app-bg（最底）→ surface（卡片）→ elevated（弹窗/tooltip），每层比前一层亮 5-8%（暗色模式）
- **禁止**：直接把亮色 token 取反（#ffffff → #000000），视觉会"过硬"
- **阴影失效**：暗色下改用 border + 轻 background-color 区分层级
- **语义色降饱和**：暗色背景上不用高饱和原色，用降亮度版（如 #22C55E → #16A34A）
- **Token 命名建议**：用 `--color-bg` 而非 `--color-white`，semantic token 自动切换

---

## 高频 Web 组件规范重点

### 表格
- 列宽：数字列右对齐，状态列居中，文本列左对齐
- 密度：standard 行高 48px；compact 36px（高密度后台）；comfortable 56px（阅读型）
- 状态：空态（插图+引导文案）、加载骨架屏、错误态（重试入口）必须定义
- 选中行：背景高亮 + 批量操作栏出现
- 冻结列/冻结表头：内容宽时应说明是否需要

### 表单
- 标签位置：上方（推荐）；左方（紧凑横向表单）
- 校验时机：实时校验（输入时）/ 提交校验（点提交时），选其一，不混用
- 错误文案：行内字段下方，不要用全局弹窗替代字段级提示
- 必填标记：* 在标签后，不在输入框内

### 弹窗/抽屉
- Modal 弹窗：确认对话框、表单编辑（不超过 5 个字段）
- 抽屉（Drawer）：详情查看、多字段表单、侧面板
- 尺寸：modal sm=480px，md=600px，lg=800px；drawer sm=400px，md=560px，lg=720px

### Toast/通知
- 成功：3s 自动消失
- 错误/警告：需要手动关闭，或至少 8s
- 位置：右上角（不遮主内容）；移动降级为底部

---

## 参考竞品（UI 规范方向）

当用户说"参考某某产品风格"时，可查阅 `references/design-systems/` 下对应文件：

| 产品类型 | 推荐参考 |
|---|---|
| 开发者工具/CLI | `linear.app` `cursor` `vercel` |
| SaaS 后台 | `stripe` `notion` `airtable` |
| 数据分析 | `posthog` `sentry` |
| AI 产品 | `claude` `cohere` `elevenlabs` |
| 金融科技 | `revolut` `wise` `coinbase` |

---

## 可访问性红线

- 键盘 focus 环必须可见（outline 不被 hover 覆盖）
- 错误态不能只靠红色，必须有字段级文案
- 图标按钮必须有 tooltip 或 aria-label
- 表格对数字右对齐，帮助用户快速扫描量级
- 图表必须有图例或文本摘要（色盲无法区分颜色）
- 对比度：正文文字 ≥ 4.5:1；大文字/UI 组件 ≥ 3:1

---

## Web 禁区

- 不要在规范文档里写 React/Vue/Tailwind 代码
- 不要替 dev-kickoff 选组件库（shadcn/ui、Ant Design、MUI 等）
- 不要写 iOS 导航栏、Android Material 专属规则
- 不要在 UI_SPEC 里定义动效的具体代码实现——只定档位（L1/L2/L3）和原则
