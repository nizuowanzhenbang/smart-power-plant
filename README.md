# 一座燃煤电厂的"数字孪生" · 智慧燃煤电厂全链路管理平台

> 🏭 一家燃煤电厂日常要管的事多得吓人：买煤、运输、计量、化验、堆存、烧、巡设备、查隐患、盯排放、算煤耗——每件事过去都是一个部门一套 Excel，数据互不通。一批煤从下单到烧进锅炉途中要换 5 次"档案"，谁也讲不全它的完整经历；港口化验热值 5500、厂里复检只剩 5200，谁动过手脚根本查不出来；点检发现管子要爆了，写在巡检本上，安全员看不到，三天后真出事了；供电煤耗每多 1 克，一台 600MW 机组一年就多烧约 1500 吨标煤、多花 130 万、多排 4000 吨 CO₂——可没人能实时说清这 1 克到底丢在哪。

**这套平台把一座燃煤电厂的日常拆成 8 个互相独立、又能拼成一张网的子系统**：从买煤、运煤、化验、堆存，到烧煤的能效优化，再到横跨全厂的设备点检、安全生产、环保排放。每个系统独立部署、独立数据库、互不强耦合，任意一个挂了别的不受影响；它们靠一套约定好的"业务编号暗号"通过 HTTP 互相拉数据，把 8 套独立的库串成一座完整的数字电厂。

> 🎯 **这是一个面向"系统设计 / 后端架构 / 数据与算法"岗位的作品集仓库**。它的价值不在于能否上线某座真实电厂，而在于用一个**业务足够复杂、闭环足够完整**的场景，集中展示：微服务式解耦、领域建模与状态机、跨库最终一致性、幂等与失败降级、工程化（测试 / Docker / PWA 离线 / 对象存储 / 电子签名），以及把**反平衡能效、统计异常检测、AI 燃烧寻优**这些算法落进真实业务的能力。
>
> 📦 **本仓库只讲设计、不放代码**——8 个子系统各有独立仓库（开发文档 / API / 部署脚本都在那里）。本仓库是整张架构的"运作原理说明书"。

---

## 🧭 给面试官的 60 秒导览：这个项目想证明什么

如果你是面试官，下面这张表就是"我希望你深挖的点"。每一行都对应一个可以聊 10 分钟的技术话题，文中都有展开。

| 能力维度 | 在这个项目里怎么体现 | 可深挖的技术点 |
|---|---|---|
| **系统设计 / 服务拆分** | 把一座电厂拆成 8 个独立部署、独立库的子系统，按"业务边界"而非"技术分层"切 | 为什么这样拆、拆的代价、什么时候该合 |
| **领域建模 / 状态机** | 全平台 15+ 套显式状态机（订单 / 合同 / 隐患 / 缺陷 / 告警…），跨系统调用就是状态机的"边" | 状态机驱动业务、每次推进可审计 |
| **跨库一致性** | 8 个库无外键，靠"业务编号"作逻辑外键 + 幂等键 + 回调/调度补偿 | 最终一致 vs 强一致的取舍、幂等实现 |
| **容错 / 韧性** | 所有跨系统调用 3s 超时、失败降级不阻断主流程、调度器与手动按钮重推 | 为什么不上熔断器、降级 vs 级联失败 |
| **算法工程** | 反平衡锅炉效率、供电煤耗拆分、Z-score/IQR/Levenshtein 异常检测、AI 燃烧寻优（最小二乘 + 机理先验） | 选型理由、可解释性、冷启动退化策略 |
| **工程化深度** | pytest 全覆盖（单测+集成+调度+seed）、Docker Compose、PWA 离线点检、S3/MinIO 对象存储、HMAC 电子签名 | 测试隔离、签名链验签、离线队列同步 |
| **领域理解** | 贯穿全文的电厂业务知识（基准氧折算、库龄自燃、两票制度、供电煤耗 KPI…） | 证明能跟工艺人员对话、需求不悬空 |

> 💡 **一句话定位**：这不是 8 个 CRUD demo 的堆叠，而是**一套用业务编号串起来、用状态机驱动、用最终一致性容错的分布式业务系统**——只不过它的"业务"是一座燃煤电厂。

---

## ⚡ 30 秒看明白这套平台帮谁做什么

| 你是谁 | 它帮你做什么 |
|---|---|
| 🤝 燃料采购 | 供应商分级审批 / 合同煤质基准全链路继承 / 信用分实时打回采购页 |
| 🚛 运输调度 | 每辆运煤车的重量/时间/铅封三道关，盈亏吨当场报警 |
| 🧪 化验员 | 港口 vs 入厂 6 维偏差，3 项同时偏差自动盖"综合异常"章 |
| 🏭 煤场操作 | 入场自动拉订单+化验，FIFO 出场防老煤烂底，自燃温度三档监控 |
| 🔥 能效工程师 | 反平衡算清每克煤耗丢在哪，AI 给最优氧量建议，节煤减碳按月量化 |
| 🔧 设备主管 | 上千台设备从巡到修全程留痕，CRITICAL 缺陷自动转安全隐患 |
| 🛡️ 安全员 | 隐患整改闭环，14/30 天超期自动飘红，复查留痕 |
| 🌫️ 环保员 | CEMS 数据按基准氧折算秒级告警，月底一键出合规报表 |
| 🏢 厂领导 | 8 个独立大屏 + 一座燃煤电厂日常运营的全部内核 |

---

## 🪨 一座燃煤电厂的四条故事线

理解了这四条故事线，整张数字网就理解了。八个子系统所有的关联，都是为了把这四条线各自串成闭环。

