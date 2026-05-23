# 智慧发电厂全链路管理平台

> 一座燃煤电厂日常要管的事，被拆成 7 个独立的小系统，彼此之间用一套约定好的"暗号"互相打招呼，最终拼成一张完整的数字网。
>
> 这个仓库不放代码，只讲 **7 个系统之间怎么配合**。

---

## 一、它解决什么问题

一家燃煤电厂，每天都在做这几件事：

- 燃料部按计划买煤，跟供应商签合同、下订单；
- 货从港口装船或装车，半路要防止司机半路卸货换次煤；
- 车到厂门口，过磅、扫铅封、化验，看看是不是说好的那批；
- 化验合格的煤进煤场，分堆存放，按"先进先出"烧；
- 锅炉、汽轮机这些大家伙得有人天天巡检，发现毛病要修；
- 厂区里任何安全隐患都要登记、整改、复查。

- 烟囱口实时排着 SO₂/NOx/烟尘，超过国家限值要被环保部罚款甚至限电。

**问题来了**：这 7 件事过去分别由 7 个部门用 7 套表格/纸单子管，数据彼此不通。

- 一批煤从下订单到烧进锅炉，途中要换 5 次"档案"，谁也讲不全它的完整经历；
- 港口化验说热值 5500，厂里化验说热值 5200，谁动了手脚？查不出来；
- 点检发现一根管子要爆了，登记在巡检本上，安全员看不到，三天后真出事了；
- 订单上写 1000 吨，实际入库 950 吨，剩下 50 吨"蒸发"在路上，没人追。

**这套平台就是把这 6 件事用同一套数字流程串起来**：每一步都自动记录、跨系统的每一次"交接"都有迹可查、任何异常实时报警。

---

## 二、一批煤的完整旅程

整个平台只讲两条故事线。**第一条是"煤的故事"** —— 一批煤从下单到烧掉的全过程：

```
①下订单         ②运输上路        ③进厂化验         ④进煤场存放        ⑤出煤场烧锅炉
   │               │                │                  │                  │
   ▼               ▼                ▼                  ▼                  ▼
燃料采购  ──►  运煤监督  ──►   煤质化验   ──►   煤场库存   ──►    （生产工艺）
   │  ▲           │              │   │              │   ▲
   │  └───── 信用回写 ◄──────────┘   │              │   │
   │                                  │              │   │
   └───────────── 拉订单信息 ────────────────────────┘   │
                                                          │
   ◄────────────── 入场回执：又有 200 吨到货了 ─────────┘
```

**第二条是"设备健康的故事"** —— 锅炉、汽轮机这些大家伙怎么被照顾：

```
   日常巡检 ──► 发现毛病登记缺陷 ──► 紧急的毛病自动转成安全隐患 ──► 修好复查
       │              │                       │                       │
       ▼              ▼                       ▼                       ▼
   设备点检  ────► 设备点检  ────────►   安全生产管理   ─────►   设备点检
                                                                  （健康度回弹）
```

**两条线的交汇点**：煤场系统根据库存里每批煤的质量给出"今天该烧哪堆煤"的建议，而锅炉能不能正常烧，又取决于设备点检的健康度。**采购的煤要好，烧煤的设备要稳，这就是一座电厂日常运营的全部内核。**

**还有第三条线 ——"合规排放的故事"**：煤烧进锅炉后，尾气从烟囱排出之前要经过脱硫、脱硝、除尘三道关；CEMS 仪表 24 小时盯着 SO₂/NOx/烟尘，超过限值立刻告警、严重的事件还会自动建一条环保隐患给安全部门。**主线管"煤怎么进来、设备怎么扛"，第三条线管"烟怎么出去"——三条线合起来才是一座电厂完整的数字命脉。**

---

## 三、六个系统分别是什么

每个系统都是一个独立的小应用，可以单独上线、单独维护，跟其他系统通过 HTTP 接口打交道。

### 📦 [燃料采购管理 · fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement)

