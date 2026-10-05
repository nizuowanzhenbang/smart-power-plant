# 10 分钟演示路线

面向电力企业信息化、业务系统开发与维护岗位。以设备点检为主线，使用模拟设备、人员与数据。先声明本人实际参与及 AI 辅助范围，再展示可复核结果。

## 演示前选好版本

| 选择 | 固定提交 | 能展示什么 |
|---|---|---|
| 当前固定展示基线 | `76d799c1fc781147ea6bbdeaff0ee57e8bc659db`（PR #14 合并） | API 闭环、点检/验收/库存并发、权限、迁移恢复、部署、盘点归零、收货重放、状态竞争及过时盘点保护 |
| 历史 API 基线 | `8b4551808524b76c7b50c3425396bd5a265ba080`（PR #3 合并） | 用于解释演进，不作为新演示的默认版本 |

演示优先使用当前固定基线，启动和迁移按该提交的文档操作。历史版本的零配置行为不能套用到新版本。[最新提交、检查及范围](RELEASE-STOCKTAKE-20261004.md)。

提前在独立虚拟环境中按[基线运行说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/DEMO.md)安装依赖。在固定版本的设备点检仓库执行：

~~~sh
cd backend
python -m pip install --require-hashes -r requirements-dev.lock
python interview_demo.py --output interview-evidence.json
~~~

成功标准是本次命令退出码 0、打印 PASS，并生成 `status: passed` 的报告。已有报告拒绝覆盖，复跑换一个文件名。脚本使用临时 SQLite、临时上传目录和随机密钥，关闭调度及外部联动，结束后销毁临时环境。

这是一条 API 演示命令，不会启动浏览器页面。要展示 UI，提前按选定版本 README 配置独立演示环境，阅读[运行模式](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/RUNTIME-SECURITY.md)和[数据库迁移](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/DATABASE-MIGRATIONS.md)说明。固定演示账户只在显式 APP_MODE=demo 下创建；正式模式需有效密钥并先迁移。报告与录屏均应带版本、日期。

## 0–1 分钟：说清业务问题

点检员在弱网中提交异常，服务器保存成功但响应丢失。再次上传必须能确认原记录；其他人员或不同内容不能被静默覆盖。异常还要连接到派工、维修、验收和审计。

说明这是个人软件原型，使用模拟数据；没有现场接入或经营收益的测量依据。

## 1–6 分钟：展示点检到验收

| 展示动作 | 报告中的预期结果 | 能解释的设计 |
|---|---|---|
| B 级设备录入 SEVERE | 一条 MAJOR 缺陷，健康度 100 → 92 | 严重度规则与跨表业务状态 |
| 同人、同内容重传 | 同记录和缺陷 ID，健康度仍 92 | 业务键与事务；数据库唯一约束作为额外保护 |
| 修改内容再上传 | 返回 409，原记录不变 | 冲突需要核对，不能靠无限自动重试 |
| supervisor 派工，repairman 检修 | 按状态推进；不合角色的操作拒绝 | 后端校验权限和状态 |
| 验收驳回后重修，再验收通过 | RUNNING、健康度 98；重复验收返回 400 | 拒绝路径与防止重复回弹 |
| 打开审计结果 | 可看到派工、驳回、通过动作 | 操作者、动作和业务记录可追溯 |

2026-10-04 的设备点检验收已运行该脚本，35 checks 全部通过；完整记录见发布证据。本轮未重复该脚本，现场展示前仍应运行命令生成带版本和日期的新报告。

弱网中“响应丢失”的精确时序及并发竞争用自动测试说明，避免手动断网偶然成功就当作证明。浏览器 IndexedDB 与 Service Worker 的效果也不能从这个 API 脚本推断。

## 6–8 分钟：用一项已集成改进说明工程能力

只选一个追问展开，避免把所有 PR 都念一遍：

