# 当前工作与接续

更新：2026-10-11 UTC。

## 当前批次 B-20261011-01

用户已授权自主实施接续补强，并要求每次对话完成更多迭代。执行者 codex-batch-20261011-01；开工进度 SHA `390535679fcdd60330ee581158147b5286342441`。

本批 PP-003/004/005 已通过 [PR #13](https://github.com/nizuowanzhenbang/smart-power-plant/pull/13) 合并，工具固定版本 `5af33d2f3a974cf0bfad54766a8bb2650cb76c18`；25 项 CLI/HTTP 回归、PR/main CI、实际恢复与 GitHub 保存操作通过。见 [证据](evidence/2026-10-11-continuity.md)。3 项 Important 全部先失败再修复，旧摘要 Minor 同步修正。

当前活动任务 PP-020，仓库 coal-quality-monitor，分支 upgrade/coal-quality-contract-20261011。业务基线 110 项通过；失败回归已推送 `4b95d183b040d0966373b21d95b7133949264226`，新用例首轮 77 failed/5 passed；极小基数追加存储断言后 3 failed/2 passed。正在实现单位/基准/范围、关键缺项、零热值与展示契约，下一动作：完整验证后推送候选并独立审查。

实时认领与最后阶段以 [SESSION.json](SESSION.json) 为准；[AUTOMATION](docs/AUTOMATION.md) 说明固定快照恢复和条件写入。本文件保留批次/业务摘要。

## 最近完成

- PP-002 接续复核文档已归档：[审查与恢复步骤](docs/CONTINUITY-REVIEW-20261011.md) 保存当时的缺口；本轮补强候选及真实状态以本文件批次首段为准。
- PP-001 已合并：中央 progress/ 发布，11 个远端根目录 AGENTS.md 接入；当前环境实际及默认 Codex home 全局规则已安装。见 [接入证据](evidence/2026-10-10-memory-integration.md)。新仓库创建权限不足，采用现有 smart-power-plant 总览解决。
- PP-010 已合并：[plant-safety PR #3](https://github.com/nizuowanzhenbang/plant-safety/pull/3)，主分支 `e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1`。统一原发现时间起算的重大 14 天、一般 30 天上限、默认与 UTC 语义；竞争更新返回 409。完整后端 68 项及前端构建通过；独立审查发现的并发问题已先复现后修复；PR 与合并后主分支检查均通过。见 [发布证据](evidence/2026-10-10-hazard-deadlines.md) 和 [执行日志](logs/2026-10-10-PP-010-hazard-deadlines.md)。

## 下一项任务

PP-020 已在本批认领：coal-quality-monitor 的煤质单位、基准、缺项和物理范围。正在实施，尚未集成，不把路线图或本地候选计为已交付。

恢复时先读取固定中央快照和 SESSION，再核对活动分支/实际阶段；按上方下一动作继续，勿重做已经推送的失败复现或已合并接续机制。

## 已完成且不重做

不要重做安全检查关联所有权、PP-010 期限规则、煤质非有限输入保护或运输证据保留、设备库存/收货重放、能效时间留出评估。对应固定版本见 SUMMARY/TASKS；新回归或新要求需先记录重开原因。

每轮沿既定方向推进一批可独立验收的任务；远期联合优化按 ROADMAP 分批实施。当前规则仅在已更新检出与 Codex 指令发现范围内生效，其他环境按 [SETUP](docs/SETUP.md) 接入。

