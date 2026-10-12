# 当前工作与接续

更新：2026-10-11 UTC。

## 当前批次 B-20261012-01

用户要求完成后继续更长时间或更大量工作，沿 D-006/007 默认队列推进 PP-030 设备采购/自动补货、PP-040 设备缺陷到安全隐患的可靠联动。当前已认领 PP-030，执行者 codex-batch-20261012-01，分支 upgrade/equipment-procurement-20261012。设计已推送设备 448e9b2、安全 49c32b9；采购失败回归推送 5ae02b9（40 failed/8 passed，迁移升级另 1 failed）。本地已实现 Decimal/原子编号/共用补货/超收保护，目标 66 项通过；正在完整后端/真实 PostgreSQL 与前端验收，未推送生产代码、未合并。下一动作：全套通过后提交采购阶段，顺序切换 PP-040/041 不可变消息与接收收据。

活动认领与检查点以 SESSION 为准，已有本地采购改动，尚未集成；具体阶段/验证和两端范围见本批日志。

## 本批已完成 B-20261011-01

用户要求自主执行，并在每次活动对话中完成更多可验收升级；偏好已保存 D-006。本批四项均已合并：

- PP-003 阶段保存/固定快照恢复、PP-004 自动发布核验、PP-005 竞争认领：[PR #13](https://github.com/nizuowanzhenbang/smart-power-plant/pull/13)，工具固定代码 `5af33d2f3a974cf0bfad54766a8bb2650cb76c18`。完整 25 项 CLI/HTTP 回归、真实 GitHub 保存/切换、PR/main CI 通过；见 [接续证据](evidence/2026-10-11-continuity.md)。
- PP-020 煤质口径：[PR #4](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/4)，固定代码 `26bdbef9360e7b2ea2f037114adbf63ffdabb947`。单位换算、基准声明、范围、关键缺项、零热值、有限比率存储及详情/合同显示已升级；完整 201 后端、6 标签渲染、构建及候选/main CI 通过；见 [煤质证据](evidence/2026-10-11-coal-quality-contract.md)。

上一批收尾时无活动认领；本批活动状态见 [SESSION.json](SESSION.json) 保留 PP-020 的实际 merged 检查点、释放理由及下一动作。代码、状态和文档签收提交分别保留；[日志](logs/2026-10-11-batch-01.md) 记录过程与实际 SHA。

## 下一批默认方向

PP-030 设备采购/自动补货边界，随后 PP-040 点检重大缺陷到安全隐患的可靠联动；均待核查，尚未认领或实施。开工步骤见 [NEXT-BATCH](plans/NEXT-BATCH.md)。

第一动作：更新中央检出并运行 `python -m progress_tools resume`，按同一 SHA 读取四核心文件和 SESSION；若无活动任务先 claim PP-030，核对 equipment-inspection 最新 main/PR/未提交状态，只读采购与补货入口后复现实际缺口。不重做煤质失败复现或已合并保护。按实际依赖选择多个可独立验收单元，关键阶段推送代码并保存 checkpoint。

## 恢复与边界

两次不带旧聊天的实际恢复均正确识别任务/分支/下一动作，见 [演练](docs/RECOVERY-EXERCISE-20261011.md)。新环境按 [SETUP](docs/SETUP.md) 接入，再遵守 [AUTOMATION](docs/AUTOMATION.md) 的认领/接管/释放规则。删除聊天不删除已推送的代码与进度；任意未接入或无权限环境仍需恢复连接。

煤质独立最终审查报告因用量限制未生成；收到的两项 Important 均先失败后修复，父代理完成范围检查和回归。没有声称完整独立批准、浏览器/现场或 PostgreSQL 并发验收。

PP-001 入口、PP-002 历史复核和 PP-010 安全期限，以及设备库存/收货重放、煤质非有限输入/运输证据、安全关联所有权、能效时间留出已交付，默认跳过。路线图不计交付；自主迭代发生在用户启动的会话，未部署无人值守模型服务。
