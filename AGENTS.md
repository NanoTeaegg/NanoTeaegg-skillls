# myskills

Codex skills 的 monorepo。

## 目录结构

- `skills/<name>/` — 各 skill 的源码，每个目录包含 `SKILL.md` 及可选的 `scripts/`、`references/`、`assets/`
- `evals/<name>/` — 对应 skill 的质量/触发评测集（`evals.json`、`trigger-eval.json`）
- `workspaces/` — 评估过程产生的临时文件，已加入 `.gitignore`

## 初始化（克隆后执行一次）

```bash
git config core.hooksPath .githooks
```

## 版本管理

每个 skill 从 `v0.1` 开始，每次迭代递增 `0.1`，没有正式发布时这个数字可以无限递增，例如`0.100`或者`0.99999`都可以，直到正式发布为 `v1.0`，继续按递增 `0.1` 的方式递增。

版本号写在 `SKILL.md` 的 frontmatter 中，提交时 `.githooks/post-commit` 会自动读取并打**注释标签**，**无需手动执行 `git tag`**。

### post-commit hook 行为

| 情况 | 行为 |
|------|------|
| tag 不存在 | 打注释标签 `git tag -a` |
| tag 已指向当前提交 | 幂等跳过 |
| tag 指向其他提交 + 终端交互 | 警告 → 询问是否递增版本并追加发布提交（默认 N） |
| tag 指向其他提交 + 非交互（IDE/GUI/CI） | 警告并给出建议，**不擅自修改** |

"tag 指向其他提交"通常意味着忘记在 `SKILL.md` 里递增 `version`。交互式询问只在终端 `git commit` 时生效；从 Cursor 或 GUI 客户端提交时会降级为只警告。

将某个 skill 还原到指定版本（不影响其他 skill）：
```bash
git checkout <skill-name>/v0.9 -- skills/<skill-name>/
git commit -m "revert <skill-name> to v0.9"
```

## 推送

每次推送时需附带 `--tags`：

```bash
git push --tags
```

## 部署到 ~/.Codex/skills/

```bash
cp -r skills/<name> ~/.Codex/skills/<name>
```

## Skill 创建与迭代

当用户要求新增、修改或优化 skill 时,默认按完整 skill-creator 工作流执行:

1. 必须调用可用的 `skill-creator` skill(例如用户显式提到 `$skill-creator` 时更要使用),不要只手写 `SKILL.md`。
2. 新 skill 从 `version: v0.1` 开始,路径遵循 `skills/<category>/<skill>/SKILL.md`。
3. 创建或修改 skill 后,自动根据项目规范创建/更新对应评测文件:
   - `evals/<category>/<skill>/evals.json`
   - `evals/<category>/<skill>/trigger-eval.json`
   - 如质量评测需要,补充或更新 `scripts/graders/<skill_name_with_underscores>.py`
4. 自动执行质量评测:为每个 eval 在 `workspaces/<skill>/<platform>/eval-<id>/outputs` 下生成产物,再运行 `./scripts/eval-skill-quality.py --evals <evals.json> --outputs-dir workspaces/<skill>/<platform>`。
5. 自动生成 review 页面供人工检查。优先使用 `skill-creator/eval-viewer/generate_review.py --static`,输出到 `workspaces/<skill>/<platform>/review.html`。生成前确保每个 eval 有 viewer 可读的 `eval_metadata.json`、`grading.json`,以及可直接展示的输出文件。
6. 自动运行低成本触发评测入口 `./scripts/eval-trigger-low-cost.py`。如果当前平台 backend 只能输出 `limited` 可信度,如实汇报限制,不要把它当作真实触发成功或失败证据。
7. 最终汇报新增/修改的文件、质量评测通过/失败、review 页路径、触发评测结果和静态兼容性审查结论。

除非用户明确说"只起草、不创建 eval、不跑测试",否则新增或迭代 skill 不应停在 `SKILL.md`。

## Skill 质量评测

当用户要求“对 @skills/<category>/<skill>/SKILL.md 进行质量测试和静态兼容性审查”时,不要使用 runner。由当前 Agent 直接执行：

1. 根据 `SKILL.md` 路径推导 `evals/<category>/<skill>/evals.json` 和 skill 名称。
2. 读取目标 `SKILL.md` 和对应 `evals.json`。
3. 为每个 eval 创建 `workspaces/<skill>/<platform>/eval-<id>/outputs`。
4. 在对应 `outputs` 目录内按目标 skill 执行 eval prompt,产物写到 grader 期望的位置。
5. 如果 eval 声明了 `files`,先复制对应文件；文件不存在时按 eval 场景创建必要输入。
6. 运行 `./scripts/eval-skill-quality.py --evals <evals.json> --outputs-dir workspaces/<skill>/<platform>`。
7. 汇报每个 eval 的通过/失败、失败原因、产物路径和静态兼容性审查结果。

这里的“静态兼容性审查”指检查 `SKILL.md`、eval 和 grader 是否存在明显的平台绑定、路径假设或工具假设；它不能证明真实跨平台兼容性。真正的兼容性必须分别在 Cursor App、Claude Code、Codex 等目标平台各实际跑过一次质量评测后才能确认。

## Skill 触发评测

当用户要求“对 @skills/<category>/<skill>/ 做触发评测”时,由当前 Agent 直接执行：

1. 根据 skill 路径推导 `evals/<category>/<skill>/trigger-eval.json` 和 skill 名称。
2. 读取目标 `SKILL.md` 和对应 `trigger-eval.json`。
3. 创建 `workspaces/<skill>/<platform>/trigger-eval/`。
4. 优先运行跨平台低成本触发评测入口：
   ```bash
   ./scripts/eval-trigger-low-cost.py \
     --platform <claude|cursor|codex|all> \
     --skill-path <skill-path> \
     --eval-set <trigger-eval.json>
   ```
   该入口会按平台调用 `scripts/trigger/backends/` 下的 backend,并在结果中标注 `mode` 和 `confidence`。Claude Code 可执行较可靠的 `runtime-trigger`；Cursor/Codex 如果当前没有可靠可编程触发信号,backend 必须输出 `limited` 可信度和判定限制,不能把质量评测或显式注入当作自动触发证据。
5. 将结构化结果写入 `workspaces/<skill>/<platform>/trigger-eval/results.json`,每条记录包含 `query`、`should_trigger`、`did_trigger`、`passed`、`evidence` 和 `notes`。
6. 汇报应触发命中率、不应触发避开率、漏触发、误触发、证据路径和 `SKILL.md` description 修改建议。

触发评测可以跨平台复用同一套 `trigger-eval.json`,但不能用某个平台的结果代表其他平台；Cursor App、Claude Code、Codex 需要分别执行并记录结果。
