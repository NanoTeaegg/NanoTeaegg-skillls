"""Quality grader for the ui-design skill."""

from __future__ import annotations

from pathlib import Path


REQUIRED_UI_TERMS = [
    "UI_SPEC",
    "目标平台",
    "平台范围",
    "设计目标",
    "视觉方向",
    "Design Tokens",
    "颜色",
    "文字",
    "间距",
    "圆角",
    "布局",
    "适配",
    "组件规范",
    "状态",
    "验收标准",
    "可访问性",
    "边界",
    "非目标",
    "开放问题",
    "变更记录",
]

PLATFORM_REQUIRED_TERMS = {
    "web": ["Web", "表格", "hover", "focus", "响应式"],
    "ios": ["iOS", "Navigation Bar", "Tab Bar", "触控", "VoiceOver"],
    "android": ["Android", "Top App Bar", "Snackbar", "触控", "Material"],
}

PLATFORM_DRIFT_TERMS = {
    "web": ["iOS", "Android", "Tab Bar", "Navigation Bar", "Material", "Snackbar", "FAB", "VoiceOver"],
    "ios": ["Web 后台", "侧边导航", "表格密度", "hover", "Android", "Material", "Snackbar", "FAB"],
    "android": ["Web 后台", "侧边导航", "表格密度", "hover", "iOS", "Tab Bar", "VoiceOver", "SwiftUI", "UIKit"],
}

IMPLEMENTATION_DRIFT_TERMS = [
    "```tsx",
    "```jsx",
    "```ts",
    "```js",
    "```css",
    "useState",
    "useEffect",
    "function ",
    "class ",
    "npm install",
    "CREATE TABLE",
    "ALTER TABLE",
    "Prisma",
    "Drizzle",
    "SwiftUI",
    "UIKit",
    "Kotlin",
    "Compose",
    "XML",
]

UX_REWRITE_TERMS = [
    "用户流程图",
    "信息架构图",
    "用户旅程",
    "步骤1",
    "步骤 1",
]


def find_ui_spec(outputs_dir: Path, eval_id: int) -> Path | None:
    candidates = [
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "UI_SPEC.md",
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "UI_SPEC.web.md",
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "UI_SPEC.ios.md",
        outputs_dir / f"eval-{eval_id}" / "outputs" / "docs" / "UI_SPEC.android.md",
        outputs_dir / f"eval-{eval_id}" / "docs" / "UI_SPEC.md",
        outputs_dir / str(eval_id) / "outputs" / "docs" / "UI_SPEC.md",
        outputs_dir / str(eval_id) / "docs" / "UI_SPEC.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    matches = sorted(outputs_dir.glob(f"**/eval-{eval_id}*/**/docs/UI_SPEC*.md"))
    return matches[0] if matches else None


def _content_section(text: str) -> str:
    """Exclude boundary/open-question/change-log sections where adjacent-domain
    terms are expected because the document is explicitly naming omissions."""
    markers = ["## 10.", "## 10 ", "非目标与边界", "边界与非目标"]
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx]
    return text


def grade(eval_item: dict, outputs_dir: Path) -> dict:
    ui_path = find_ui_spec(outputs_dir, eval_item["id"])
    checks = []

    if ui_path is None:
        return {
            "artifact": None,
            "passed": False,
            "checks": [
                {
                    "text": "writes docs/UI_SPEC.md",
                    "passed": False,
                    "evidence": "No docs/UI_SPEC.md found under the eval output directory.",
                }
            ],
        }

    text = ui_path.read_text(encoding="utf-8")
    content = _content_section(text)

    checks.append({
        "text": "writes docs/UI_SPEC.md",
        "passed": True,
        "evidence": str(ui_path),
    })

    missing_terms = [term for term in REQUIRED_UI_TERMS if term not in text]
    checks.append({
        "text": "includes core UI design-spec sections and tokens",
        "passed": not missing_terms,
        "evidence": "Missing terms: " + ", ".join(missing_terms) if missing_terms else "All required terms found.",
    })

    target_platform = eval_item.get("target_platform")
    if target_platform:
        required_platform_terms = PLATFORM_REQUIRED_TERMS.get(target_platform, [])
        missing_platform_terms = [term for term in required_platform_terms if term not in text]
        checks.append({
            "text": f"covers only the requested {target_platform} platform vocabulary",
            "passed": not missing_platform_terms,
            "evidence": "Missing platform terms: " + ", ".join(missing_platform_terms) if missing_platform_terms else "Requested platform terms found.",
        })

        platform_drift = [term for term in PLATFORM_DRIFT_TERMS.get(target_platform, []) if term in content]
        checks.append({
            "text": "does not mix in other platform-specific UI rules",
            "passed": not platform_drift,
            "evidence": "Other-platform terms found: " + ", ".join(platform_drift) if platform_drift else "No other-platform drift terms found.",
        })

    component_terms = ["按钮", "表单", "表格", "弹窗", "Toast"]
    if target_platform == "ios":
        component_terms = ["Navigation Bar", "Tab Bar", "List", "Form", "Sheet", "Alert"]
    elif target_platform == "android":
        component_terms = ["Top App Bar", "Navigation Bar", "Button", "List", "Dialog", "Snackbar"]
    found_components = [term for term in component_terms if term in text]
    checks.append({
        "text": "covers common component specifications",
        "passed": len(found_components) >= 4,
        "evidence": "Found components: " + ", ".join(found_components),
    })

    state_terms = ["hover", "focus", "disabled", "loading", "空态", "错误态"]
    found_states = [term for term in state_terms if term in text]
    checks.append({
        "text": "covers visual states for interactive UI",
        "passed": len(found_states) >= 4,
        "evidence": "Found states: " + ", ".join(found_states),
    })

    implementation_drift = [term for term in IMPLEMENTATION_DRIFT_TERMS if term in content]
    checks.append({
        "text": "does not drift into frontend code, database, or ORM implementation",
        "passed": not implementation_drift,
        "evidence": "Implementation terms found: " + ", ".join(implementation_drift) if implementation_drift else "No implementation drift terms found.",
    })

    ux_rewrite_drift = [term for term in UX_REWRITE_TERMS if term in content]
    checks.append({
        "text": "does not rewrite UX flows or information architecture",
        "passed": not ux_rewrite_drift,
        "evidence": "UX rewrite terms found: " + ", ".join(ux_rewrite_drift) if ux_rewrite_drift else "No UX rewrite drift terms found.",
    })

    return {
        "artifact": str(ui_path),
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