**做什么**：管供应商档案、签合同、下采购订单。一批煤的"出生证"就是这里开的。

**关键点**：合同里会写明这批煤应该是什么质量（热值、灰分、硫分、水分四个指标的上下限），这些数字后面会被煤场和化验系统拿去做对比依据。合同金额超过 100 万 / 500 万 要走多级审批；订单到货一点点累加，累计到 99% 自动结案。

<details>
<summary>📋 数据表与状态机详情</summary>

**7 张表**：`users`（账户，4 角色）/ `suppliers`（供应商，编号 GYS-NNNN）/ `fuel_contracts`（合同，编号 HT-YYYYMM-NNNN，含 `spec_calorific_value / spec_ash_max / spec_sulfur_max / spec_moisture_max` 四项煤质基准）/ `contract_approvals`（审批流水）/ `contract_price_history`（单价调整审计）/ `purchase_orders`（订单，编号 PO-YYYYMMDD-NNNN）/ `supplier_quality_scores`（来自化验系统的信用回写）

**三套状态机**：
- 供应商：`PENDING_REVIEW → ACTIVE → SUSPENDED / BLACKLISTED / ARCHIVED`
- 合同：`DRAFT → PENDING_APPROVAL → ACTIVE → COMPLETED / EXPIRED / TERMINATED`
- 订单：`PLANNED → DISPATCHED → PARTIAL_RECEIVED → RECEIVED → SETTLED`

**审批金额阈值**：`< 100 万`→1 级、`100–500 万`→2 级、`> 500 万`→3 级

**单价审计**：生效合同的单价调整必须走 `POST /contracts/{id}/adjust-price`，旧值写入 `contract_price_history`，不可直改字段
</details>

---

### 🚛 [运煤监督 · coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor)

**做什么**：盯着每一辆运煤车在路上有没有"动手脚"。

**怎么盯**：三个关键点 —— **重量**（出港和进厂分别过磅，差太多就报警）、**时间**（同样路线别人 6 小时，这车走了 12 小时，说明半路停过）、**铅封**（出港时贴的铅封二维码和进厂时的对不上，说明被撬开过）。

<details>
<summary>📋 三大分析器算法详情</summary>

**5 张表**：`users` / `vehicles`（车牌 + 皮重 + 司机）/ `transport_records`（运输主表，带 `batch_number` 关联化验）/ `seal_records`（铅封记录，DEPARTURE/ARRIVAL 两种）/ `alerts`

**算法**：
- **WeightAnalyzer**：3‰ 基础阈值 + Z-score 动态阈值（同车队同煤种近 30 天的统计学异常）
- **TimeAnalyzer**：IQR（四分位距）基准，识别异常滞留
- **SealAnalyzer**：QR 码用 Levenshtein 编辑距离比对相似度

**其他**：WebSocket 实时预警、CSV 导出（UTF-8 BOM）、ORM N+1 查询优化
</details>

---

### ⚗️ [煤质化验 · coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor)

**做什么**：每一批煤进厂时都要化验，把"港口化验结果"和"入厂化验结果"做对比。

**为什么重要**：六个核心指标（热值、灰分、硫分、水分、挥发分、固定碳）只要偏差超过阈值就说明"出港时是 A 货，进厂时变成 B 货"，要么是供应商作假，要么是运输途中被换。同时把每个供应商最近 20 批煤的表现打个分（0-100），回写给采购系统，下次签合同就有数据依据。

<details>
<summary>📋 8 种预警类型与评分算法</summary>

**6 张表**：`users` / `suppliers`（与采购系统按 name 软关联）/ `coal_batches`（批次主表，含 `batch_number` 关联运输、`order_no` 关联采购）/ `quality_tests`（化验明细，PORT/FACTORY 两种）/ `quality_alerts` / `audit_logs`