| 故事线 | 一句话 | 涉及子系统 |
|---|---|---|
| ① **煤的物流** | 从下单到进煤场，一批煤途中换 5 次档案也不丢身份 | 采购 → 运煤 → 化验 → 煤场 |
| ② **煤的能效** | 煤烧进锅炉之后烧得值不值，每克煤耗拆到底 | 能效与燃烧优化 |
| ③ **设备的健康** | 巡检发现的隐患不靠人转抄，当场建单 | 设备点检 → 安全生产 |
| ④ **烟囱的排放** | CEMS 实时折算判超标，月底一键出合规报表 | 环保排放 |

### 第一条：煤的旅程（从下单到进煤场）

一批煤从供应商手里到煤场要经过 4 个系统，**任何两个相邻系统都有数据来往**：

| 阶段 | 主导系统 | 这一步要去问/通知哪个系统 | 怎么串得起来 |
|---|---|---|---|
| ①下订单 | 燃料采购 | （独立） | 生成 `订单号 PO-…`，记下 `合同煤质基准`（热值/灰/硫/水四项） |
| ②运输上路 | 运煤监督 | 每条运输记录带 `批次号` 供化验来拉 | 出港过磅、铅封；到厂前一直自走 |
| ③进厂化验 | 煤质化验 | **运煤系统**：按 `批次号` 关联港口/入厂两次化验 | 化验完算供应商评分，**回写采购系统**更新信用分 |
| ④进煤场存放 | 煤场库存 | 入场同时调 **采购** 拿订单详情 + 调 **化验** 拿化验汇总 | 入完成功**回调采购**："你这单又到了 200 吨" → 推进订单状态机 |

**关键回环**：化验 → 采购的"信用分回写"让供应商口碑可量化；煤场 → 采购的"入场回执"让订单 `delivered_quantity` 自动累加，到 99% 自动结案。

### 第二条：煤的能效（煤烧进锅炉之后）

煤进了锅炉，物流线就交棒给能效线——这一段决定了"同样一吨煤，能多发多少电"。

| 关注点 | 怎么做 |
|---|---|
| **算清煤耗** | 反平衡法（锅炉效率 = 100 − 各项热损失）→ 供电煤耗，对标理论极限 122.84 g/kWh |
| **耗差分析** | 把实际煤耗和基准煤耗的差，按灵敏度折算到氧量/排烟温度/飞灰含碳量等可控参数，告诉运行人员"这 3 克丢在哪" |
| **AI 燃烧寻优** | 用历史工况拟合"煤耗 = f(负荷, 氧量, 排烟温度, 飞灰含碳量)"，叠加机理先验，给当前负荷下的**最优氧量建议** |
| **节煤减碳量化** | 把优化前后的煤耗差换算成节煤吨数、省的钱、减的 CO₂，按日/月出报表——这是给厂领导汇报的"政绩" |
| **跨系统联动** | 拉化验系统的"入炉煤低位发热量"做输入；锅炉效率异常 → 推设备点检建缺陷；重大能耗事件 → 推安全生产备案 |

### 第三条：设备的健康（巡检 → 缺陷 → 修复）

只有两个系统在唱主角，但联动的瞬间最关键：

| 阶段 | 主导系统 | 跨系统联动 | 暗号 |
|---|---|---|---|
| 日常巡检 | 设备点检 | 无 | `EQ-XX-NNNN` 设备编号 |
| 录入缺陷 | 设备点检 | **CRITICAL 缺陷自动推到 plant-safety 建隐患** | `DF-…` 缺陷号 + `external_no` 幂等键 |
| 隐患整改 | 安全生产 | 自身闭环（巡查员/安全员/复查人三方留痕） | `YH-…` 隐患号 |
| 复查回弹 | 安全生产 → 设备点检 | 设备点检反查 `/hazards/by-external` 拿隐患状态，回到设备健康度评分 | 同上 |

**关键设计**：紧急缺陷**当场**就建出隐患单（而不是等人转抄），因为漏报一次就可能出事故。幂等键 `(external_source, external_no)` 保证就算调用重试也不会建两条隐患。

### 第四条：烟囱的合规排放

一个系统主唱，对外有两个联动伏笔：

| 阶段 | 主导系统 | 跨系统联动 |
|---|---|---|
| CEMS 实时取数 | 环保排放 | 无（直接对接现场分析仪） |
| 基准氧折算 + 限值判定 | 环保排放 | 严重超标 → 推 plant-safety 建环保隐患 |
| 告警闭环（5 阶段） | 环保排放 | CEMS 故障 → 推 equipment-inspection 建点检缺陷 |
| 月度合规报表 | 环保排放 | 煤质化验"入厂煤硫分异常"会在大屏预警 SO₂ 即将突升 |

> 💡 **四条线的交汇点**：采购的煤要好（物流线）、烧煤要烧得值（能效线）、烧煤的设备要稳（设备线）、烟囱排得清（排放线）——**这就是一座燃煤电厂日常运营的全部内核。**

---

## 📦 八个子系统

每个系统都是一个独立的小应用，可以单独上线、单独维护，跟其他系统通过 HTTP 接口打交道。

### 📦 [燃料采购管理 · fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement)

**做什么**：管供应商档案、签合同、下采购订单。一批煤的"出生证"就是这里开的。

**关键点**：合同里写明这批煤应该是什么质量（热值、灰分、硫分、水分四个指标的上下限），这些数字后面被煤场和化验系统拿去做对比依据。合同金额超过 100 万 / 500 万 要走多级审批；订单到货一点点累加，累计到 99% 自动结案。

<details>
<summary>📋 数据表与状态机详情</summary>

**7 张表**：`users`（4 角色）/ `suppliers`（GYS-NNNN）/ `fuel_contracts`（HT-YYYYMM-NNNN，含 `spec_calorific_value / spec_ash_max / spec_sulfur_max / spec_moisture_max` 四项煤质基准）/ `contract_approvals` / `contract_price_history` / `purchase_orders`（PO-YYYYMMDD-NNNN）/ `supplier_quality_scores`（化验系统信用回写）

