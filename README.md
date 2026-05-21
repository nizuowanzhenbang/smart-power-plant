# 智慧发电厂全链路管理平台 · Smart Power Plant Suite

> 一套围绕燃煤发电厂日常运营，从**燃料采购**到**入厂运输**、从**质量验收**到**煤场库存**、从**设备点检**到**安全隐患**的**全链路数字化管理体系**。
>
> 由 6 个独立部署、通过共享密钥互联互通的微服务子系统构成，覆盖"**人 / 煤 / 机 / 险**"四大业务域。

---

## 一、为什么需要这套系统

传统发电厂的运营痛点：

- **数据孤岛**：采购系在 Excel、化验在 LIMS、煤场在台账、点检在纸质单 —— 同一批煤的旅程被切成六段，没人能讲全。
- **反舞弊难**：港口实测 vs 入厂实测、订单合同价 vs 实际结算价、出场重量 vs 实际燃用 —— 偏差散落在各子系统，没人盯。
- **闭环断点**：点检发现的重大隐患没人转工单；缺陷修了没人复查；入场的煤没人对煤质。
- **责任不清**：跨部门协同走纸质流程，超期不报警，整改不追踪。

本套件以「**一批煤的完整旅程**」为主线，把六个子系统串成数字闭环，每一个环节都有数据沉淀、每一次跨系统流转都有审计可查。

---

## 二、整体业务运作原理

```
       ┌─────────────────────────────────────────────────────────────────┐
       │                    一批煤的完整数字旅程                            │
       └─────────────────────────────────────────────────────────────────┘

   [1] 燃料部下计划        [2] 港口装船 / 汽车启运       [3] 入厂磅房 + 化验
        ↓                         ↓                              ↓
  ┌──────────────┐          ┌──────────────┐            ┌──────────────────┐
  │ fuel-        │  订单号  │ coal-        │  铅封 / 重 │ coal-quality-    │
  │ procurement  │─────────►│ transport-   │───────────►│ monitor          │
  │ (供应商/合同/│          │ monitor      │  量 / 时长 │ (六维偏差雷达)    │
  │  订单 三层)  │          │ (三大分析器) │            │                   │
  └──────┬───────┘          └──────────────┘            └─────────┬────────┘
         │                                                        │
         │ ◄────── 信用回写 ─── 供应商质量评分 ───────────────────┘
         │
         │  订单履约
         ▼
  ┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
  │ coal-yard-   │  扣减   │  锅炉燃用    │  健康度  │ equipment-       │
  │ management   │────────►│  (生产工艺)  │─────────►│ inspection       │
  │ (堆区/FIFO/  │  库存   │              │  关联    │ (点检/缺陷/工单) │
  │  库龄/温度)  │         │              │          │                   │
  └──────┬───────┘         └──────────────┘          └─────────┬────────┘
         │                                                     │
         │ ◄──── 入场回调 / 化验汇总 ──────────────────────────┘
         │                                                     │
         │                                                     │ CRITICAL 缺陷
         │                                                     ▼
         │                                            ┌──────────────────┐
         └───────────── 横向监督 ────────────────────►│ plant-safety     │
                                                     │ (隐患排查/整改)   │
                                                     └──────────────────┘
```

### 一条业务主线 + 一条监督副线

**主线（物的流转）**：`采购订单 → 运输入厂 → 化验验收 → 煤场入场 → FIFO 出场 → 锅炉燃用`

**副线（设备 + 安全）**：`日常点检 → 异常发现 → 缺陷工单 → CRITICAL 缺陷 → 隐患单 → 整改复查`

两条线在「**煤场**」和「**设备健康**」处交汇 —— 煤质偏差影响锅炉效率，锅炉缺陷影响发电能力。

---

## 三、六个子系统逐一介绍

### 📦 [fuel-procurement](https://github.com/nizuowanzhenbang/fuel-procurement) · 燃料采购管理

**定位**：链路起点。燃料部所有"采购意图"在这里固化为合同与订单。

