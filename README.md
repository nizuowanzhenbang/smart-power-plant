# 智慧发电厂全链路管理平台 · Smart Power Plant Suite

> 围绕燃煤发电厂日常运营，从 **燃料采购 → 港口装船 → 入厂运输 → 化验验收 → 煤场存储 → 锅炉燃用** 的「物的流转」主线，以及 **日常点检 → 缺陷处理 → 隐患整改** 的「设备 + 安全」副线，由 **6 个独立部署、通过共享密钥互联互通** 的子系统组成的一体化数字管理体系。
>
> 本仓库不放代码，是 6 个子系统的 **总览、运作原理、数据联动、技术栈说明书**。

---

## 目录

- [一、为什么需要这套系统](#一为什么需要这套系统)
- [二、整体业务运作原理（一批煤的完整数字旅程）](#二整体业务运作原理一批煤的完整数字旅程)
- [三、六个子系统逐一介绍](#三六个子系统逐一介绍)
- [四、跨系统数据联动设计（统一数据字典）](#四跨系统数据联动设计统一数据字典)
- [五、跨系统集成接口矩阵](#五跨系统集成接口矩阵)
- [六、技术栈逐项](#六技术栈逐项)
- [七、默认端口与账户矩阵](#七默认端口与账户矩阵)
- [八、端到端冒烟测试](#八端到端冒烟测试)
- [九、迭代路线](#九迭代路线)
- [十、设计哲学](#十设计哲学)

---

## 一、为什么需要这套系统

传统燃煤发电厂的运营痛点：

- **数据孤岛**：采购台账在 Excel、港口/入厂化验在 LIMS、煤场库存在纸质台账、点检在巡检本 —— 同一批煤的旅程被切成 5–6 段，没人能完整讲一遍。
- **反舞弊难**：港口实测 vs 入厂实测、订单合同价 vs 实际结算、出场过磅 vs 实际燃用 —— 偏差散落在各子系统，没人系统性盯。
- **闭环断点**：点检发现的重大缺陷没人转隐患单；隐患整改后没人复查；入场的煤没人对煤质化验数据；订单到货状态没人推进。
- **责任不清**：跨部门流转走纸质，超期不报警，整改不追踪，权责不可审计。

本套件以 **「一批煤的完整旅程」+「设备健康的全生命周期」** 为两条主线，把 6 个子系统串成数字闭环 —— 每一个环节都有数据沉淀、每一次跨系统流转都通过 `X-Integration-Token` 鉴权 + 幂等键审计可查。

---

## 二、整体业务运作原理（一批煤的完整数字旅程）

```
                ┌─────────────────────────────────────────────────────────────────────┐
                │   主线（物的流转） · 一批煤的完整数字旅程   2026·智慧电厂   │
                └─────────────────────────────────────────────────────────────────────┘

   [1] 燃料部下计划             [2] 港口装船 / 汽车启运         [3] 入厂磅房 + 双端化验
        │                              │                                │
        ▼                              ▼                                ▼
┌──────────────────┐    order_no   ┌──────────────────┐  batch_number  ┌──────────────────┐
│ fuel-procurement │──────────────►│ coal-transport-  │───────────────►│ coal-quality-    │
│   采购管理       │               │   monitor 运输   │ supplier_name  │   monitor 化验   │
│ 供应商/合同/订单 │               │ 重量/时间/铅封  │                │ 港口vs入厂六维   │
└─────────┬────────┘               └────────┬─────────┘                └────────┬─────────┘
          │                                 │ transport-event(批次)             │
          │                                 ▼                                   │
          │                       ┌──────────────────┐    供应商信用分回写     │
          │                       │ 运输事件 → 质量  │◄────────────────────────┘
          │ ◄─── /webhook/         │   预警归集表    │
          │     quality-score     └──────────────────┘
          │
          │  GET /api/integration/order-info  (订单 + 合同 + 煤质基准)
          │  ◄──────────────────────────────────────────────────────────────────┐
          │                                                                     │
          │  POST /api/integration/yard-stocked  (入场回调，推进 delivered_qty) │
          │  ◄──────────────────────────────────────────────────────────────────┤
          ▼                                                                     │
┌──────────────────┐    order_no    ┌──────────────────┐   去向：锅炉/磨煤机    │
│ coal-yard-       │◄───────────────│ coal-yard-       │────────────────►   #1机组 / #2磨煤机
│ management 库存  │   FIFO 扣减    │ management 出场  │
│ 堆区/入场/盘点   │                └──────────────────┘
│ 温度/库龄/配煤   │
└─────────┬────────┘  GET /api/integration/order-quality-summary
          │  ◄───────────────────────────────────────────────────────────► coal-quality-monitor
          │
          │
                ┌─────────────────────────────────────────────────────────────────────┐
                │   副线（设备 + 安全） · 健康度全生命周期监督                          │
                └─────────────────────────────────────────────────────────────────────┘

[A] 日常点检路线        [B] 异常发现 → 缺陷工单           [C] CRITICAL 缺陷 → 隐患单
       │                         │                                      │
       ▼                         ▼                                      ▼
┌──────────────────┐  生成缺陷  ┌──────────────────┐  POST           ┌──────────────────┐
│ equipment-       │──────────►│ equipment-       │  /api/           │ plant-safety     │
│ inspection 点检  │            │ inspection 缺陷  │  integration/   │  隐患排查         │
│ 8系统/13张表/    │            │ + 两票管理       │  hazards        │ 11分区/13类别     │
│ APScheduler 调度 │            │ + 健康度联动     │ ─────────────► │ 整改/复查闭环     │
└─────────┬────────┘            └────────┬─────────┘                  └─────────┬────────┘
          │                              │                                       │
          │ 设备 360° 视图               │ safety_hazard_no 回写                │
          └──────────────────────────────┘ ◄─────────────────────────────────────┘
```

### 两条主线 + 一个交汇点

- **主线一（物的流转）**：`采购合同 → 订单调度 → 港口装船/汽运 → 进厂过磅 → 双端化验比对 → 煤场堆放 → FIFO 出场 → 锅炉燃用`
- **主线二（设备健康）**：`点检路线巡检 → 异常自动生成缺陷 → 工作票/操作票管控 → CRITICAL 缺陷自动建隐患单 → 现场整改 → 复查关闭 → 健康度回弹`
- **交汇点**：煤场库存「入煤综合评分」直接影响「锅炉燃用」选煤；设备健康决定「能否燃用」。两条线在 **配煤建议** 与 **#1/#2 机组检修计划** 处合流。

---

## 三、六个子系统逐一介绍

每个子系统都是 **独立后端 (FastAPI) + 独立前端 (React + TypeScript + Ant Design 5 + ECharts) + 独立 SQLite/PostgreSQL** 的完整应用，可单独启动、单独迁移、单独退役。

### 📦 [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) · 燃料采购管理 — v2.1

**业务定位**：链路起点。燃料部所有「采购意图」在这里固化为 **供应商档案 → 框架/长协/现货合同 → 采购订单** 三层数据，是煤场入场时核对履约的权威源。

**数据库表（7 张）**：

| 表名 | 作用 | 核心字段 |
|---|---|---|
| `users` | 4 类角色账户 | role(ADMIN/BUYER/APPROVER/VIEWER) |
| `suppliers` | 供应商档案 | **code(GYS-NNNN)**, name, tier(STRATEGIC/PREFERRED/QUALIFIED/PROBATION), status, credit_score |
| `fuel_contracts` | 合同主表 | **contract_no(HT-YYYYMM-NNNN)**, supplier_id, coal_type, **spec_calorific_value, spec_ash_max, spec_sulfur_max, spec_moisture_max**, status, delivered_quantity |
| `contract_approvals` | 多级审批流水 | level(1/2/3), approver, approved_at |
| `contract_price_history` | 单价调整审计 | old_price, new_price, reason |
| `purchase_orders` | 订单主表 | **order_no(PO-YYYYMMDD-NNNN)**, contract_id, planned_quantity, delivered_quantity, unit_price, status |
| `supplier_quality_scores` | 来自化验系统的信用回写 | supplier_name, score, sample_count |

**业务规则**：

- **三套状态机**：
  - 供应商：`PENDING_REVIEW → ACTIVE → SUSPENDED / BLACKLISTED / ARCHIVED`
  - 合同：`DRAFT → PENDING_APPROVAL → ACTIVE → COMPLETED / EXPIRED / TERMINATED`
  - 订单：`PLANNED → DISPATCHED → PARTIAL_RECEIVED → RECEIVED → SETTLED`
- **金额阈值审批**：`< 100 万 / 100–500 万 / > 500 万` 自动触发 `1 / 2 / 3` 级审批，审批人由 `APPROVER` 角色担任
- **价格审计**：生效合同的单价调整不能直改 `unit_price`，必须走 `POST /contracts/{id}/adjust-price`，旧值写入 `contract_price_history`
- **自动履约**：煤场入场回调 → `orders.delivered_quantity` 累加 → 同步累加到 `contracts.delivered_quantity` → 达到 99% 自动 `COMPLETED`

**对外接口（被调用）**：
- `GET /api/integration/order-info?order_no=` → 返回订单 + 合同 + 供应商 + **合同煤质基准**（spec_*）给煤场系统
- `POST /api/integration/yard-stocked` → 接收煤场入场回调，自动累计 `delivered_quantity` 并推进状态机
- `POST /api/webhook/quality-score` → 接收化验系统推送的供应商信用分，落到 `supplier_quality_scores`

---

### 🚛 [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) · 运煤监督与风险预警 — v2.0

**业务定位**：港口 → 厂区的 **运输过程反舞弊监控**。每一台运煤车出港和入厂都过磅 + 扫铅封，三大分析器实时识别「以次充好、半路换货、虚报重量、人为滞留」四类风险。

**数据库表（5 张）**：

| 表名 | 作用 | 核心字段 |
|---|---|---|
| `users` | 账户 | admin/admin123 |
| `vehicles` | 车辆档案 | **plate_number(车牌)**, tare_weight(皮重), driver_name |
| `transport_records` | 运输主表 | **batch_number(关联化验系统)**, vehicle_id, supplier_name, departure_weight/arrival_weight, weight_diff_ratio, transport_duration, status |
| `seal_records` | 铅封扫描 | qr_code, seal_type(DEPARTURE/ARRIVAL), transport_id |
| `alerts` | 预警归集 | alert_type, severity, threshold_value, actual_value |

**三大分析器（services/）**：

- **WeightAnalyzer**：亏吨/盈吨检测，`3‰` 基础阈值 + **Z-score 动态阈值**（同车队同煤种近 30 天）
- **TimeAnalyzer**：运输时长 **IQR (四分位距) 基准**，识别异常滞留
- **SealAnalyzer**：QR 码铅封 **Levenshtein 相似度** 比对，识别篡改/替换

**v2.0 增强**：

- WebSocket 实时预警广播（JWT 鉴权 + ConnectionManager）
- CSV 导出（UTF-8 BOM 防 Excel 乱码）
- ORM N+1 查询优化（joinedload 批量预取）
- 前端 TypeScript 类型完善

**对外推送**：
- 运输完成时主动 `POST /api/integration/transport-event` → coal-quality-monitor，把重量差/时长/铅封异常事件写入化验系统的 `quality_alerts` 表，关联同 `batch_number`

---

### ⚗️ [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) · 煤质化验数据比对 — v2.1

**业务定位**：**港口化验 vs 入厂化验** 六维煤质指标偏差检测，是「以次充好、货物掉包」的最后一道防线，同时是供应商长期信用评分的计算源。

**数据库表（6 张）**：

| 表名 | 作用 | 核心字段 |
|---|---|---|
| `users` | 账户 | admin/admin123 |
| `suppliers` | 供应商（与采购系统按 `name` 软关联） | name, credit_score |
| `coal_batches` | 批次主表 | **batch_number**, **order_no(关联采购+煤场)**, supplier_id, contract_calorific_value, contract_ash_max, contract_sulfur_max, contract_moisture_max, status, risk_score |
| `quality_tests` | 化验明细 | batch_id, test_type(PORT/FACTORY), calorific_value, ash, sulfur, moisture, volatile, fixed_carbon |
| `quality_alerts` | 预警归集 | batch_id, alert_type, severity, threshold/actual, status |
| `audit_logs` | 操作审计 | user, action, target |

**8 种预警类型**：

`CALORIFIC_SHORTAGE`（热值不足）/ `ASH_EXCESS`（灰分超标）/ `SULFUR_EXCESS`（硫分超标）/ `MOISTURE_EXCESS`（水分超标）/ `CONTRACT_CALORIFIC` / `CONTRACT_ASH` / `CONTRACT_SULFUR`（合同基准超标）/ `COMPREHENSIVE`（六维综合偏差）

**核心可视化**：

- **六维归一化雷达图**：热值 / 灰分 / 硫分 / 水分 / 挥发分 / 固定碳
- **供应商信用评分** (`services/supplier_scorer.py`)：0–100 分，基于近 20 批次 + 加权（热值 40% + 灰硫水 各 15% + 综合预警 15%）
- WebSocket JWT 鉴权 + 实时预警推送

**对外接口**：
- `GET /api/integration/order-quality-summary?order_no=` → 给煤场入场前拉化验汇总（PORT/FACTORY 均值 + 严重预警计数 + conclusion）
- `GET /api/integration/supplier-credit?supplier_name=` → 给采购系统查信用分
- `GET /api/integration/order-quality?order_no=` → 给采购系统查订单化验明细
- `POST /api/integration/transport-event` ← 接收运输系统推送的运输事件，落 `quality_alerts`

---

### 🏭 [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) · 煤场库存管理 — v2.1

**业务定位**：燃料链的「最后一公里」—— 到货之后到燃用之前的 **实物管理**。是整个套件中跨系统调用最多的中心节点（同时调采购 + 化验 + 接收回调）。

**数据库表（7 张）**：

| 表名 | 作用 | 核心字段 |
|---|---|---|
| `users` | 账户（4 类角色） | role(ADMIN/OPERATOR/SUPERVISOR/VIEWER) |
| `coal_yards` | 堆区档案 | **code(DQ-NNN)**, designated_coal_type, capacity, status(ACTIVE/MAINTENANCE/DISABLED) |
| `stock_ins` | 入场主表 | **stockin_no(IN-YYYYMMDD-NNNN)**, yard_id, **order_no(关联采购)**, supplier_name, coal_type, quantity, **calorific_value/ash/sulfur/moisture (从化验系统同步)**, quality_synced, **remaining_quantity(FIFO 用)**, stocked_at |
| `stock_outs` | 出场主表 | **stockout_no(OUT-YYYYMMDD-NNNN)**, yard_id, quantity, destination, **fifo_breakdown(JSON 扣减明细)**, status(PENDING_APPROVAL/APPROVED/REJECTED/COMPLETED), approver |
| `stocktakes` | 盘点单 | **stocktake_no(PD-YYYYMMDD-NNN)**, book_quantity, actual_quantity, status |
| `inventory_snapshots` | 每日库存快照 | yard_id, snapshot_date, end_quantity |
| `temperature_readings` | 自燃温度监控 | yard_id, temperature, level(NORMAL/WARN/ALERT/DANGER) |

**业务规则**：

- **堆区状态机**：`ACTIVE ⇄ MAINTENANCE`，→ `DISABLED` 需空仓
- **入场约束**：堆区必须 `ACTIVE` + 煤种必须匹配 `designated_coal_type` + 不超过 `capacity`
- **FIFO 出场**：按 `stock_ins.stocked_at ASC` 扣减 `remaining_quantity`，明细写 `stock_outs.fifo_breakdown(JSON)`
- **库龄三级预警**：`≤15 天 绿 / 15–30 天 黄 / >30 天 红`，前端 Dashboard 库龄红榜
- **盘点缩放**：审批通过则按 `actual/book` 比例缩放所有 `remaining_quantity > 0` 的批次
- **自燃温度三档**：`50℃ WARN / 65℃ ALERT / 80℃ DANGER`，前端温度页含高温榜 + 趋势图
- **入煤综合评分** (`utils/coal_score.py`)：`热值基础 + (灰/硫/水)扣分 + 库龄衰减` → Dashboard 配煤建议表按 `(评分 + 库龄权重)` 排序
- **大额出场审批**：`>= 5000 吨` 创建即 `PENDING_APPROVAL`（不扣减），主管审批通过才执行 FIFO 扣减

**关键集成（核心枢纽）**：

```
[创建入场单] ──► 调 fuel-procurement /order-info  (拉合同煤质基准 + 供应商)
              ──► 调 coal-quality-monitor /order-quality-summary  (拉化验均值)
              ──► 写 stock_ins，stocked
[入场成功]   ──► 回调 fuel-procurement /yard-stocked  (推进订单 delivered_quantity)
```

---

### 🔧 [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) · 设备点检与缺陷管理 — v2.5

**业务定位**：发电核心设备的 **健康保障中心**。13 张表覆盖从「设备台账 → 点检路线 → 测点 → 任务 → 缺陷 → 工作票/操作票 → 备品备件」的完整闭环，CRITICAL 缺陷自动同步到 plant-safety 建隐患单。

**数据库表（13 张）**：

| 模块 | 表 |
|---|---|
| 账户 | `users` (5 角色：ADMIN/INSPECTOR/REPAIRMAN/SUPERVISOR/VIEWER) |
| 设备 | `equipments` (8 系统 × 3 关键度 A/B/C) |
| 点检 | `inspection_routes` / `inspection_points` / `inspection_tasks` / `inspection_records` |
| 缺陷 | `defects` (含 `safety_sync_status` / `safety_hazard_no` / `safety_sync_attempts` 联动字段) |
| 两票 | `work_tickets` / `operation_tickets` / `operation_templates` |
| 备件 | `spare_parts` / `stock_movements` |
| 审计 | `audit_logs` |

**业务规则**：

- **设备状态机**：`RUNNING ⇄ STANDBY ⇄ MAINTENANCE → DECOMMISSIONED`；点检 SEVERE 自动转 `MAINTENANCE`
- **缺陷状态机**：`NEW → ASSIGNED → IN_REPAIR → REPAIRED → VERIFIED(=CLOSED)`，超 SLA 打 `OVERDUE` 标
- **缺陷自动派生**：点检异常 → 自动生成缺陷，`severity = 设备等级 × 异常程度` (A + SEVERE = CRITICAL)
- **SLA**：MINOR `72h` / MAJOR `24h` / CRITICAL `4h`
- **健康度联动**：缺陷扣分（CRITICAL -15、MAJOR -8、MINOR -3），验收回弹（+10/+6/+3）
- **APScheduler 4 job**：超期扫描 / 漏检扫描 / 任务自动生成 / 联动重试（plant-safety 失败重推）
- **预测性维护算法**：`综合风险 = 缺陷30% + CRITICAL率25% + 异常率15% + 健康度20% + 等级状态加成`，sigmoid 平滑成失效概率
- **两票管理**：
  - 工作票：`DRAFT → SUBMITTED → ISSUED → IN_WORK → COMPLETED → CLOSED`，许可时设备自动转 MAINTENANCE，归档时无在工票自动恢复 RUNNING
  - 操作票：`DRAFT → REVIEWED → APPROVED → EXECUTING → COMPLETED`，`steps(JSON)` 分步 PASS/FAIL
  - 安全措施清单 + 逐条勾选 API
- **PWA + 移动扫码**：manifest + service worker；`/m/scan` 路由用 `BarcodeDetector` 摄像头扫码 + 拍照上报
- **QR 批量打印**：`segno` 生成 SVG + `/equipment-qr-print` A4 4 列网格
- **WebSocket 5 个事件**：`defect.critical_created` / `defect.overdue_swept` / `task.missed_swept` / `defect.safety_synced` / `defect.safety_sync_failed`

**对外推送**：
- CRITICAL 缺陷自动 `POST /api/integration/hazards` → plant-safety，幂等基于 `defect_no`，失败由 APScheduler 重试

---

### 🛡️ [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) · 安全生产管理 — v1.1

**业务定位**：发电厂日常 **隐患排查与整改闭环**。既独立接收人工巡查上报，也作为 equipment-inspection CRITICAL 缺陷的下游隐患承接系统。

**数据库表（2 张）**：

| 表名 | 作用 | 核心字段 |
|---|---|---|
| `users` | 账户 | admin/admin123 |
| `hazards` | 隐患主表 | **hazard_code(YH-YYYYMMDD-NNNN)**, area(11 分区), category(13 类别), level(GENERAL/MAJOR), status, **external_source / external_no(幂等键)**, assignee, deadline |

**11 个分区**：主厂房 / 锅炉区 / 汽轮机区 / 电气区 / 燃料区 / 化学水 / 除灰除渣 / 脱硫脱硝 / 冷却塔 / 开关站 / 办公区

**13 个风险类别**：电气安全 / 锅炉压力容器 / 危险化学品 / 高处作业 / 有限空间 / 动火作业 / 起重作业 / 辐射防护 / 消防安全 / 机械伤害 / 环境排放 / 现场环境 / 其他

**业务规则**：

- **状态机**：`PENDING → IN_PROGRESS → RECTIFIED → VERIFIED`，超期自动 `OVERDUE`
- **整改期限**：重大隐患 `14 天`，一般隐患 `30 天`
- **设备号 → 分区映射**：接收 equipment-inspection 推送时，按设备号前缀（`-BL-` 锅炉 / `-TB-` 汽轮机 / `-EL-` 电气 / `-CH-` 化学 / `-AS-` 除灰除渣 / `-DS-` 脱硫脱硝）自动 `area`
- **CRITICAL → MAJOR(14d)，其他 → GENERAL(30d)**

**对外接口（被调用）**：

- `POST /api/integration/hazards` → 接收外部推送，**幂等基于 `external_source + external_no` 唯一**，返回 `hazard_code` 给对方回写
- `GET /api/integration/hazards/by-external/{source}/{external_no}` → 反查

---

## 四、跨系统数据联动设计（统一数据字典）

**联动设计的核心：把"主键"统一在业务编号上，而不是数据库自增 ID。** 6 个子系统是 6 个独立数据库，没有外键约束，但通过下面这套 **共享业务编号 + 共享密钥** 实现端到端的数据联动可追溯：

### 1) 关键共享字段（跨系统 Join Key）

| 共享字段 | 在哪些系统出现 | 字段定义 | 作用 |
|---|---|---|---|
| `order_no` (PO-YYYYMMDD-NNNN) | fuel-procurement(`purchase_orders.order_no`)<br/>coal-yard(`stock_ins.order_no`)<br/>coal-quality-monitor(`coal_batches.order_no`) | String(50) | **物的流转主干**：从合同→订单→运输→化验→入场全程同一个 order_no |
| `supplier_name` | fuel-procurement(`suppliers.name`)<br/>coal-quality-monitor(`suppliers.name`, `coal_batches.supplier_id→name`)<br/>coal-transport-monitor(`transport_records.supplier_name`) | String(100~200) | **供应商画像主干**：信用分计算、信用回写按 name 软关联 |
| `batch_number` | coal-transport-monitor(`transport_records.batch_number`)<br/>coal-quality-monitor(`coal_batches.batch_number`) | String(50) | **运输 ↔ 化验** 上下游键，同一批煤的运输事件与化验结果挂钩 |
| `contract_no` (HT-YYYYMM-NNNN) | fuel-procurement(`fuel_contracts.contract_no`)<br/>coal-yard(`stock_ins.contract_no`) | String(50) | 入场单回填的合同号，便于煤场快速反查履约 |
| `defect_no` (DF-YYYYMMDD-NNNN) | equipment-inspection(`defects.defect_no`)<br/>plant-safety(`hazards.external_no`) | String(50) | **缺陷 → 隐患** 上下游键，幂等防重 |
| `hazard_code` (YH-YYYYMMDD-NNNN) | plant-safety(`hazards.hazard_code`)<br/>equipment-inspection(`defects.safety_hazard_no`) | String(50) | plant-safety 内部隐患号，回写给设备系统形成双向链 |
| `equipment_code` (EQ-XX-NNNN) | equipment-inspection(`equipments.code`)<br/>plant-safety(`hazards.title/description` 文本含) | String(50) | 设备前缀（BL/TB/GN/AX/EL/CH/AS/DS）→ plant-safety 分区映射 |
| `yard_code` (DQ-NNN) | coal-yard(`coal_yards.code`)<br/>fuel-procurement(回调 payload) | String(50) | 入场回调里告知采购"入了哪个堆区" |

### 2) 合同煤质基准的跨系统继承

```
fuel_contracts.spec_calorific_value
fuel_contracts.spec_ash_max          ┐
fuel_contracts.spec_sulfur_max       ├──► /api/integration/order-info  携带
fuel_contracts.spec_moisture_max     ┘                ↓
                                                煤场入场时与化验值比对
                                                     ↓
                                         coal_batches.contract_calorific_value
                                         coal_batches.contract_ash_max     ┐
                                         coal_batches.contract_sulfur_max  ├─ 化验系统冗余存储，
                                         coal_batches.contract_moisture_max┘   便于离线偏差分析
```

合同煤质基准（`spec_*` 四维）作为「事实数据」，从 `fuel-procurement` 单向流向 `coal-yard` 和 `coal-quality-monitor`，避免化验员手动录入出错。化验系统冗余 `contract_*` 字段是为了支持离线/历史回溯。

### 3) 状态机的跨系统级联

```
采购订单履约状态：
PLANNED ──► DISPATCHED ──► PARTIAL_RECEIVED ──► RECEIVED ──► SETTLED
              ↑                  ↑                   ↑
              │                  │                   │
       由 yard-stocked 回调驱动（累计 delivered_quantity / planned_quantity）

设备健康联动：
点检 SEVERE ──► Defect.severity=CRITICAL ──► POST /hazards ──► Hazard.PENDING
                                                                   │
       Equipment.status=MAINTENANCE   ◄─── 整改期间 ───            │
                                                                   ▼
       Equipment.health_score 回弹    ◄─── Hazard.VERIFIED ◄─── 复查通过
```

### 4) 鉴权与幂等约定

- **共享密钥**：所有跨系统调用使用同一个 `INTEGRATION_SECRET`（生产环境通过环境变量注入，开发用 `.env` 默认值）
- **统一 Header**：新接口 `X-Integration-Token`；老接口（运输→化验、缺陷→隐患）保留 `X-Integration-Secret` 兼容
- **幂等键**：缺陷→隐患用 `(external_source, external_no)` 唯一约束；入场回调用 `(order_no, stockin_no)` 防重；运输事件用 `batch_number + alert_type` 软去重
- **降级策略**：所有跨系统 HTTP 客户端超时 `3s`，失败不抛错，由后台 APScheduler / 手动重推恢复

---

## 五、跨系统集成接口矩阵

| # | 调用方 → 被调方 | 方法 | 路径 | 鉴权 Header | 用途 | 失败降级 |
|---|---|---|---|---|---|---|
| 1 | **coal-yard → fuel-procurement** | GET | `/api/integration/order-info?order_no=` | X-Integration-Token | 入场时拉订单+合同+供应商+**煤质基准 spec_***| 入场单 supplier_name/contract_no 留空 |
| 2 | **coal-yard → fuel-procurement** | POST | `/api/integration/yard-stocked` | X-Integration-Token | 入场后回调，累计 delivered_quantity + 推进状态机 | 由 fuel-procurement 调度补登记 |
| 3 | **coal-yard → coal-quality-monitor** | GET | `/api/integration/order-quality-summary?order_no=` | X-Integration-Token | 入场前拉化验汇总（PORT/FACTORY 均值 + conclusion） | 入场单 quality_synced=False，待手动同步 |
| 4 | **fuel-procurement → coal-quality-monitor** | GET | `/api/integration/supplier-credit?supplier_name=` | X-Integration-Token | 供应商详情页拉信用分 | 显示"暂无" |
| 5 | **fuel-procurement → coal-quality-monitor** | GET | `/api/integration/order-quality?order_no=` | X-Integration-Token | 订单详情聚合化验明细 | 显示"待化验" |
| 6 | **coal-quality-monitor → fuel-procurement** | POST | `/api/webhook/quality-score` | X-Integration-Token | 信用分变更回写采购的 supplier_quality_scores | 由化验系统调度补推 |
| 7 | **coal-transport-monitor → coal-quality-monitor** | POST | `/api/integration/transport-event` | X-Integration-Secret（兼容） | 运输完成事件 → 化验系统预警归集 | 写本地日志，人工补录 |
| 8 | **equipment-inspection → plant-safety** | POST | `/api/integration/hazards` | X-Integration-Secret | CRITICAL 缺陷自动建隐患单，回写 hazard_code | APScheduler 重试 + 前端手动重推 |
| 9 | **equipment-inspection → plant-safety** | GET | `/api/integration/hazards/by-external/{source}/{external_no}` | X-Integration-Secret | 反查隐患状态 | 显示"未同步" |

**所有接口的 payload 都遵循统一响应壳**：`{ code: 200, message: "...", data: {...} }`

---

## 六、技术栈逐项

### 6.1 通用基线（6 个系统共享）

| 层 | 选型 | 版本 |
|---|---|---|
| 后端框架 | **FastAPI** | ≥ 0.100 |
| 异步运行时 | **uvicorn[standard]** | ≥ 0.20 |
| ORM | **SQLAlchemy 2.x** | ≥ 2.0 |
| 数据校验 | **Pydantic 2.x** + pydantic-settings | ≥ 2.0 |
| 鉴权 | **JWT** (python-jose) + **bcrypt** (passlib) | — |
| 跨系统调用 | **httpx** | ≥ 0.24 |
| 前端框架 | **React 18** + **TypeScript 5** | — |
| 构建 | **Vite 5** | — |
| UI 库 | **Ant Design 5** + **@ant-design/icons** | — |
| 图表 | **ECharts 5** + echarts-for-react | — |
| 状态管理 | **Zustand 4** | — |
| 路由 | **react-router-dom 6** | — |
| HTTP | **axios** | — |
| 数据库 | **SQLite**（开发） / **PostgreSQL**（生产可平移，无方言锁定） | — |

### 6.2 各系统独有技术栈

| 子系统 | 独有依赖与亮点 |
|---|---|
| **fuel-procurement** | 仅基线 + httpx → 业务纯度最高，重在状态机与审批流 |
| **coal-transport-monitor** | **numpy + pandas + scikit-learn**（三大分析器统计学算法）+ **websockets**（实时预警）+ **openpyxl**（Excel 导出）+ **alembic**（迁移）+ **pytest** |
| **coal-quality-monitor** | **numpy + pandas + scikit-learn**（六维偏差 + 供应商评分）+ **websockets** + **alembic** + **pytest** |
| **coal-yard-management** | 基线 + httpx，自研 `utils/coal_score.py`（入煤评分算法） + `utils/integration_client.py`（双下游集成客户端） |
| **equipment-inspection** | **APScheduler**（4 job 调度器：超期/漏检/任务生成/联动重试） + **segno**（设备 QR 码生成）+ httpx + **WebSocket** + **PWA**（manifest + service worker） + **BarcodeDetector**（前端原生扫码 API） |
| **plant-safety** | 仅基线，无 httpx（纯接收方），重在状态机与幂等接口 |

### 6.3 部署与运维

- **进程模型**：每个子系统独立 `uvicorn` 进程（开发期）/ 独立容器（生产）
- **配置**：每个子系统的 `app/config.py` 用 `pydantic_settings.BaseSettings` 从 `.env` 加载
- **关键环境变量**：
  - `INTEGRATION_SECRET` — 共享密钥
  - `FUEL_PROCUREMENT_URL` — 在 coal-yard 配置
  - `QUALITY_SYSTEM_URL` — 在 coal-yard、fuel-procurement 配置
  - `SAFETY_SYSTEM_URL` — 在 equipment-inspection 配置
  - `INTEGRATION_TIMEOUT_SEC` — 跨系统调用超时（默认 3s）

---

## 七、默认端口与账户矩阵

| 系统 | 后端端口 | 前端端口 | 默认账户 |
|---|---|---|---|
| [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) | **8000** | 5173 | admin/admin123, buyer/buyer123, approver/approver123, viewer/viewer123 |
| [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) | **8001** | 5174 | admin/admin123, operator/operator123, supervisor/supervisor123, viewer/viewer123 |
| [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) | **8002** | 5176 | admin/admin123 |
| [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) | **8003** | 5175 | admin/admin123, inspector/inspector123, repairman/repairman123, supervisor/supervisor123, viewer/viewer123 |
| [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) | 8000 ⚠️ | 5173 ⚠️ | admin/admin123 |
| [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) | 8000 ⚠️ | 5173 ⚠️ | admin/admin123 |

> ⚠️ **端口冲突说明**：plant-safety、coal-transport-monitor 与 fuel-procurement 默认同端口（8000/5173）。生产环境通过 Docker Compose / Nginx 反代分离；开发环境通过覆盖 `.env` 的 `PORT` 与 `vite --port` 二选一启动，或改为预留：
> - fuel-procurement: 8000 / 5173
> - coal-yard-management: 8001 / 5174
> - coal-quality-monitor: 8002 / 5176
> - equipment-inspection: 8003 / 5175
> - plant-safety: 8004 / 5177（建议生产覆盖）
> - coal-transport-monitor: 8005 / 5178（建议生产覆盖）

---

## 八、端到端冒烟测试

[coal-yard-management/backend/integration_smoke_test.py](https://github.com/nizuowanzhenbang/coal-yard-management/blob/main/backend/integration_smoke_test.py) 提供 **三方端到端冒烟脚本**：

```bash
# 默认端口：8000(fuel-procurement) / 8001(coal-yard) / 8002(coal-quality-monitor)
cd coal-yard-management/backend
python integration_smoke_test.py --run-yard
```

`--run-yard` 触发真实入场流程，覆盖：

1. coal-yard 调 fuel-procurement `/order-info` 拉订单
2. coal-yard 调 coal-quality-monitor `/order-quality-summary` 拉化验
3. 写入 `stock_ins` 完成入场
4. coal-yard 回调 fuel-procurement `/yard-stocked` 推进订单 → `delivered_quantity` 累加 → 状态机推进

**equipment-inspection ↔ plant-safety 联动**：通过 [equipment-inspection/backend/seed_data.py](https://github.com/nizuowanzhenbang/equipment-inspection) 模拟 `SYNCED / FAILED / PENDING / SKIPPED` 四种状态，前端 DefectList 显示"隐患联动"列 + 失败可手动重推。

---

## 九、迭代路线

| 系统 | 当前版本 | 规划要点 |
|---|---|---|
| fuel-procurement | v2.1 | v3.0：招标比价模块；与 ERP 财务结算对接；合同电子签章 |
| coal-yard-management | v2.1 | v3.0：三方智能配煤算法升级；与 SCADA 实时取数；皮带秤直连 |
| coal-quality-monitor | v2.1 | v3.0：多港口化验机构接入；化验设备 (CKIC/SDLA) 直连；LIMS 推送 |
| equipment-inspection | v2.5 | v3.0：S3/OSS 对象存储、两票电子签名、离线模式、备件 → 采购单、Docker Compose |
| plant-safety | v1.1 | v2.0：两票管理、安全检查模块、WebSocket 推送、角色权限拦截 |
| coal-transport-monitor | v2.0 | v3.0：GPS 轨迹接入；与 coal-yard 入场磅房直连；车辆人脸识别 |

---

## 十、设计哲学

1. **物理隔离 + 逻辑闭环** —— 每个系统独立部署、独立数据库、独立账户体系；通过共享密钥 + 标准 HTTP 接口跨系统协作，单点故障不会级联。任何一个子系统宕机，其他系统继续按本地数据正常运作，待恢复后由调度器/手动重推补齐。
2. **状态机驱动业务** —— 6 个系统共定义了 **15+ 套状态机**，所有跨系统调用都是状态机的边，每一次推进可审计、可回滚（pre/post 状态都落 `updated_at` + `audit_logs`）。
3. **编号即语义** —— `GYS-` / `HT-` / `PO-` / `IN-` / `OUT-` / `DQ-` / `DF-` / `WT-` / `OT-` / `YH-` / `EQ-` 等前缀让单据在任何系统间流转都能反查上下文，是去中心化系统中"主键"的替代品。
4. **双闭环监督** —— 物的流转闭环（采购→运输→化验→库存→燃用）+ 设备健康闭环（点检→缺陷→隐患→整改）；两条闭环在 **煤场配煤建议** 与 **#1/#2 机组检修计划** 处合流，覆盖发电厂日常 90% 的运营事件。
5. **WebSocket 不是装饰** —— 实时预警在 (i) 反舞弊（运输/化验异常）、(ii) 设备 CRITICAL 缺陷、(iii) 库存温度异常 三个场景下是核心 UX，不是噱头。
6. **失败降级优于级联熔断** —— 所有跨系统 HTTP 调用 `3s` 超时，失败不抛错，由对端调度器/前端按钮重推，避免任何一个子系统的网络抖动拖垮全链路。
7. **不引入业务无关的中间件** —— 不上 Kafka / RabbitMQ / Redis；6 个 SQLite/PostgreSQL 实例 + HTTPS 直连，业务逻辑全部在 FastAPI 层显式表达，便于工艺人员审计和接手。

---

## 仓库一览

| 子系统 | 仓库（PRIVATE） |
|---|---|
| 燃料采购 | https://github.com/nizuowanzhenbang/fuel-procurement |
| 运煤监督 | https://github.com/nizuowanzhenbang/coal-transport-monitor |
| 煤质化验 | https://github.com/nizuowanzhenbang/coal-quality-monitor |
| 煤场库存 | https://github.com/nizuowanzhenbang/coal-yard-management |
| 设备点检 | https://github.com/nizuowanzhenbang/equipment-inspection |
| 安全生产 | https://github.com/nizuowanzhenbang/plant-safety |
| **本仓库（总览）** | https://github.com/nizuowanzhenbang/smart-power-plant |

---

> 📌 本 README 是 6 个子系统的「外部观察者视角」总览说明书。各子系统内部的详细开发文档、API Reference、部署脚本均在各自仓库内。
