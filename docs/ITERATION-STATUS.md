# 迭代进度与接续入口

更新日期：2026-10-04。[长期规划](LONG-TERM-PLAN-20261003.md)。主作品equipment-inspection；辅助案例coal-unit-efficiency、coal-quality-monitor。用户允许从其他电厂项目选择改进。

## 授权与执行方式

用户持续授权自主设计、开发、长时间分析、自动化测试、GitHub推送与必要审查；验证后的合并自主完成。一个主代理负责集成，有限委派独立选题/测试/审查，每轮实修一个主目标。本轮两个只读候选检查、一个API测试作者和一个独立审查者；没有并行修改同一产品文件。没有后台定时任务、模型侧实时额度读数或跨账户限制承诺。

## 当前固定版本

| 项目 | main / 来源 / 证据 |
|---|---|
| 煤质监督，本轮已交付 | `f6efd459f596293fe21ddd44104eb48a957684b6`，源`3aaec74f918d76b527e7c733608a310de7c5353e`，tree`80e49442d2bba59b3ebb5f919658205999c1bc09`；[PR #2](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/2)，[完整证据](RELEASE-COAL-QUALITY-20261004.md) |
| 设备点检，前轮固定基线 | `76d799c1fc781147ea6bbdeaff0ee57e8bc659db`；[PR #14](https://github.com/nizuowanzhenbang/equipment-inspection/pull/14)，[历史证据](RELEASE-STOCKTAKE-20261004.md)，本轮未改动或重复全验收 |

煤质本地35pass0fail/skip，含新增数据库8和API6；构建/Ruff/diff/pip检查通过。PR Quality `37190541433` 与新main Quality `37190662818` success；两处均backend35/Ruff/frontend构建。整分支审查无发现，独立SQLite边界检查通过。文档仓库实际版本查main历史，避免自引用SHA。

## 长期单元进度

- 01–04已完成；设备历史#4–#10不重复实施。
- 05–07库存精度、归零、过时盘点、收货重放及采购状态保护完成；采购创建/自动补货边界仍待核查。
- 17–18煤质辅助案例完成“重评保留运输证据”的一个实际API/数据库场景；输入/单位/合同等完整核查未完成，不把阶段全部标为完成。
- 其余单元按实际范围继续，不从已有迁移恢复/依赖升级重做。

## 本轮行为和边界

化验重评只替换质量引擎自有八类预警，保留运输记录ID、字段与处理信息；按实际全部预警计算状态、数量和风险。手动/自动/修改三入口回归通过；处理状态历史计分政策不变。没有接口字段、迁移、依赖或前端源码变化。

历史被删运输证据须核对源系统或备份，本轮不自动恢复。运输事件的替换/重放、并发协调及化验保存与评估的既有分阶段提交未重做。框架弃用、大包和依赖范围未锁边界见发布证据；没有生产部署、容量或全平台联合验收。

## 下一项具体动作

优先plant-safety检查结果的隐患关联隔离。已核查main `f4c84538824e67dbfc4e23d509e92f2e8a741db5`；只读探针创建计划/记录、启动后提交不符合项且附`hazard_id=999999`，提交200并持久化，转换400“已转隐患单”，实际hazards为0。普通不附ID的控制能成功转换。

先核对实际main并读取该仓库CLAUDE.md、`backend/app/schemas/safety_check.py`、`backend/app/api/safety_checks.py`及前端提交字段。输入/输出共用CheckResultItem，提交直接保存客户端hazard_id，转换信任该字段。比较拒绝非null客户端关联与分开写入DTO的方案；同时核对已转换记录是否能重提及表单回显，防止丢失合法服务器关联。先真实失败回归再最小修复，保留服务器创建ID和重复转换拒绝；本轮未提前实施该设计。

## 其他候选队列

| 项目与范围 | 已知事实 / 状态 |
|---|---|
| 煤质非有限化验输入 | 前一main`11bb3c8c8f11f64b599c22ca681cee5a45c35106`实际探针Infinity入厂热值200并写inf、批次正常；创建/修改有限值校验待修 |
| 隐患整改期限 | 同plant-safety探针MAJOR60天被接受，超过仓库CLAUDE/README所写14天；规则兼容与更新入口待核查，不当作已交付 |
| 采购创建/自动补货 | 设备点检float金额/count+1编号为源码线索，尚未真实复现本轮输入/并发，不宣称已确认缺陷 |
| 燃气计量 | clone main`349c9e947535e800dd4f1e44e36612c5ed0ca10f`；旧共用venv探针被缺openpyxl阻塞，没有完成API缺陷验证，无源码变化 |

只读探针使用临时SQLite与测试密钥；煤质选择探针鉴权被局部替换，其发现已由新增真实JWT回归验证。隐患探针为真实临时用户鉴权；候选结果不算进煤质35项正式验收。

## 本地接续

- 煤质worktree：`/workspace/worktrees/coal-quality-alerts-20261004`，分支`maintenance/quality-transport-alerts-20261004`，已推送且工作树干净。
- 煤质main clone：`/workspace/scratch/selection-coal-quality-20261004`，已快进新main；与worktree共用Git refs，fetch顺序执行。
- 煤质venv：`/workspace/scratch/coal-quality-venv-20261004`。本轮测试SQLite自行销毁，未新建容器/持久测试服务。
- 文档：`/workspace/smart-power-plant`，分支`docs/coal-quality-release-20261004`。
- 结果：`/workspace/scratch/coal-quality-test-results-20261004.md`；后端XML：coal-quality-final-20261004.xml；日志：coal-quality-baseline、unit-red、api-red、full、build、install、npm-install，均带20261004后缀。
- 审查/交付摘要：`/workspace/scratch/coal-quality-progress-20261004.md`；源与发布metadata同scratch目录。
- 只读候选：`/workspace/scratch/selection-plant-safety-20261004`；探针plant-safety-selection-probe-20261004.py、selection-coal-quality-probe-20261004.py。默认库、旧设备环境与其他scratch保留。

新会话先核对实际Git/PR/AGENTS或CLAUDE指令，再按下一项推进。若工作区重建，依据固定SHA与依赖说明恢复，不依赖本地路径或缓存仍存在。
