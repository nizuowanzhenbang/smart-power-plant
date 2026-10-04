# 2026-10-04 煤质重评保护发布证据

[coal-quality-monitor PR #2](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/2) 已合并。固定 main：`f6efd459f596293fe21ddd44104eb48a957684b6`；源提交：`3aaec74f918d76b527e7c733608a310de7c5353e`；本地审查/验收、上传及最终 main tree 均为 `80e49442d2bba59b3ebb5f919658205999c1bc09`。前一基线为 `11bb3c8c8f11f64b599c22ca681cee5a45c35106`。

设备点检固定版本仍为 `76d799c1fc781147ea6bbdeaff0ee57e8bc659db`，见[设备点检发布快照](RELEASE-STOCKTAKE-20261004.md)；本轮没有重复设备点检验收或把其测试数加进煤质结果。

## 问题与结果

真实隔离接口复现：两份正常化验后收到严重铅封运输预警，批次SEVERE、数量1；再评估删除了运输证据，批次COMPLETED、数量/风险归零，供应商重算100分。

现在质量评估只替换八类自有预警，保留三类运输记录全部字段及处理信息。显式flush后按实际全部记录汇总；只有严重铅封时仍SEVERE、数量1、风险0.60，按现有规则重算供应商95分。支持手动重评、第二份化验自动评估、既有化验修改后的重评；过时质量预警仍能清除，另一批次不变。

响应alerts及广播继续仅含新生成质量预警，汇总字段包含两来源。已处理运输预警的历史评分政策保留。新预警替换/汇总事务在真实插入故障下回滚。一次整分支独立审查无Critical/Important/Minor发现，另作SQLite缓存关系、关闭autoflush、复用质量ID、处理状态及风险上限边界检查通过。

## 实际验证

| 检查 | 结果 |
|---|---|
| 原有基线 | 21 passed |
| 新数据库回归先失败 | 6 failed / 2 passed，失败均为运输证据被删 |
| 新实际API回归先失败 | 5 failed / 1 passed，鉴权控制通过 |
| 修复后完整本地后端 | 35 passed、0 failed、0 skipped；含新增数据库8项、API6项 |
| TypeScript/Vite / Ruff / diff / pip check | 全部通过 |
| [PR Quality](https://github.com/nizuowanzhenbang/coal-quality-monitor/actions/runs/37190541433) | success；backend35 passed/Ruff，frontend构建 |
| [新main Quality](https://github.com/nizuowanzhenbang/coal-quality-monitor/actions/runs/37190662818) | success；backend35 passed/Ruff，frontend构建 |

测试使用真实临时SQLite、JWT及角色查询、集成密钥检查和实际路由。没有替换评估算法或数据库查询，没有操作默认演示库或进入默认应用lifespan。14项新增回归已包含在35项中，各作业重叠用例不相加。

本地Python3.12.14、Node24.19.0；远端Python3.11、Node22。项目依赖范围未改，另建独立venv安装项目/dev requirements；本地FastAPI0.142.2、Pydantic2.13.5、SQLAlchemy2.1.3、pytest8.4.2。Python范围依赖未固定为哈希锁，保留未来版本兼容核查。357条本地弃用警告与已有2394.64kB前端包警告保留。本轮没有新增浏览器验收、依赖安全扫描或PG专项检查。

## 兼容、恢复与后续

没有迁移、接口字段、依赖文件或前端源码变化。升级不会找回已删除的历史运输证据，须从可信运输源或备份核对恢复。运输事件自身替换/重放、并发写入以及化验保存/评估分阶段提交属于既有边界，不新增全局原子性或容量承诺。

同轮只读核查另有两个待修范围：plant-safety的客户端hazard_id可阻塞实际隐患转换；coal-quality的Infinity化验输入可被判正常。均为隔离探针证据，没有在本轮修复。下一轮优先隐患关联隔离，具体版本、入口和探针见[交接](ITERATION-STATUS.md)。

[固定版本技术说明](https://github.com/nizuowanzhenbang/coal-quality-monitor/blob/f6efd459f596293fe21ddd44104eb48a957684b6/docs/TRANSPORT-ALERT-REEVALUATION.md) · [长期规划](LONG-TERM-PLAN-20261003.md)。
