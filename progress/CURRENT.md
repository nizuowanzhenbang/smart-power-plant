# 当前工作与接续

更新：2026-10-28 UTC。B-20261027-01实现已合并，主分支验收通过。SESSION无活动认领，last保留PP051真实merged/release。

- PP-042：[安全PR5](https://github.com/nizuowanzhenbang/plant-safety/pull/5)，a972bd8；备份/维护窗口/统一切换与恢复说明。候选/main三项CI成功，未执行实际恢复演练。
- PP-031/043：[设备PR16](https://github.com/nizuowanzhenbang/equipment-inspection/pull/16)，09ee584；采购余量和日常联动原因。本地后端366通过248环境跳过，前端18/构建/audit0，收货4+原因1真实浏览器通过；候选五项成功，main五项CI成功。
- PP-051：[能效PR3](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/3)，974d526；带来源血缘、显式批次/机组/时间关联的热值适配与真实能效算法情景预览。完整146通过，候选/master两项CI成功。PP-050总体仍进行中，不包含持久映射、来源导出或实际入炉消耗证明。
- 唯一独立审查无阻塞，日期极值Minor登记PP-052。详细[本批证据](evidence/2026-10-28-visibility-coal-preview.md)与[日志](logs/2026-10-28-batch-01.md)。

## 最近已交付

- PP-030采购四单元、PP-040可靠发送：[设备PR #15](https://github.com/nizuowanzhenbang/equipment-inspection/pull/15)，固定业务2312540c6d4c85ac0b921100937476067f87a506。完整608后端（SQLite/真实PostgreSQL/真实两应用）、前端18/构建、ruff/依赖/interview_demo通过。固定候选和该main的backend/postgresql/frontend/safety_contract/compose-browser五项成功；PG CI已包含根目录发送恢复回归。
- PP-041原子接收/内容冲突/三入口共用编号：[安全PR #4](https://github.com/nizuowanzhenbang/plant-safety/pull/4)，固定业务6f12503f00fdd485a55e737f17d08e8ff8b833f0。完整119通过/1刻意跳过（PG外键阻止的人工损坏映射，SQLite实际覆盖），固定候选/main三项CI成功。安全先发布，设备随后发布。
- 三任务分别保存真实merged/release，8条RELEASES记录范围在线核验；接续工具本轮完整25项通过。唯一整批审查3个Important先失败后单轮修正，3个Minor延期；无第二次审查。[完整证据/裁定与成本](evidence/2026-10-14-procurement-safety.md)、[批次日志](logs/2026-10-12-batch-01.md)、[第三次冷恢复实录](docs/RECOVERY-EXERCISE-20261013.md)均已保存。

最终中央快照bb01d8558737e6e8c526ff4c7b97c28be66f401a已实际按同一SHA复读9文件并resume一致，Progress checks38631234716成功；后续签收日志提交不改变交付状态。

代码与文档签收SHA分开：安全aed22d6最新文档main CI成功；设备55a3275关闭计划，最新文档质量CI38630239143四项成功；业务发布2312540五项成功。文档与业务索引不混用。

PP-100另一会话[面试讲解卡](docs/INTERVIEW-CARDS-20261014.md)/[前沿与国产设计](docs/INTERVIEW-TECH-ROADMAP-20261014.md)已通过[PR #14](https://github.com/nizuowanzhenbang/smart-power-plant/pull/14)、固定文档5f6e6ebb9724e6c7ef13ac3c4104cf730c237e06交付并释放。其旧候选描述是当时快照；未实施RAG、基础模型、联合优化或国产部署。成果与[日志](logs/2026-10-14-PP-100-interview.md)保留。

## 下一批第一动作

从最新固定中央五文件resume。先核对本批main验收和RELEASES，不重做已合并功能。然后处理PP-052：新预览输入极端时区日期归一UTC应422，而不是500，补年1/9999边界及正常跨日回归。

能力主线继续PP-050：按[下一批入口](plans/NEXT-BATCH.md)，优先为已有煤质记录提供显式导出契约，保留来源实例/批次/化验ID、Qnet/ar元数据和明确时间来源。之后设计持久关联与实际批次消耗，再推进PP060联合决策。PP051已是实际情景计算能力，但不是全厂身份治理完成。

## 默认跳过与恢复

PP-001/002/003/004/005/010/020和本批030/040/041/100已交付；设备库存/收货重放/盘点、煤质运输/非有限输入/单位、安全归属/期限、能效时间留出保护默认不重做。此前固定发布与证据保留于SUMMARY/REPOSITORIES。[上一批证据](evidence/2026-10-11-continuity.md)、[煤质证据](evidence/2026-10-11-coal-quality-contract.md)是历史记录，不冒充本轮重新跑煤质/能效。

删除聊天不删除已推送代码/进度；三个实际冷恢复识别了接续任务。新环境按[SETUP](docs/SETUP.md)接入，再按[AUTOMATION](docs/AUTOMATION.md)认领/保存/释放。任意未接入或无权限环境需恢复连接；没有启动无人值守模型开发服务。只证明版本化原型与明确故障契约，未验收现场、性能、任意数据库篡改恢复或跨库exactly-once。
