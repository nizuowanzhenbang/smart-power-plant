# 一座火电厂的"数字孪生" · 智慧火电厂全链路管理平台

> 🏭 一家火电厂日常要管的事多得吓人：买煤/接管道气、运输、计量、化验、堆存、烧、巡设备、查隐患、盯排放——每件事过去都是一个部门一套 Excel，数据互不通。一批煤从下单到烧进锅炉途中要换 5 次"档案"，谁也讲不全它的完整经历；港口化验热值 5500、厂里复检只剩 5200，谁动过手脚根本查不出来；点检发现管子要爆了，写在巡检本上，安全员看不到，三天后真出事了。

**这套平台把火电厂的日常拆成两条产品线**：**燃煤线**（7 个子系统已上线 ✅）覆盖买煤运煤化验堆存烧煤的完整链路；**燃气线**（3 个子系统规划中 🚧）覆盖管道气计量、燃机性能、燃气环保。两条线共享"安全生产 / 设备点检 / 环保排放 / 物资采购"四个通用底座，再通过一套约定好的"暗号"（业务编号）把所有子系统串成一张完整的数字网——每个系统独立部署、独立数据库、互不强耦合，任意一个挂了别的不受影响。

> 📦 **本仓库只讲设计，不放代码**。子系统的开发文档 / API / 部署脚本都在各自仓库里。
>
> ⚠️ **免责声明**：本平台是 **厂内运营管理工具**，不能替代 ERP / 财务 / DCS / 国控点 CNEMC 联网等法定系统。

---

## ⚡ 30 秒看明白这套平台帮谁做什么

| 你是谁 | 它帮你做什么 |
|---|---|
| 🤝 燃料采购 | 供应商分级审批 / 合同煤质基准全链路继承 / 信用分实时打回采购页 |
| 🚛 运输调度 | 每辆运煤车的重量/时间/铅封三道关，盈亏吨当场报警 |
| 🧪 化验员 | 港口 vs 入厂 6 维偏差，3 项同时偏差自动盖"综合异常"章 |
| 🏭 煤场操作 | 入场自动拉订单+化验，FIFO 出场防老煤烂底，自燃温度三档监控 |
| 🔧 设备主管 | 上千台设备从巡到修全程留痕，CRITICAL 缺陷自动转安全隐患 |
| 🛡️ 安全员 | 隐患整改闭环，14/30 天超期自动飘红，复查留痕 |
| 🌫️ 环保员 | CEMS 数据按基准氧折算秒级告警，月底一键出合规报表 |
| 🏢 厂领导 | 7 个独立大屏 + 一座电厂日常运营的全部内核 |

---

## 🗺️ 火电厂双线总览

火电厂在中国发电结构中分两类，业务逻辑差异很大：

| 维度 | 燃煤电厂线 | 燃气电厂线 |
|---|---|---|
| **燃料形态** | 散装原煤（动力煤） | 管道天然气 / LNG |
| **燃料入厂** | 港口/车队运输 → 过磅 → 化验 | 计量站 → GC 色谱仪在线热值 → 直供燃机 |
| **典型机组** | 600MW / 1000MW 超（超）临界 | F 级 / H 级燃气-蒸汽联合循环 |
| **运行方式** | 带基荷为主，连续运行 | 调峰为主，启停频繁（一天 3-5 次） |
| **燃料存储** | 煤场堆区，库龄/自燃管控 | 无储气，管道直供 |
| **主控污染物** | SO₂ + NOx + 烟尘 | NOx 为主（几乎无 SO₂、无烟尘） |
| **基准氧** | 6%（GB13223 火电厂） | 15%（GB13223 燃气轮机条款） |
| **配套大件** | 锅炉 / 汽轮机 / 磨煤机 / 输煤皮带 / 脱硫塔 / 电除尘 | 燃机 / 余热锅炉 / SCR / 燃料模块 / 进气过滤 |

**两条线共享的"通用基础设施"**：

| 共享子系统 | 在燃煤线 | 在燃气线 |
|---|---|---|
| 🛡️ 安全生产 (plant-safety) | 直接复用 | 直接复用 |
| 🔧 设备点检 (equipment-inspection) | 设备模板：锅炉/汽轮机/磨煤机… | 设备模板切换：燃机/余热锅炉/燃料模块… |
| 🌫️ 环保排放 (emission-monitoring) | 基准氧 6%、三指标 | 参数库切换：基准氧 15%、NOx 单一主控 |
| 📦 物资采购审批 (fuel-procurement 框架) | 用于煤炭采购 | 框架复用，业务对象替换为天然气合同 |