- **三层模型**：供应商（GYS-NNNN） → 合同（HT-YYYYMM-NNNN） → 订单（PO-YYYYMMDD-NNNN）
- **三套状态机**：供应商生命周期、合同审批与履约、订单调度与到货
- **金额阈值审批**：< 100 万 / 100–500 万 / > 500 万 → 1 / 2 / 3 级审批
- **价格审计**：生效合同的单价调整走专用接口 + 历史轨迹
- **角色矩阵**：admin / buyer / approver / viewer

**对外接口**：
- `GET /api/integration/order-info?order_no=` → 给煤场系统拉订单履约与煤质基准
- `POST /api/integration/yard-stocked` → 接收煤场入场回调，自动累计 delivered_quantity + 推进状态机
- `POST /api/webhook/quality-score` → 接收 coal-quality-monitor 的供应商信用分

---

### 🚛 [coal-transport-monitor](https://github.com/nizuowanzhenbang/coal-transport-monitor) · 运煤监督与风险预警

**定位**：港口到厂区运输过程的反舞弊监控。

- **WeightAnalyzer**：亏吨/盈吨检测，3‰ 阈值 + Z-score 动态阈值
- **TimeAnalyzer**：运输时长 IQR 基准检测异常滞留
- **SealAnalyzer**：QR 码铅封 Levenshtein 相似度比对，识别篡改
- **WebSocket** 实时预警广播，CSV 导出

---

### ⚗️ [coal-quality-monitor](https://github.com/nizuowanzhenbang/coal-quality-monitor) · 煤质化验数据比对

**定位**：港口化验 vs 入厂化验六维煤质指标偏差检测，识别"以次充好、货物掉包"。

- **六维指标**：热值 / 灰分 / 硫分 / 水分 / 挥发分 / 固定碳
- **8 种预警类型**：CALORIFIC_SHORTAGE / ASH_EXCESS / SULFUR_EXCESS / MOISTURE_EXCESS / CONTRACT_* / COMPREHENSIVE
- **核心可视化**：六维归一化雷达图
- **供应商信用评分**（0–100，基于近 20 批次）回写采购系统
- **WebSocket** JWT 鉴权 + 实时预警

**对外接口**：
- `GET /api/integration/order-quality-summary?order_no=` → 给煤场系统拉订单化验汇总（PORT / FACTORY 均值 + 严重预警计数 + conclusion）

---

### 🏭 [coal-yard-management](https://github.com/nizuowanzhenbang/coal-yard-management) · 煤场库存管理

**定位**：燃料链最后一环 —— 到货之后到燃用之前的实物管理。

- **堆区**（DQ-NNN） → **入场**（IN-YYYYMMDD-NNNN） → **出场**（OUT-YYYYMMDD-NNNN） → **盘点**（PD-YYYYMMDD-NNN）
- **FIFO 出场**：按 `stocked_at ASC` 扣减 remaining_quantity，明细写 fifo_breakdown JSON
- **库龄三级预警**：≤15 天绿 / 15–30 天黄 / >30 天红
- **自燃温度监控**：50/65/80 ℃ 三档阈值 + 高温榜 + 趋势图
- **入煤综合评分 + 配煤建议**：热值基础 + 灰/硫/水扣分 + 库龄衰减
- **大额出场审批**：≥5000 吨需主管审批

**关键集成**：入场时实时调用 fuel-procurement 拉订单信息，调用 coal-quality-monitor 拉化验汇总，入场成功后回调 fuel-procurement 推进订单状态。

---

### 🔧 [equipment-inspection](https://github.com/nizuowanzhenbang/equipment-inspection) · 设备点检与缺陷管理

**定位**：发电核心设备的健康保障。

