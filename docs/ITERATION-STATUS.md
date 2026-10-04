# 迭代进度与接续入口

2026-10-04更新。[长期规划](LONG-TERM-PLAN-20261003.md)。用户授权自主开发、测试、审查、GitHub推送与验证后合并；允许选择其他电厂项目，目标是内部招聘面试。岗位未进一步指定时采用信息化/生产技术/安全管理共同业务案例。

## 本轮已完成

安全检查提交不再允许客户端指定hazard_id，兼容省略/null，服务器转换成功后仍返回真实编号。前端API类型同步，既有完成态不可重提/开始。加入[面试案例卡](https://github.com/nizuowanzhenbang/plant-safety/blob/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df/docs/CHECK-HAZARD-OWNERSHIP.md)，包含模拟业务、流程图、3个测试入口及5个追问；README明确整改期限上限尚未完整实现。

| 项目 | 固定main / 证据 |
|---|---|
| plant-safety，本轮 | `24e33ec011c0d0cc3dd3d9dcc79dffb1440541df`；源`092f6986a704d0c141c9b5442891d405b6600bf8`；tree`be2418f2fcc06f30cb8de9468af3a71dfe37f93f`；[PR #2](https://github.com/nizuowanzhenbang/plant-safety/pull/2) / [发布证据](RELEASE-SAFETY-20261004.md) |
| coal-quality-monitor，前轮 | `f6efd459f596293fe21ddd44104eb48a957684b6`；[证据](RELEASE-COAL-QUALITY-20261004.md) |
| equipment-inspection，既有主作品 | `76d799c1fc781147ea6bbdeaff0ee57e8bc659db`；[证据](RELEASE-STOCKTAKE-20261004.md) |

本地15pass/0fail/skip，新增13项包含其中；构建、Ruff、pip/diff通过。PR Quality 37197447105 与新main Quality 37197648635 均success，已核对实际后端15项与前端日志；独立整分支审查无问题。文档仓库版本查main历史，避免自引用SHA。

## 进度与范围

- 01–04基线整理完成；05–07库存精度、收货重放、状态竞争和过时盘点保护已交付，采购创建仍待核查。
- 17–18煤质已有“重评保留运输证据”一个案例，完整输入/单位/合同核查未完成。
- 本轮安全检查是可替换的本地业务案例，不代表11–14跨系统联动完成；20–21新增一张案例卡和追问，尚未进行限时模拟面试。
- 历史错误关联需人工按来源核对；并发转换、序号完整性和期限校验待做。没有新增生产部署、浏览器或容量验收。

## 下一项具体动作

优先coal-quality-monitor化验非有限数输入。前轮隔离探针证实入厂热值Infinity可以返回200、写入inf并被判正常；当前固定main `f6efd459f596293fe21ddd44104eb48a957684b6`只修复运输预警归属，没有修这个输入缺口。

先核对main及指令，读取化验create/update schema、前端输入与质量引擎对None的语义。对热值、灰分、水分、硫分等实际浮点字段复现NaN/Infinity路径；按业务和现有接口决定有限值校验，保留允许缺省字段的兼容，不擅自推断所有上下界。先RED再最小修复，验证拒绝后化验/预警/评分不变及正常重评；最终留下可复跑面试案例。

后续队列：plant-safety重大14天/一般30天规则（已复现创建和转换接受MAJOR60天，更新入口及时区仍待核查）；检查项seq完整性/并发转换；设备采购创建float金额/count+1编号仍为待复现线索；燃气计量旧探针因openpyxl缺失未完成API验证，不作为已确认缺陷。

## 本地接续与交付记录

- 主实现worktree：`/workspace/worktrees/plant-safety-association-20261004`，`maintenance/check-hazard-ownership-20261004`，已推送且干净。
- main clone：`/workspace/scratch/selection-plant-safety-20261004`，已快进main；与worktree共用Git refs，fetch顺序执行。
- 独立venv：`/workspace/scratch/plant-safety-venv-20261004`；默认库/lifespan未操作，没有创建持久服务或容器，测试SQLite自行销毁。
- 文档：`/workspace/smart-power-plant`，`docs/safety-interview-release-20261004`。
- scratch结果：plant-safety-test-results-20261004.md、plant-safety-final-20261004.xml、plant-safety-progress-20261004.md；baseline/red-verified/full/build/install/npm-install日志与source/release metadata同目录。
- 下轮煤质：`/workspace/scratch/selection-coal-quality-20261004`和`/workspace/scratch/coal-quality-venv-20261004`；旧煤质worktree、日志和所有默认库保留。

一个主代理实施，适用审查技能要求下委派一次只读审查；不额外扩散任务。新会话先核对实际Git/PR和AGENTS/CLAUDE。环境重建时按固定版本恢复，不假设本地缓存永远存在；没有后台定时任务或模型侧实时额度读数。