**两条线各自特有的部分**：
- **燃煤独有**：运煤监督 / 煤场库存 / 煤质化验 / 配煤建议
- **燃气独有**：管道气计量 / 热值在线分析 / 燃机性能 / 启停寿命

---

# 第一部分：燃煤电厂线（v2.x · 7 子系统已上线 ✅）

## 🪨 燃煤厂日常的三条故事线

理解了这三条故事线，燃煤侧的整张数字网就理解了。

### 第一条：煤的旅程（从下单到烧进锅炉）

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

### 第二条：设备健康（巡检 → 缺陷 → 修复）

```
   日常巡检 ──► 发现毛病登记缺陷 ──► 紧急的毛病自动转成安全隐患 ──► 修好复查
       │              │                       │                       │
       ▼              ▼                       ▼                       ▼
   设备点检  ────► 设备点检  ────────►   安全生产管理   ─────►   设备点检
                                                                  （健康度回弹）
```

### 第三条：合规排放（从锅炉到烟囱）

```
   煤烧进锅炉 → 脱硫脱硝除尘三道关 → CEMS 24h 盯 SO₂/NOx/烟尘 → 超低限值告警闭环 → 月度合规报表
                                              │
                                              ▼（v2 规划）
                                  推 plant-safety 建环保隐患
```

> 💡 **三条线的交汇点**：煤场系统根据库存里每批煤的质量给出"今天该烧哪堆煤"的建议，锅炉能不能正常烧又取决于设备点检的健康度，最后烟囱排得清不清取决于环保系统的告警闭环。**采购的煤要好、烧煤的设备要稳、烟囱排得清——这就是一座燃煤电厂日常运营的全部内核。**

---

## 📦 燃煤线的七个子系统

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

## 🔗 7 个系统怎么互相对话

**核心思路**：每个系统都有自己独立的数据库，互不强连接（不设外键）。但大家约定好用 **同一套"业务编号"作为暗号**，需要数据时就用 HTTP 调用对方接口拉过来。

### 八个跨系统通用的"暗号"

> 💡 **同一批煤、同一台设备、同一张隐患单，在不同系统里都用同一个编号**。

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

### 一次完整的入场流程是怎么联动的

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

<details>
<summary>📋 9 个跨系统接口的完整清单与鉴权</summary>

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

### 合同煤质基准是怎么"流"过去的

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

> 💡 **为什么要这么传？** 化验员不应该手动录入合同指标（容易抄错），合同基准在签合同时就定死，全链路只读取不修改。

---

## 🛠️ 燃煤线的技术栈

### 7 个系统共享的基线

| 层 | 选型 |
|---|---|
| 后端 | **FastAPI** + SQLAlchemy 2 + Pydantic 2 + JWT |
| 前端 | **React 18** + TypeScript + Vite + Ant Design 5 + ECharts + Zustand |
| 数据库 | SQLite（开发）/ PostgreSQL（生产可平移） |
| 跨系统调用 | httpx + 共享密钥头 |

### 各系统独有的部分

| 系统 | 独有的东西 | 干什么用 |
|---|---|---|
| 运煤监督 | numpy + pandas + scikit-learn + websockets | 统计学算法识别异常 + 实时预警 |
| 煤质化验 | numpy + pandas + scikit-learn + websockets | 六维偏差 + 供应商评分 + 实时预警 |
| 煤场库存 | httpx（双下游集成）+ 自研评分模块 | 同时调采购和化验，给配煤建议 |
| 设备点检 | APScheduler + segno + WebSocket + PWA + boto3 | 5 个定时任务 / 设备二维码 / 移动扫码 / 对象存储 |
| 燃料采购 | 仅基线 | 业务纯度最高，重在状态机与审批流 |
| 安全生产 | 仅基线 | 纯接收方，重在状态机与幂等接收 |
| 环保排放 | 仅基线（v2 加 APScheduler + WebSocket） | CEMS 时序流 + 基准氧折算 + 合规报表 |

---

## 🔌 默认端口与账户