**三套状态机**：
- 供应商：`PENDING_REVIEW → ACTIVE → SUSPENDED / BLACKLISTED / ARCHIVED`
- 合同：`DRAFT → PENDING_APPROVAL → ACTIVE → COMPLETED / EXPIRED / TERMINATED`
- 订单：`PLANNED → DISPATCHED → PARTIAL_RECEIVED → RECEIVED → SETTLED`

**审批金额阈值**：`< 100 万`→1 级、`100–500 万`→2 级、`> 500 万`→3 级。生效合同改单价必须走 `POST /contracts/{id}/adjust-price`，旧值写入审计表，不可直改字段。
</details>

---

### 🚛 [运煤监督 · coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor)

**做什么**：盯着每一辆运煤车在路上有没有"动手脚"。

**怎么盯**：三个关键点 —— **重量**（出港和进厂分别过磅，差太多就报警）、**时间**（同样路线别人 6 小时，这车走了 12 小时，说明半路停过）、**铅封**（出港时贴的铅封二维码和进厂时的对不上，说明被撬开过）。

<details>
<summary>📋 三大分析器算法详情</summary>

**5 张表**：`users` / `vehicles`（车牌+皮重+司机）/ `transport_records`（带 `batch_number` 关联化验）/ `seal_records`（DEPARTURE/ARRIVAL）/ `alerts`

**算法**：
- **WeightAnalyzer**：3‰ 基础阈值 + Z-score 动态阈值（同车队同煤种近 30 天的统计学异常）
- **TimeAnalyzer**：IQR（四分位距）基准，识别异常滞留
- **SealAnalyzer**：QR 码用 Levenshtein 编辑距离比对相似度

**其他**：WebSocket 实时预警、CSV 导出（UTF-8 BOM）、ORM N+1 查询优化
</details>

---

### ⚗️ [煤质化验 · coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor)

**做什么**：每一批煤进厂时都要化验，把"港口化验结果"和"入厂化验结果"做对比。

**为什么重要**：六个核心指标（热值、灰分、硫分、水分、挥发分、固定碳）只要偏差超阈值就说明"出港时是 A 货，进厂时变成 B 货"，要么供应商作假、要么运输途中被换。同时把每个供应商最近 20 批煤打个分（0-100）回写采购系统，下次签合同就有数据依据。

<details>
<summary>📋 8 种预警类型与评分算法</summary>

**6 张表**：`users` / `suppliers`（与采购系统按 name 软关联）/ `coal_batches`（含 `batch_number` 关联运输、`order_no` 关联采购）/ `quality_tests`（PORT/FACTORY）/ `quality_alerts` / `audit_logs`

**8 种预警**：热值不足 / 灰分超标 / 硫分超标 / 水分超标 / 合同热值·灰·硫基准超标 / 综合异常

**供应商评分**：基于近 20 批次，加权 = 热值 40% + 灰硫水各 15% + 综合预警 15%

**核心可视化**：六维归一化雷达图 + WebSocket JWT 鉴权实时预警
</details>

---

### 🏭 [煤场库存 · coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management)

**做什么**：煤进厂后到底放在哪个堆区、放了多久、什么时候烧。

**关键点**：
- **先进先出（FIFO）**：早进的煤先烧，避免某堆煤放半年开始自燃；
- **库龄三色预警**：≤15 天绿、15-30 天黄、>30 天红，红色批次优先消化；
- **温度监控**：每个堆装温度传感器，超 50/65/80℃ 三档预警（自燃前兆）；
- **配煤建议**：每批煤入场打综合分（热值高加分、灰硫水超标扣分、库龄长扣分），系统每天给"今天该先烧哪几堆"；
- **大额出场审批**：一次性出 5000 吨以上必须主管批准。

**它是煤物流线的"中枢"**：入场时同时找采购问订单、找化验问质量，入完场还要回头通知采购"又到货 200 吨"。

<details>
<summary>📋 7 张表 + FIFO 与配煤算法</summary>

**7 张表**：`users`（4 角色）/ `coal_yards`（DQ-NNN）/ `stock_ins`（IN-…，含 `remaining_quantity` 用于 FIFO）/ `stock_outs`（OUT-…，含 `fifo_breakdown` JSON 扣减明细）/ `stocktakes` / `inventory_snapshots`（每日快照）/ `temperature_readings`

**FIFO 实现**：出场时按 `stock_ins.stocked_at ASC` 依次扣减 `remaining_quantity`，扣减路径写 JSON。盘点审批通过后按 `actual/book` 比例缩放所有在库批次。

**配煤评分** (`utils/coal_score.py`)：`热值基础分 + (灰/硫/水超标各扣分) + 库龄衰减`，Dashboard 按 `(评分 + 库龄权重)` 排序给建议。
</details>

---

### 🔥 [机组能效与智能燃烧优化 · coal-unit-efficiency](https://github.com/nizuowanzhenbang/coal-unit-efficiency)

**做什么**：煤烧进锅炉之后，算清"这吨煤烧得值不值"——把供电煤耗拆到每一克，找出能耗丢在哪，并用 AI 给最优燃烧参数建议。这是整套平台**最贴近"节能降耗 + AI"** 的子系统。

**关键点**：
- **反平衡能效画像**：锅炉效率 η = 100 − (q2 排烟 + q3 化学不完全燃烧 + q4 机械不完全燃烧 + q5 散热 + q6 灰渣物理热)，参考 **GB 10184 / DL/T 904**；再算供电煤耗，对标理论极限 `122.84 = 3600/29307`；
- **耗差分析**：把"实际煤耗 − 基准煤耗"按灵敏度折算到各可控参数（氧量、排烟温度、飞灰含碳量…），区分 LOWER/HIGHER_BETTER 方向，瀑布图告诉运行人员每一克丢在哪；
- **AI 燃烧寻优**：用 numpy 最小二乘拟合"煤耗 = f(负荷, 氧量, 排烟温度, 飞灰含碳量)"，叠加机理先验（**最优氧量随负荷升高而降低**）；样本不足 8 条时退回纯机理先验，保证冷启动也能给建议；
- **节煤减碳量化**：优化前后煤耗差 → 节煤吨数 / 省的金额 / 减的 CO₂，日报月报直接给领导汇报；
- **跨系统联动**：拉 **化验** 的入炉煤低位发热量做输入；锅炉效率异常 → 推 **设备点检** 建缺陷；重大能耗事件 → 推 **安全生产** 备案。

