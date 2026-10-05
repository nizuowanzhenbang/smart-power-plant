# 2026-10-05 化验非有限输入发布证据

[coal-quality-monitor PR #3](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/3) 已合并。main `d58a634e2dee43256ed27d6915903f70353f9219`；源 `5c532d0ba3626e9ab348559f9882eeb93d52c27e`；本地审查/验收、上传及main tree均为 `5348b5ce087138b3e82f92fc37f7809ff9067f25`。原基线 `f6efd459f596293fe21ddd44104eb48a957684b6`。

## 业务结果与面试用途

旧创建/修改的8指标Optionalfloat接受NaN/Infinity及指数溢出，正式真实API回归中52项输入返回200。异常可污染化验并改变偏差判定。现在请求类型使用有限数；解析后的非有限float转可序列化文本供校验拒绝，合法JSON指数1e309也返回422。没有改全局错误处理器。

省略/null/零/有限数值字符串转换兼容；修改省略保留原值，null保留清空语义。拒绝后整份业务请求不落库，真实数据库全字段与批次API快照核对化验、其他批次、质量/运输预警、处理记录和供应商评分不变。正常6000→5800热值、15→16灰分仍预警，运输处理历史保留。

[固定版本案例卡](https://github.com/nizuowanzhenbang/coal-quality-monitor/blob/d58a634e2dee43256ed27d6915903f70353f9219/docs/LAB-FINITE-VALUES.md)包含业务说明、流程图、3个演示测试与5个追问。信息化可讲校验、HTTP错误与测试；生产/燃料管理可讲化验来源与异常核对。按实际理解和参与说明AI辅助，不宣称现场投运或完成全部化验规则。

## 实际验证

| 检查 | 结果 |
|---|---|
| 原有基线 | 35 passed |
| 输入先失败 | 52 failed / 9 passed，52项均200应422 |
| 错误序列化先失败 | 有限约束后扩展8指标/双入口raw指数：16 failed / 59 passed，16项均500应422 |
| 修复后完整后端 | 110 passed，0 failed/errors/skipped；含新增75项参数化回归 |
| 新75项构成 | 48非有限字符串矩阵 + 18指数表示 + 9业务兼容/权限控制 |
| TypeScript/Vite、Ruff、pip/diff | 通过 |
| [PR Quality](https://github.com/nizuowanzhenbang/coal-quality-monitor/actions/runs/37268445110) | success，实际后端110项、静态检查与前端构建通过 |
| [新main Quality](https://github.com/nizuowanzhenbang/coal-quality-monitor/actions/runs/37268682255) | success，实际后端110项、静态检查与前端构建通过 |
| 独立整候选审查 | Critical/Important均0；1处Minor警告表述已核对修正，附加128次HTTP边界核对通过 |

参数矩阵与CI重复用例均不相加。真实SQLite/JWT角色、集成密钥和实际路由，没有替换业务算法或鉴权、没有默认库/lifespan操作或新服务/容器。本地Python3.12.14/Node24.19.0，复用隔离coal-quality-venv-20261004且pip check通过；依赖文件未改。远端Python3.11/Node22。

本地1390条警告（含弃用与测试收集警告）及已有2394.64kB包警告保留。未新增浏览器、PG专项/并发或依赖安全扫描。维护指南修正从backend切换frontend的相对路径。

## 范围与后续

历史无效化验须按原报告核对，本轮不自动改写。单位、基准、物理范围、缺项完整性、极端有限数计算及其他浮点接口继续核查；没有迁移、接口字段、前端源码、依赖或质量阈值变化。

下一轮优先plant-safety隐患整改期限规则。保留[前轮煤质证据](RELEASE-COAL-QUALITY-20261004.md)、[安全检查证据](RELEASE-SAFETY-20261004.md)及[设备基线](RELEASE-STOCKTAKE-20261004.md)为各自历史快照，本轮未重复其他项目全验收。详见[交接](ITERATION-STATUS.md)。
