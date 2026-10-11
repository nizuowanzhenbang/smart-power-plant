# PP-003/004/005 接续发布证据

代码仓库 nizuowanzhenbang/smart-power-plant；[PR #13](https://github.com/nizuowanzhenbang/smart-power-plant/pull/13)，实际 squash 合并 `5af33d2f3a974cf0bfad54766a8bb2650cb76c18`。

- 25 项真实 CLI/本地 HTTP 契约回归、离线结构/链接、实际远端发布索引核验通过。
- 一次独立整分支审查：3 Important 全接受并 RED→GREEN 修复；旧摘要 Minor 已修正，无拒绝或延期。
- 修复候选 60e53197d3c76b9952bff2115829594315b0d34c 的 [CI 38122162757](https://github.com/nizuowanzhenbang/smart-power-plant/actions/runs/38122162757) 成功，实际合并代码 SHA 的 progress 检查亦成功。
- 不继承旧聊天的 reviewer 从固定 main SHA f8e9c06 恢复，实际结果见 [报告](../docs/RECOVERY-EXERCISE-20261011.md)。报告发现旧摘要不一致，已在 901b777 和最终集成中修正。
- 工具合并后实际 GitHub resume、幂等 claim、merged checkpoint、release、claim PP-020、reproduced checkpoint 成功。真实写入版本及拒绝路径见 [台账](../logs/2026-10-11-batch-01.md)。

SESSION 为实时活动状态，RELEASES 为明确索引的发布证据；固定文件使用同一中央 SHA 读取。CI 自动检查文档/状态并验证索引的真实 PR、合并 SHA 和指定检查。

边界：HTTP fixture 不覆盖生产 GitHub 的所有 fast-forward/权限/分支保护情况；实际正常写入已验证，不声称故障注入或跨平台全覆盖。GitHub 可保留代码与进度，不能保证任意未接入环境的代理自动读取，按 SETUP 接入。自主迭代发生在用户启动的 Codex 会话，未部署无人值守模型服务或现场联合控制。