<details>
<summary>📋 8 张表 + 算法层 + 调度器 + RBAC</summary>

**8 张表**：`users`（5 角色 ADMIN/OPERATOR/ENERGY_ENG/MANAGER/VIEWER）/ `coal_units`（机组 U-NN）/ `operating_snapshots`（工况快照）/ `efficiency_records` / `benchmark_targets`（分机组基准）/ `deviation_analyses` / `optimization_suggestions`（OPT-…）/ `energy_reports`（ER-…）/ `alerts`（AL-…）

**算法层** (`app/algorithms`)：
- `boiler_efficiency`：反平衡 η=100−(q2+q3+q4+q5+q6)
- `coal_consumption`：供电煤耗（理论极限 122.84，net = gross/(1−厂用电率)）
- `deviation`：耗差灵敏度折算（按指标的"越低越好/越高越好"方向）
- `combustion_optimizer`：最小二乘拟合 + 机理先验，样本 <8 退回先验

**APScheduler 3 类**：`efficiency_calc`（1min 补算未处理快照）/ `deviation_scan`（5min 耗差+告警）/ `daily_report`（每日 01:00）；内部 `_xxx(db)` 与 `*_job()` 分离便于单测。

**seed**：5 用户 + 3 机组（600MW 亚临界故意亚健康触发告警 / 660MW 超临界 / 1000MW 超超临界）+ 72 条 24h 工况 + AI 建议 + 日报。**108 pytest 全过**（算法单测 + 路由集成 + 调度作业 + seed，conftest 独立 sqlite + autouse 隔离）。
</details>

---

### 🔧 [设备点检与缺陷 · equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection)

**做什么**：发电厂里那些大设备（锅炉、汽轮机、发电机等 8 大类）的日常巡检、缺陷登记、维修工单。

**关键点**：
- **自动派生缺陷**：点检录入"严重异常" → 自动生成缺陷工单 → 按 SLA 计时（紧急 4h / 重要 24h / 一般 72h）；
- **两票管理**：动设备前先开"工作票"、操作高压设备前开"操作票"；
- **健康度评分**：每台设备一个 0-100 健康分，出缺陷扣分、修好回弹；
- **CRITICAL 缺陷自动报安全**：紧急缺陷登记瞬间自动调 plant-safety 建隐患，避免漏报；
- **移动扫码 + 离线点检**：手机扫码查/报，弱网/无网先入 IndexedDB，恢复后自动同步（PWA）；
- **两票电子签名**：关键流转节点再次输密码生成 HMAC 签名，不可篡改 + 可验签；
- **备件采购闭环**：低库存自动建采购申请 → 主管审批 → 推 fuel-procurement → 到货回填。

<details>
<summary>📋 14 张表 + 调度器 + 预测性维护算法 + S3/Docker</summary>

**14 张表**：`users`（5 角色）/ `equipments`（8 系统 × 3 关键度）/ `inspection_routes` / `inspection_points` / `inspection_tasks` / `inspection_records` / `defects`（含 `safety_sync_status / safety_hazard_no` 联动字段）/ `work_tickets`（含 `signatures` 签名链）/ `operation_tickets` / `operation_templates` / `spare_parts` / `stock_movements` / `audit_logs` / `purchase_requests`

**APScheduler 5 个定时任务**：超期缺陷扫描 / 漏检扫描 / 任务自动生成 / plant-safety 联动重试 / 备件低库存采购申请（每 12h）

**预测性维护算法**：`综合风险 = 缺陷数 30% + CRITICAL 率 25% + 异常率 15% + 健康度 20% + 等级状态加成`，sigmoid 平滑成失效概率

**两票电子签名**：HMAC-SHA256(SECRET, `ticket_no|stage|user|ts`)，`signatures` JSON 链可重算校验，`GET /{type}-tickets/{id}/signatures/verify` 一键验签

**对象存储**：`STORAGE_BACKEND=local|s3` 切换，兼容 AWS / MinIO / 阿里云 OSS（boto3 sigv4），自动签发预签名 URL

**Docker Compose**：backend(8003) + frontend(8080) + postgres16 + minio，一条命令拉起全栈
</details>

---

### 🛡️ [安全生产管理 · plant-safety](https://github.com/nizuowanzhenbang/plant-safety)

**做什么**：厂区所有安全隐患的登记 → 整改 → 复查闭环。

**两个来源**：① 巡查员主动登记（13 种风险类别）；② 设备点检/能效系统自动推送。重大隐患 14 天必须整改完、一般隐患 30 天，超期自动标红；整改完需复查人确认才关闭。

<details>
<summary>📋 11 分区 + 13 类别 + 接收幂等</summary>

**2 张表**：`users` / `hazards`（YH-…，含 `external_source / external_no` 幂等键）

**接收映射**：从 equipment-inspection 推来的缺陷按设备编号前缀自动判分区（`-BL-`→锅炉、`-TB-`→汽轮机、`-EL-`→电气…），CRITICAL→MAJOR(14d)、其他→GENERAL(30d)。

**幂等键**：`(external_source, external_no)` 唯一约束，同一缺陷重复推不会建两条隐患。
</details>

---

### 🌫️ [环保排放在线监测 · emission-monitoring](https://github.com/nizuowanzhenbang/emission-monitoring)

