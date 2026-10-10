# 2026-10-10 · PP-010 · 期限规则执行记录

- 执行方式：主代理在隔离分支直接实施，按 requesting-code-review 进行一次独立只读整分支审查，不委派实现。
- 计划/规则：plant-safety 的 docs/superpowers/plans/2026-10-10-hazard-deadlines.md 和 docs/DEADLINE-POLICY.md。
- 开工中央提交：b2b30735f27c99666286a0f00a16647147deb5f0；认领记录 baadd66。
- 代码基线：b8a1c05a4f39fe5e3e56741bed6cd7d0f27f6dd0；候选：4dff3d2da3fddbf16380e54c214e8e5a234d9bf9。
- 本地路径：/workspace/worktrees/plant-safety-deadlines-20261010；venv /workspace/scratch/plant-safety-venv-20261010，均仅本环境有效。

## TDD 与本轮实际结果

1. 干净基线后端 15 passed。
2. 49 项新增真实入口回归先运行：37 failed、12 passed；失败分别对应超限、缺省/null、UTC 偏移、双时刻锚点与极端时间处理。追加空等级用例复现原 500。
3. 实现公共 UTC/期限工具和创建/修改/转换/集成校验；登记界面补说明和上限。完整后端 65 passed；Ruff E9,F63,F7,F82、pip check、diff 检查均通过。
4. 前端 tsc/Vite 构建通过，保留既有大包提示。Python 3.12 环境有旧 datetime/passlib/TestClient 弃用警告，不在本轮顺手升级依赖；CI 使用其既有 Python 3.11。
5. 候选已推送，PR 与 CI 待最终记录；独立审查进行中，尚未合并。

## 决策与范围

以原发现时间起算，不按修改请求时间续期；新建缺省/null 补期限，更新 null 重置默认。无关字段更新保留旧超限/空期限记录；升级等级遇超限要求明确调整，不静默覆盖。当前回归使用 SQLite 临时数据库，没有 PostgreSQL 并发或现场验收声明。

## 下一项具体操作

接收独立审查结果；有实际问题先失败回归再修复；核对 PR 完整检查和候选 SHA，按本轮用户授权集成并回写发布证据。日志文件在 /workspace/scratch/plant-safety-*20261010.log。

## 12:06 UTC · 审查与修复

- 一次独立只读审查完成：没有其他 Critical/Important；发现一项 Important 并发漏洞。先读取 GENERAL/7 天后，期限请求校验 30 天，另一请求升级 MAJOR；原候选两个请求均 200，最终留下 MAJOR/30 天。
- 主代理新增 3 项真实 HTTP/JWT/SQLite 请求交错回归，覆盖等级/期限两个竞争顺序及校验后复查关闭。原候选 3 failed，均错误返回 200。
- 改为以原等级、发现时间、期限、状态、更新时间为条件的原子 UPDATE；冲突回滚并返回 409。刷新后重试重新校验，不能靠重放绕过上限。
- 修复后完整后端 68 passed（新增 53 项，原 15 项保留）；Ruff 和 diff 检查通过。前端未在本修复改变，沿用本轮实际构建结果；最终 CI 会再构建。
- 最终候选 9dd1c18e7d089ebb4e02349998271f9ec8a7de87 已推送；[PR #3](https://github.com/nizuowanzhenbang/plant-safety/pull/3) 已更新说明，检查运行 38050745250 尚在等待完整结果，未合并。
- GitHub CLI 的 PR 编辑因旧 Projects GraphQL 字段失败；已通过 REST PATCH 更新同一 PR，不是发布阻塞。
