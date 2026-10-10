# Codex 读取范围与跨环境设置

中央记录：[smart-power-plant/progress/](https://github.com/nizuowanzhenbang/smart-power-plant/tree/main/progress)。

## 三层入口

1. 总览仓库根目录 AGENTS.md 指向 progress/AGENTS.md 和核心摘要。
2. 10 个业务代码仓库根目录 AGENTS.md 指向中央记录，要求开工读取与收尾回写。
3. 当前环境实际 CODEX_HOME 及默认 ~/.codex 安装仅适用于电厂工作的全局规则；其他环境可复制 templates/GLOBAL-AGENTS.md，保留既有用户指令。

## 官方加载范围

参考：[Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)。全局使用 CODEX_HOME（默认 ~/.codex）；非空 AGENTS.override.md 优先于 AGENTS.md。项目从仓库根目录到当前目录发现指令，更深层规则可覆盖上层。旧检出、未重新启动的会话、指令长度和运行界面都可能影响加载。

本机制是版本化工作约定，不是监控所有 Codex 会话的后台服务，也不启动定时开发。文件存在与远端读取成功不能单独证明任意界面已经加载规则。

## 其他环境

更新目标电厂仓库到包含根目录 AGENTS.md 的版本。在已检出总览仓库根目录且不存在既有全局文件时，可执行：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}"
cp -n progress/templates/GLOBAL-AGENTS.md "${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
```

已有 AGENTS.md 或 override 时合并规则，不覆盖或删除既有内容。此命令不改变 HOME 或 CODEX_HOME。

启动一个新会话，先要求它报告指令来源、中央提交 SHA、当前任务和已经完成而不应重做的内容。无自动 Git 检出的连接会话，用 GitHub 文件工具读取 progress/ 的四个核心文件；具备写权限才能回写。

## 新增仓库与并发

将 progress/templates/REPO-AGENTS.md 合并到新仓库根目录，并更新 REPOSITORIES.md 的接入提交。仅添加中央台账不会让新仓库自动获得入口。

开工认领一个任务，写入前核对中央 HEAD，冲突先合并，不强推覆盖。读取/回写失败时保存本地交接与原始错误，最终明确未读取或未同步；记录机制不提供跨仓库事务锁。