**做什么**：盯着烟囱里实时排出的 SO₂、NOx、烟尘三项，超过国家"超低排放"限值（35 / 50 / 10 mg/Nm³）立即告警，月底自动出合规报表。

**关键点**：
- **基准氧折算**：CEMS 实测浓度要按 `C折 = C实测 × (21 - 6) / (21 - O2实测)` 折算到 6% 基准氧后才能跟限值比；
- **数据有效性**：校准/故障/替代值自动标记不参与合规均值；
- **三档严重度**：达标 / 一般超标 / 严重超标（≥1.5×），持续 30 分钟自动升级；
- **告警闭环**：OPEN → 确认 → 处置 → 解决 → 归档；
- **合规报表**：日/月/年三档，DRAFT → SUBMITTED → APPROVED → ARCHIVED；
- **对外伏笔**：严重告警 → plant-safety 建环保隐患；CEMS 故障 → equipment-inspection 建缺陷。

<details>
<summary>📋 7 张表 + 折算公式 + 严重度算法</summary>

**7 张表**：`users`（5 角色）/ `units`（机组，4 种燃料、状态机）/ `emission_points`（排放口，5 类，`is_compliance_point` 标记合规上报口）/ `cems_devices`（4 状态 ONLINE/OFFLINE/CALIBRATING/FAULT）/ `emission_readings`（分钟级时序，实测+折算双列）/ `emission_alerts`（含 peak + duration_minutes + 完整处置链路）/ `emission_standards`（超低/特别/一般火电三档）/ `emission_reports`

**核心算法**：基准氧折算（GB13223-2011，O2 ≥ 20.5 视为异常不折算）；超限 ≥1.5× 即 SEVERE；同点位未结告警自动合并、持续 ≥30min 升级 ESCALATED、恢复达标自动写 ended_at。
</details>

---

## 🔗 八个系统怎么互相对话

**核心思路**：每个系统都有自己独立的数据库，互不强连接（不设外键）。但大家约定好用 **同一套"业务编号"作为暗号**，需要数据时就用 HTTP 调用对方接口拉过来。

### 第一步：先看每个系统的"邻居"

下面这张"通讯录"——你可以反查任意两个系统之间到底有没有数据来往、是谁主动找谁。

| 系统 | 主动调用谁（出库） | 被谁调用（入库） |
|---|---|---|
| 燃料采购 fuel-procurement | — | ← 煤场（订单详情）/ ← 煤场（入场回调）/ ← 化验（信用分回写） |
| 运煤监督 coal-transport-monitor | → 化验（运输完成事件） | — |
| 煤质化验 coal-quality-monitor | → 采购（信用分回写） | ← 运煤 / ← 采购（拉化验汇总）/ ← 煤场 / ← 能效（拉入炉煤热值） |
| 煤场库存 coal-yard-management | → 采购（拉订单/回调入场）/ → 化验（拉化验汇总） | — |
| 能效与燃烧优化 coal-unit-efficiency | → 化验（拉入炉煤热值）/ → 设备点检（锅炉效率异常建缺陷）/ → 安全（重大能耗事件备案） | — |
| 设备点检 equipment-inspection | → 安全（CRITICAL 缺陷建隐患）/ → 安全（反查隐患状态）/ → 采购（备件采购申请） | ← 能效（锅炉效率异常建缺陷） |
| 安全生产 plant-safety | — | ← 设备点检 / ← 能效（重大能耗事件） |
| 环保排放 emission-monitoring | （规划）→ 安全 / → 设备点检 | — |

> 💡 一眼看出哪个系统最"中心"：**煤场库存**（同时拉采购和化验）和**设备点检**（既推安全又被能效推）是两个枢纽；**安全生产**是最纯粹的接收方（设备 + 能效都往它这里送）。

### 第二步：跨系统通用的"暗号"

> **同一批煤、同一台设备、同一张隐患单、同一台机组，在不同系统里都用同一个编号**——这是 8 套独立数据库能拼成一张网的根本。

| 暗号 | 长什么样 | 谁在用 | 用来串什么 |
|---|---|---|---|
| **订单号** | `PO-20260520-0001` | 采购 / 煤场 / 化验 | 一批煤的主线：从合同到入库全程同一个号 |
| **供应商名** | 例：神华煤业 | 采购 / 化验 / 运煤 | 供应商画像：算信用分、回写采购 |
| **批次号** | `B-20260520-001` | 运煤 / 化验 | 运输 ↔ 化验 对应同一批货 |
| **合同号** | `HT-202605-0001` | 采购 / 煤场 | 入场单回填合同号，便于反查履约 |
| **机组号** | `U-01` | 能效 / 化验 | 入炉煤热值、能效画像按机组归集 |
| **缺陷号** | `DF-20260520-0001` | 设备点检 / 安全 / 能效 | 缺陷 → 隐患 的幂等键 |
| **隐患号** | `YH-20260520-0001` | 安全 → 设备点检 | 安全系统建好的隐患号反写到设备系统 |
| **设备号** | `EQ-BL-0001` | 设备点检 / 安全 | 设备号前缀（BL/TB/EL…）映射到隐患分区 |
| **堆区号** | `DQ-001` | 煤场 / 采购 | 入场回调时告诉采购"入了哪个堆" |

### 第三步：跟一次最典型的"入场登记"，看 3 个系统怎么联动

一辆运煤车开到煤场门口，操作员点"新建入场单"输入订单号回车——这一秒钟系统做了 4 件事：

1. **煤场 → 采购**：调 `/order-info?order_no=PO-…`，拿回供应商名、合同号、合同煤质基准。
2. **煤场 → 化验**（与上一步并行）：调 `/order-quality-summary`，拿回港口 vs 入厂两次化验的均值和偏差结论。
3. **煤场**自己：落库 `stock_ins`，自动填好供应商、合同基准、化验偏差——操作员不用手抄。
4. **煤场 → 采购**：成功后再调 `/yard-stocked`，告诉采购"又到了 200 吨"，采购的 `delivered_quantity` 累加，订单状态可能从 `PARTIAL_RECEIVED` 推进到 `RECEIVED`。