| 系统 | 后端 | 前端 | 默认账户 |
|---|---|---|---|
| [燃料采购](https://github.com/nizuowanzhenbang/fuel-procurement) | 8000 | 5173 | admin/buyer/approver/viewer（密码同名+123） |
| [煤场库存](https://github.com/nizuowanzhenbang/coal-yard-management) | 8001 | 5174 | admin/operator/supervisor/viewer |
| [煤质化验](https://github.com/nizuowanzhenbang/coal-quality-monitor) | 8002 | 5176 | admin/admin123 |
| [设备点检](https://github.com/nizuowanzhenbang/equipment-inspection) | 8003 | 5175 | admin/inspector/repairman/supervisor/viewer |
| [安全生产](https://github.com/nizuowanzhenbang/plant-safety) | 8004 | 5177 | admin/admin123 |
| [运煤监督](https://github.com/nizuowanzhenbang/coal-transport-monitor) | 8005 | 5178 | admin/admin123 |
| [环保排放](https://github.com/nizuowanzhenbang/emission-monitoring) | 8004 | 5176 | admin/operator/analyst/supervisor/viewer（密码同名+123） |

> 🔧 环保排放 v1 暂用 8004/5176，与安全生产/煤质化验前端端口表面冲突。实际开发期同时启的人极少；生产部署建议统一在反代后规划，把上面 7 套端口全部唯一化。

---

## 🧪 怎么验证整个链路是通的

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

## 🚧 燃煤线迭代路线

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

# 第二部分：燃气电厂线（v0.x · 建设中 🚧）

## 燃气厂的痛点跟燃煤完全不是一回事

> 🔥 燃气电厂虽然也是火电，但日常运营和燃煤完全不同：
> - 燃料不是用车拉来的，是从中石油/中石化的**管道直接接进来**；没有运输监督、没有堆场、没有库龄；
> - 上游气源可能在西气东输、俄气、进口 LNG 之间切换，**每种气热值不同**（30-38 MJ/Nm³ 不等），结算单价随热值浮动；
> - 燃机调峰能力强，**一天启停 3-5 次很常见**，启停次数和热冲击直接计入机组寿命；
> - 主控污染物是 **NOx**，几乎没有 SO₂、没有烟尘；脱硝靠 SCR + 干式低 NOx 燃烧器（DLN），参数和煤电完全两套；
> - 燃机制造商（GE / 三菱 / 西门子）的保修协议非常强势，**点检规程必须按 OEM 走**，否则失保。

**这一线的目标**：把燃气厂特化的业务（燃料计量、燃机性能、启停寿命、燃气环保）补齐，同时复用煤电线已建好的安全/点检/审批通用底座，**两条线共享一座"火电厂"品牌**。

---

## 📦 燃气线已落地的子系统

### ⛽ [燃料计量与气源管理 · gas-fuel-metering](https://github.com/nizuowanzhenbang/gas-fuel-metering) （v1.0 落地 ✅）

**做什么**：管理多路气源（中石油/中石化/LNG）的入厂计量、热值在线分析、与上游气源公司的结算对账。

**关键点**：
- **管道气计量**：多路计量站数据接入（流量计/压力变送器/温度变送器），按 GB/T 22634 做温压补偿，算标准状态体积（Nm³）；
- **热值在线分析**：GC 色谱仪每分钟更新组分和高位热值（MJ/Nm³），热值变化直接影响结算单价；
- **与上游对账**：拉中石油/中石化的日计量单、月结算单，跟厂内计量数据三方核对，差异超过 0.5% 自动告警；
- **管网监控**：进厂压力、流量异常告警（计量站压力降、流量突变、调压橇故障）；
- **能耗匹配**：把耗气量和燃机出力关联，算实时热效率（kJ/kWh），跟出厂保证值比对。

**业务编号**：`GAS-YYYYMMDD-NNNN` 计量批次、`SETTLE-YYYYMM-NN` 月结算单、`SRC-NNN` 气源（多路）

> 💡 **对应煤电线的位置**：相当于 coal-transport-monitor + coal-quality-monitor + 部分 fuel-procurement 三者合一——燃气没有"运输"和"入场化验"两个独立环节，统一在计量站完成。

### 🔥 燃机性能与启停管理 · gas-turbine-performance（规划中）

**做什么**：燃机机组性能监控、启停曲线管理、热部件寿命与保修评估。

**关键点**：燃机出力曲线 / 热耗率 / 排气温度（EGT）/ 压气机进口防冰状态 / 启停次数累计 / 热部件等效运行小时数 / 与 OEM 保修条款挂钩的维护节点提醒。

### 🌫️ 燃气环保监测 · gas-emission-monitoring（基于 emission-monitoring 改造）

**做什么**：从现有环保排放系统 fork 一份，切换参数库适配燃机。

**关键差异**：

| 项 | 燃煤 | 燃气 |
|---|---|---|
| 基准氧 | 6% | **15%**（折算公式 `C折 = C实测 × (21 - 15) / (21 - O2实测)`） |
| 主控指标 | SO₂ + NOx + 烟尘 | **NOx 单一**（燃气几乎不产生 SO₂ 和烟尘） |
| 超低排放限值 | SO₂ 35 / NOx 50 / 烟尘 10 mg/Nm³ | NOx ≤ **50 mg/Nm³** |

---

## 🔗 共享子系统在两条线之间怎么切

| 共享子系统 | 改造工作量 | 改造点 |
|---|---|---|
| plant-safety | 极小 | 11 分区改为"燃机区/余热锅炉区/燃料模块/SCR 区/CCR 控制室…"；13 类别基本保留 |
| equipment-inspection | 中等 | 8 大类设备模板换成"燃机/余热锅炉/燃料模块/SCR/DCS…"；流程（两票/缺陷/PWA 移动端）通用 |
| emission-monitoring | 较小 | 折算公式系数 + 限值表 + 默认 seed 切换；状态机、告警闭环、报表流程通用 |
| fuel-procurement | 较小 | 业务对象从"煤炭合同"换为"天然气合同/LNG 合同"；审批框架、状态机、合同煤质基准（变热值/组分基准）通用 |

## 🚧 燃气线迭代路线

| 子系统 | 当前状态 | 下一步 |
|---|---|---|
| [gas-fuel-metering](https://github.com/nizuowanzhenbang/gas-fuel-metering) | **v1.0 落地 ✅**（FastAPI + 9 路由 + APScheduler 4 类巡检 + React/AntD/ECharts 全栈 + Docker，97 测试） | v0.2 月对账闭环 + 跨系统联动 |
| gas-turbine-performance | 未启动 | 基于 gas-fuel-metering 的跨系统接口启动 |
| gas-emission-monitoring | 未启动 | 基于 emission-monitoring fork，参数库切换 |
| 共享适配（plant-safety / equipment-inspection） | 未启动 | 增加燃气厂参数库 / 模板库 |

---

## 🎨 设计哲学

> 1. **互相独立，逻辑闭环。** 每个系统单独一个数据库，任何一个挂了不影响其他系统继续工作。
>
> 2. **编号即语义。** `PO-` 是订单、`HT-` 是合同、`IN-` 是入场、`DF-` 是缺陷……单据在哪个系统都能反查全部上下文。
>
> 3. **状态机驱动业务。** 整套平台定义了 15+ 套状态机，跨系统调用就是状态机的"边"，每次推进可审计。
>
> 4. **三闭环监督。** 物的流转闭环（采购→烧煤）+ 设备健康闭环（点检→隐患）+ 合规排放闭环（CEMS→报表）。
>
> 5. **失败降级优于级联熔断。** 所有跨系统 HTTP 调用 3 秒超时，失败不报错，由调度器或前端按钮重推，单点抖动不会拖垮全链路。
>
> 6. **不引入业务无关的中间件。** 不上 Kafka / MQ / Redis，7 个数据库 + HTTPS 直连，业务逻辑全部在 FastAPI 显式表达，工艺人员能看懂、能接手。
>
> 7. **双线共享底座，业务库分线落地。** 安全/点检/环保/采购四个通用底座两线共用代码，靠参数库/模板库切换；燃料链各自独立，因为燃煤"散装"和燃气"管道"完全是两套实物管理逻辑。

---

## 📚 仓库一览

### 燃煤电厂线（v2.x ✅）

| 子系统 | GitHub |
|---|---|
| 燃料采购 | https://github.com/nizuowanzhenbang/fuel-procurement |
| 运煤监督 | https://github.com/nizuowanzhenbang/coal-transport-monitor |
| 煤质化验 | https://github.com/nizuowanzhenbang/coal-quality-monitor |
| 煤场库存 | https://github.com/nizuowanzhenbang/coal-yard-management |
| 设备点检 ★ | https://github.com/nizuowanzhenbang/equipment-inspection |
| 安全生产 ★ | https://github.com/nizuowanzhenbang/plant-safety |
| 环保排放 ★ | https://github.com/nizuowanzhenbang/emission-monitoring |

> ★ = 设计上**双线共享**，燃气电厂线将复用（参数库 / 模板库切换，详见上方"火电厂双线总览"）

### 燃气电厂线（v0.x 🚧）

| 子系统 | GitHub |
|---|---|
| 燃料计量与气源管理 | https://github.com/nizuowanzhenbang/gas-fuel-metering |
| 燃机性能与启停管理 | 规划中（gas-turbine-performance） |
| 燃气环保监测 | 规划中（gas-emission-monitoring，基于 emission-monitoring 改造） |

### 总览

| 仓库 | GitHub |
|---|---|
| 本仓库（双线总览） | https://github.com/nizuowanzhenbang/smart-power-plant |

## 📜 License

私有项目，未开源。
