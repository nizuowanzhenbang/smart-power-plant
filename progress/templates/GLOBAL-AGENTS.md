# 电厂数智化工作记忆

以下规则只适用于用户的电厂数智化任务，以及 nizuowanzhenbang 的 power-plant-digitalization-progress、smart-power-plant、equipment-inspection、coal-quality-monitor、coal-transport-monitor、fuel-procurement、coal-yard-management、plant-safety、emission-monitoring、coal-unit-efficiency、gas-fuel-metering、gas-turbine-performance、gas-emission-monitoring 仓库。其他任务不需要读取电厂进度。

开工前通过可用 GitHub 连接或已认证 gh/git，读取进度目录 https://github.com/nizuowanzhenbang/smart-power-plant/tree/main/progress 默认分支 main 的 `progress/AGENTS.md`、`progress/SUMMARY.md`、`progress/CURRENT.md`、`progress/TASKS.md`。先取得提交 SHA，尽量按同一提交读取；报告 SHA、任务编号、已完成且不重做的内容和第一项动作。按任务读取其他记录，核对实际代码分支、HEAD 和 PR；用户当前指令优先，不将历史授权扩大到新任务。

有实质工作时开工认领任务；结束或中断前回写中央当前进度和任务状态，追加日志，保存提交/PR/验证/阻塞/下一步，并提交推送。已合并或已有覆盖默认不重做，重新打开需记录实际原因；并发更新先合并，不强推。访问失败或回写失败时保存本地交接，最终明确未读取/未同步，不声称中央进度已最新。

仓库级 `AGENTS.md` 和中央规则给出详细流程。历史快照只作证据；本地文件与远端不一致时核对实际情况。新会话读取新进度，不依赖上一会话或本地环境一直存在。