> 💡 **操作员的体验只是"点一下保存"**，但系统层完成了一次三方数据流转 + 一个状态机推进。任意一步失败（如化验系统暂时挂了）都不阻断入场——3 秒超时降级，事后由按钮重推。

<details>
<summary>📋 12 个跨系统接口的完整清单与鉴权</summary>

| # | 谁调谁 | 方法 | 路径 | 鉴权 | 用途 |
|---|---|---|---|---|---|
| 1 | 煤场 → 采购 | GET | `/api/integration/order-info?order_no=` | X-Integration-Token | 入场前拉订单详情 + 合同煤质基准 |
| 2 | 煤场 → 采购 | POST | `/api/integration/yard-stocked` | X-Integration-Token | 入场后回调，推进订单状态 |
| 3 | 煤场 → 化验 | GET | `/api/integration/order-quality-summary?order_no=` | X-Integration-Token | 入场前拉化验汇总 |
| 4 | 采购 → 化验 | GET | `/api/integration/supplier-credit?supplier_name=` | X-Integration-Token | 供应商详情页拉信用分 |
| 5 | 采购 → 化验 | GET | `/api/integration/order-quality?order_no=` | X-Integration-Token | 订单详情聚合化验明细 |
| 6 | 化验 → 采购 | POST | `/api/webhook/quality-score` | X-Integration-Token | 信用分变更回写 |
| 7 | 运煤 → 化验 | POST | `/api/integration/transport-event` | X-Integration-Secret | 运输完成事件 → 化验预警归集 |
| 8 | 设备 → 安全 | POST | `/api/integration/hazards` | X-Integration-Secret | CRITICAL 缺陷自动建隐患 |
| 9 | 设备 → 安全 | GET | `/api/integration/hazards/by-external/{source}/{external_no}` | X-Integration-Secret | 反查隐患状态 |
| 10 | 能效 → 化验 | GET | `/api/integration/coal-lhv?unit=` | X-Integration-Secret | 拉入炉煤低位发热量做能效输入 |
| 11 | 能效 → 设备 | POST | `/api/integration/defects` | X-Integration-Secret | 锅炉效率异常自动建缺陷 |
| 12 | 能效 → 安全 | POST | `/api/integration/hazards` | X-Integration-Secret | 重大能耗事件自动备案 |

**统一约定**：所有跨系统响应都用 `{ code: 200, message, data }` 包壳；超时 3 秒；失败不抛错而是降级（局部功能缺失，由调度器/手动按钮重推）；幂等键防重复入账。
</details>

---

## 🧠 面试高频问答（架构决策自问自答）

> 这一节专门预答面试官最可能追问的问题。每一问都是一次"为什么这样设计、代价是什么、什么时候会换方案"的取舍说明——这正是评委想听的。

<details>
<summary><b>Q1：为什么拆成 8 个独立系统，而不是一个大单体？</b></summary>

**按业务边界拆，不是按技术分层拆。** 一座电厂现实里就是"一个部门一套系统"：采购科、运行部、化验室、煤场、设备部、安环部各管各的。拆分后每个子系统能**独立部署、独立迭代、故障隔离**（化验系统挂了不影响煤照样入场），也方便不同人/小组并行开发。

**代价我也清楚**：跨系统一致性要自己在应用层兜（没有数据库外键和本地事务兜底了），调试要跨服务。所以拆分的前提是**业务边界清晰、跨边界交互少而明确**——本平台子系统之间最多 2 跳调用，正好落在"拆了划算"的区间。如果交互密到要分布式事务，那反而该合。
</details>

<details>
<summary><b>Q2：8 个库都没有外键，跨库数据一致性怎么保证？</b></summary>

**用"业务编号"当逻辑外键 + 最终一致，而不是强一致。** 同一批煤在采购/煤场/化验三个库里都用 `PO-…` 订单号；要别人的数据就 HTTP 实时拉，不冗余存（或只读冗余）。写操作（如入场回写采购的 `delivered_quantity`）走**回调 + 幂等键**，失败由调度器补偿重推，最终一致。

**为什么敢用最终一致**：业务能容忍秒级延迟——煤已经物理入场了，回写采购晚 3 秒、甚至挂掉等下次重推，都不影响现场。把"强一致"的成本花在不需要它的地方才是过度设计。
</details>

<details>
<summary><b>Q3：跨系统 HTTP 调用失败了怎么办？不会雪崩吗？</b></summary>

**失败降级，而不是级联熔断。** 所有跨系统调用统一 **3 秒超时**；失败不抛错，而是**局部功能缺失**——比如入场时拉不到化验汇总，那一栏就空着，入场照常完成，事后由调度器/前端按钮重推。

**为什么没上 Hystrix 那种熔断器**：调用链很浅（最多 2 跳），不存在长链路放大；真正的韧性来自"主流程不依赖旁路调用的成功"这个设计，而不是熔断中间件。幂等键保证重推安全，所以"超时即重试"是安全的。
</details>

<details>
<summary><b>Q4：幂等具体怎么实现的？</b></summary>

**唯一约束 + 命中即返回已有记录。** 以"设备缺陷 → 安全隐患"为例：隐患表上有 `(external_source, external_no)` 唯一约束。设备系统重推同一个缺陷号时，安全系统插入命中约束冲突，就直接返回那条已存在的隐患，而不是报错或建第二条。这样"超时重试""调度器补偿""人工重推"三条路径都天然安全。
</details>

<details>
<summary><b>Q5：为什么不上 Kafka / Redis / 服务网格？</b></summary>

