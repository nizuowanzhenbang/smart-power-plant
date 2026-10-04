# 2026-10-03 收货重放发布证据

这是 PR #12 的历史发布快照。当前演示版本及后续采购状态竞争修复见 [2026-10-04 发布证据](RELEASE-PURCHASE-STATE-20261004.md)；以下提交、测试与当时待做范围保留作历史记录。

[PR #12](https://github.com/nizuowanzhenbang/equipment-inspection/pull/12) 已合并。固定演示 main 为 `04f898fb63f4b389f95eba264eff3b7138850870`；源提交 `fc9f4102d51fad3901728df8f5d6a1c87b944a7b`。本地验证、上传、最终 main tree 均为 `ca4a2495466f632f9f566b3c57ba684c4868a62a`。此前 #11 与 #4–#10 的成果全部保留；[上一发布快照](RELEASE-20261003.md)只作历史参考。

## 问题与最终行为

分批收到 2 件，服务器已入库但浏览器没收到响应，旧流程会在重试时再次累计。现在可选 UUID 与采购单绑定，同账户及数值等价数量重试返回首次快照，只记账一次；换数量/操作人返回 409。已完成或取消的原成功请求仍可确认，无键旧客户端保留每次累计行为。

库存、采购数量、流水及成功快照同事务提交；记录写入失败不占用键。首次响应在提交前固定快照，避免下一批在响应发送前提交而污染首次结果。前端发送前持久化，刷新/关闭后保留；两个标签页固定各自显示的原请求，确认和人工放弃不删除更新后的记录。账户变化时先阻止发送，并绑定校验过的凭证。

独立整分支审查发现三个 Important：旧标签页生成/切换请求、混用账户凭证、放弃旧记录误删新记录。均先复现再修复，并用真实浏览器/账户与 Node 回归。无剩余 Important 或 deferred minor。

## 证据

| 检查 | 实际结果 |
|---|---|
| API/迁移第一轮红绿 | 28 failed / 31 passed → 59 passed |
| 提交后响应竞争 | SQLite/PG 2 failed → 2 passed |
| 后端完整本地 | 404 passed、0 skipped，含真实 PG 142 项 |
| Node / TypeScript / Vite | 16 passed / 构建通过 |
| 本地 Chromium | 8 passed，SQLite/Vite，含响应丢失、两标签页、新批次、换账户 |
| API 面试演示 | 35 checks，status=passed |
| Ruff / diff / 上传树 | 通过 / 通过 / 与测试树一致 |
| [PR Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37162973445) | success；backend262 passed/142 skipped；PG专项232 passed（142PG+90SQLite）；frontend16/audit/build |
| [PR Compose](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37162973440) | success；实际 nginx/PG 冷启动、就绪、Chromium 8 项和日志检查 |
| [新 main Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37163166239) | success；backend262 passed/142 skipped，PG232 passed，frontend16/audit/build |

本地 Python 3.12.14、Node 24.19.0，远端 Python 3.11、Node 22。普通后端跳过的 PG 场景由专用作业执行；不将 skip 记为 pass。Python 弃用和已有大包警告保留。

## 升级与范围

新增冻结 `0003_purchase_receipts` 与第十五张表；0001/0002 及原十四表合同不变。正式模式先维护窗口备份，显式 `python -m app.migrate upgrade` / `check`，再启动。旧 0002 数据保留，结构漂移拒绝，DDL 失败全事务回滚；旧备份恢复后需先升级。代码回退不能代替恢复旧数据库，不自动删除表或数据。

清除浏览器存储、更换浏览器、旧客户端、两个标签页同时创建全新业务意图不能靠服务端猜测去重；人工放弃前先核对流水。同数量的真实两批到货使用不同 UUID。取消/审批与首次收货竞争、过时 ADJUST、采购创建/自动补货精度和金额、超量政策及物料编号仍待后续。指定模拟场景和 CI 不等于现场容量或跨系统 exactly-once 证明。

[接口/恢复说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/04f898fb63f4b389f95eba264eff3b7138850870/docs/PURCHASE-RECEIPT-REPLAY.md) · [下一轮入口](ITERATION-STATUS.md) · [长期规划](LONG-TERM-PLAN-20261003.md)。
