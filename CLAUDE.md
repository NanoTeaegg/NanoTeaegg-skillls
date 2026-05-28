# myskills

Claude Code skills 的 monorepo。

## 目录结构

- `skills/<name>/` — 各 skill 的源码，每个目录包含 `SKILL.md` 及可选的 `scripts/`、`references/`、`assets/`
- `evals/<name>/` — 对应 skill 的测试用例（`evals.json`）
- `workspaces/` — 评估过程产生的临时文件，已加入 `.gitignore`

## 版本管理

给单个 skill 打 tag：
```bash
git tag skill-name/v1.0
```

## 部署到 ~/.claude/skills/

```bash
cp -r skills/<name> ~/.claude/skills/<name>
```
