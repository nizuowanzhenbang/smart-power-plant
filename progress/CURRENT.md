# 当前工作与接续

更新：2026-10-10 UTC。当前没有进行中的任务认领。

## 最近完成

- PP-001 已合并：中央 progress/ 发布，11 个远端根目录 AGENTS.md 接入；当前环境实际及默认 Codex home 全局规则已安装。见 [接入证据](evidence/2026-10-10-memory-integration.md)。新仓库创建权限不足，采用现有 smart-power-plant 总览解决。
- PP-010 已合并：[plant-safety PR #3](https://github.com/nizuowanzhenbang/plant-safety/pull/3)，主分支 `e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1`。统一原发现时间起算的重大 14 天、一般 30 天上限、默认与 UTC 语义；竞争更新返回 409。完整后端 68 项及前端构建通过；独立审查发现的并发问题已先复现后修复；PR 与合并后主分支检查均通过。见 [发布证据](evidence/2026-10-10-hazard-deadlines.md) 和 [执行日志](logs/2026-10-10-PP-010-hazard-deadlines.md)。

## 下一项任务

PP-020，状态待核查：coal-quality-monitor 的煤质单位、基准、缺项和物理范围。尚未认领、实施或验收，不把路线图计为已交付。

第一项动作：先取得中央最新 SHA 并读取四个核心文件；认领 PP-020，核对 coal-quality-monitor 当前默认分支、未合并 PR 与未提交改动；读取 DTO/schema、化验创建/修改及评分计算入口，列清 8 指标的单位、基准、null/缺项含义和有限极端值的真实行为。先复现具体缺口，再确定可验收的小范围改动。

## 已完成且不重做

不要重做安全检查关联所有权、PP-010 期限规则、煤质非有限输入保护或运输证据保留、设备库存/收货重放、能效时间留出评估。对应固定版本见 SUMMARY/TASKS；新回归或新要求需先记录重开原因。

下一轮沿既定方向推进一个主目标；远期联合优化仍按 ROADMAP 分轮实施。当前规则仅在已更新检出与 Codex 指令发现范围内生效，其他环境按 [SETUP](docs/SETUP.md) 接入。
