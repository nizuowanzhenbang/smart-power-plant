# 迭代进度与接续入口

更新日期：2026-10-04。[长期规划](LONG-TERM-PLAN-20261003.md)。主作品 equipment-inspection；辅助案例 coal-unit-efficiency、coal-quality-monitor。

## 授权与方式

用户持续授权自主迭代、长时间分析、测试、GitHub 推送与必要审查；验证后的合并自主完成。默认单代理、每轮一个主目标，复杂变化单独做一次整分支审查。无后台定时任务、模型侧实时额度读数或跨账户限制运行承诺；额度/上下文切换后从本文件继续。

## 实际进度

| 单元 | 状态 |
|---|---|
| 01–04 | 完成；#11 收拢历史成果，#12/#13/#14 更新演示基线，历史 #4–#10 不重复实施 |
| 05–06 | 库存锁、事务流水、收货重放及六入口采购状态竞争保护完成 |
| 07 | 精度、累计上限、盘点归零及过时绝对盘点保护完成；采购创建/自动补货边界待核查 |
| 08–24 | 尚未完整执行；已有迁移/恢复与依赖升级证据按实际范围复用 |

## 当前固定版本

- 仓库：`nizuowanzhenbang/equipment-inspection`。
- 最新 main：`76d799c1fc781147ea6bbdeaff0ee57e8bc659db`，由 [PR #14](https://github.com/nizuowanzhenbang/equipment-inspection/pull/14) 合并。
- 源提交：`d2f06048453ac7cbd319673a770ab46dcdff173d`；本地/上传/main tree：`16fa73b67b503296db888e102a7793768ba392dd`。
- 前一基线 `170b8393e622d31e23a5a546419748183f07ce20` 与[采购状态发布快照](RELEASE-PURCHASE-STATE-20261004.md)保留历史。
- 本轮后端492（真实PG186）、Node16、API35、本地Chromium11、tsc/Vite/Ruff/diff全部通过；PR Quality/Compose success（实际nginx/PG、Chromium11），新 main Quality success。详见[完整证据](RELEASE-STOCKTAKE-20261004.md)。
- 文档仓库：`nizuowanzhenbang/smart-power-plant`，实际文档版本查 main 历史，避免自引用 SHA。

## 完成与限制

数量与流水版本同一 SQL 快照；ADJUST 等锁刷新后拒绝缺失/过时版本；数量先变后恢复仍冲突。并发同版本盘点、合法零盘点、真实约束失败回滚、等锁刷新及提交后响应一致性已由实际数据库固定交错验证。前端冲突保留原快照，刷新后明确输入新数量，等待响应期间禁止编辑/关闭/重复提交。一次整分支独立审查无发现，独立6项SQLite通过。

旧 ADJUST 客户端须升级，否则409；IN/OUT兼容，无新迁移或依赖，HEAD保持0003。手工SQL、修改/删除流水及恢复中的旧浏览器会话不在版本保证范围，恢复后重新读取核对；ADJUST响应丢失须人工核对，不自动重试。原收货UUID与部分取消规则保留；同步外部推送持锁、远端成功无法本地撤销的既有边界不变。弃用、大包与扫描范围限制见发布证据；没有生产部署或容量证明。

## 下一项具体动作

核查采购创建与自动补货。实际入口与内嵌请求模型在 `backend/app/api/purchase_requests.py`，持久化模型在 `backend/app/models/purchase_request.py`，编号辅助在 `backend/app/utils/helpers.py`；没有独立 `schemas/purchase_request.py` 或 `services` 目录，不按猜测路径读取。

先读取 `PRCreate`、`create_pr`、`auto_generate`、`_next_pr_seq`、金额/数量字段及现有测试。已见源码使用 float 计算申请数量/金额、count+1 生成序号；这只是核查线索，不把未运行的输入或竞争写成已确认缺陷。下一轮在隔离 SQLite/PG 固定超精度/非有限数、Decimal金额边界、并发手工创建和自动补货交错，分别确认实际行为与兼容要求。超量收货政策单独确认，不顺手改变合法既有流程。

保留本轮库存版本、原收货UUID与采购状态保护；若有实际缺口，先设计和失败回归再最小修复。随后按长期路线处理认证依赖、前端加载及可靠联动。

## 本地接续

- worktree：`/workspace/worktrees/equipment-autonomous-20261003`，分支 `maintenance/stocktake-snapshot-20261004`，已推送，工作树干净。
- 主 checkout：`/workspace/equipment-inspection`；新会话先 fetch 并核对真实 main；与 linked worktree 共用 Git refs，fetch 顺序执行。
- 文档 checkout：`/workspace/smart-power-plant`，分支 `docs/stocktake-release-20261004`。
- venv：`/workspace/scratch/inspection-venv`；PG包装：`/workspace/scratch/pg-tools-stocktake-20261004`，复跑须重建对应隔离容器 `inspection-pg-stocktake-20261004`。本轮自建容器、API/Vite/报告服务已停止；旧默认数据库与其他 scratch 保留。
- 日志：scratch 下 stocktake-red、stocktake-green、stocktake-browser-red、stocktake-browser-pending-red、stocktake-browser-green、stocktake-browser-confirmation、stocktake-full、stocktake-node-final、stocktake-build-final、stocktake-e2e-final、stocktake-interview；完整后端XML：stocktake-final.xml。
- 实际测试截图：`/workspace/scratch/stocktake-tests-20261004.png`；简单结果：`/workspace/scratch/stocktake-test-results-20261004.md`；审查/交付摘要：`/workspace/scratch/stocktake-progress-final.md`。

若工作区重建，按固定提交与哈希锁恢复，不依赖本地路径仍存在。接续前核对实际 Git/PR 与文档，不按历史快照从头执行。