- **8 大系统**：锅炉 / 汽轮机 / 发电机 / 辅机 / 电气 / 化学水 / 除灰除渣 / 脱硫脱硝
- **3 级关键度** A / B / C，**5 种角色**：admin / inspector / repairman / supervisor / viewer
- **13 张表覆盖**：设备 / 路线 / 测点 / 任务 / 点检记录 / 缺陷 / 工作票 / 操作票 / 操作模板 / 备件 / 库存流水 / 用户 / 审计日志
- **SLA**：MINOR 72h / MAJOR 24h / CRITICAL 4h
- **健康度联动**：缺陷扣分、验收回弹
- **APScheduler 内置调度器**：超期扫描 / 漏检扫描 / 任务生成 / 联动重试
- **预测性维护**：综合风险算法（缺陷 30% + CRITICAL 25% + 异常 15% + 健康度 20% + 等级状态加成），sigmoid 平滑成失效概率
- **两票管理**：工作票 5 类状态机 + 操作票 5 步执行 + 安全措施清单
- **PWA + 移动扫码**：BarcodeDetector 摄像头 + 拍照上报
- **QR 批量打印**：segno 生成 SVG + A4 4 列排版

**关键集成**：CRITICAL 缺陷自动调用 plant-safety 的隐患接收接口建隐患单，幂等重试 + 状态回写。

---

### 🛡️ [plant-safety](https://github.com/nizuowanzhenbang/plant-safety) · 安全生产管理

**定位**：发电厂日常隐患排查与整改闭环。

- **11 个分区**：主厂房 / 锅炉区 / 汽轮机区 / 电气区 / 燃料区 / 化学水 / 除灰除渣 / 脱硫脱硝 / 冷却塔 / 开关站 / 办公区
- **13 个风险类别**：电气安全 / 压力容器 / 危险化学品 / 高处作业 / 有限空间 / 动火作业 / 起重作业 / 辐射防护 / 消防安全 / 机械伤害 / 环境排放 / 现场环境 / 其他
- **状态机**：PENDING → IN_PROGRESS → RECTIFIED → VERIFIED，超期自动 OVERDUE
- **整改期限**：重大隐患 14 天，一般 30 天
- **隐患编号**：YH-YYYYMMDD-NNNN

**对外接口**：
- `POST /api/integration/hazards` → 接收外部系统推送的隐患单，幂等基于 external_source + external_no
- `GET /api/integration/hazards/by-external/{source}/{external_no}` → 反查

---

## 四、系统间集成关系矩阵

| 调用方 → 被调方                           | 接口                                       | 用途                                        |
| ----------------------------------------- | ------------------------------------------ | ------------------------------------------- |
| coal-yard → fuel-procurement              | `GET /api/integration/order-info`          | 入场时拉订单 / 合同 / 供应商 / 煤质基准     |
| coal-yard → fuel-procurement              | `POST /api/integration/yard-stocked`       | 入场成功后回调，推进订单履约                |
| coal-yard → coal-quality-monitor          | `GET /api/integration/order-quality-summary` | 入场前拉订单化验汇总，判定是否合格         |
| coal-quality-monitor → fuel-procurement   | `POST /api/webhook/quality-score`          | 供应商信用分回写采购系统                    |
| equipment-inspection → plant-safety       | `POST /api/integration/hazards`            | CRITICAL 缺陷自动建隐患单                   |
| coal-transport-monitor ↔ coal-quality-monitor | `transport-event`（X-Integration-Secret） | 运输 → 质量上下游事件流                    |

**鉴权统一**：所有跨系统接口使用 `X-Integration-Token` 头 + 各系统 `INTEGRATION_SECRET` 共享密钥；coal-quality-monitor 保留对老的 `X-Integration-Secret` 兼容。

---

## 五、统一技术栈

| 层次       | 选型                                                           |
| ---------- | -------------------------------------------------------------- |
| 后端       | **FastAPI** + SQLAlchemy + Pydantic + JWT                      |
| 前端       | **React 18** + TypeScript + Vite + Ant Design 5 + ECharts      |
| 数据库     | SQLite（开发）/ PostgreSQL（生产可平移）                       |
| 实时通信   | **WebSocket**（JWT 鉴权 + ConnectionManager + 跨线程 emit）   |
| 调度任务   | **APScheduler**（equipment-inspection 内置 4 个 job）          |
| 跨系统调用 | httpx + 共享密钥头 `X-Integration-Token`                       |
| 部署       | 各系统独立端口 + .env 配置 + uvicorn / vite dev server         |