**8 种预警**：`CALORIFIC_SHORTAGE`（热值不足）/ `ASH_EXCESS`（灰分超标）/ `SULFUR_EXCESS`（硫分超标）/ `MOISTURE_EXCESS`（水分超标）/ `CONTRACT_CALORIFIC` / `CONTRACT_ASH` / `CONTRACT_SULFUR`（合同基准超标）/ `COMPREHENSIVE`（综合）

**供应商评分**：基于近 20 批次，加权 = 热值 40% + 灰硫水各 15% + 综合预警 15%

**核心可视化**：六维归一化雷达图 + WebSocket JWT 鉴权实时预警
</details>

---

### 🏭 [煤场库存 · coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management)

**做什么**：煤进厂后到底放在哪个堆区、放了多久、什么时候烧。

**关键点**：
- **先进先出（FIFO）**：早进的煤先烧，避免某堆煤放半年开始自燃；
- **库龄三色预警**：≤15 天绿色、15-30 天黄色、>30 天红色，红色批次优先消化；
- **温度监控**：每个堆都装温度传感器，超过 50/65/80℃ 三档预警（煤堆自燃前兆）；
- **配煤建议**：每批煤入场时都打一个综合分（热值高加分、灰硫水超标扣分、库龄长扣分），系统每天给"今天该先烧哪几堆"的建议；
- **大额出场审批**：一次性出 5000 吨以上必须主管批准才放行。

**它是整个套件的"中枢"**：入场时要同时找采购系统问订单详情、找化验系统问质量结果，入完场还要回头通知采购系统"又到货 200 吨"。

<details>
<summary>📋 7 张表 + FIFO 与配煤算法</summary>

**7 张表**：`users`（4 角色）/ `coal_yards`（堆区，编号 DQ-NNN）/ `stock_ins`（入场，IN-YYYYMMDD-NNNN，含 `remaining_quantity` 用于 FIFO）/ `stock_outs`（出场，OUT-YYYYMMDD-NNNN，含 `fifo_breakdown` JSON 扣减明细）/ `stocktakes`（盘点，PD-YYYYMMDD-NNN）/ `inventory_snapshots`（每日快照）/ `temperature_readings`（温度）

**FIFO 实现**：出场时按 `stock_ins.stocked_at ASC` 依次扣减 `remaining_quantity`，扣减路径写 JSON

**盘点缩放**：盘点审批通过后，按 `actual/book` 比例缩放所有 `remaining_quantity > 0` 的批次

**配煤评分** (`utils/coal_score.py`)：`热值基础分 + (灰/硫/水超标各扣分) + 库龄衰减`，Dashboard 按 `(评分 + 库龄权重)` 排序给建议
</details>

---

### 🔧 [设备点检与缺陷 · equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection)

**做什么**：发电厂里那些大设备（锅炉、汽轮机、发电机等 8 大类）的日常巡检、缺陷登记、维修工单。

**关键点**：
- **巡检路线**：师傅手机扫设备二维码，按测点录数据，发现异常一键拍照上报；
- **自动派生缺陷**：点检录入"严重异常" → 系统自动生成缺陷工单 → 按 SLA 计时（紧急 4 小时 / 重要 24 小时 / 一般 72 小时）；
- **两票管理**：动设备前要先开"工作票"（写清楚谁在哪干什么）、操作高压设备前开"操作票"（一步一步走清单）；
- **健康度评分**：每台设备一个 0-100 的健康分，出缺陷扣分、修好回弹；
- **CRITICAL 缺陷自动报安全**：紧急缺陷登记的瞬间，自动调用 plant-safety 建一个隐患单，避免漏报；
- **移动扫码 + 离线点检**：师傅在现场用手机扫码就能查/报，弱网/无网点检结果先入 IndexedDB，恢复后自动同步（PWA）；
- **两票电子签名**：工作票签发/许可/终结/归档、操作票审核/批准/每步执行都要再次输入密码生成 HMAC 签名，不可篡改 + 可验签；
- **备件采购闭环**：低库存自动建采购申请 → 主管审批 → 推送到 fuel-procurement → 到货回填库存。

