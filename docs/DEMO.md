# 10 分钟演示路线

面向电力企业信息化、业务系统开发与维护岗位。以设备点检为主线，使用模拟设备、人员与数据。先声明本人实际参与及 AI 辅助范围，再展示可复核结果。

## 演示前选好版本

| 选择 | 固定提交 | 能展示什么 |
|---|---|---|
| 当前固定展示基线 | `b2bd35cea7ad40a0a0ab9b836707b6af6539738b`（PR #11 合并） | API 闭环、点检/验收/库存并发、权限、迁移恢复、部署及盘点归零 |
| 历史 API 基线 | `8b4551808524b76c7b50c3425396bd5a265ba080`（PR #3 合并） | 用于解释演进，不作为新演示的默认版本 |

演示优先使用当前固定基线，启动和迁移按该提交的文档操作。历史版本的零配置行为不能套用到新版本。[最新提交、检查及范围](RELEASE-20261003.md)。

提前在独立虚拟环境中按[基线运行说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/DEMO.md)安装依赖。在固定版本的设备点检仓库执行：

~~~sh
cd backend
python -m pip install --require-hashes -r requirements-dev.lock
python interview_demo.py --output interview-evidence.json
~~~

成功标准是本次命令退出码 0、打印 PASS，并生成 `status: passed` 的报告。已有报告拒绝覆盖，复跑换一个文件名。脚本使用临时 SQLite、临时上传目录和随机密钥，关闭调度及外部联动，结束后销毁临时环境。

这是一条 API 演示命令，不会启动浏览器页面。要展示 UI，提前按选定版本 README 配置独立演示环境，阅读[运行模式](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/RUNTIME-SECURITY.md)和[数据库迁移](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/DATABASE-MIGRATIONS.md)说明。固定演示账户只在显式 APP_MODE=demo 下创建；正式模式需有效密钥并先迁移。报告与录屏均应带版本、日期。

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

本轮已重新运行该脚本，35 checks 全部通过；完整记录见发布证据。现场展示前仍应运行命令生成带版本和日期的新报告。

弱网中“响应丢失”的精确时序及并发竞争用自动测试说明，避免手动断网偶然成功就当作证明。浏览器 IndexedDB 与 Service Worker 的效果也不能从这个 API 脚本推断。

## 6–8 分钟：用一项已集成改进说明工程能力

只选一个追问展开，避免把所有 PR 都念一遍：

- **为什么有唯一键还要处理并发？** 展示 [PostgreSQL 回归说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/POSTGRESQL.md)及 [验收竞争说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/VERIFICATION-CONCURRENCY.md)，讲清事务、锁顺序、等锁后刷新和回滚范围。
- **升级失败如何恢复？** 展示 [迁移兼容矩阵](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/DATABASE-MIGRATIONS.md)与 [独立恢复方案](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/BACKUP-RESTORE.md)，说明代码回退不等于数据恢复，恢复验证后再切换连接。
- **部署如何复核？** 展示 [PR #11 的 Compose 检查](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/37144134103)：构建启动、就绪检查、Chromium 登录授权与盘点归零、日志凭证检查。该作业通过不能证明完整离线浏览器流程或生产容量。

这些改进已纳入 PR #11 的固定 main 基线。还可选择[库存精度与归零](https://github.com/nizuowanzhenbang/equipment-inspection/blob/b2bd35cea7ad40a0a0ab9b836707b6af6539738b/docs/STOCK-CONSISTENCY.md)：解释先复现舍入/竞争、再检查真实库存和流水。指定场景通过并不代表所有收货、盘点或外部联动问题已解决。

## 8–9 分钟：辅助案例

用燃煤能效的[已合并 PR #2](https://github.com/nizuowanzhenbang/coal-unit-efficiency/pull/2)说明：历史样本按时间划分，模型误差与均值基线比较；样本不足、退化或超出训练范围时明确降级。模型评分不是成功概率，预测节煤不是已实现收益。

煤质案例作为后续补充，待按长期规划复验后再纳入完整演示。

## 9–10 分钟：映射岗位能力和下一步

| 岗位关心什么 | 用哪个事实回答 |
|---|---|
| 需求与业务沟通 | 把重传、冲突、驳回重修转成具体验收场景 |
| 数据可靠性 | 沿 API、事务和数据库讲清一次业务写入 |
| 权限与运维 | 说明演示模式、角色拒绝、迁移与恢复范围 |
| 软件交付 | 给出提交、PR 和 CI 链接，明确已合并与候选 |
| 下一步如何选 | 固定基线已形成；优先部分收货重放幂等，再处理盘点版本、依赖和联动缺口 |

按本人实际完成、理解与讲解程度组织简历：围绕电厂设备点检场景维护 FastAPI、React 原型，验证弱网重传、内容冲突、缺陷闭环与库存可靠性；通过可重复的 API 场景与 CI 留下交付证据。注明实际参与及 AI 辅助范围。

[长期规划](LONG-TERM-PLAN-20261003.md) · [最新交接](ITERATION-STATUS.md)
