# 2026-10-04 采购状态竞争发布证据

本文件保留 PR #13 当时的历史版本、检查和下一步。当前演示基线已更新，见[过时盘点发布证据](RELEASE-STOCKTAKE-20261004.md)。

[PR #13](https://github.com/nizuowanzhenbang/equipment-inspection/pull/13) 已合并。固定演示 main：`170b8393e622d31e23a5a546419748183f07ce20`；源提交：`63653ebfddec80101a9b689e110b0c82ab5d2232`。本地验收、上传及最终 main tree 均为 `56b62bec60a1ede25494a8ccb2380c0a6ebd823e`。前一基线 `04f898fb63f4b389f95eba264eff3b7138850870` 与[收货重放发布快照](RELEASE-RECEIPTS-20261003.md)保留历史；此前能力全部保留。

## 问题与最终行为

最终5件收货已入库，先读到旧 APPROVED 状态的取消可能把 RECEIVED 覆盖为 CANCELLED。旧状态的提交、批准、驳回和推送也可能在取消后重新修改单据。现在六个既有状态入口与收货共用备件锁，取得锁后刷新采购单及备件关系，再按当前状态判断。

取消先完成时，等待中的首次收货等操作被拒绝；最终到货先完成时取消400，库存、received和流水一致。部分到货2件后取消仍合法，不退库，原成功UUID继续返回首次快照。批准/驳回竞争与重复状态操作须重新判断，不能用“总是只有一个成功”误禁止合法的先后操作。

审批状态、操作人、时间与审计同事务；发送状态、时间、外部单号与审计也一起提交。推送服务停止内部 commit。真实数据库审计约束失败不留下部分状态；解除故障后恢复操作。

一次新整分支独立审查无 Critical、Important 或 Minor 发现；审查者独立复跑48项SQLite通过，48项PG有意排除，另核对本轮真实PG证据。保留已解释的同步持锁与远端不能回滚的取舍，无待修审查项。

## 验证证据

| 检查 | 实际结果 |
|---|---|
| 状态竞争先失败/后修复 | 22 failed / 6 passed；加锁后状态/库存/重放相关80 passed |
| 审计约束失败 | 4 failed → 状态与审计回滚通过 |
| 实际本地HTTP | 2 failed / 8 passed → 10 passed；包含真实负载、503/坏JSON、发送与收货等待、远端成功/本地失败 |
| 采购状态/HTTP/重放/库存相关 | 96 passed（SQLite与实际PG） |
| 完整本地后端 | 448 passed、0 skipped，包含实际PostgreSQL164项 |
| Node / TypeScript / Vite | 16 passed / 构建通过 |
| API面试演示 | 35 checks，status=passed |
| Ruff / diff / 上传树 | 通过 / 通过 / 与测试树一致 |
| [PR Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37178519919) | success；backend284 passed/164 skipped；PG专项276 passed（164PG+112SQLite）；frontend16/audit/build |
| [PR Compose](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37178519939) | success；实际nginx/PG冷启动、就绪、Chromium8项和日志检查 |
| [新main Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37178800978) | success；backend284 passed/164 skipped；PG专项276 passed（164PG+112SQLite）；frontend16/audit/build |

本地Python3.12.14、Node24.19.0，远端Python3.11、Node22。普通后端的PG skip由专项执行，不计为pass。浏览器本轮由远端Compose复验既有8场景，未新增前端源码或重复本地浏览器全量。当前依赖扫描仅证明指定锁及阈值检查；Python弃用与已有大包警告保留。

## 范围、恢复与下一步

无新迁移、依赖或前端源码变化；HEAD保持 `0003_purchase_receipts`，既有0001/0002及原表合同不变。已有0003部署按原流程运行；从0002升级继续先维护窗口备份、显式upgrade/check。代码回退不能恢复业务数据；需要时在独立目标恢复核验后切换。

同步发送在HTTP期间持备件锁，沿用既有 `PROCUREMENT_TIMEOUT_SEC`（默认5秒）；PG同备件写入会等待，SQLite写锁还会阻塞其他写入。HTTP失败或坏JSON保留APPROVED，结束请求后释放锁。远端已成功而本地审计/提交失败，数据库回滚无法撤销远端订单，重发前先核对外部系统。本轮有实际失败演练，没有修改上游成功判定、增加自动重试或承诺耗时上限。持久化投递、远端去重与取消通知属于后续范围。

下一项为过时ADJUST快照保护；采购创建/自动补货精度金额、超量政策与编号竞争继续待核查。指定模拟交错与CI通过不能证明生产容量、现场投运或跨系统全局exactly-once。

[技术说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/170b8393e622d31e23a5a546419748183f07ce20/docs/PURCHASE-STATE-CONSISTENCY.md) · [下一轮入口](ITERATION-STATUS.md) · [长期规划](LONG-TERM-PLAN-20261003.md)。