<details>
<summary>📋 14 张表 + 调度器 + 预测性维护算法 + S3/Docker</summary>

**14 张表**：`users`（5 角色：ADMIN/INSPECTOR/REPAIRMAN/SUPERVISOR/VIEWER）/ `equipments`（8 系统 × 3 关键度 A/B/C）/ `inspection_routes` / `inspection_points` / `inspection_tasks` / `inspection_records` / `defects`（含 `safety_sync_status` / `safety_hazard_no` 联动字段）/ `work_tickets`（含 v3.0 `signatures` 签名链）/ `operation_tickets`（含 `signatures`）/ `operation_templates` / `spare_parts` / `stock_movements` / `audit_logs` / `purchase_requests`（v3.0）

**APScheduler 5 个定时任务**：超期缺陷扫描 / 漏检任务扫描 / 任务自动生成 / plant-safety 联动重试 / 备件低库存采购申请自动生成（每 12h）

**预测性维护算法**：`综合风险 = 缺陷数 30% + CRITICAL 率 25% + 异常率 15% + 健康度 20% + 等级状态加成`，sigmoid 平滑成失效概率

**WebSocket 事件**：`defect.critical_created` / `defect.overdue_swept` / `task.missed_swept` / `defect.safety_synced` / `defect.safety_sync_failed`

**移动端**：PWA（manifest + service worker v2） + `/m/scan` 路由用浏览器原生 `BarcodeDetector` 扫码 + 拍照上报 + IndexedDB 离线队列

**两票电子签名（v3.0）**：HMAC-SHA256(SECRET, `ticket_no|stage|user|ts`)，关键流转节点必须再次输入密码；`signatures` JSON 链可重算校验，`GET /{type}-tickets/{id}/signatures/verify` 一键验签

**对象存储（v3.0）**：`STORAGE_BACKEND=local|s3` 切换，S3 后端兼容 AWS / MinIO / 阿里云 OSS（boto3 sigv4），自动签发预签名 URL

**Docker Compose（v3.0）**：4 服务 backend(8003) + frontend(8080) + postgres16 + minio，一条命令拉起全栈

**QR 打印**：`segno` 生成 SVG，`/equipment-qr-print` 提供 A4 4 列网格批量打印页
</details>

---

### 🛡️ [安全生产管理 · plant-safety](https://github.com/nizuowanzhenbang/plant-safety)

**做什么**：厂区所有安全隐患的登记 → 整改 → 复查的闭环。

**两个来源**：
1. 巡查员主动登记（电气安全、消防、动火作业等 13 种风险类别）；
2. 设备点检系统自动推送（紧急缺陷转隐患）。

**整改时限**：重大隐患 14 天必须整改完，一般隐患 30 天，超期自动标红。整改完了需要复查人确认才算关闭。

<details>
<summary>📋 11 分区 + 13 类别 + 接收幂等</summary>

**2 张表**：`users` / `hazards`（隐患主表，编号 YH-YYYYMMDD-NNNN，含 `external_source / external_no` 幂等键）

**11 分区**：主厂房 / 锅炉区 / 汽轮机区 / 电气区 / 燃料区 / 化学水 / 除灰除渣 / 脱硫脱硝 / 冷却塔 / 开关站 / 办公区

**13 类别**：电气安全 / 锅炉压力容器 / 危险化学品 / 高处作业 / 有限空间 / 动火作业 / 起重作业 / 辐射防护 / 消防安全 / 机械伤害 / 环境排放 / 现场环境 / 其他

**接收映射**：从 equipment-inspection 推过来的缺陷，按设备编号前缀自动判分区（`-BL-`→锅炉、`-TB-`→汽轮机、`-EL-`→电气...），CRITICAL→MAJOR(14d)、其他→GENERAL(30d)

**幂等键**：`(external_source, external_no)` 唯一约束，同一缺陷重复推不会建出两条隐患
</details>

