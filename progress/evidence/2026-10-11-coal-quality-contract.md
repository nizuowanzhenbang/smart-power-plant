# PP-020 煤质口径发布证据

代码仓库 nizuowanzhenbang/coal-quality-monitor；[PR #4](https://github.com/nizuowanzhenbang/coal-quality-monitor/pull/4)，实际 squash 合并 `26bdbef9360e7b2ea2f037114adbf63ffdabb947`。

## 已交付

- 两个热值可输入 kcal/kg/MJ/kg，仅换算本次给出的字段，统一存 kcal/kg；输出八指标单位与固定分析基准，拒绝不支持的基准声明。
- 化验与合同采用热值 0–10000 kcal/kg、百分数 0–100 的项目宽范围保护；错误请求整体拒绝。空值、零、数字字符串、局部更新语义保留。
- 港口/入厂净热值、灰分、全硫、全水关键指标缺失时返回明确清单，无预警也不能写 COMPLETED；已知质量/运输预警仍优先，处理历史及评分保留。
- 入厂零热值触发亏损/合同检查；不可表示的相对偏差存 null，保留绝对偏差判定。
- 详情页读取实际双端字段，正确标注 Vd/FCd，缺项不生成虚假雷达分数；合同标签直接比较数值，科学计数法不会误判。

## 实际验证

- 基线完整 110 passed。首次 82 项业务回归 77 failed/5 passed；追加极小基数数据库断言先 3 failed/2 passed。
- 审查超大整数回归先 4 failed/4 passed；实际 AntD 标签渲染先 2 failed/4 passed。
- 修复后完整 **201 后端 passed、6 前端标签渲染 passed**；ruff E9/F63/F7/F82、pip check、TypeScript/Vite 构建及 diff 检查通过。
- 修复候选 `ab101aebb28409ff859c9fed6f6a8734c2fa27fc` 的 [CI 38141089655](https://github.com/nizuowanzhenbang/coal-quality-monitor/actions/runs/38141089655) backend/frontend 成功。
- 实际合并代码的 [main CI 38141214245](https://github.com/nizuowanzhenbang/coal-quality-monitor/actions/runs/38141214245) backend/frontend 成功；前端 CI 同时运行六项标签回归。
- 关键 reproduced/implemented/reviewed/pr_open/merged 与 release 在真实 GitHub 保存；独立无旧聊天恢复正确找到任务、分支、固定候选与下一动作，见 [恢复演练](../docs/RECOVERY-EXERCISE-20261011.md)。

## 审查与边界

一次独立 reviewer 对首次候选复跑 192 项并核对 CI，返回两项已复现 Important：MJ/kg 超大整数转 float 溢出和科学计数法合同误判。全部接受并先失败再修复。TASKS 旧第一动作 Minor 已修正；无拒绝或延期收到的建议。最终独立报告因用量限制未生成；父代理继续全范围检查和回归，未声称独立批准。

验证为 SQLite/JWT/真实 HTTP、实际 React 服务端标签渲染、构建与 GitHub CI，未执行浏览器/现场或 PostgreSQL 并发验收。范围保护不是行业合格认证；保留既有列的分析基准，不推断或自动换算干基/收到基。不做数据库迁移或历史回填，不调整风险权重，也不证明全厂联合寻优已完成。

详细过程见 [批次日志](../logs/2026-10-11-batch-01.md)；实现分支计划位于煤质仓库 docs/plans/2026-10-11-measurement-contract.md。
