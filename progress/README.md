# 电厂数智化进度与工作记忆

集中记录电厂项目的现状、当前重点、已完成工作、验证证据和下一步。下一次 Codex 从这些文件接续，不从历史对话或旧路线图重新猜进度。

仓库：`nizuowanzhenbang/smart-power-plant`。进度目录：`progress/`。默认分支：`main`。全部日期使用 UTC。

## 每轮先读

1. [AGENTS.md](AGENTS.md)：开工、核对、收尾规则。
2. [SUMMARY.md](SUMMARY.md)：两分钟摘要、已交付能力和边界。
3. [CURRENT.md](CURRENT.md)：当前工作、阻塞与第一项具体动作。
4. [TASKS.md](TASKS.md)：任务状态，防止重复实现。
5. 按本轮范围读取 [REPOSITORIES.md](REPOSITORIES.md)、[ROADMAP.md](ROADMAP.md)、[DECISIONS.md](DECISIONS.md) 和相关证据。

## 记录分工

| 文件 | 用途 | 更新时机 |
|---|---|---|
| SUMMARY.md | 当前全局摘要 | 能力、基线或重点变化 |
| CURRENT.md | 下一位 Codex 的业务与批次摘要 | 开工、暂停、收尾 |
| SESSION.json | 实时唯一认领与最后交接 | claim、checkpoint、release 发布 |
| RELEASES.json | 固定交付及需核验的检查 | 实际合并且验收后 |
| TASKS.md | 有编号的任务及状态 | 状态或验收结论变化 |
| REPOSITORIES.md | 仓库、代码基线和指令覆盖 | 仓库或基线变化 |
| ROADMAP.md | 数智化能力路线与验收目标 | 方向或依赖变化 |
| DECISIONS.md | 决策、理由和被替代方案 | 作出重要选择 |
| logs/ | 每轮追加的工作记录 | 每次有实质工作时 |
| evidence/ | 固定版本、PR 与验证依据 | 交付或复核时 |

[接续模板](templates/HANDOFF.md) · [跨环境设置](docs/SETUP.md) · [首次基线核对](evidence/2026-10-09-baseline.md) · [入口接入证据](evidence/2026-10-10-memory-integration.md) · [整改期限发布](evidence/2026-10-10-hazard-deadlines.md)

删除对话或换环境后，从 [接续审查与恢复步骤](docs/CONTINUITY-REVIEW-20261011.md) 恢复；其中区分已保存保障和待补强措施，不需要旧聊天作为开工前提。

接续工具与阶段保存见 [AUTOMATION](docs/AUTOMATION.md)：固定快照恢复、竞争认领、阶段检查点及发布核验。实时认领以 [SESSION](SESSION.json) 为准，核验覆盖索引见 [RELEASES](RELEASES.json)。用户的自主/批量交付偏好保存在 DECISIONS D-006。

## 快速接续指令

> 继续电厂项目。先从 nizuowanzhenbang/smart-power-plant 默认分支的同一 SHA 读取 progress/AGENTS.md、SUMMARY.md、CURRENT.md、TASKS.md 和 SESSION.json（或更新检出后运行 python -m progress_tools resume）。按记录认领或明确接管，一批完成多项可验收升级；关键阶段保存代码 SHA 与下一动作，收尾回写实际证据，避免重做已交付能力。

GitHub 上的 `AGENTS.md` 在对应仓库被检出并进入 Codex 指令发现范围时生效。它不会让所有陌生环境自动获得跨仓库权限；使用范围和补救方法见 [SETUP.md](docs/SETUP.md)。本仓库保存工作记忆，不启动后台开发或定时任务。