---

### 🌫️ [环保排放在线监测 · emission-monitoring](https://github.com/nizuowanzhenbang/emission-monitoring)

**做什么**：盯着烟囱里实时排出的 SO₂、NOx、烟尘三项指标，超过国家"超低排放"限值（35 / 50 / 10 mg/Nm³）立即告警，月底自动出合规报表。

**关键点**：
- **基准氧折算**：CEMS 直接测出来的浓度还不能用，要按公式 `C折 = C实测 × (21 - 6) / (21 - O2实测)` 折算到 6% 基准氧后才能跟限值比；
- **数据有效性**：仪表校准、故障、替代值会被自动标记不参与合规均值，CEMS 校准时入库自动转 `CALIBRATING`；
- **三档严重度**：达标 / 一般超标 / 严重超标（≥1.5×），持续 30 分钟以上自动升级；
- **告警闭环**：OPEN → 确认 → 处置 → 解决 → 监督员归档；超标过程的峰值、持续分钟、原因、整改措施一条不漏；
- **合规报表**：日 / 月 / 年三档，自动算每个排放口的均值/峰值/可用率/合规率，状态机 DRAFT → SUBMITTED → APPROVED → ARCHIVED；
- **与兄弟系统的伏笔（v2）**：严重告警自动推 plant-safety 建环保隐患；CEMS 故障自动推 equipment-inspection 建点检缺陷；coal-quality-monitor 检出入厂煤高硫时大屏预警 SO₂ 突升。

<details>
<summary>📋 7 张表 + 折算公式 + 严重度算法</summary>

**7 张表**：`users`（5 角色：ADMIN/OPERATOR/ANALYST/SUPERVISOR/VIEWER）/ `units`（机组，编号 `UNIT-N`，含容量 MW、4 种燃料、状态机）/ `emission_points`（排放口，编号 `EP-U{N}-NNN`，5 类：STACK / PRE_DESULFUR / POST_DESULFUR / PRE_DENOX / POST_DENOX，`is_compliance_point` 标记合规上报口）/ `cems_devices`（编号 `CEMS-NNNN`，4 状态 ONLINE / OFFLINE / CALIBRATING / FAULT）/ `emission_readings`（分钟级时序，实测+折算双列，`severity` + `validity` 入库时算好）/ `emission_alerts`（编号 `AL-YYYYMMDD-NNNN`，含 peak_so2/nox/dust + duration_minutes + 完整处置链路）/ `emission_standards`（标准库，超低/特别排放/一般火电三档）/ `emission_reports`（编号 `RPT-YYYYMM-NN`）

**核心算法**：
- **基准氧折算**（GB13223-2011）：`C折 = C实测 × (21 - 6) / (21 - O2实测)`，O2 ≥ 20.5 视为异常不折算
- **严重度判定**：超限 ≥1.5× 即 SEVERE；多指标取最大倍数
- **告警合并**：同点位若已有未结告警则合并（更新 peak / duration_minutes / indicators），否则新建；持续 ≥30 min 自动升级 ESCALATED；恢复达标自动写 ended_at

**Dashboard**：30 天合规率 + CEMS 可用率（合规线 95%）+ 24h 折算趋势 + 各排放口合规率柱图 + 告警等级/状态饼图 + 实时大屏（每个合规口最新值 + 限值红线）

**默认 seed**：5 用户 + 2 机组（300MW + 600MW）+ 6 排放口 + 6 CEMS + 48h × 5min 真实风格读数 + 2 段超标段（一般已关闭 + 严重处置中） + 1 月报草稿
</details>

---

## 四、7 个系统怎么互相对话

**核心思路**：每个系统都有自己独立的数据库，互不强连接（不设外键）。但大家约定好用 **同一套"业务编号"作为暗号**，需要数据时就用 HTTP 调用对方接口拉过来。

### 4.1 八个跨系统通用的"暗号"

