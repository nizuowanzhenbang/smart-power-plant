# 迭代进度与接续入口

更新日期：2026-10-03。[长期规划](LONG-TERM-PLAN-20261003.md)。主作品 equipment-inspection；辅助案例 coal-unit-efficiency、coal-quality-monitor。

## 授权与方式

用户持续授权自主迭代、长时间分析、测试、GitHub 推送和相关操作；通过必要审查/验证后的合并自主完成。默认单代理、每轮一个主目标，复杂变化单独做一次整分支审查。无后台定时任务、模型侧实时额度读数或跨账户限制运行承诺；额度/上下文窗口切换后从本文件继续。

## 实际进度

| 单元 | 状态 |
|---|---|
| 01–04 | 完成；#11 收拢历史成果，#12 更新演示基线，历史 #4–#10 不重复实施 |
| 05–06 | 库存锁、事务流水和部分收货重放幂等完成；首次收货与取消/审批竞争待做 |
| 07 | 精度、累计上限、盘点归零完成；过时绝对盘点保护待做 |
| 08–24 | 尚未完整执行；已有迁移/恢复与依赖升级证据按实际范围复用 |

## 当前固定版本

- 仓库：`nizuowanzhenbang/equipment-inspection`。
- 最新 main：`04f898fb63f4b389f95eba264eff3b7138850870`，由 [PR #12](https://github.com/nizuowanzhenbang/equipment-inspection/pull/12) 合并。
- 源提交：`fc9f4102d51fad3901728df8f5d6a1c87b944a7b`；本地/上传/main tree：`ca4a2495466f632f9f566b3c57ba684c4868a62a`。
- 上一基线 `b2bd35cea7ad40a0a0ab9b836707b6af6539738b` 与[上一发布快照](RELEASE-20261003.md)保留历史；#4 自动 merged、#5–#9 被 #11 集成后关闭，历史 head 都是 main 祖先。
- 本轮后端404（真实PG142）、Node16、Chromium8、API35、tsc/Vite/Ruff/diff全部通过；PR Quality/Compose 均 success，新 main Quality 为 success。详见[完整证据](RELEASE-RECEIPTS-20261003.md)。
- 文档仓库：`nizuowanzhenbang/smart-power-plant`，实际文档版本查 main 历史，避免自引用 SHA。

## 完成与限制

本轮补齐稳定 UUID、快照、同事务回滚、显式迁移、刷新恢复和标签页/账户隔离。原请求确认不会生成新键，人工放弃不能误删后续记录。新 HEAD=0003；正式升级需维护窗口备份/upgrade/check，旧备份先升级。无历史数据批改或生产部署。

无键旧客户端仍每次累计。清除存储、更换浏览器或多标签页同时创建独立新意图无法自动认定为同一收货；人工放弃先核对流水。取消/审批竞争、过时盘点和采购创建边界仍待做。既有弃用、大包与扫描边界保留，测试不是现场投运证明。

## 下一项具体动作

先处理取消/审批与首次收货竞争。读取 main 的 purchase_requests 状态入口、库存锁及 test_receipt_replay/test_stock_transactions。先用整单最后到货 5 件的场景，用两个真实连接固定“收货取得备件锁后、取消读取并写状态”的交错，核对最终状态、received_qty、库存与流水。先复现，再确定共用锁顺序和状态刷新；保留已成功 UUID 的重放行为。写单独设计及失败回归后最小修复，不重做已交付去重或迁移。

随后是过时 ADJUST 快照版本、采购创建/自动补货精度金额、超量收货政策及编号竞争；认证依赖与前端加载测量继续按长期路线。

## 本地接续

- worktree：`/workspace/worktrees/equipment-autonomous-20261003`，分支 `maintenance/receipt-idempotency-20261003`，已推送，工作树干净。
- 主 checkout：`/workspace/equipment-inspection`；新会话先 fetch 并核对真实 main。
- 文档 checkout：`/workspace/smart-power-plant`，分支 `docs/receipt-release-20261003`。
- venv：`/workspace/scratch/inspection-venv`；PG包装：`/workspace/scratch/pg-tools`，需重建隔离容器。测试容器/临时服务已停止。
- 本轮日志：scratch 下 receipt-red、receipt-green、receipt-snapshot-red/green、receipt-review-browser-red、receipt-full-final、receipt-node-final、receipt-e2e-verified、receipt-interview-final；完整后端 XML 为 receipt-final.xml。

若工作区重建，按固定提交与哈希锁恢复，不依赖本地路径仍存在。接续前核对实际 Git/PR 与文档，不按历史快照从头执行。
