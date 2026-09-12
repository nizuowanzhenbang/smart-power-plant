# 智慧电厂业务软件作品集

以电厂采购、燃料、设备、隐患和能效场景练习业务软件开发与维护。面向电力企业信息化岗位，重点展示需求分析、流程控制、数据可靠性、接口集成及工程验证。

**项目性质：个人软件原型与模拟场景。** 已有 10 个业务代码仓库；本仓库是导览与文档入口。尚未完成全平台联合验收，不宣称电厂生产投运、接入 DCS/SIS、替代现场两票制度或取得经济收益。

- [10 分钟演示路线](docs/DEMO.md)
- [维护记录与验收边界](docs/MAINTENANCE-20260912.md)
- [后续建设路线](docs/ROADMAP.md)
- [历史总体方案](docs/ARCHITECTURE-HISTORY.md)（含待验证设计，不作为交付证据）

## 推荐先看什么

| 顺序 | 作品 | 能展示的能力 | 代码证据 |
|---|---|---|---|
| 1 | 设备点检与缺陷管理 | 台账、点检、缺陷闭环；操作票的步骤顺序、角色校验、失败阻断和数据库保存 | [操作票接口](https://github.com/nizuowanzhenbang/equipment-inspection/blob/main/backend/app/api/operation_tickets.py)、该仓库维护 PR 中的回归测试 |
| 2 | 煤质监督 | 将化验结果与合同指标关联，触发质量预警 | [质量引擎与测试](https://github.com/nizuowanzhenbang/coal-quality-monitor/tree/main/backend) |
| 3 | 燃煤机组能效 | 将能效计算和业务接口拆开验证，说明算法输入与适用边界 | [算法与接口测试](https://github.com/nizuowanzhenbang/coal-unit-efficiency/tree/master/backend) |

先完整讲透一项，再用另外两项证明能力可以迁移。其余模块是扩展场景，不必在一次面试里逐项展示。

## 模块索引

| 仓库 | 业务范围 | 当前维护重点 |
|---|---|---|
| [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) | 设备台账、点检、缺陷、备件、两票原型 | 操作步骤完整性、数据库回归测试 |
| [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) | 煤质化验、合同指标、供应商评分 | 图表构建修复、质量引擎检查 |
| [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) | 运输重量、时长、铅封异常 | 编译修复、修正测试对象构造 |
| [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) | 供应商、合同、采购订单 | 应用与认证冒烟检查 |
| [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) | 入出场、库存、盘点、温度 | 温度筛选类型修复、基础检查 |
| [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) | 隐患排查与整改闭环 | 应用与认证冒烟检查 |
| [emission-monitoring](https://github.com/nizuowanzhenbang/emission-monitoring) | 排放数据、告警、报表 | 构建修复、基础检查 |
| [coal-unit-efficiency](https://github.com/nizuowanzhenbang/coal-unit-efficiency) | 燃煤机组能效分析 | 既有算法和接口回归测试 |
| [gas-fuel-metering](https://github.com/nizuowanzhenbang/gas-fuel-metering) | 燃气计量、热值、对账 | 既有计量和接口回归测试 |
| [gas-turbine-performance](https://github.com/nizuowanzhenbang/gas-turbine-performance) | 燃机与联合循环性能 | 既有性能和接口回归测试 |

各仓库的维护改动已在本地分支完成，计划通过 PR 交付；当前 GitHub 写入返回 403，尚未创建远端 PR。`gas-emission-monitoring` 本轮检查为空仓库，不计入已实现模块。

## 如何评价这套作品

- **业务理解**：能描述数据来自哪里、交给谁、如何处理异常。
- **实现能力**：能沿着前端请求、后端校验、数据库记录讲清一条链路。
- **质量意识**：有可重跑的测试和构建，知道测试覆盖不到什么。
- **信息化运维意识**：能说明账户权限、配置、备份恢复和接口故障的处理方案；计划中的能力明确标注。
- **诚实边界**：规则模型不等于经校准的工业模型，模拟数据不等于现场验证，HMAC 记录不等于第三方法律电子签章服务。