这是最关键的设计 —— **同一批煤、同一台设备、同一张隐患单，在不同系统里都用同一个编号**。

| 暗号 | 长什么样 | 谁在用 | 用来串什么 |
|---|---|---|---|
| **订单号** | `PO-20260520-0001` | 采购 / 煤场 / 化验 | **一批煤的主线**：从合同到入库全程同一个号 |
| **供应商名** | 例：神华煤业 | 采购 / 化验 / 运煤 | **供应商画像**：算信用分、回写采购 |
| **批次号** | `B-20260520-001` | 运煤 / 化验 | **运输 ↔ 化验** 对应同一批货 |
| **合同号** | `HT-202605-0001` | 采购 / 煤场 | 入场单回填合同号，便于反查履约 |
| **缺陷号** | `DF-20260520-0001` | 设备点检 / 安全 | **缺陷 → 隐患** 的幂等键 |
| **隐患号** | `YH-20260520-0001` | 安全 → 设备点检 | 安全系统建好的隐患号反写到设备系统 |
| **设备号** | `EQ-BL-0001` | 设备点检 / 安全 | 设备号前缀（BL/TB/EL...）映射到隐患分区 |
| **堆区号** | `DQ-001` | 煤场 / 采购 | 入场回调时告诉采购"入了哪个堆" |

### 4.2 一次完整的入场流程是怎么联动的

举个最典型的例子 —— 当一辆运煤车开到煤场门口，要做入场登记时：

```
                    ┌──────────────────────────────────────────────┐
                    │  煤场操作员在系统里点"新建入场单"，输入订单号    │
                    └──────────────────────────────────────────────┘
                                          │
       ①拉订单详情                       ▼                  ②拉化验汇总
   ┌──────────────────┐                                  ┌──────────────────┐
   │ 调用采购系统:    │ ◄─────── 煤场系统 ────────► │ 调用化验系统:     │
   │ /order-info       │       同时发起两个调用       │ /order-quality-    │
   │ 拿回:             │                              │ summary           │
   │ 供应商/合同/      │                              │ 拿回:              │
   │ 合同煤质基准      │                              │ 港口vs入厂均值/    │
   │                  │                              │ 偏差结论           │
   └──────────────────┘                              └──────────────────┘
                                          │
                                          ▼
                              ┌──────────────────────┐
                              │  煤场系统落库 stock_ins  │
                              │  字段自动填好           │
                              └──────────────────────┘
                                          │
                              ③入场成功，回调一次     │
                                          ▼
                                  ┌──────────────────┐
                                  │ 调用采购系统:    │
                                  │ /yard-stocked     │
                                  │ 通知"又到 200 吨" │
                                  │ → 累计 delivered  │
                                  │ → 推进订单状态机  │
                                  └──────────────────┘
```

整个过程对操作员而言只是"点一下保存"，对系统而言完成了一次三方数据流转 + 状态机推进。**这就叫"逻辑闭环"**。

### 4.3 完整接口清单

<details>
<summary>📋 9 个跨系统接口的详细路径与鉴权</summary>

| # | 谁调谁 | 方法 | 路径 | 鉴权 | 用途 |
|---|---|---|---|---|---|
| 1 | 煤场 → 采购 | GET | `/api/integration/order-info?order_no=` | X-Integration-Token | 入场前拉订单详情 + 合同煤质基准 |
| 2 | 煤场 → 采购 | POST | `/api/integration/yard-stocked` | X-Integration-Token | 入场后回调，推进订单状态 |
| 3 | 煤场 → 化验 | GET | `/api/integration/order-quality-summary?order_no=` | X-Integration-Token | 入场前拉化验汇总 |
| 4 | 采购 → 化验 | GET | `/api/integration/supplier-credit?supplier_name=` | X-Integration-Token | 供应商详情页拉信用分 |
| 5 | 采购 → 化验 | GET | `/api/integration/order-quality?order_no=` | X-Integration-Token | 订单详情聚合化验明细 |
| 6 | 化验 → 采购 | POST | `/api/webhook/quality-score` | X-Integration-Token | 信用分变更回写 |
| 7 | 运煤 → 化验 | POST | `/api/integration/transport-event` | X-Integration-Secret | 运输完成事件 → 化验系统预警归集 |
| 8 | 设备 → 安全 | POST | `/api/integration/hazards` | X-Integration-Secret | CRITICAL 缺陷自动建隐患 |
| 9 | 设备 → 安全 | GET | `/api/integration/hazards/by-external/{source}/{external_no}` | X-Integration-Secret | 反查隐患状态 |

