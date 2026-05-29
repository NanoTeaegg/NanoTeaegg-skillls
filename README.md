# myskills

NanoTeaegg的Skills合集，通过monorepo架构用于统一开发、版本管理和部署自定义 skills。

## 目录结构

```
myskills/
├── skills/                        # skill 源码
│   ├── Development/               # 开发类
│   │   ├── code-review/
│   │   └── web-development/
│   └── Research/                  # 研究类
│       └── market-research/
├── evals/                         # 每个 skill 的质量/触发评测集
│   ├── Development/
│   └── Research/
├── workspaces/                    # 评估临时文件（不纳入版本控制）
└── .githooks/                     # git hooks
    └── post-commit                # 自动同步 SKILL.md 版本号到 tag
```

## Skills

### Development

| Skill | 版本 | 描述 |
|-------|------|------|
| code-review | v0.1 | 待开发 |
| web-development | v0.1 | 待开发 |

### Research

| Skill | 版本 | 描述 |
|-------|------|------|
| market-research | v0.1 | 待开发 |

## 版本管理

每个 skill 从 `v0.1` 开始，每次迭代递增 `0.1`，正式发布为 `v1.0`。版本号写在各 skill 的 `SKILL.md` frontmatter 中，提交时 post-commit hook 自动打 tag，无需手动操作。

还原某个 skill 到历史版本（不影响其他 skill）：

```bash
git checkout <skill-name>/v0.9 -- skills/<category>/<skill-name>/
git commit -m "revert <skill-name> to v0.9"
```

## 初始化（克隆后执行一次）

```bash
git config core.hooksPath .githooks
```

## 推送

每次推送时需附带 `--tags`，确保版本 tag 同步到 GitHub：

```bash
git push --tags
```

## 评测

仓库里的 eval 分为两类：

- **质量评测**：验证 skill 被执行后产物是否达标。评测集放在 `evals/<category>/<skill>/evals.json`，产物写入 `workspaces/<skill>/<platform>/...`，再由 `scripts/eval-skill-quality.py` 调用对应 grader 判分。
- **触发评测**：验证某个平台是否会在合适的用户请求中自动使用 skill。评测集放在 `evals/<category>/<skill>/trigger-eval.json`，结果写入 `workspaces/<skill>/<platform>/trigger-eval/results.json`。

质量评测的核心逻辑是“当前 Agent 执行，脚本判分”：Agent 读取目标 `SKILL.md` 和 `evals.json`，逐条完成 eval prompt 并保存产物；grader 只检查产物是否满足要求，不调用模型。不同平台可以复用同一套 `evals.json` 和 grader，但需要分别在 Cursor App、Claude Code、Codex 等目标平台实际跑一次，才能说明该平台兼容。

触发评测的核心逻辑是“同一组 query，按平台分别判定”：`trigger-eval.json` 记录用户可能说的话以及 `should_trigger` 期望；当前平台逐条测试后记录 `did_trigger`、证据、漏触发和误触发。触发评测可以复用同一套 query，但不能用某个平台的结果代表其他平台。

平台差异：

- **Claude Code**：主要根据 skill 的 `name` 和 `description` 决定是否读取 `SKILL.md`，可通过 `scripts/eval-trigger-low-cost.py --platform claude` 做低成本触发评测。
- **Cursor**：触发机制与 Claude Code 不同，应在 Cursor 当前环境中记录是否自动读取/使用目标 skill；如果没有可编程触发信号，需说明证据来源和判定限制。
- **Codex**：触发机制也需单独验证，应在 Codex 当前环境中记录是否自动读取/使用目标 skill；不能复用 Claude Code 的触发结论。

低成本触发评测统一入口：

```bash
./scripts/eval-trigger-low-cost.py \
  --platform <claude|cursor|codex|all> \
  --skill-path skills/Development/requirements-definition \
  --eval-set evals/Development/requirements-definition/trigger-eval.json
```

该入口会调用 `scripts/trigger/backends/` 下对应平台的 backend，并在 `results.json` 中标注 `mode` 和 `confidence`。Claude Code backend 可执行较可靠的 `runtime-trigger`；Cursor/Codex backend 如果没有可靠可编程触发信号，会输出 `limited` 可信度和判定限制，不会把质量评测或显式注入当作自动触发证据。

常用触发语句：

- `请对 @skills/Development/requirements-definition/SKILL.md 进行质量测试和静态兼容性审查。`
- `请对 @skills/Development/requirements-definition/ 做触发评测。`

## 部署到本地

```bash
cp -r skills/<category>/<skill-name> ~/.agent/skills/<skill-name>
```
