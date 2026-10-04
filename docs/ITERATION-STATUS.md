# 迭代进度与接续入口

更新日期：2026-10-04。[长期规划](LONG-TERM-PLAN-20261003.md)。主作品 equipment-inspection；辅助案例 coal-unit-efficiency、coal-quality-monitor。

## 授权与方式

用户持续授权自主迭代、长时间分析、测试、GitHub 推送与必要审查；验证后的合并自主完成。默认单代理、每轮一个主目标，复杂变化单独做一次整分支审查。无后台定时任务、模型侧实时额度读数或跨账户限制运行承诺；额度/上下文切换后从本文件继续。

## 实际进度

| 单元 | 状态 |
|---|---|
| 01–04 | 完成；#11 收拢历史成果，#12/#13 更新演示基线，历史 #4–#10 不重复实施 |
| 05–06 | 库存锁、事务流水、收货重放及六入口采购状态竞争保护完成 |
| 07 | 精度、累计上限、盘点归零完成；过时绝对盘点保护为下一项 |
| 08–24 | 尚未完整执行；已有迁移/恢复与依赖升级证据按实际范围复用 |

## 当前固定版本

- 仓库：`nizuowanzhenbang/equipment-inspection`。
- 最新 main：`170b8393e622d31e23a5a546419748183f07ce20`，由 [PR #13](https://github.com/nizuowanzhenbang/equipment-inspection/pull/13) 合并。
- 源提交：`63653ebfddec80101a9b689e110b0c82ab5d2232`；本地/上传/main tree：`56b62bec60a1ede25494a8ccb2380c0a6ebd823e`。
- 前一基线 `04f898fb63f4b389f95eba264eff3b7138850870` 与[收货重放发布快照](RELEASE-RECEIPTS-20261003.md)保留历史；#4–#10 成果已纳入 #11。
- 本轮后端448（真实PG164）、Node16、API35、tsc/Vite/Ruff/diff全部通过；PR Quality/Compose success（远端Chromium8），新 main Quality success。详见[完整证据](RELEASE-PURCHASE-STATE-20261004.md)。
- 文档仓库：`nizuowanzhenbang/smart-power-plant`，实际文档版本查 main 历史，避免自引用 SHA。

## 完成与限制

六个既有状态入口统一在备件锁后刷新采购单。最终收货先完成则取消400；部分收货后取消仍合法并保留已成功 UUID。批准和发送的状态、元数据及审计同事务；真实审计约束失败全部回滚。使用真实 SQLite/PG 和本地 HTTP 服务验证竞争、发送失败恢复及发送/最后收货交错。一次整分支独立审查无发现；独立复跑48项SQLite通过。

本轮没有迁移、依赖或前端源码变化，HEAD保持0003；从0002升级仍按原维护窗口备份/upgrade/check。同步外部推送持备件锁，PostgreSQL 同备件写入会等待，SQLite 写锁也会阻塞其他写入。远端成功而本地失败不能撤销远端订单，重发前核对外部系统；outbox、远端去重、取消通知等留待后续。

原无键客户端、清除浏览器存储、更换浏览器和多标签页新建独立意图的去重边界仍保留。过时盘点、采购创建/自动补货精度金额、超量政策及编号竞争待做。弃用、大包与扫描范围限制见发布证据；本轮无生产部署或容量证明。

## 下一项具体动作

处理过时绝对盘点。先读 main 的 `backend/app/api/spare_parts.py`、`backend/app/schemas/spare_part.py`、`frontend/src/pages/SparePartList.tsx` 和 `backend/tests/postgresql/test_stock_transactions.py`。ADJUST 目前把库存直接置为 qty，现有写锁只能串行提交，不能辨认用户读取盘点快照后发生的出入库。先用真实 SQLite/PG 固定“读取库存10 → 新增入库2 → 旧快照盘点为10”的交错，检查库存与流水是否静默丢失新增2。此处是待复现范围，不把未运行的场景写成已确认缺陷。

再比较版本号与期望状态方案，确定旧客户端及迁移兼容、冲突响应和前端重读确认；单独写设计、失败回归后最小修复。保留当前收货 UUID 与合法部分取消行为，不重做既有库存锁或迁移。

随后核查采购创建/自动补货精度金额、超量政策与编号竞争；认证依赖、前端加载及可靠联动继续按长期路线。

## 本地接续

- worktree：`/workspace/worktrees/equipment-autonomous-20261003`，分支 `maintenance/purchase-state-20261004`，已推送，工作树干净。
- 主 checkout：`/workspace/equipment-inspection`；新会话先 fetch 并核对真实 main。
- 文档 checkout：`/workspace/smart-power-plant`，分支 `docs/purchase-state-release-20261004`。
- venv：`/workspace/scratch/inspection-venv`；PG包装：`/workspace/scratch/pg-tools-20261004`，复跑须重建对应隔离容器 `inspection-pg-20261004`。本轮自建测试容器/临时服务已停止。
- 日志：scratch 下 purchase-state-red、purchase-audit-red、purchase-http-red、purchase-state-atomic-green、purchase-state-full、purchase-state-node、purchase-state-build、purchase-state-interview；完整后端 XML：purchase-state-final.xml。审查/交付摘要：purchase-state-progress-final.md。

若工作区重建，按固定提交与哈希锁恢复，不依赖本地路径仍存在。接续前核对实际 Git/PR 与文档，不按历史快照从头执行。