**统一约定**：所有跨系统响应都用 `{ code: 200, message, data }` 包壳；超时 3 秒；失败不抛错而是降级（局部功能缺失，由调度器/手动按钮重推）；幂等键防重复入账。

</details>

### 4.4 合同煤质基准是怎么"流"过去的

合同里写"这批煤热值不低于 5500 kcal/kg、灰分不高于 18%"，这几个数字在三个系统之间是**单向继承**的：

```
  fuel_contracts.spec_calorific_value (合同写好)
                  │
                  │ 通过 /order-info 接口携带
                  ▼
  煤场入场时拿到，用来跟化验值对比
  化验系统同时也存一份冗余 (coal_batches.contract_calorific_value)
                  │
                  ▼
  用于离线/历史偏差分析
```

**为什么要这么传？** 因为化验员不应该手动录入合同指标（容易抄错），合同基准在签合同时就定死，全链路只读取不修改。

---

## 五、技术栈

### 5.1 6 个系统共享的基线

| 层 | 选型 |
|---|---|
| 后端 | **FastAPI** + SQLAlchemy 2 + Pydantic 2 + JWT |
| 前端 | **React 18** + TypeScript + Vite + Ant Design 5 + ECharts + Zustand |
| 数据库 | SQLite（开发） / PostgreSQL（生产可平移） |
| 跨系统调用 | httpx + 共享密钥头 |

### 5.2 各系统独有的部分

| 系统 | 独有的东西 | 干什么用 |
|---|---|---|
| 运煤监督 | numpy + pandas + scikit-learn + websockets | 统计学算法识别异常 + 实时预警 |
| 煤质化验 | numpy + pandas + scikit-learn + websockets | 六维偏差 + 供应商评分 + 实时预警 |
| 煤场库存 | httpx（双下游集成）+ 自研评分模块 | 同时调采购和化验，给配煤建议 |
| 设备点检 | APScheduler + segno + WebSocket + PWA | 4 个定时任务 / 设备二维码 / 移动扫码 |
| 燃料采购 | 仅基线 | 业务纯度最高，重在状态机与审批流 |
| 安全生产 | 仅基线 | 纯接收方，重在状态机与幂等接收 |
| 环保排放 | 仅基线（v2 加 APScheduler + WebSocket） | CEMS 时序流 + 基准氧折算 + 合规报表 |

---

## 六、默认端口与账户

