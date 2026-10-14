# 任务台账

更新：2026-10-14 UTC。稳定编号不复用；本轮用户任务优先于默认队列。

状态：待核查 / 待做 / 进行中 / 已验证候选 / 已合并 / 阻塞 / 已有覆盖 / 取消。

## 接续队列

| 编号 | 优先级 | 状态 | 任务 | 验收与第一项动作 |
|---|---|---|---|---|
| PP-100 | 用户本轮优先 | 已验证候选 | 求职面试讲解、前沿升级与国产备用设计 | [讲解卡](../docs/INTERVIEW-CARDS-20261014.md)与[技术设计](../docs/INTERVIEW-TECH-ROADMAP-20261014.md)已整理；离线链接/结构检查通过，待候选发布与CI；新增智能能力及国产环境未实现 |
| PP-001 | 完成 | 已合并 | 进度仓库与 Codex 接续入口 | 中央发布 b2b3073；11/11 根目录入口远端一致；当前环境全局规则已安装 |
| PP-002 | 完成 | 已合并 | 开发接续可靠性与删除对话后的恢复复核 | [审查文档](docs/CONTINUITY-REVIEW-20261011.md)；只读核查/恢复指令已归档，不表示自动补强均实施；当时建议的接续缺口已由 PP-003/004/005 落地 |
| PP-010 | 完成 | 已合并 | 隐患整改期限 | [PR #3](https://github.com/nizuowanzhenbang/plant-safety/pull/3)，`e5e62e7`；68 项后端及构建通过，包含并发冲突保护；见 [证据](evidence/2026-10-10-hazard-deadlines.md) |
| PP-020 | 完成 | 已合并 | 煤质单位、基准、缺项和物理范围 | [PR #4](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/4)，`26bdbef`；201 后端/6 标签回归、构建及 PR/main CI 通过；见 [证据](evidence/2026-10-11-coal-quality-contract.md) |
| PP-030 | 本批 1 | 已验证候选 | 设备采购创建与自动补货边界 | 数量/金额精度、超量收货政策、编号竞争按实际代码逐项核查；不重做收货重放 |
| PP-040 | 本批 2 | 已验证候选 | 点检重大缺陷到安全隐患可靠联动 | 核对双方契约；对端宕机、响应丢失、重放、内容冲突和恢复有证据 |
| PP-041 | 本批 3 | 已验证候选 | 安全端原子联动收据与内容冲突保护 | 配套 PP-040；自然键唯一、完整内容防冲突、历史核对、真实双数据库并发和故障恢复 |
| PP-050 | 能力基础 | 待做 | 统一业务身份、单位、时间和指标口径 | 先列供应商/煤批次/设备/机组标识与来源；不能只按显示名称关联 |
| PP-060 | 深化 | 待做 | 煤质—配煤—燃烧—排放联合决策 | 定义同一场景的输入、约束、方案比较及目标，分轮交付 |
| PP-070 | 深化 | 待做 | 设备预测与风险校准 | 明确故障类型、预测窗口、标签、基线和校准指标 |
| PP-080 | 远期 | 待做 | 电价、负荷、检修与燃料成本协同 | 定义经营目标、约束与情景比较；先做可解释的模拟决策 |
| PP-090 | 远期 | 待做 | 执行效果验证和策略反馈 | 记录动作与效果，控制负荷/煤质干扰，分别显示预测和测量收益 |

这些是长期能力队列，不是已批准的一次性全部实现。PP-001 与 PP-010 已交付，PP-002 为 2026-10-11 的文档审查；本批 PP-003/004/005/020 已交付，下一批从 PP-030/040 核查接续，以 CURRENT/SESSION 为准，远期能力仍按可验收单元逐项实施。

## 本批流程改进交付

来自 PP-002 审查，用户本轮已明确授权实施；批次 B-20261011-01 已集成并验收，证据如下。

| 编号 | 状态 | 交付 | 验收证据 |
|---|---|---|---|
| PP-003 | 已合并 | 阶段检查点与无历史恢复演练 | [PR #13](https://github.com/nizuowanzhenbang/smart-power-plant/pull/13)；固定工具代码 5af33d2；25 项 CLI/HTTP 回归、真实恢复与 GitHub 保存/切换、PR/main CI 成功；见 [证据](evidence/2026-10-11-continuity.md) |
| PP-004 | 已合并 | 进度证据自动核验 | [PR #13](https://github.com/nizuowanzhenbang/smart-power-plant/pull/13)；固定工具代码 5af33d2；25 项 CLI/HTTP 回归、真实恢复与 GitHub 保存/切换、PR/main CI 成功；见 [证据](evidence/2026-10-11-continuity.md) |
| PP-005 | 已合并 | 多会话认领与冲突处理 | [PR #13](https://github.com/nizuowanzhenbang/smart-power-plant/pull/13)；固定工具代码 5af33d2；25 项 CLI/HTTP 回归、真实恢复与 GitHub 保存/切换、PR/main CI 成功；见 [证据](evidence/2026-10-11-continuity.md) |

## 已有覆盖：不要从头重做

| 编号 | 状态 | 内容 | 证据与边界 |
|---|---|---|---|
| DONE-EQ-01 | 已有覆盖 | 离线重放、点检检修验收、库存/收货/状态竞争及盘点基线 | [equipment-inspection PR #14](https://github.com/nizuowanzhenbang/equipment-inspection/pull/14)；包含前序成果，未证明所有采购创建入口 |
| DONE-CQ-01 | 已有覆盖 | 重评保留运输证据与供应商扣分 | [coal-quality-monitor PR #2](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/2)；未覆盖全部煤质单位规则 |
| DONE-CQ-02 | 已有覆盖 | 8 指标非有限输入保护 | [coal-quality-monitor PR #3](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/3)；有限极端值/缺项留待核查 |
| DONE-SF-01 | 已有覆盖 | 安全检查转隐患关联归属 | [plant-safety PR #2](https://github.com/nizuowanzhenbang/plant-safety/pull/2)，PP-010 保留原 15 项回归；期限升级另见 PP-010 |
| DONE-CE-01 | 已有覆盖 | 能效模型评估、基线和降级 | [coal-unit-efficiency PR #2](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/2)；未证明工业校准或实际节煤收益 |

重新打开已覆盖任务时，新增日志写清实际回归、新需求或证据冲突；不能因为换了会话就重新实施。
