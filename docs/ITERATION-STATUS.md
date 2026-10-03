# 迭代进度与接续入口

更新日期：2026-10-03。[长期规划](LONG-TERM-PLAN-20261003.md)；主作品 equipment-inspection，辅助案例 coal-unit-efficiency 和 coal-quality-monitor。

## 授权与工作方式

用户已授权代理自主迭代、测试、推送 GitHub 及所有相关操作。常规开发、验证、推送和通过审查/检查后的合并自主推进，授权持续沿用。每轮一个明确目标，默认单代理；并发/数据一致性改动做必要的独立审查。

本轮没有配置后台定时任务。本文件用于恢复上下文，不假装有模型侧实时额度读数。

## 已完成与仍待做

| 单元 | 实际状态 |
|---|---|
| 01 | 作品集文档、演示路线、证据索引和交接已完成，随 smart-power-plant PR #5 集成；是否合并查实际 PR 状态 |
| 02 | #4–#9 元数据依赖和 CI 已核对；整条历史差异的独立审查、兼容性与集成阻塞复核未完成 |
| 03 | 库存修复候选已在干净虚拟环境复跑后端全量和 API 演示；远端 Compose 浏览器验收也通过 |
| 04 | 未形成 main 发布基线；依赖链尚未全部合并 main |
| 05–06 | 已核查库存写入口，修复出入库/采购收货并发及回滚；重复请求的完整幂等规则仍待建设 |
| 07–24 | 尚未完整执行；不把提前触及的一部分记成全部完成 |

## 本轮代码成果

- 库存 10 件时，两个请求各领 7 件，旧实现两次成功且只扣一次；SQLite 和 PostgreSQL 均复现。
- 出入库和采购收货共用备件事务写锁，等锁后刷新库存及采购状态；库存、流水和收货状态同事务。
- 新增 18 项回归验证并发领用、入库、收货/领用交错、完成订单竞争、拒绝权限和事务失败回滚。
- [设备点检 PR #10](https://github.com/nizuowanzhenbang/equipment-inspection/pull/10) 已合并至 #9 的候选分支；尚未进入 main。
- [复现、取舍及限制](https://github.com/nizuowanzhenbang/equipment-inspection/blob/2691882aaeeeaae493b8d0b01b3f22a2c60f178b/docs/STOCK-CONSISTENCY.md)。

## 仓库、分支与版本

- 文档仓库：`nizuowanzhenbang/smart-power-plant`，PR #5 分支 `docs/long-term-iteration-20261003`；文档最新 SHA 查 PR head，避免本文件自引用。
- 代码工作区：`/workspace/worktrees/equipment-autonomous-20261003`，分支 `maintenance/autonomous-reliability-20261003`。
- 代码开始提交：`8b86c084032a446d065cd64b54759e3e50c5d8bc`。
- 已测试并推送提交：`2691882aaeeeaae493b8d0b01b3f22a2c60f178b`。
- #10 合入 #9 后候选提交：`f6efc764fc166a003190925cc633b32600a51256`，分支 `maintenance/frontend-dependency-upgrade-20261001`。
- 本地 staged tree、GitHub 创建的 tree 及合并后候选 tree 均为 `eb99f16e6ca28bdadf60ce165fd8fd2f0d46b751`，内容一致。
- 已合并的旧演示基线仍为 `8b4551808524b76c7b50c3425396bd5a265ba080`，不能把候选当作 main。
- 尚未集成 main 的链：#4 → #5 → #6 → #7 → #8 → #9；#10 已进入 #9，不再作为后续待合并项。
- [单元 01 的历史元数据快照](EVIDENCE-20261003.md)记录旧 #9 head；本文件中的新候选覆盖当前接续版本。

## 实际验证

| 检查 | 结果 |
|---|---|
| 修复前新增库存回归 | 12 failed / 6 passed，已读到预期响应和库存断言失败 |
| 修复后库存回归 | 18 passed |
| 本地完整后端 `python -m pytest -q` | 227 passed、0 skipped，包含真实 PostgreSQL 56 项 |
| API 面试演示 | 35 checks passed；本地报告 `/workspace/scratch/inspection-interview-20261003.json` |
| 前端 Node 测试 / TypeScript 与生产构建 | 7 passed / 构建通过 |
| Ruff E9/F63/F7/F82 / diff 检查 | 通过 |
| 独立只读代码审查 | 本轮变更无阻塞；不宣称已经审查整条历史候选链 |
| [Quality checks](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37139047092) | 提交 2691882aaeeeaae493b8d0b01b3f22a2c60f178b 的 backend、postgresql、frontend 均 success |
| [Compose browser acceptance](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37139047084) | 同一提交的 compose-browser success |

本地 Python 3.12.14 / Node 24.19.0，后端按哈希锁安装；PostgreSQL 16 使用独立容器及匹配客户端包装。远端 CI 是 Python 3.11 / Node 22。既有弃用与大包警告仍在，没有宣称无警告、全平台验收或现场投运。

本轮没有 schema、历史数据、生产配置或部署变更。代码回退会恢复旧并发风险，也不会纠正历史库存流水差异。测试只触及自己创建的 schema、数据库和模拟对象。

## 下一项具体操作

继续单元 02：读取设备点检 #4 的 diff 和 PostgreSQL 说明，核对 UUID 编号兼容性、锁/事务边界及回归；依次审查 #5–#9 的集成要求。候选已包含 #10，别再次单独合并 #10 或重复实现库存锁。

库存后续核查：部分收货重传仍会累计，未提供请求幂等键；取消/审批/收货竞争、过时盘点快照、精度校验、盘点清零、超量收货政策和新物料编号竞争仍未覆盖。按实际问题拆成下一轮的小任务。

## 本轮决定

发现真实库存竞争后，先完成一项范围明确、可复现的修复，而没有凭过去绿灯批量合并未审查的历史 PR。代价是单元 02 的完整差异复核仍待下一轮；收益是已有一项真实红到绿、远端通过并进入候选的代码成果。

沿用文档 PR #5 保存进度，避免新增文档草稿链。测试通过、独立审查完成后，按用户新授权合并 #10 到候选分支。未来接续优先核对实际 head；没有变化的文件与检查不重复全量扫描。
