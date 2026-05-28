# myskills

Claude Code skills 的 monorepo。

## 目录结构

- `skills/<name>/` — 各 skill 的源码，每个目录包含 `SKILL.md` 及可选的 `scripts/`、`references/`、`assets/`
- `evals/<name>/` — 对应 skill 的测试用例（`evals.json`）
- `workspaces/` — 评估过程产生的临时文件，已加入 `.gitignore`

## 初始化（克隆后执行一次）

```bash
git config core.hooksPath .githooks
```

## 版本管理

每个 skill 从 `v0.1` 开始，每次迭代递增 `0.1`，没有正式发布时这个数字可以无限递增，例如`0.100`或者`0.99999`都可以，直到正式发布为 `v1.0`，继续按递增 `0.1` 的方式递增。

版本号写在 `SKILL.md` 的 frontmatter 中，提交时 `.githooks/post-commit` 会自动读取并打 tag，**无需手动执行 `git tag`**。

将某个 skill 还原到指定版本（不影响其他 skill）：
```bash
git checkout <skill-name>/v0.9 -- skills/<skill-name>/
git commit -m "revert <skill-name> to v0.9"
```

## 部署到 ~/.claude/skills/

```bash
cp -r skills/<name> ~/.claude/skills/<name>
```
