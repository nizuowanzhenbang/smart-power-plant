# 接续命令与阶段保存

在更新过的 smart-power-plant 检出根目录执行 `python -m progress_tools`；Python 3.11+，无第三方依赖。GitHub 使用当前 GH_TOKEN/GITHUB_TOKEN 或已有 gh 登录；不要将凭证写入参数、文档或输出。

## 开工与实时认领

```bash
python -m progress_tools resume
python -m progress_tools check --offline
python -m progress_tools claim PP-020 --owner 本次会话唯一标识 --code-repo nizuowanzhenbang/coal-quality-monitor --branch 本次业务分支
```

resume 取得 main 固定 SHA，按同一版本读取四份核心文件与 SESSION。SESSION.json 是实时认领和最后交接的权威入口；CURRENT.md 保存业务摘要、批次与下一项。claim 不把任务写为完成，也不替代阅读实际代码。

认领/检查点/释放使用读到的中央 HEAD 作为父提交，并以非强制 Git ref 更新发布。其他会话或文档在读后写入时，过时发布拒绝；重新读取后核对执行者，不自动重试覆盖。权限不足、分支保护、断网和冲突均非零退出。未成功发布的临时 Git 对象不是已保存进度。

## 关键阶段保存

先将业务代码提交并推送其工作分支，再记录对应完整远端代码 SHA：

```bash
python -m progress_tools checkpoint PP-020 --owner 本次会话唯一标识 --phase reproduced --commit 完整代码SHA --note '实际失败用例与结果' --next-action '实施最小修复'
python -m progress_tools checkpoint PP-020 --owner 本次会话唯一标识 --phase implemented --commit 完整代码SHA --note '实际验证命令与结果' --next-action '独立审查'
```

阶段：decision、reproduced、implemented、reviewed、pr_open、merged。决策确定、失败复现、实现验证、审查修复、PR、合并均保存；阶段名称不单独证明验证通过。pr_open/merged 必须附 `--pr 编号`，脚本核对实际状态及相应 SHA。代码尚未推送则拒绝记录该 SHA。

```bash
python -m progress_tools release PP-020 --owner 本次会话唯一标识 --reason '实际完成并回写，或明确的暂停理由'
```

release 保留最后检查点，不自动将 TASKS 标为已合并。合并后的验收通过再更新摘要、台账、RELEASES 索引及证据。原始关键失败事实和可复跑用例应随版本保存，不依赖本地绝对路径或 Actions 日志永久存在。

## 明确接管

旧会话仍有认领时，先核对代码分支、PR、最后交接和实际进度。确需接管时，在 claim 提供 `--takeover-from 原执行者 --reason '核对结果和接管理由'`；保持原任务/仓库/分支，保留原检查点和接管历史。不按时间自动抢占。认领身份是协作标识，不是新的安全权限边界。

## 自动核验范围

```bash
python -m progress_tools check --offline
python -m progress_tools check --remote
```

离线核对核心文件、任务编号/状态、SESSION/RELEASES 结构及 Markdown 本地文件链接。在线额外核对 RELEASES 中逐条列出的固定代码、PR 合并 SHA 和指定检查的最新结果；缺失、pending、失败或访问错误均失败。当前索引范围由 RELEASES 明示，不等于全仓库联合验收；锚点内容、现场收益与模型是否读懂不由此判断。

Progress checks 对 push/PR 自动运行相同测试与核验，token 仅 contents:read；不执行状态写入或模型开发。手动状态命令需要既有写权限，不能绕过分支保护。

每次活动会话按照中央批次推进多项可独立验收的升级；失败阻塞独立项时保存结果，继续可独立验证的同批工作。自动化不改变实际检查、授权与证据边界。
