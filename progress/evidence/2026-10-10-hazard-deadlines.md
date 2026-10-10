# 2026-10-10 · PP-010 · 隐患整改期限发布证据

## 固定版本与发布

- 仓库：[nizuowanzhenbang/plant-safety](https://github.com/nizuowanzhenbang/plant-safety)。
- 实施基线：`b8a1c05a4f39fe5e3e56741bed6cd7d0f27f6dd0`，包含前轮安全检查关联保护。
- 首候选：`4dff3d2da3fddbf16380e54c214e8e5a234d9bf9`；审查修复候选：`9dd1c18e7d089ebb4e02349998271f9ec8a7de87`。
- [PR #3](https://github.com/nizuowanzhenbang/plant-safety/pull/3) 已于 2026-10-10 12:07:33 UTC squash 合并。
- 固定主分支：[e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1](https://github.com/nizuowanzhenbang/plant-safety/commit/e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1)。已比较其文件树与最终候选，无差异。
- 最终候选 [PR Quality 38050745250](https://github.com/nizuowanzhenbang/plant-safety/actions/runs/38050745250)：backend/frontend 均 success，head 为 `9dd1c18e7d089ebb4e02349998271f9ec8a7de87`。
- 合并后 [main Quality 38050827389](https://github.com/nizuowanzhenbang/plant-safety/actions/runs/38050827389)：backend/frontend 均 success，head 为 `e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1`。
- 主分支运行日志复读：后端 `68 passed, 2 warnings in 5.02s`，Ruff `All checks passed`，前端 `built in 8.55s`。

## 结果与兼容

发现时间起算，重大最多 14 天、一般最多 30 天；新建/检查转换缺省或 null 补默认。修改明确期限或实际改变等级时重新校验，超限 422；更新 null 重置等级默认，不表示取消期限。无关更新仍能维护旧超限或空期限行，不批量改写历史数据。

偏移时间统一为 UTC naive；检查转换与外部集成使用同一个发现时间锚点；重复集成保留原记录。过时的更新以条件原子写入检测冲突，返回 409，不覆盖竞争请求或关闭状态。登记界面提示默认上限并限制日期。

无需新数据库迁移或依赖。过去日期仍可输入，原超期识别继续工作；权限与安全检查关联保护保留。

## 本轮实际验证

| 检查 | 实际结果 |
|---|---|
| 基线后端 | 15 passed |
| 原期限漏洞失败回归 | 首批 49 项：37 failed、12 passed；额外 null 等级用例复现原 500 |
| 首修复完整后端 | 65 passed（新增 50 项） |
| 独立审查 | 一次整分支只读审查；发现 1 项 Important 并发漏洞，无其他 Critical/Important |
| 并发失败回归 | 3 failed，原候选均错误返回 200；两个竞争顺序可留下 MAJOR/30 天，另一个可修改已关闭行 |
| 最终完整后端 | 68 passed（新增 53 项，原 15 项保留）；真实 HTTP/JWT/SQLite 数据库 |
| 静态与依赖检查 | Ruff E9,F63,F7,F82、pip check、git diff --check 通过 |
| 前端 | 锁定依赖安装、TypeScript 与 Vite 生产构建通过 |

回归覆盖微秒上限、不同 UTC 偏移、缺省/null、原发现时间、等级升降、旧数据、默认单一时刻、重复集成、极端日期、拒绝后全部字段不变，以及等级/期限竞争和并发关闭后拒绝过时写入。确定性地调度真实请求交错，未用伪造数据库结果替代写入验证。

可复跑的固定测试：[test_hazard_deadlines.py](https://github.com/nizuowanzhenbang/plant-safety/blob/e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1/backend/tests/test_hazard_deadlines.py)。[规则](https://github.com/nizuowanzhenbang/plant-safety/blob/e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1/docs/DEADLINE-POLICY.md)；[执行计划](https://github.com/nizuowanzhenbang/plant-safety/blob/e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1/docs/superpowers/plans/2026-10-10-hazard-deadlines.md)。

## 验证边界与接续

本地 Python 3.12 有既有 datetime/passlib/TestClient 弃用警告，前端有既有大包提示；未在本轮升级依赖或分包。CI 沿用 Python 3.11/Node 22。没有 PostgreSQL 运行时、浏览器交互、现场投运或跨系统可靠投递验收。

原始输出在 `/workspace/scratch/plant-safety-*20261010.log`，仅本环境有效；永久可接续证据以本文件、固定测试、PR 和 GitHub 检查为准。

下一任务 PP-020 核对煤质单位/基准/缺项/有限极端值；本轮未实施该任务。开工先读中央四份核心文件并核对实际代码，避免重做既有非有限输入和运输证据保护。
