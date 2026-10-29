# 任务台账

更新：2026-10-29 UTC。稳定编号不复用；本轮用户任务优先于默认队列。

状态：待核查 / 待做 / 进行中 / 已验证候选 / 已合并 / 阻塞 / 已有覆盖 / 取消。

## 接续队列

| 编号 | 优先级 | 状态 | 任务 | 验收与第一项动作 |
|---|---|---|---|---|
| PP-101 | 完成 | 已合并 | 入门面试问答与练习手册 | [手册](docs/INTERVIEW-ANSWER-GUIDE.md)已通过PR15/971d2d8合并；候选progress CI通过；按真实参与填写，不虚构个人贡献 |
| PP-100 | 完成 | 已合并 | 求职面试讲解、前沿升级与国产备用设计 | [讲解卡](docs/INTERVIEW-CARDS-20261014.md)与[技术设计](docs/INTERVIEW-TECH-ROADMAP-20261014.md)已通过[PR #14](https://github.com/nizuowanzhenbang/smart-power-plant/pull/14)合并，固定文档5f6e6ebb9724e6c7ef13ac3c4104cf730c237e06；25项接续/离线/在线索引核验及候选CI通过；新增智能能力及国产环境未实现 |
| PP-001 | 完成 | 已合并 | 进度仓库与 Codex 接续入口 | 中央发布 b2b3073；11/11 根目录入口远端一致；当前环境全局规则已安装 |
| PP-002 | 完成 | 已合并 | 开发接续可靠性与删除对话后的恢复复核 | [审查文档](docs/CONTINUITY-REVIEW-20261011.md)；只读核查/恢复指令已归档，不表示自动补强均实施；当时建议的接续缺口已由 PP-003/004/005 落地 |
| PP-010 | 完成 | 已合并 | 隐患整改期限 | [PR #3](https://github.com/nizuowanzhenbang/plant-safety/pull/3)，`e5e62e7`；68 项后端及构建通过，包含并发冲突保护；见 [证据](evidence/2026-10-10-hazard-deadlines.md) |
| PP-020 | 完成 | 已合并 | 煤质单位、基准、缺项和物理范围 | [PR #4](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/4)，`26bdbef`；201 后端/6 标签回归、构建及 PR/main CI 通过；见 [证据](evidence/2026-10-11-coal-quality-contract.md) |
| PP-030 | 完成 | 已合并 | 设备采购创建与自动补货边界 | PR #15、2312540；完整608/前端18，四单元和候选/main五项CI成功；[证据](evidence/2026-10-14-procurement-safety.md) |
| PP-040 | 完成 | 已合并 | 点检重大缺陷到安全隐患可靠联动 | 同PR #15、2312540；不可变outbox/严格ACK/历史坏引用恢复，真正双应用丢ACK重启与双库回归通过；候选/main五项CI成功 |
| PP-041 | 完成 | 已合并 | 安全端原子联动收据与内容冲突保护 | PR #4，6f12503；完整119通过/1刻意跳过，候选/main三项CI通过，原子收据/冲突/三入口编号；见本批证据 |
| PP-031 | 后续小项 | 已合并 | 采购页面显式剩余数量 | 设备PR16/09ee584；列表详情余量，两位小数；浏览器4项及候选五项CI成功，主分支五项CI成功 |
| PP-042 | 完成 | 已合并 | 安全接收升级操作说明 | PR5/a972bd8；升级操作说明，候选/main三项CI成功，未实际演练恢复 |
| PP-043 | 后续小项 | 已合并 | 联动原因日常可见 | 设备PR16/09ee584；查询响应和日常列表原因；本地及候选五项CI通过，主分支五项CI成功 |
| PP-050 | 能力基础 | 进行中 | 统一业务身份、单位、时间和指标口径 | [四模块固定源码核查](docs/PP050-DISCOVERY-20261014.md)已保存；PP051已交付情景适配；下一步来源导出与持久关联，不按显示名称关联 |
| PP-051 | 当前子单元 | 已合并 | 带煤质来源血缘的能效情景预览（PP-050子项） | 能效PR3/974d526；完整146通过；候选/master两项CI成功；显式请求内关联，无持久映射或账本写入；1日期Minor见PP052 |
| PP-052 | 完成 | 已合并 | 预览极端日期UTC归一校验 | 能效PR4/c604b02；完整155通过，候选/master两项CI成功；测试精度Minor见PP053 |
| PP-053 | 完成 | 已合并 | 日期校验测试精度 | 能效PR5/30e8e6a；33目标测试，撤除校验8失败；候选/master CI成功 |
| PP-054 | 完成 | 已合并 | 煤质化验来源导出 | 煤质PR5/1973c4a；完整213通过；合成记录真实双API验证；实例与时区依据需部署方/操作员核实 |
| PP-055 | 完成 | 已合并 | 煤质导出到能效预览持续回归 | 煤质PR6/308b3ba；独立双应用CI和两端来源校验，候选/main三项成功；时间依据由调用方持有 |
| PP-056 | 完成 | 已合并 | 可追溯的煤批次与机组情景关联 | 能效PR6/81233d8；SQLite完整167、独立PG10（含并发分页）通过；候选/master三项CI成功；仅情景声明 |
| PP-057 | 能力基础 | 已合并 | 时区声明依据的持久血缘与关联预览 | 能效PR7/a214bfd、煤质PR7/6de4862已合并；SQLite185、PG28、候选CI通过；主分支最终签收见[日志](logs/2026-10-29-PP-057-time-evidence.md) |
| PP-058 | 能力基础 | 进行中 | 煤场账面出场依据导出 | 固定来源、FIFO守恒校验、时间声明；不视为实际入炉计量 |
| PP-059 | 能力基础 | 待做 | 煤场库存写入守恒与并发保护 | 核查全部写入口，正有限数量、精度、FIFO和审批争抢 |
| PP-060 | 深化 | 待做 | 煤质—配煤—燃烧—排放联合决策 | 定义同一场景的输入、约束、方案比较及目标，分轮交付 |
| PP-070 | 深化 | 待做 | 设备预测与风险校准 | 明确故障类型、预测窗口、标签、基线和校准指标 |
| PP-080 | 远期 | 待做 | 电价、负荷、检修与燃料成本协同 | 定义经营目标、约束与情景比较；先做可解释的模拟决策 |
| PP-090 | 远期 | 待做 | 执行效果验证和策略反馈 | 记录动作与效果，控制负荷/煤质干扰，分别显示预测和测量收益 |

这些是长期能力队列，不是一次性全部实现。PP-030/040/041本批已合并；PP-100另一会话材料已合并，设计不计业务代码。下一批从PP-050实际批次消耗证据核查接续，按[下一批入口](plans/NEXT-BATCH.md)推进；既有保护默认不重做。

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