**规模不需要，且运维方是工艺人员。** 电厂级数据量（一天几千条入场、分钟级 CEMS 读数）单机 PostgreSQL 绰绰有余；引入 MQ/缓存/网格会让本来工艺人员能看懂的"一次 HTTP 调用 = 一次业务动作"变成黑盒，接手成本陡增。

**但我能讲清什么时候该上**：如果跨系统是高频广播（一份事件 N 个消费者）、或要削峰填谷、或要严格的发布订阅解耦，就该上 MQ；如果同一份热数据被高频读，才上缓存。当前都不满足，所以"不引入业务无关中间件"是**有意识的克制**，不是不会用。
</details>

<details>
<summary><b>Q6：AI 燃烧寻优是真 AI 还是规则？冷启动怎么办？</b></summary>

**是"轻量数据驱动 + 机理先验"的混合模型，我不夸大成深度学习。** 核心是用 numpy 最小二乘拟合"煤耗 = f(负荷, 氧量, 排烟温度, 飞灰含碳量)"，在当前负荷下求让煤耗最低的氧量。叠加一条机理先验——**最优氧量随负荷升高而降低**——既约束解的合理性，也解决**冷启动**：当历史样本不足 8 条时，直接退回纯机理先验给建议，不会因为"没数据"而瘫痪。

**为什么不一上来就深度学习**：样本少、要可解释（运行人员得能问"凭什么让我降氧量"）、要能跟机理对得上。演进路线也想清了：数据攒够后接 MLflow 做在线训练、分负荷段建模。
</details>

<details>
<summary><b>Q7：锅炉效率为什么用反平衡法？</b></summary>

**正平衡测不准入炉燃料量，反平衡是行业标准。** 直接称"烧了多少煤、发了多少热"（正平衡）在现场误差大；反平衡是 `η = 100 − 各项热损失(q2 排烟 + q3 化学 + q4 机械 + q5 散热 + q6 灰渣)`，每项损失都有可测的现场参数支撑，符合 GB 10184 / DL/T 904。再由锅炉效率推供电煤耗，对标理论极限 122.84 g/kWh，把差距拆成可控参数——这就是耗差分析。
</details>

<details>
<summary><b>Q8：运煤防作弊的三个统计算法为什么这么选？</b></summary>

**每个异常的分布特性不同，算法就不同，而且都要可解释：**
- **重量用 Z-score**：同车队、同煤种的盈亏吨近似正态，Z-score 能给出"偏离几个标准差"这种能跟监管解释的量；
- **滞留时间用 IQR**：路途时间长尾、有离群，四分位距比均值±标准差更抗离群；
- **铅封用 Levenshtein 编辑距离**：二维码 OCR 会有零星字符误读，编辑距离能容忍 1-2 字符差异，避免把"识别误差"误判成"被撬开"。

**为什么不用深度学习**：样本少、要可解释、阈值要能跟监管和司机当面说清楚。可解释性在这个场景比精度更重要。
</details>

<details>
<summary><b>Q9：两票电子签名怎么防篡改？离线点检怎么同步？</b></summary>

**签名**：每个关键流转节点（工作票签发/许可/终结、操作票每步执行）都要再次输密码，生成 `HMAC-SHA256(SECRET, ticket_no|stage|user|ts)`，串成 `signatures` JSON 链。任何字段被改，重算 HMAC 就对不上，`/signatures/verify` 一键验签。

**离线**：现场弱网/无网很常见，点检端是 PWA（manifest + service worker），扫码上报的数据先进 **IndexedDB 队列**，网络恢复后自动重放同步。保证师傅在锅炉房没信号也能正常点检。
</details>

<details>
<summary><b>Q10：工程质量怎么保证的？</b></summary>

**每个子系统都有 pytest 全覆盖**，分四层：算法单测（反平衡/耗差/异常检测纯函数）、路由集成测试（带角色令牌）、调度作业测试（内部 `_xxx(db)` 与 `*_job()` 分离，可单独喂测试库）、seed 数据测试。conftest 用独立 sqlite + autouse 的 drop/create 做**每用例隔离**。例如能效系统 108 个用例全过、设备点检多角色 RBAC 全覆盖。Docker Compose 一键拉起全栈做端到端冒烟。
</details>

---

## 🛠️ 技术栈

### 8 个系统共享的基线

| 层 | 选型 |
|---|---|
| 后端 | **FastAPI** + SQLAlchemy 2 + Pydantic 2 + JWT/RBAC |
| 前端 | **React 18** + TypeScript + Vite + Ant Design 5 + ECharts + Zustand |
| 数据库 | SQLite（开发）/ PostgreSQL（生产可平移） |
| 跨系统调用 | httpx + 共享密钥头 |
| 部署 | Docker / Docker Compose |

### 各系统独有的"加分项"

| 系统 | 独有的东西 | 干什么用 |
|---|---|---|
| 运煤监督 | numpy + pandas + scikit-learn + websockets | 统计学异常检测 + 实时预警 |
| 煤质化验 | numpy + pandas + scikit-learn + websockets | 六维偏差 + 供应商评分 + 实时预警 |
| 煤场库存 | httpx（双下游集成）+ 自研评分模块 | 同时调采购和化验，给配煤建议 |
| 能效优化 | numpy（最小二乘）+ APScheduler + 反平衡/耗差/寻优算法 | 反平衡能效 + AI 燃烧寻优 + 节煤减碳量化 |
| 设备点检 | APScheduler + segno + WebSocket + PWA + boto3 | 定时任务 / 设备二维码 / 移动扫码离线 / 对象存储 |
| 燃料采购 | 仅基线 | 业务纯度最高，重在状态机与审批流 |
| 安全生产 | 仅基线 | 纯接收方，重在状态机与幂等接收 |
| 环保排放 | 仅基线（+ APScheduler + WebSocket） | CEMS 时序流 + 基准氧折算 + 合规报表 |

