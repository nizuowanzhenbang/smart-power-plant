# 迭代进度与接续入口

更新日期：2026-10-03。[长期规划](LONG-TERM-PLAN-20261003.md)；主作品 equipment-inspection，辅助案例 coal-unit-efficiency 和 coal-quality-monitor。

## 授权与工作方式

用户已授权代理自主迭代、长时间分析、自动化测试、推送 GitHub 及所有相关操作。常规开发、验证、推送和通过必要审查/检查后的合并自主推进，授权持续沿用。每轮保持明确范围，独立历史审查与风险修复可并行完成。

本轮未配置后台定时任务，没有模型侧实时额度读数。本文件用于额度窗口或会话切换后的接续；不承诺跨越账户限制持续运行。

## 已完成与仍待做

| 单元 | 实际状态 |
|---|---|
| 01 | 导览、演示、证据及交接完成；原文档 PR #5 已合并，当前更新查本文件提交历史 |
| 02 | #4–#9 元数据、全部历史差异、核心/配置/迁移/交付/前端独立复核完成；发现的恢复目标问题已修复 |
| 03 | 候选在隔离环境全量复验，API 闭环、真实 PG 和远端 Compose 浏览器通过 |
| 04 | #11 已合并 main，形成固定展示基线；main 新 CI 通过，源码逆补丁检查通过；数据恢复另按现有工具验证 |
| 05–06 | 出入库/采购收货主要写入口、并发及失败回滚已验证；部分收货重放幂等仍待补齐 |
| 07 | 数量精度、累计上限和盘点归零已修复；过时绝对盘点快照/版本保护仍待做 |
| 08–24 | 尚未完整执行；迁移恢复已有验证可复用，不按旧列表重复开发 |

## 固定版本与 GitHub 状态

- 代码仓库：`nizuowanzhenbang/equipment-inspection`。
- 固定 main 基线：`b2bd35cea7ad40a0a0ab9b836707b6af6539738b`，由 [PR #11](https://github.com/nizuowanzhenbang/equipment-inspection/pull/11) 合并。
- 本轮开始候选：`f6efc764fc166a003190925cc633b32600a51256`；修复提交：`2f24753fff332d28dc1df0875b4a6fbaa4acbfb9`。
- 已测试本地、上传代码及合并 main 的 tree 均为 `d8f39a42953d1529c2b57d3086132aa1b8fc55bf`，内容一致。
- #4 自动显示已合并；#5–#9 关闭为被 #11 集成，merged=false 不代表代码遗漏。六个历史 head 均已验证为 main 的祖先。#10 已在原 #9 候选中，不需重复合并。
- 旧 API 基线 `8b4551808524b76c7b50c3425396bd5a265ba080` 和[首轮证据快照](EVIDENCE-20261003.md)仅作为历史记录。
- 文档仓库：`nizuowanzhenbang/smart-power-plant`；当前文档提交查实际 main 历史，避免自引用 SHA。

## 本轮修复与验证

库存输入统一有限非负两位 Decimal，范围与 Numeric(10,2) 一致；原始位数检查防止长尾精度绕过。锁内检查累计库存及收货上限，拒绝时库存、流水与采购状态不变。ADJUST 支持 0，前端失焦不再改成 0.01，实际零库存和流水均有浏览器回归。

恢复工具提前拒绝含 `=` 或以 PostgreSQL URI 前缀开头的库名，防止 pg_restore 重解释目标。真实 PG 先复现错误库写入，修复后验证原业务表和行保留、字面目标仍空。

| 检查 | 实际结果 |
|---|---|
| 首批库存边界 | 修复前 70 failed / 40 passed；修复后 110 passed |
| 长尾精度追加 | 修复前 18 failed；最终纳入完整验证，共库存新增 128 项 |
| 恢复路由追加 | 修复前 7 failed；专项修复后 19 passed |
| 本地完整后端 | 362 passed、0 skipped，含真实 PostgreSQL 121 项 |
| API 面试演示 | 35 checks，status=passed |
| 前端 Node / TypeScript / Vite | 7 passed / 构建通过 |
| 本地 Chromium | 5 passed；本地是 SQLite/Vite，部署组合由远端另验 |
| 独立复核 / Ruff / diff | 无剩余重要问题 / 通过 |
| [修复提交 Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37144133975) | backend、postgresql、frontend success |
| [修复提交 Compose](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37144134103) | success；实际 nginx/PG 冷启动、就绪、Chromium 5 项及日志检查 |
| [合并 main Quality](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37144413840) | success；backend 241 passed / 121 skipped，PG 专项 194 passed（121 PG + 73 SQLite），前端 7 项/扫描/构建通过 |
| 源码回退检查 | 对旧 main 的完整逆补丁检查通过；未实际回退代码或业务数据 |

[完整发布证据](RELEASE-20261003.md)。本地 Python 3.12.14 / Node 24.19.0，远端 Python 3.11 / Node 22。既有弃用与大包警告保留；未宣称无漏洞、完整浏览器离线流程或现场投运。

本轮没有新增 schema、历史数据改写或生产部署。测试仅使用隔离 schema、独立恢复库和模拟账户。本地测试容器及临时服务已停止；工作树保留供下一轮使用，忽略的演示库和构建文件不提交、不作为正式数据源。

## 下一项具体操作

优先补齐部分采购收货重放幂等。先读取 main 的 `backend/app/api/purchase_requests.py`、库存模型、迁移合同及现有 stock 测试；复现同一部分到货请求在响应丢失后重发造成双记账，再设计稳定请求键、内容冲突及与库存/流水同事务的记录。明确旧客户端兼容与数据库迁移范围，先失败回归再最小实现。

随后处理取消/审批/收货竞争、过时 ADJUST 版本保护、采购创建/自动补货精度与金额上限、超量收货业务政策和物料编号竞争。认证依赖核查及前端加载测量仍按长期路线推进。不要重复实现已合入 main 的锁、迁移、部署或依赖升级。

## 本地接续

- 代码 worktree：`/workspace/worktrees/equipment-autonomous-20261003`，分支 `maintenance/release-baseline-20261003`，已推送且代码工作树干净。
- 主 checkout：`/workspace/equipment-inspection`；先 fetch 再判断本地 main，勿误把旧本地 main 当最新远端。
- 文档 checkout：`/workspace/smart-power-plant`，分支 `docs/release-baseline-20261003`。
- venv：`/workspace/scratch/inspection-venv`；PG 客户端包装：`/workspace/scratch/pg-tools/`，需重建独立测试容器才能使用。
- red/green/全量证据位于 `/workspace/scratch/stock-quantities-red.log`、`stock-long-decimal-red.log`、`backup-routing-red.log`、`backup-routing-green.log`、`inspection-full-round2.log`、`stock-browser-green.log`、`inspection-interview-round2.log`。

新一轮先核对真实 main/PR 与文档；若工作区被重建，按固定提交与哈希锁恢复环境，不依赖这些本地路径仍存在。
