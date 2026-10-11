# 接续补强 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans inline. Steps use checkbox syntax.

**Goal:** PP-003/004/005 同批交付阶段保存、无历史恢复、自动核验和竞争认领。
**Architecture:** Python 标准库分为 GitHub 客户端、状态/核验、CLI。Git 非强制 ref 更新防止过时中央写入；固定 SHA 读取，Markdown 保持摘要，SESSION 为实时活动认领来源。
**Tech Stack:** Python 3.11+、unittest、urllib、GitHub Actions/REST；无第三方依赖。
**Spec:** progress/specs/2026-10-11-continuity-batch.md。

## Global Constraints

用户已授权本批自主设计、实现、检查、集成；当前主代理实现，一次 fresh-context 整分支审查。只检查明确索引的交付；无后台模型服务；不强推、不过期自动抢占。

## Review Focus

- 两会话读取同一中央 HEAD，竞争认领仅一项成功；重试不得偷改所有者。
- 已完成任务、未知任务、畸形状态、空所有者、未经说明的接管不可写入。
- 分支在读后发生任意变更，过时写入不得覆盖；断网/403 不得写成已保存或通过。
- PR 未合并、合并 SHA 不同、检查 pending/failed 或缺失不得通过发布核验。
- 新会话只读固定远端快照能区分已交付与待做，不依赖旧对话内容。

## Task 1 · 状态与阶段保存

Files: progress_tools/github.py、state.py、cli.py、__main__.py；tests/test_progress_tools.py。
Interfaces: snapshot(api, repo) -> (sha, files)；mutate(api, repo, command, task, owner, metadata) -> commit_sha。
- [x] 写真实临时 HTTP API 回归：固定版本读取、竞争/过时写入、所有者/任务保护、明确接管、错误状态、远端代码/合并验证；先确认 CLI/模块缺失失败。
- [x] 实现最小 REST 客户端与 SESSION 校验、claim/checkpoint/release/resume；运行完整 unittest，核对状态及非零拒绝。
- [x] 添加 SESSION/RELEASES 配置、使用说明；实际推送候选并记录验证，不提前标为合并。

## Task 2 · 自动核验与批量约定

Files: progress_tools/audit.py；tests/test_progress_tools.py；.github/workflows/progress.yml；progress/AGENTS.md、CURRENT.md、README.md。
Interfaces: audit(root, remote_api=None) -> list[str]；CLI check --offline / --remote。
- [x] 写坏链接/重复编号/错误状态/畸形 JSON/真实 PR 与检查不符回归，先失败再实现。
- [x] 实现本地/远端核验、只读 CI，中央规则改为一批多项、关键阶段保存，保留证据边界。
- [ ] 全套测试/离线/真实在线核验；提交候选。一次 fresh-context 审查，重要问题 RED→GREEN 修复；候选 CI 后集成，复核 main CI。

## Task 3 · 恢复演练与接续

- [x] reviewer 不继承旧聊天，先只读取远端核心进度，报告最新 SHA、已完成/活动任务/第一动作；保存实际报告与范围。
- [ ] 使用已发布工具实际认领/保存/释放或切换至 PP-020；回写运行结果及批次剩余，随后执行独立煤质设计与计划。

## 执行台账

插件支持脚本资源此前不可用，采用本版本化计划与 progress/logs/2026-10-11-batch-01.md 的实际提交、命令和结果接续。高优先级自主执行指令覆盖重复确认；本轮沿已批准审查建议，不增加设计等待。