---

## 🔌 默认端口与账户

| 系统 | 后端 | 前端 | 默认账户 |
|---|---|---|---|
| [燃料采购](https://github.com/nizuowanzhenbang/fuel-procurement) | 8000 | 5173 | admin/buyer/approver/viewer（密码同名+123） |
| [煤场库存](https://github.com/nizuowanzhenbang/coal-yard-management) | 8001 | 5174 | admin/operator/supervisor/viewer |
| [煤质化验](https://github.com/nizuowanzhenbang/coal-quality-monitor) | 8002 | 5176 | admin/admin123 |
| [设备点检](https://github.com/nizuowanzhenbang/equipment-inspection) | 8003 | 8080 | admin/inspector/repairman/supervisor/viewer |
| [安全生产](https://github.com/nizuowanzhenbang/plant-safety) | 8004 | 5177 | admin/admin123 |
| [运煤监督](https://github.com/nizuowanzhenbang/coal-transport-monitor) | 8005 | 5178 | admin/admin123 |
| [环保排放](https://github.com/nizuowanzhenbang/emission-monitoring) | 8004 | 5176 | admin/operator/analyst/supervisor/viewer（密码同名+123） |
| [能效优化](https://github.com/nizuowanzhenbang/coal-unit-efficiency) | 8012 | 5182 | admin/operator/energyeng/manager/viewer（密码统一 demo123） |

> 🔧 开发期个别端口表面冲突（同时全启的场景极少）；生产建议统一在反向代理后规划，把 8 套端口全部唯一化。

---

## 🚧 迭代路线

| 系统 | 当前版本 | 下一步 |
|---|---|---|
| 燃料采购 | v2.1 | 招标比价、ERP 财务对接、合同电子签章 |
| 运煤监督 | v2.0 | GPS 轨迹接入、磅房直连、车辆人脸识别 |
| 煤质化验 | v2.1 | 多港口化验机构接入、化验设备直连、LIMS 推送 |
| 煤场库存 | v2.1 | 三方智能配煤升级、SCADA 实时取数、皮带秤直连 |
| 能效优化 | v1.0 ✅ | 分负荷段对标库、吹灰优化、锅炉汽机数字孪生三维、SIS 实时流接入、燃烧模型在线训练（MLflow） |
| 设备点检 | v3.0 ✅ | 真 CA 签名、DCS 报警对接、移动语音录入、大模型运维问答 |
| 安全生产 | v1.1 | 两票管理、安全检查模块、WebSocket、角色权限 |
| 环保排放 | v1.0 | APScheduler 月报、与 plant-safety / equipment-inspection 联动、DCS 直连 |

---

## 🎨 设计哲学

> 1. **互相独立，逻辑闭环。** 每个系统单独一个数据库，任何一个挂了不影响其他系统继续工作。
>
> 2. **编号即语义。** `PO-` 是订单、`HT-` 是合同、`IN-` 是入场、`DF-` 是缺陷、`U-` 是机组、`OPT-` 是优化建议……单据在哪个系统都能反查全部上下文。
>
> 3. **状态机驱动业务。** 整套平台定义了 15+ 套状态机，跨系统调用就是状态机的"边"，每次推进可审计。
>
> 4. **四闭环监督。** 物流闭环（采购→入场）+ 能效闭环（工况→寻优→节煤）+ 设备健康闭环（点检→隐患）+ 合规排放闭环（CEMS→报表）。
>
> 5. **失败降级优于级联熔断。** 所有跨系统 HTTP 调用 3 秒超时，失败不报错，由调度器或前端按钮重推，单点抖动不会拖垮全链路。
>
> 6. **不引入业务无关的中间件。** 不上 Kafka / MQ / Redis，8 个数据库 + HTTPS 直连，业务逻辑全部在 FastAPI 显式表达，工艺人员能看懂、能接手。
>
> 7. **可解释优先于复杂度。** 异常检测用统计学、能效用机理反平衡、AI 寻优叠机理先验——在工业场景里，能跟监管和运行人员讲清楚的模型，胜过黑盒。

---

## 📚 仓库一览

| 子系统 | 一句话 | GitHub |
|---|---|---|
| 燃料采购 | 供应商/合同/订单，煤的"出生证" | https://github.com/nizuowanzhenbang/fuel-procurement |
| 运煤监督 | 重量/时间/铅封三关防作弊 | https://github.com/nizuowanzhenbang/coal-transport-monitor |
| 煤质化验 | 港口 vs 入厂六维偏差 + 供应商评分 | https://github.com/nizuowanzhenbang/coal-quality-monitor |
| 煤场库存 | FIFO + 库龄/自燃预警 + 配煤建议 | https://github.com/nizuowanzhenbang/coal-yard-management |
| 能效优化 ⭐ | 反平衡能效 + AI 燃烧寻优 + 节煤减碳 | https://github.com/nizuowanzhenbang/coal-unit-efficiency |
| 设备点检 | 巡检/缺陷/两票/PWA离线/对象存储 | https://github.com/nizuowanzhenbang/equipment-inspection |
| 安全生产 | 隐患登记→整改→复查闭环 | https://github.com/nizuowanzhenbang/plant-safety |
| 环保排放 | CEMS 基准氧折算 + 合规报表 | https://github.com/nizuowanzhenbang/emission-monitoring |
| **本仓库（总览）** | 八子系统架构说明书 | https://github.com/nizuowanzhenbang/smart-power-plant |

> ⭐ = 与 AI / 节能降耗最相关，面试可重点展开。

---

## 🔒 安全基线

- [SQL 注入防护基线 · 8 个子系统统一规范](./docs/sql-injection-baseline.md) — 强制规范、一键自查脚本、PR/Release/季度复审节奏

## 📜 License

个人作品集项目，仅供学习与求职展示。
