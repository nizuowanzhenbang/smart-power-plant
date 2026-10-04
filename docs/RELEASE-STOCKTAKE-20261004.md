# 2026-10-04 过时盘点发布证据

本文件保留设备点检 PR #14 的固定基线与历史检查。作品集最新迭代为[煤质重评保护](RELEASE-COAL-QUALITY-20261004.md)；设备点检版本本轮未变。

[PR #14](https://github.com/nizuowanzhenbang/equipment-inspection/pull/14) 已合并。固定演示 main：`76d799c1fc781147ea6bbdeaff0ee57e8bc659db`；源提交：`d2f06048453ac7cbd319673a770ab46dcdff173d`。本地验收、上传及最终 main tree 均为 `16fa73b67b503296db888e102a7793768ba392dd`。前一基线 `170b8393e622d31e23a5a546419748183f07ce20` 与[采购状态发布快照](RELEASE-PURCHASE-STATE-20261004.md)保留历史；既有收货 UUID、状态竞争、精度与归零能力全部保留。

## 问题与最终行为

真实 SQLite 复现：读取库存 10，随后入库 2，旧盘点提交 10 被接受，最终库存恢复为 10。旧写锁只能串行写入，无法识别用户读取之后已经发生的库存变化。

现在备件响应包含同 SQL 读取的 `stock_revision`，取该备件最后一条已提交流水 ID，无流水为 0。ADJUST 携带 `expected_stock_revision`，取得备件锁并刷新后比较；缺失或过时返回 409，不修改库存和流水。先入后出回原数量也不能绕过。匹配版本允许归零；同版本重复或并发盘点只有一次成功。真实流水写入失败回滚后可按原版本重试。

首次收货、出入库和合法盘点生成新版本；成功收货 UUID 重放、另一备件流水、仅更新元数据不改变当前版本。成功出入库响应在 commit 前保存数量、流水及版本，随后发生的写入不污染首次响应。

前端保留打开时的快照；冲突后不静默换版本，不自动重试。关闭并刷新后重新核对、明确输入数量；取消或重开清空旧表单。实际请求等待期间禁止重复提交、编辑和关闭。

一次新整分支独立审查无 Critical、Important 或 Minor 发现；审查者另跑 6 项 SQLite 并发、快照、回滚及响应测试通过。没有待修审查项，没有独立重复整套 PG/浏览器检查。

## 验证证据

| 检查 | 实际结果 |
|---|---|
| 新后端回归先失败 | 42 failed / 2 passed；两个权限/缺失对象控制保持通过 |
| 库存/重放/采购状态及实际 HTTP 相关 | 修复后 268 passed（SQLite 与实际 PG） |
| 新浏览器回归先失败 | 3 failed；另一个已提交但延迟响应场景 1 failed，定位后修复 |
| 完整本地后端 | 492 passed、0 failed、0 skipped，包含实际 PostgreSQL 186 项 |
| 本地 Node / TypeScript / Vite | 16 passed / 构建通过 |
| 本地 Chromium | 11 passed、0 failed、0 skipped、0 flaky；隔离 SQLite/Vite |
| API 面试演示 | 35 checks，status=passed |
| Ruff / diff / 上传树 | 通过 / 通过 / 与审查及测试树一致 |
| [PR Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37183237858) | success；backend306 passed/186 skipped；PG专项320 passed（186PG+134SQLite）；frontend16/audit/build |
| [PR Compose](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37183237840) | success；实际 nginx/PG 冷启动、就绪、Chromium11项和日志检查 |
| [新 main Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37183510996) | success；backend306 passed/186 skipped；PG专项320 passed；frontend16/audit/build |

本地 Python3.12.14、Node24.19.0，远端 Python3.11、Node22。普通后端 PG skip 由专项实际执行，不计为 pass；各作业重叠用例不相加成新的测试数。本地报告中部署用例的标题仍提 nginx/PG，但该次运行环境是 SQLite/Vite；远端 Compose 才是实际 nginx/PG。真实 HTML 报告截图与简单结果保存在交接列出的本地文件。

浏览器诊断曾修正重复 ARIA 定位，及 AntD 保留 loading 图标导致的按钮名称匹配；没有延长超时或删减业务断言。当前扫描仅证明指定锁与阈值，5391 项既有 Python 弃用警告及前端大包警告保留。

## 兼容、恢复与边界

旧 ADJUST 客户端必须更新并携带期望版本；缺失/null 返回 409。版本必须为 JSON 整数 0..2147483647，布尔、浮点、字符串、负数或超限值 422。IN/OUT 可省略版本，角色、精度、关联对象及合法零盘点规则保留。没有新 DDL、依赖或迁移；HEAD保持 `0003_purchase_receipts`。从0002升级仍按原维护窗口备份、upgrade/check。

版本依赖追加流水合同；手工 SQL 修改库存、删除/修改流水及恢复数据库时仍打开的旧会话不在保证范围。恢复后重新读取并核对业务数据。ADJUST 响应丢失后不保证自动重放成功，必须刷新核对。代码回退不能恢复业务数据；回退服务端会重新接受无版本旧盘点。同步采购推送持锁与远端成功不能被本地回滚的既有边界仍保留。

下一项为采购创建/自动补货精度金额、超量政策与编号竞争的真实复现。指定模拟交错和 CI 不作为生产容量、现场投运或跨系统全局 exactly-once 证明。

[技术说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/STOCKTAKE-SNAPSHOT.md) · [下一轮入口](ITERATION-STATUS.md) · [长期规划](LONG-TERM-PLAN-20261003.md)。
