# 10 分钟演示路线

面向电力企业信息化、业务系统开发与维护岗位。以设备点检为主线，使用模拟设备、人员与数据。先声明本人实际参与及 AI 辅助范围，再展示可复核结果。

## 演示前选好版本

| 选择 | 固定提交 | 能展示什么 |
|---|---|---|
| 已合并基线 | `8b4551808524b76c7b50c3425396bd5a265ba080`（PR #3 的合并提交） | 点检、重传与冲突、检修验收、角色拒绝和审计的 API 场景 |
| 草稿候选 | `8b86c084032a446d065cd64b54759e3e50c5d8bc`（PR #9 head） | 包含后续并发、配置、迁移恢复与部署改动；仍未合并 |

首次演示优先使用已合并基线；需要讲后续改进时明确称为候选。两者启动和迁移要求可能不同，按对应提交的文档操作。[证据及版本关系](EVIDENCE-20261003.md)。

提前在独立虚拟环境中按[基线运行说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b4551808524b76c7b50c3425396bd5a265ba080/docs/DEMO.md)安装依赖。在设备点检仓库执行：

~~~sh
cd backend
python -m pip install -r requirements.txt -r requirements-dev.txt
python interview_demo.py --output interview-evidence.json
~~~

成功标准是本次命令退出码 0、打印 PASS，并生成 `status: passed` 的报告。已有报告拒绝覆盖，复跑换一个文件名。脚本使用临时 SQLite、临时上传目录和随机密钥，关闭调度及外部联动，结束后销毁临时环境。

这是一条 API 演示命令，不会启动浏览器页面。要展示 UI，提前按选定版本 README 配置独立演示环境；候选版本须阅读[运行模式](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b86c084032a446d065cd64b54759e3e50c5d8bc/docs/RUNTIME-SECURITY.md)和[数据库迁移](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b86c084032a446d065cd64b54759e3e50c5d8bc/docs/DATABASE-MIGRATIONS.md)说明。报告与录屏均应带版本、日期；报告不通过时先定位原因。

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

上表是对应脚本的验收预期，不是本轮新生成的业务报告。本轮仅更新导览与核对远端证据；现场展示前运行命令取得自己的新报告。

弱网中“响应丢失”的精确时序及并发竞争用自动测试说明，避免手动断网偶然成功就当作证明。浏览器 IndexedDB 与 Service Worker 的效果也不能从这个 API 脚本推断。

## 6–8 分钟：用一项候选改进说明工程能力

只选一个追问展开，避免把所有 PR 都念一遍：

- **为什么有唯一键还要处理并发？** 展示 [PostgreSQL 回归说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b86c084032a446d065cd64b54759e3e50c5d8bc/docs/POSTGRESQL.md)及 [验收竞争说明](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b86c084032a446d065cd64b54759e3e50c5d8bc/docs/VERIFICATION-CONCURRENCY.md)，讲清事务、锁顺序、等锁后刷新和回滚范围。
- **升级失败如何恢复？** 展示 [迁移兼容矩阵](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b86c084032a446d065cd64b54759e3e50c5d8bc/docs/DATABASE-MIGRATIONS.md)与 [独立恢复方案](https://github.com/nizuowanzhenbang/equipment-inspection/blob/8b86c084032a446d065cd64b54759e3e50c5d8bc/docs/BACKUP-RESTORE.md)，说明代码回退不等于数据恢复，恢复验证后再切换连接。
- **部署如何复核？** 展示 [PR #9 的 Compose 检查](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/36763007942)：构建启动、就绪检查、Chromium 登录授权、日志凭证检查。该作业通过不能证明完整离线浏览器流程或生产容量。

这些属于草稿候选，先指出提交与 PR 状态。不能把候选通过的检查当成主分支已经集成。

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
| 下一步如何选 | 先收拢现有 PR，再按证据处理库存、依赖和联动缺口 |

按本人实际完成、理解与讲解程度组织简历：围绕电厂设备点检场景维护 FastAPI、React 原型，验证弱网重传、内容冲突及缺陷闭环；通过可重复的 API 场景与 CI 留下交付证据。涉及候选改进时标注分支状态。

[长期规划](LONG-TERM-PLAN-20261003.md) · [最新交接](ITERATION-STATUS.md)
