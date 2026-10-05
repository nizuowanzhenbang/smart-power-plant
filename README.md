# 智慧电厂业务软件作品集

以电厂采购、燃料、设备、隐患和能效场景练习业务软件开发与维护。面向电力企业内部招聘，重点展示业务理解、流程控制、数据可靠性及工程验证；按信息化、生产技术或安全管理岗位调整讲解深度。

**项目性质：个人软件原型与模拟场景。** 已有 10 个业务代码仓库；本仓库是导览与文档入口。尚未完成全平台联合验收，不宣称电厂生产投运、接入 DCS/SIS、替代现场两票制度或取得经济收益。

- [10 分钟演示路线](docs/DEMO.md)
- [本轮化验输入发布证据](docs/RELEASE-COAL-FINITE-20261005.md)
- [煤质输入内部招聘案例](https://github.com/nizuowanzhenbang/coal-quality-monitor/blob/d58a634e2dee43256ed27d6915903f70353f9219/docs/LAB-FINITE-VALUES.md)
- [安全检查发布证据](docs/RELEASE-SAFETY-20261004.md)
- [安全检查内部招聘讲解卡](https://github.com/nizuowanzhenbang/plant-safety/blob/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df/docs/CHECK-HAZARD-OWNERSHIP.md)
- [煤质发布证据](docs/RELEASE-COAL-QUALITY-20261004.md)
- [设备点检固定基线](docs/RELEASE-STOCKTAKE-20261004.md)
- [首次核对的历史证据快照](docs/EVIDENCE-20261003.md)
- [长期迭代规划](docs/LONG-TERM-PLAN-20261003.md)
- [本轮进度与下一步](docs/ITERATION-STATUS.md)
- [维护记录与验收边界](docs/MAINTENANCE-20260912.md)
- [后续建设路线](docs/ROADMAP.md)
- [历史总体方案](docs/ARCHITECTURE-HISTORY.md)（含待验证设计，不作为交付证据）

## 当前交付状态（2026-10-05 核对）

设备点检已通过 [PR #14](https://github.com/nizuowanzhenbang/equipment-inspection/pull/14) 集成到 main，固定演示提交为 `76d799c1fc781147ea6bbdeaff0ee57e8bc659db`。该基线包含离线重传、点检/验收与库存并发、运行配置、迁移恢复、可复现部署和前端升级，并新增数量精度、盘点归零、恢复目标隔离、采购收货重放幂等、状态竞争及过时盘点保护。#4–#9 的全部历史提交已纳入该基线，旧草稿已收拢。

[设备点检发布证据](docs/RELEASE-STOCKTAKE-20261004.md)记录本地后端 492 项（含实际 PostgreSQL 186 项）、前端 16 项、远端 Chromium 11 项及 GitHub 检查。按固定提交的文档准备独立演示环境；合并与绿灯说明代码和指定检查的状态，现场投运仍需单独验收。

该设备版本要求旧 ADJUST 客户端更新并携带库存版本，缺失或过时返回 409；冲突后刷新库存并重新输入盘点数量，无需新数据库迁移。

煤质监督前轮通过 [PR #2](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/2) 合并，该轮固定 main 为 `f6efd459f596293fe21ddd44104eb48a957684b6`。化验重评保留运输预警及处理记录，合并计算批次风险，供应商重算保留运输扣分。完整后端35项（含新增14项实际数据库/API回归）、构建及 PR/新main Quality 均通过，见[煤质证据](docs/RELEASE-COAL-QUALITY-20261004.md)。

安全检查已通过 [plant-safety PR #2](https://github.com/nizuowanzhenbang/plant-safety/pull/2) 合并，固定 main `24e33ec011c0d0cc3dd3d9dcc79dffb1440541df`。提交检查结果拒绝客户端指定隐患编号，正常转换由服务器保存真实关联。完整后端15项（含新增13项）、构建、PR/新main检查通过，见[发布证据](docs/RELEASE-SAFETY-20261004.md)。

本轮化验创建和修改通过 [煤质 PR #3](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/3) 集成，固定 main `d58a634e2dee43256ed27d6915903f70353f9219`。8指标拒绝NaN、无穷及指数溢出并返回可序列化422；正常有限值、省略/null和既有预警/评分行为有回归。完整后端110项（含新增75项参数化回归）、构建和PR/新main检查通过，见[本轮证据](docs/RELEASE-COAL-FINITE-20261005.md)。

## 推荐先看什么

| 顺序 | 作品 | 能展示的能力 | 代码证据 |
|---|---|---|---|
| 1 | 设备点检与缺陷管理 | 弱网重传、缺陷闭环、角色审计、并发库存、迁移恢复与部署验收 | [固定基线 API 演示](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/DEMO.md)、[集成验证](docs/RELEASE-STOCKTAKE-20261004.md) |
| 2 | 煤质监督 | 化验与运输预警保留、风险汇总及供应商扣分依据 | [输入校验与面试案例](https://github.com/nizuowanzhenbang/coal-quality-monitor/blob/d58a634e2dee43256ed27d6915903f70353f9219/docs/LAB-FINITE-VALUES.md)、[本轮验证](docs/RELEASE-COAL-FINITE-20261005.md)、[前轮重评保护](docs/RELEASE-COAL-QUALITY-20261004.md) |
| 3 | 安全检查转隐患 | 业务断点、输入信任边界、权限拒绝和故障回滚 | [案例与面试追问](https://github.com/nizuowanzhenbang/plant-safety/blob/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df/docs/CHECK-HAZARD-OWNERSHIP.md) |
| 4 | 燃煤机组能效 | 模型留出评估、基线比较与规则降级；说明算法输入和适用边界 | [已合并的模型质量 PR #2](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/2) |

先完整讲透一项，再按岗位选择一到两项辅助案例。其余模块是扩展场景，不必在一次面试里逐项展示。

## 模块索引

| 仓库 | 业务范围 | 当前维护重点 |
|---|---|---|
| [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) | 设备台账、点检、缺陷、备件、两票原型 | 固定展示基线；收货重放、状态竞争与过时盘点保护已交付；下一项为采购创建及自动补货边界 |
| [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) | 煤质化验、合同指标、供应商评分 | 运输预警重评保护及非有限输入校验已交付；单位/范围等规则继续核查 |
| [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) | 运输重量、时长、铅封异常 | 编译修复、修正测试对象构造 |
| [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) | 供应商、合同、采购订单 | 应用与认证冒烟检查 |
| [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) | 入出场、库存、盘点、温度 | 温度筛选类型修复、基础检查 |
| [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) | 隐患排查与整改闭环 | 隐患关联隔离已交付；整改期限上限等边界待修 |
| [emission-monitoring](https://github.com/nizuowanzhenbang/emission-monitoring) | 排放数据、告警、报表 | 构建修复、基础检查 |
| [coal-unit-efficiency](https://github.com/nizuowanzhenbang/coal-unit-efficiency) | 燃煤机组能效分析 | 既有算法和接口回归测试 |
| [gas-fuel-metering](https://github.com/nizuowanzhenbang/gas-fuel-metering) | 燃气计量、热值、对账 | 既有计量和接口回归测试 |
| [gas-turbine-performance](https://github.com/nizuowanzhenbang/gas-turbine-performance) | 燃机与联合循环性能 | 既有性能和接口回归测试 |

历史维护记录中的 GitHub 写入 403 和草稿依赖链是当时的状态。设备点检、煤质监督与安全检查按各自发布快照完成集成；其他模块的历史维护重点保留作索引，本轮实施煤质输入修复，未重新验收全部仓库。`gas-emission-monitoring` 在 2026-09-12 记录中为空仓库，本轮未重新检查，不计入这份作品集的已实现模块。

## 如何评价这套作品

- **业务理解**：能描述数据来自哪里、交给谁、如何处理异常。
- **实现能力**：能沿着前端请求、后端校验、数据库记录讲清一条链路。
- **质量意识**：有可重跑的测试和构建，知道测试覆盖不到什么。
- **信息化运维意识**：能说明账户权限、配置、备份恢复和接口故障的处理方案；计划中的能力明确标注。
- **诚实边界**：规则模型不等于经校准的工业模型，模拟数据不等于现场验证，HMAC 记录不等于第三方法律电子签章服务。
