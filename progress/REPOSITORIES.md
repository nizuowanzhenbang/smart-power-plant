# 仓库与代码基线

核对：2026-10-09 UTC。代码基线是加入本轮接续指令之前的固定提交；文档接入会产生新的 HEAD，不改变这些业务代码基线。

| 仓库 | 默认分支 | 代码基线 | Codex 入口 |
|---|---|---|---|
| [smart-power-plant](https://github.com/nizuowanzhenbang/smart-power-plant) | `main` | [`b31e8c817c2c`](https://github.com/nizuowanzhenbang/smart-power-plant/commit/b31e8c817c2c4b76a446753ccb53c760cf471e70) | 本轮待接入根目录 AGENTS.md |
| [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) | `main` | [`76d799c1fc78`](https://github.com/nizuowanzhenbang/equipment-inspection/commit/76d799c1fc781147ea6bbdeaff0ee57e8bc659db) | 本轮待接入根目录 AGENTS.md |
| [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) | `main` | [`d58a634e2dee`](https://github.com/nizuowanzhenbang/coal-quality-monitor/commit/d58a634e2dee43256ed27d6915903f70353f9219) | 本轮待接入根目录 AGENTS.md |
| [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) | `main` | [`357de14ac550`](https://github.com/nizuowanzhenbang/coal-transport-monitor/commit/357de14ac5506e131acd15698989f352e4f1e9e2) | 本轮待接入根目录 AGENTS.md |
| [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) | `main` | [`db6bfd756ea1`](https://github.com/nizuowanzhenbang/fuel-procurement/commit/db6bfd756ea1f110080caac0a0e3235f17a07cb8) | 本轮待接入根目录 AGENTS.md |
| [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) | `master` | [`140cfc237996`](https://github.com/nizuowanzhenbang/coal-yard-management/commit/140cfc2379969a443a16d09bb7f718b440d9ede0) | 本轮待接入根目录 AGENTS.md |
| [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) | `main` | [`24e33ec011c0`](https://github.com/nizuowanzhenbang/plant-safety/commit/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df) | 本轮待接入根目录 AGENTS.md |
| [emission-monitoring](https://github.com/nizuowanzhenbang/emission-monitoring) | `master` | [`f8384855e957`](https://github.com/nizuowanzhenbang/emission-monitoring/commit/f8384855e957196e22eac9787c84376011d8ac9c) | 本轮待接入根目录 AGENTS.md |
| [coal-unit-efficiency](https://github.com/nizuowanzhenbang/coal-unit-efficiency) | `master` | [`08534f680222`](https://github.com/nizuowanzhenbang/coal-unit-efficiency/commit/08534f680222dba098255deb0b3fc5e9e6ab6093) | 本轮待接入根目录 AGENTS.md |
| [gas-fuel-metering](https://github.com/nizuowanzhenbang/gas-fuel-metering) | `main` | [`349c9e947535`](https://github.com/nizuowanzhenbang/gas-fuel-metering/commit/349c9e947535e800dd4f1e44e36612c5ed0ca10f) | 本轮待接入根目录 AGENTS.md |
| [gas-turbine-performance](https://github.com/nizuowanzhenbang/gas-turbine-performance) | `main` | [`2d33c531abef`](https://github.com/nizuowanzhenbang/gas-turbine-performance/commit/2d33c531abef379e8a6becf7da95511b5f5a27fc) | 本轮待接入根目录 AGENTS.md |

进度仓库自身也带根目录 AGENTS.md。接入结果和文档提交在本轮集成证据中补充。

`gas-emission-monitoring` 不计为已交付业务模块：旧记录为空，本轮没有重新验收该仓库；未来有实际工作时接入入口并核对状态。

## 更新原则

代码发布后更新业务基线；只改进度指令时记录文档接入 SHA，保留业务证据的原始固定版本。不要只依靠默认分支名作为长期验收证据。