- **为什么有唯一键还要处理并发？** 展示 [PostgreSQL 回归说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/POSTGRESQL.md)及 [验收竞争说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/VERIFICATION-CONCURRENCY.md)，讲清事务、锁顺序、等锁后刷新和回滚范围。
- **升级失败如何恢复？** 展示 [迁移兼容矩阵](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/DATABASE-MIGRATIONS.md)与 [独立恢复方案](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/BACKUP-RESTORE.md)，说明代码回退不等于数据恢复，恢复验证后再切换连接。
- **部署如何复核？** 展示 [PR #14 的 Compose 检查](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37183237840)：构建启动、就绪检查、Chromium 登录授权、盘点归零、过时盘点冲突与收货故障恢复、日志凭证检查。该作业通过不能证明完整离线浏览器流程或生产容量。

这些改进已纳入 PR #14 的固定 main 基线。还可选择[库存精度与归零](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/STOCK-CONSISTENCY.md)：解释先复现舍入/竞争、再检查真实库存和流水。指定场景通过并不代表所有收货、盘点或外部联动问题已解决。

可选择[收货响应丢失](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/PURCHASE-RECEIPT-REPLAY.md)：部分收到 2 件，服务器已提交但响应丢失，刷新后复用 UUID 只记一条流水；新一批同数量使用新 UUID。解释为何按数量或时间猜测重复会误伤真实分批到货，以及为何提交后的 HTTP 响应要使用已保存快照。补充两个标签页和换账户的恢复边界。正式演示先维护窗口备份并 upgrade/check 到 0003。

可选择[采购状态竞争](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/PURCHASE-STATE-CONSISTENCY.md)：最终 5 件已收货后，先读到旧状态的取消返回 400；部分收到 2 件后仍可取消并确认原 UUID。说明等锁后重读状态、状态与审计一起提交，以及外部推送成功后本地失败为什么不能撤销远端订单。这些竞争由真实数据库自动测试固定交错，不依赖手工操作时机。

可选择[过时盘点保护](https://github.com/nizuowanzhenbang/equipment-inspection/blob/76d799c1fc781147ea6bbdeaff0ee57e8bc659db/docs/STOCKTAKE-SNAPSHOT.md)：打开库存 10 的盘点框，另一操作入库 2 后，旧快照提交 10 返回 409，当前库存仍为 12；关闭并刷新后重新输入 11 才能提交。即使先入 2 再出 2 回到 10，旧版本仍冲突。库存与流水版本同一 SQL 读取；冲突不自动替换版本或重试。旧 ADJUST 客户端须升级，此次没有新迁移。浏览器等待真实响应时不能编辑或关闭对话框。

## 8–9 分钟：辅助案例

用燃煤能效的[已合并 PR #2](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/2)说明：历史样本按时间划分，模型误差与均值基线比较；样本不足、退化或超出训练范围时明确降级。模型评分不是成功概率，预测节煤不是已实现收益。

煤质重评保护的前轮固定版本为 `f6efd459f596293fe21ddd44104eb48a957684b6`，见[煤质发布证据](RELEASE-COAL-QUALITY-20261004.md)。正常港口/入厂化验后收到严重铅封运输预警，再次化验重评仍保留原运输记录、处理信息和SEVERE状态；预警数1、风险0.60、供应商手动重算95分。解释为何各来源只替换自己生成的预警，以及为何计分必须看数据库实际保存的全部记录。可在固定版本按维护说明执行 `cd backend && python -m pytest tests/test_quality_transport_api.py -q`，复核六个实际API用例。该故事不代表现场煤质检测或全链路联合验收。

本轮也可选择“异常化验输入”案例：字符串NaN/Infinity或JSON指数1e309原先可进入数据库并影响比对；现在创建/修改均返回422，既有批次、预警、处理历史和评分记录不变。正常6000→5800热值与15→16灰分仍触发预警。用[固定版本案例卡](https://github.com/nizuowanzhenbang/coal-quality-monitor/blob/d58a634e2dee43256ed27d6915903f70353f9219/docs/LAB-FINITE-VALUES.md)选三个真实测试说明异常拒绝、错误响应本身的序列化和正常评估；[发布证据](RELEASE-COAL-FINITE-20261005.md)记录110项完整后端及CI。结合化验来源和异常核对讲业务，再按追问展开类型与浮点表示，不把参数矩阵数量当成能力指标。

内部招聘也可选择安全检查案例替换上述辅助案例：讲“防护罩缺损 → 检查不符合 → 真实隐患单”。旧接口允许客户端塞入虚假编号，导致系统误判已转单；现在拒绝并保持原记录不变，正常转换由服务器生成关联。用[固定版本讲解卡](https://github.com/nizuowanzhenbang/plant-safety/blob/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df/docs/CHECK-HAZARD-OWNERSHIP.md)中的三个真实测试演示异常拒绝、正常转换和事务回滚；[证据](RELEASE-SAFETY-20261004.md)记录15项完整后端与CI。当前没有安全检查编辑页面，按API场景讲解。

## 9–10 分钟：映射岗位能力和下一步

| 岗位关心什么 | 用哪个事实回答 |
|---|---|
| 需求与业务沟通 | 把重传、冲突、驳回重修转成具体验收场景 |
| 数据可靠性 | 沿 API、事务和数据库讲清一次业务写入 |
| 权限与运维 | 说明演示模式、角色拒绝、迁移与恢复范围 |
| 软件交付 | 给出提交、PR 和 CI 链接，明确已合并与候选 |
| 下一步如何选 | 固定基线已形成；安全检查关联隔离已交付；煤质非有限输入校验已交付；下一项优先隐患期限规则，采购创建边界保留后续 |

按本人实际完成、理解与讲解程度组织简历：围绕电厂设备点检场景维护 FastAPI、React 原型，验证弱网重传、内容冲突、缺陷闭环与库存可靠性；通过可重复的 API 场景与 CI 留下交付证据。注明实际参与及 AI 辅助范围。

岗位侧重：信息化讲接口、事务与测试；生产技术讲现场记录到整改任务的交接；安全管理讲责任、追溯和异常处置。案例可证明具体软件行为，不代替现场规程。先用90秒讲业务问题与结果，再按追问展开[5个问答](https://github.com/nizuowanzhenbang/plant-safety/blob/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df/docs/CHECK-HAZARD-OWNERSHIP.md)。

[长期规划](LONG-TERM-PLAN-20261003.md) · [最新交接](ITERATION-STATUS.md)
