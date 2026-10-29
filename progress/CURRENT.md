# 当前工作与接续

更新：2026-10-29 UTC。PP057已交付：能效PR7/a214bfd、煤质PR7/6de4862，候选与默认分支各三项CI均成功；SESSION已释放。下列旧批次段落为历史记录。

- PP-042：[安全PR5](https://github.com/nizuowanzhenbang/plant-safety/pull/5)，a972bd8；备份/维护窗口/统一切换与恢复说明。候选/main三项CI成功，未执行实际恢复演练。
- PP-031/043：[设备PR16](https://github.com/nizuowanzhenbang/equipment-inspection/pull/16)，09ee584；采购余量和日常联动原因。本地后端366通过248环境跳过，前端18/构建/audit0，收货4+原因1真实浏览器通过；候选五项成功，main五项CI成功。
- PP-051：[能效PR3](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/3)，974d526；带来源血缘、显式批次/机组/时间关联的热值适配与真实能效算法情景预览。完整146通过，候选/master两项CI成功。PP-050总体仍进行中，不包含持久映射、来源导出或实际入炉消耗证明。
- 唯一独立审查无阻塞，日期极值Minor登记PP-052。详细[本批证据](evidence/2026-10-28-visibility-coal-preview.md)与[日志](logs/2026-10-28-batch-01.md)。

## 用户当前学习重点：面试问答

PP-101 已交付[从零开始的面试问答手册](docs/INTERVIEW-ANSWER-GUIDE.md)，[PR #15](https://github.com/nizuowanzhenbang/smart-power-plant/pull/15)，合并971d2d8415111a51258829839205875edccde046；候选progress CI通过。用户表示不熟悉面试准备方法；后续先从简单业务例子出发，一次教一个问题、让用户用自己的话复述，再按其实际理解追问。个人贡献、AI参与和现场经验只能按用户真实经历填写，不能虚构。用户主动学习/面试问题优先；若转回开发，按下一批入口接续PP057。

## 2026-10-28 继续批次

执行者 codex-20261028-next。PP053：[能效PR5](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/5)，4edc72a；33项目标测试通过，临时移除UTC校验8个用例均失败，独立审查无问题；已合并30e8e6a，master CI通过。

PP054：[煤质PR5](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/5)，已合并1973c4a；配置来源实例、操作者明确声明时区及依据，从入厂化验导出measurement。完整213通过；合成记录的实际煤质API输出经独立能效API预览，4000 kcal/kg得16747.2 kJ/kg。审查两项边界已先失败后修复；候选及main CI均成功；来源及时间声明真实性依操作者核实，不自动识别模拟记录，不证明入炉。第一动作：PP055实现跨系统持续回归，再继续持久关联设计。

## 2026-10-29 批次

PP055：[煤质PR6](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/6)，候选a8e378a。独立进程实际导出与能效预览、来源/基准错配与不写快照，固定能效30e8e6a；本地契约通过、煤质完整213通过。审查指出应独立断言来源/时间，模拟错误来源先失败后修复，候选CI进行中。固定版本与人工时区依据边界保留。

PP055煤质PR6已合并308b3ba，候选与main三项CI全部成功；已签收。

PP056：[能效PR6](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/6)，已合并81233d8；情景关联持久化并按ID预览。独立审查指出NUL与非法Unicode导致500及机组编号约束不一致，先失败后修复；SQLite完整167通过，隔离PostgreSQL10通过含并发/分页；按来源和批次分页查回，分页非一致快照需刷新。候选及master的backend/frontend/scenario_postgresql三项均成功。未验证现场升级，不能把声明当实际入炉证明。当前已release，SESSION无活动认领。

## 最近已交付

- PP-030采购四单元、PP-040可靠发送：[设备PR #15](https://github.com/nizuowanzhenbang/equipment-inspection/pull/15)，固定业务2312540c6d4c85ac0b921100937476067f87a506。完整608后端（SQLite/真实PostgreSQL/真实两应用）、前端18/构建、ruff/依赖/interview_demo通过。固定候选和该main的backend/postgresql/frontend/safety_contract/compose-browser五项成功；PG CI已包含根目录发送恢复回归。
- PP-041原子接收/内容冲突/三入口共用编号：[安全PR #4](https://github.com/nizuowanzhenbang/plant-safety/pull/4)，固定业务6f12503f00fdd485a55e737f17d08e8ff8b833f0。完整119通过/1刻意跳过（PG外键阻止的人工损坏映射，SQLite实际覆盖），固定候选/main三项CI成功。安全先发布，设备随后发布。
- 三任务分别保存真实merged/release，8条RELEASES记录范围在线核验；接续工具本轮完整25项通过。唯一整批审查3个Important先失败后单轮修正，3个Minor延期；无第二次审查。[完整证据/裁定与成本](evidence/2026-10-14-procurement-safety.md)、[批次日志](logs/2026-10-12-batch-01.md)、[第三次冷恢复实录](docs/RECOVERY-EXERCISE-20261013.md)均已保存。

最终中央快照bb01d8558737e6e8c526ff4c7b97c28be66f401a已实际按同一SHA复读9文件并resume一致，Progress checks38631234716成功；后续签收日志提交不改变交付状态。

代码与文档签收SHA分开：安全aed22d6最新文档main CI成功；设备55a3275关闭计划，最新文档质量CI38630239143四项成功；业务发布2312540五项成功。文档与业务索引不混用。

PP-100另一会话[面试讲解卡](docs/INTERVIEW-CARDS-20261014.md)/[前沿与国产设计](docs/INTERVIEW-TECH-ROADMAP-20261014.md)已通过[PR #14](https://github.com/nizuowanzhenbang/smart-power-plant/pull/14)、固定文档5f6e6ebb9724e6c7ef13ac3c4104cf730c237e06交付并释放。其旧候选描述是当时快照；未实施RAG、基础模型、联合优化或国产部署。成果与[日志](logs/2026-10-14-PP-100-interview.md)保留。

## 当前后续：PP-052

执行者 codex-batch-20261028-02；能效分支 fix/coal-preview-date-boundaries-20261028，开始2026-10-28 UTC。PR4已合并c604b0276dd0e0c74f3fc68f36e593b027d8b420；四字段上下日期越界先复现失败再修复，合法跨日通过，完整155通过，独立审查无阻塞，候选CI通过，master CI通过。审查Minor：测试只断言422，部分用例可能因其他时间规则拒绝，需将字段位置/消息断言与可表示极值另列后续。

## 下一批第一动作

PP057已完成，本轮签收状态见[日志](logs/2026-10-29-PP-057-time-evidence.md)及SESSION。能效PR7与煤质PR7联合验证时间依据持久化与关联预览，默认分支CI已验收。从PP050继续核查煤场/运行系统的实际批次消耗证据：哪些记录证明某批煤在何时、以多少数量进入哪台机组。先固定源码核查数据来源及缺口，再决定新增事实模型；不得把情景声明自动升级为实际入炉事实。PP060联合决策仍待该业务口径明确。

## 默认跳过与恢复

PP-001/002/003/004/005/010/020和本批030/040/041/100已交付；设备库存/收货重放/盘点、煤质运输/非有限输入/单位、安全归属/期限、能效时间留出保护默认不重做。此前固定发布与证据保留于SUMMARY/REPOSITORIES。[上一批证据](evidence/2026-10-11-continuity.md)、[煤质证据](evidence/2026-10-11-coal-quality-contract.md)是历史记录，不冒充本轮重新跑煤质/能效。

删除聊天不删除已推送代码/进度；三个实际冷恢复识别了接续任务。新环境按[SETUP](docs/SETUP.md)接入，再按[AUTOMATION](docs/AUTOMATION.md)认领/保存/释放。任意未接入或无权限环境需恢复连接；没有启动无人值守模型开发服务。只证明版本化原型与明确故障契约，未验收现场、性能、任意数据库篡改恢复或跨库exactly-once。

## PP-057 本轮认领

执行者 codex-time-evidence-20261029；2026-10-29 UTC；能效分支 feat/coal-time-evidence-20261029。保存不可变测量与操作者时区声明，通过记录ID与已有情景关联预览；随后升级双应用契约。

本轮PP057已释放，最终证据见对应日志；早前手工认领段落仅为历史。

## 本轮PP050来源核查
执行者codex-consumption-20261029；2026-10-29 UTC；smart-power-plant分支docs/consumption-discovery-20261029。先核查煤场与能效来源，再交付煤场账面出场证据导出。