| 系统 | 后端 | 前端 | 默认账户 |
|---|---|---|---|
| [燃料采购](https://github.com/nizuowanzhenbang/fuel-procurement) | 8000 | 5173 | admin/buyer/approver/viewer（密码同名+123） |
| [煤场库存](https://github.com/nizuowanzhenbang/coal-yard-management) | 8001 | 5174 | admin/operator/supervisor/viewer |
| [煤质化验](https://github.com/nizuowanzhenbang/coal-quality-monitor) | 8002 | 5176 | admin/admin123 |
| [设备点检](https://github.com/nizuowanzhenbang/equipment-inspection) | 8003 | 5175 | admin/inspector/repairman/supervisor/viewer |
| [安全生产](https://github.com/nizuowanzhenbang/plant-safety) | 8004 | 5177 | admin/admin123 |
| [运煤监督](https://github.com/nizuowanzhenbang/coal-transport-monitor) | 8005 | 5178 | admin/admin123 |
| [环保排放](https://github.com/nizuowanzhenbang/emission-monitoring) | 8004 | 5176 | admin/operator/analyst/supervisor/viewer（密码同名+123） |

> 注意：环保排放 v1 暂用 8004/5176，与安全生产 / 煤质化验前端端口表面冲突。实际开发期同时启的人极少；生产部署建议统一在反代后规划，把上面 7 套端口全部唯一化。

---

## 七、怎么验证整个链路是通的

煤场系统仓库里有一个端到端冒烟脚本：

```bash
cd coal-yard-management/backend
python integration_smoke_test.py --run-yard
```

跑一次会自动验证：
1. 煤场调用采购拿到订单详情
2. 煤场调用化验拿到化验汇总
3. 写入入场单
4. 煤场回调采购通知到货，订单 `delivered_quantity` 累加，状态推进

设备点检 ↔ 安全生产的联动通过 `seed_data.py` 模拟四种状态（已同步 / 失败 / 等待 / 跳过），前端缺陷列表上能直接看到"隐患联动"状态，失败的可以一键重推。

---

## 八、迭代路线

| 系统 | 当前版本 | 下一步 |
|---|---|---|
| 燃料采购 | v2.1 | 招标比价、ERP 财务对接、合同电子签章 |
| 煤场库存 | v2.1 | 三方智能配煤升级、SCADA 实时取数、皮带秤直连 |
| 煤质化验 | v2.1 | 多港口化验机构接入、化验设备直连、LIMS 推送 |
| 设备点检 | v3.0 ✅ | 真 CA 签名、DCS 报警对接、移动语音录入、大模型运维问答 |
| 安全生产 | v1.1 | 两票管理、安全检查模块、WebSocket、角色权限 |
| 运煤监督 | v2.0 | GPS 轨迹接入、磅房直连、车辆人脸识别 |
| 环保排放 | v1.0 | APScheduler 月报、与 plant-safety / equipment-inspection 联动、WebSocket、DCS 直连 |

---

## 九、设计哲学

**1. 互相独立，逻辑闭环。** 每个系统单独一个数据库，任何一个挂了不影响其他系统继续工作。

**2. 编号即语义。** `PO-` 是订单、`HT-` 是合同、`IN-` 是入场、`DF-` 是缺陷……单据在哪个系统都能反查全部上下文。

**3. 状态机驱动业务。** 整套平台定义了 15+ 套状态机，跨系统调用就是状态机的"边"，每次推进可审计。

**4. 双闭环监督。** 物的流转闭环（采购→烧煤）+ 设备健康闭环（点检→隐患），覆盖电厂日常 90% 的事件。

**5. 失败降级优于级联熔断。** 所有跨系统 HTTP 调用 3 秒超时，失败不报错，由调度器或前端按钮重推，单点抖动不会拖垮全链路。

**6. 不引入业务无关的中间件。** 不上 Kafka / MQ / Redis，6 个数据库 + HTTPS 直连，业务逻辑全部在 FastAPI 显式表达，工艺人员能看懂、能接手。

---

## 仓库一览

| 子系统 | GitHub |
|---|---|
| 燃料采购 | https://github.com/nizuowanzhenbang/fuel-procurement |
| 运煤监督 | https://github.com/nizuowanzhenbang/coal-transport-monitor |
| 煤质化验 | https://github.com/nizuowanzhenbang/coal-quality-monitor |
| 煤场库存 | https://github.com/nizuowanzhenbang/coal-yard-management |
| 设备点检 | https://github.com/nizuowanzhenbang/equipment-inspection |
| 安全生产 | https://github.com/nizuowanzhenbang/plant-safety |
| 环保排放 | https://github.com/nizuowanzhenbang/emission-monitoring |
| 本仓库（总览） | https://github.com/nizuowanzhenbang/smart-power-plant |

> 这个 README 只讲整体设计。每个子系统的开发文档、API、部署脚本都在各自仓库里。
