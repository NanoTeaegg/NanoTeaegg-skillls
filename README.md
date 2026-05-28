# myskills

个人 Claude Code skills 的 monorepo，用于统一开发、版本管理和部署自定义 skills。

## 目录结构

```
myskills/
├── skills/                        # skill 源码
│   ├── Development/               # 开发类
│   │   ├── code-review/
│   │   └── web-development/
│   └── Research/                  # 研究类
│       └── market-research/
├── evals/                         # 每个 skill 的测试用例
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

## 部署到本地

```bash
cp -r skills/<category>/<skill-name> ~/.claude/skills/<skill-name>
```
