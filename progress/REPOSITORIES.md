# 仓库与代码基线

核对：2026-10-10 UTC。代码基线是加入本轮接续指令之前的固定提交；文档接入会产生新的 HEAD，不改变这些业务代码基线。

| 仓库 | 默认分支 | 代码基线 | Codex 入口 |
|---|---|---|---|
| [smart-power-plant](https://github.com/nizuowanzhenbang/smart-power-plant) | `main` | [`b31e8c817c2c`](https://github.com/nizuowanzhenbang/smart-power-plant/commit/b31e8c817c2c4b76a446753ccb53c760cf471e70) | [已接入 `b2b30735f27c`](https://github.com/nizuowanzhenbang/smart-power-plant/commit/b2b30735f27c99666286a0f00a16647147deb5f0) |
| [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) | `main` | [`76d799c1fc78`](https://github.com/nizuowanzhenbang/equipment-inspection/commit/76d799c1fc781147ea6bbdeaff0ee57e8bc659db) | [已接入 `8047049bb315`](https://github.com/nizuowanzhenbang/equipment-inspection/commit/8047049bb3158959172edc5a7148dd5f35be4217) |
| [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) | `main` | [`d58a634e2dee`](https://github.com/nizuowanzhenbang/coal-quality-monitor/commit/d58a634e2dee43256ed27d6915903f70353f9219) | [已接入 `e527426b9816`](https://github.com/nizuowanzhenbang/coal-quality-monitor/commit/e527426b9816d3843886dd9cd6b7629b2661e8ad) |
| [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) | `main` | [`357de14ac550`](https://github.com/nizuowanzhenbang/coal-transport-monitor/commit/357de14ac5506e131acd15698989f352e4f1e9e2) | [已接入 `9ad9a0ba94cf`](https://github.com/nizuowanzhenbang/coal-transport-monitor/commit/9ad9a0ba94cf79838365387f97d95059b0b3b491) |
| [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) | `main` | [`db6bfd756ea1`](https://github.com/nizuowanzhenbang/fuel-procurement/commit/db6bfd756ea1f110080caac0a0e3235f17a07cb8) | [已接入 `fe025025b6c0`](https://github.com/nizuowanzhenbang/fuel-procurement/commit/fe025025b6c039992fba49b94ea957044b13ab6a) |
| [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) | `master` | [`140cfc237996`](https://github.com/nizuowanzhenbang/coal-yard-management/commit/140cfc2379969a443a16d09bb7f718b440d9ede0) | [已接入 `d2a2aa569dd2`](https://github.com/nizuowanzhenbang/coal-yard-management/commit/d2a2aa569dd2637263fc42c58ba2a903236e1796) |
| [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) | `main` | [`24e33ec011c0`](https://github.com/nizuowanzhenbang/plant-safety/commit/24e33ec011c0d0cc3dd3d9dcc79dffb1440541df) | [已接入 `b8a1c05a4f39`](https://github.com/nizuowanzhenbang/plant-safety/commit/b8a1c05a4f39fe5e3e56741bed6cd7d0f27f6dd0) |
| [emission-monitoring](https://github.com/nizuowanzhenbang/emission-monitoring) | `master` | [`f8384855e957`](https://github.com/nizuowanzhenbang/emission-monitoring/commit/f8384855e957196e22eac9787c84376011d8ac9c) | [已接入 `eefab6262450`](https://github.com/nizuowanzhenbang/emission-monitoring/commit/eefab6262450ba26d7192dbfc317b3bba2a9380e) |
| [coal-unit-efficiency](https://github.com/nizuowanzhenbang/coal-unit-efficiency) | `master` | [`08534f680222`](https://github.com/nizuowanzhenbang/coal-unit-efficiency/commit/08534f680222dba098255deb0b3fc5e9e6ab6093) | [已接入 `39180dc6eed8`](https://github.com/nizuowanzhenbang/coal-unit-efficiency/commit/39180dc6eed80b5d8392641e03f72f3c60fe6ae3) |
| [gas-fuel-metering](https://github.com/nizuowanzhenbang/gas-fuel-metering) | `main` | [`349c9e947535`](https://github.com/nizuowanzhenbang/gas-fuel-metering/commit/349c9e947535e800dd4f1e44e36612c5ed0ca10f) | [已接入 `bba7b57086ff`](https://github.com/nizuowanzhenbang/gas-fuel-metering/commit/bba7b57086ff5854cd128d4c5415167a379ef0c9) |
| [gas-turbine-performance](https://github.com/nizuowanzhenbang/gas-turbine-performance) | `main` | [`2d33c531abef`](https://github.com/nizuowanzhenbang/gas-turbine-performance/commit/2d33c531abef379e8a6becf7da95511b5f5a27fc) | [已接入 `3da515e6e5fa`](https://github.com/nizuowanzhenbang/gas-turbine-performance/commit/3da515e6e5fab29b70b217006e7c6f6afe74ffa1) |

总览根目录与全部 10 个业务仓库已接入入口；11 个远端文件按接入提交复读并与模板逐字比较一致。记录在 [集成证据](evidence/2026-10-10-memory-integration.md)。

`gas-emission-monitoring` 不计为已交付业务模块：旧记录为空，本轮没有重新验收该仓库；未来有实际工作时接入入口并核对状态。

## 更新原则

代码发布后更新业务基线；只改进度指令时记录文档接入 SHA，保留业务证据的原始固定版本。不要只依靠默认分支名作为长期验收证据。