---

## 六、默认端口与账户矩阵（开发环境）

| 系统                   | 后端端口 | 前端端口 | 默认账户                                                                       |
| ---------------------- | -------- | -------- | ------------------------------------------------------------------------------ |
| fuel-procurement       | 8000     | 5173     | admin/admin123, buyer/buyer123, approver/approver123, viewer/viewer123         |
| coal-yard-management   | 8001     | 5174     | admin/admin123, operator/operator123, supervisor/supervisor123, viewer/viewer123 |
| coal-quality-monitor   | 8002     | 5176     | admin/admin123                                                                 |
| equipment-inspection   | 8003     | 5175     | admin/admin123, inspector/inspector123, repairman/repairman123, supervisor/supervisor123, viewer/viewer123 |
| plant-safety           | 8000     | 5173     | admin/admin123（独立部署，与 fuel-procurement 不同时启动）                     |
| coal-transport-monitor | —        | —        | admin/admin123                                                                 |

> 端口冲突说明：plant-safety 与 fuel-procurement 同端口，生产环境通过容器化或反代分离；开发环境二选一启动。

---

## 七、端到端冒烟测试

`coal-yard-management/backend/integration_smoke_test.py` 提供三方端到端冒烟脚本：

```bash
# 默认端口 8000 (fuel-procurement) / 8001 (coal-yard) / 8002 (coal-quality-monitor)
python backend/integration_smoke_test.py --run-yard
```

`--run-yard` 触发真实入场流程，覆盖：
1. coal-yard 调 fuel-procurement 拉订单信息
2. coal-yard 调 coal-quality-monitor 拉化验汇总
3. 入场成功后 coal-yard 回调 fuel-procurement 推进状态

equipment-inspection ↔ plant-safety 联动通过 seed_data 模拟 SYNCED / FAILED / PENDING / SKIPPED 四种状态，前端 DefectList 显示"隐患联动"列 + 手动重推按钮。

---

## 八、迭代路线

| 系统                   | 当前版本 | 规划要点                                                            |
| ---------------------- | -------- | ------------------------------------------------------------------- |
| fuel-procurement       | v2.1     | 招标比价模块；与 ERP 财务结算对接                                  |
| coal-yard-management   | v2.1     | 三方智能配煤算法升级；与 SCADA 实时取数                            |
| coal-quality-monitor   | v2.1     | 多港口化验机构接入；化验设备直连                                   |
| equipment-inspection   | v2.5     | v3.0：S3/OSS 存储、两票电子签名、离线模式、备件→采购单、Docker Compose |
| plant-safety           | v1.1     | v2.0：两票管理、安全检查、WebSocket 推送、角色权限拦截             |
| coal-transport-monitor | v2.0     | GPS 轨迹接入；与 coal-yard 入场磅房直连                            |

---

## 九、设计哲学

1. **物理隔离 + 逻辑闭环** —— 每个系统独立部署、独立数据库、独立账户体系；通过共享密钥 + 标准 HTTP 接口跨系统协作，单点故障不会级联。
2. **状态机驱动业务** —— 6 个系统共定义了 15+ 套状态机，所有跨系统调用都是状态机的边，每一次推进可审计、可回滚。
3. **编号即语义** —— `GYS-` / `HT-` / `PO-` / `IN-` / `OUT-` / `DF-` / `WT-` / `YH-` 等前缀让单据在任何系统间流转都能反查上下文。
4. **双闭环监督** —— 物的流转闭环（采购→库存）+ 设备健康闭环（点检→隐患）；两条闭环在煤场与锅炉处交汇，覆盖发电厂日常 90% 的运营事件。
5. **WebSocket 不是装饰** —— 实时预警在反舞弊、设备 CRITICAL、库存温度异常 3 个场景下是核心 UX，不是噱头。
