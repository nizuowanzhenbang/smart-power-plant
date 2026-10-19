# 测试覆盖分析与改进建议

> 本文档梳理整套平台各子系统的测试现状，并提出优先级排序的改进方向。

---

## 一、当前测试现状

| 子系统 | 已知测试数量 | 来源 |
|---|---|---|
| gas-fuel-metering | 97 条 | README 中明确提及 |
| equipment-inspection | 未知 | README 提及 v3.0 完整部署，但无测试计数 |
| fuel-procurement | 未知 | 无相关信息 |
| coal-transport-monitor | 未知 | 无相关信息 |
| coal-quality-monitor | 未知 | 无相关信息 |
| coal-yard-management | 无自动化套件，有手动冒烟脚本 | `integration_smoke_test.py` |
| plant-safety | 未知 | 无相关信息 |
| emission-monitoring | 未知 | 无相关信息 |

**核心问题：** 8 个子系统中，只有 1 个有确认的测试数量，6 个没有任何测试数据，1 个仅有手动冒烟脚本（不属于自动化回归套件）。

---

## 二、高优先级：需立即补充的测试

### 1. 跨系统集成接口测试

**现状：** 9 条跨系统 HTTP 接口是整个平台业务逻辑闭环的骨架，目前只有 `coal-yard-management` 有一个手动烟雾测试脚本，其余系统无任何自动化集成测试。

**需要覆盖的 9 条接口：**

| 接口 | 调用方 | 被调方 | 核心风险 |
|---|---|---|---|
| `GET /api/integration/order-info` | coal-yard | fuel-procurement | 入场时拿不到订单，系统无法落单 |
| `POST /api/integration/yard-stocked` | coal-yard | fuel-procurement | 回调失败则订单交付量无法累积，永远不结案 |
| `GET /api/integration/order-quality-summary` | coal-yard | coal-quality | 拿不到化验汇总，配煤建议丢失依据 |
| `GET /api/integration/supplier-credit` | fuel-procurement | coal-quality | 采购页信用分长期停留旧数据 |
| `GET /api/integration/order-quality` | fuel-procurement | coal-quality | 订单详情页化验明细缺失 |
| `POST /api/webhook/quality-score` | coal-quality | fuel-procurement | 信用分回写失败则采购无法感知质量恶化 |
| `POST /api/integration/transport-event` | coal-transport | coal-quality | 运输事件丢失则化验预警归集失效 |
| `POST /api/integration/hazards` | equipment | plant-safety | CRITICAL 缺陷未自动建隐患是安全合规风险 |
| `GET /api/integration/hazards/by-external/{source}/{no}` | equipment | plant-safety | 设备系统无法反查隐患状态 |

**建议测试场景：**
- 正常路径：请求返回预期数据，下游状态机正确推进
- 超时（3 秒）：被调方不响应时，调用方应降级而非抛出 500
- 重试幂等：同一 POST 调用两次，数据库不出现重复记录（尤其 `yard-stocked` 和 `hazards`）
- Token 鉴权失败：无 `X-Integration-Token` 或 Token 错误时返回 401/403

---

### 2. 状态机边界测试

**现状：** 平台定义了 15+ 套状态机，是跨系统协作的核心契约，但状态机本身（尤其无效跳转的防护）的测试情况未知。

**高风险状态机及必测场景：**

#### 采购合同状态机（fuel-procurement）
```
DRAFT → PENDING_APPROVAL → ACTIVE → COMPLETED/EXPIRED/TERMINATED
```
- 未审批合同能否直接跳到 `ACTIVE`？（应拒绝）
- `COMPLETED` 合同能否被重新激活？（应拒绝）
- `ACTIVE` 合同的单价只能通过 `POST /contracts/{id}/adjust-price`，直接 PATCH 应被拒绝

#### 订单状态机（fuel-procurement）
```
PLANNED → DISPATCHED → PARTIAL_RECEIVED → RECEIVED → SETTLED
```
- `delivered_quantity` 累积到 99% 时是否自动触发结案
- 超过 100% 的到货量（超收）如何处理

#### 缺陷 SLA 计时（equipment-inspection）
- 紧急缺陷 4 小时、重要 24 小时、一般 72 小时——超期后的状态标记是否正确
- 修复后健康度回弹算法的正确性

#### 告警合并逻辑（emission-monitoring）
- 同一排放口已有未结告警时，新数据应更新 `peak/duration_minutes`，而不是新建告警
- 持续 ≥30 分钟时应自动从 `OPEN` 升级到 `ESCALATED`
- 恢复达标后 `ended_at` 是否正确写入

---

### 3. 核心业务算法测试

这些算法直接影响业务判断和监管合规，任何计算错误都可能造成漏报或误报。

#### 基准氧折算公式（emission-monitoring）—— 法规强制要求

```python
# GB13223-2011：C折 = C实测 × (21 - 6) / (21 - O2实测)
# O2 ≥ 20.5 时视为异常，不执行折算
```

**必测用例：**
```
正常：C实测=40 mg/Nm³, O2=10% → C折 = 40 × 15/11 ≈ 54.5（超低限值 35 的 1.56 倍 → SEVERE）
边界：O2=20.5% → 不折算，直接用实测值
边界：O2=20.4% → 正常折算，结果会极大放大
燃气线：基准氧改为 15%，折算系数变为 (21-15)/(21-O2)，需单独测试
```

#### 供应商信用评分（coal-quality-monitor）

```
评分 = 热值达标率×40% + 灰分达标率×15% + 硫分达标率×15% + 水分达标率×15% + 综合预警通过率×15%
基于最近 20 批次
```

**必测用例：**
- 不足 20 批次时的处理（新供应商）
- 全部达标 → 100 分；全部不达标 → 0 分；边界批次精确加权
- 评分变更后是否立即回写到 `fuel-procurement.supplier_quality_scores`

#### FIFO 出场扣减（coal-yard-management）

```python
# 按 stock_ins.stocked_at ASC 依次扣减 remaining_quantity
# 扣减路径写入 fifo_breakdown JSON
```

**必测用例：**
- 一次出场跨越多个入场批次的正确拆分
- 出场量恰好等于某批次 `remaining_quantity`（边界）
- 出场量超过全部库存（应拒绝或告警）
- 盘点缩放后按 `actual/book` 比例缩放所有批次，FIFO 顺序不变

#### 运煤重量/时间/铅封异常检测（coal-transport-monitor）

```python
# WeightAnalyzer：3‰ 基础阈值 + Z-score 动态阈值（近 30 天同车队）
# TimeAnalyzer：IQR 四分位距基准
# SealAnalyzer：Levenshtein 编辑距离
```

**必测用例：**
- 不足 30 天历史数据时 Z-score 的 fallback 行为
- Levenshtein 距离阈值边界（相差 1 个字符 vs 2 个字符）
- IQR 计算中异常值对基准的污染防护

#### 配煤评分（coal-yard-management）

```
score = 热值基础分 + (灰/硫/水各超标扣分) + 库龄衰减
```

**必测用例：**
- 库龄 15/30 天的颜色分级边界（≤15绿/15-30黄/>30红）
- 温度三档（50/65/80℃）预警触发
- 大额出场 5000 吨审批阈值边界

---

## 三、中优先级：建议尽快补充的测试

### 4. 幂等性测试

plant-safety 对外开放的隐患接收接口使用 `(external_source, external_no)` 唯一约束防重复，但需要验证：
- 相同 `(external_source, external_no)` 的第二次 POST：应返回成功且不创建新记录
- 不同 `external_no` 的 POST：应正常创建
- 并发场景：两个相同请求同时到达时数据库约束是否足够（或需要应用层锁）

### 5. 角色权限测试

各子系统定义了 4-5 种角色，需验证权限边界：

| 子系统 | 角色 | 典型权限边界 |
|---|---|---|
| equipment-inspection | INSPECTOR/REPAIRMAN/SUPERVISOR | INSPECTOR 不能直接关闭缺陷；REPAIRMAN 不能审批工作票 |
| emission-monitoring | OPERATOR/ANALYST/SUPERVISOR | OPERATOR 不能 APPROVED 合规报表 |
| fuel-procurement | buyer/approver | buyer 不能自审批自己提交的合同 |
| plant-safety | — | 整改责任人不能自行完成复查确认 |

**关键场景：** 用错误角色的 JWT Token 调用受保护接口，应返回 403。

### 6. APScheduler 定时任务测试（equipment-inspection）

5 个定时任务目前可能完全缺乏测试覆盖：
- 超期缺陷扫描：手动将缺陷创建时间设为 5 小时前，验证是否触发超期标记
- 漏检任务扫描：手动模拟巡检任务未完成，验证是否触发漏检标记
- plant-safety 联动重试：将 `safety_sync_status=FAILED` 的缺陷放入队列，验证重试逻辑
- 备件低库存采购申请自动生成（每 12h）：库存降至阈值以下时是否自动创建

### 7. 两票电子签名安全测试（equipment-inspection v3.0）

```python
# HMAC-SHA256(SECRET, f"{ticket_no}|{stage}|{user}|{ts}")
```

- 签名链完整性验证：`GET /{type}-tickets/{id}/signatures/verify` 应对所有历史签名逐一验签
- 篡改检测：手动修改 `signatures` JSON 中任一字段后，验签接口应返回失败
- 重放攻击：相同 `(ticket_no, stage, user, ts)` 的签名不应被二次接受

---

## 四、低优先级：可在后续迭代中改善

### 8. WebSocket 实时预警测试

coal-transport-monitor 和 coal-quality-monitor 使用 WebSocket 广播实时预警。建议：
- 使用 `websockets` 测试客户端验证告警触发后客户端确实收到推送
- WebSocket JWT 鉴权：无效 Token 应拒绝握手
- 客户端断连重连后的消息补发逻辑（如有）

### 9. PWA 离线队列测试（equipment-inspection 移动端）

- IndexedDB 离线队列在网络恢复后是否按顺序重放
- 离线期间与在线提交的数据无冲突
- Service Worker 更新不影响未同步的本地数据

### 10. 合同煤质基准传导测试

合同指标（`spec_calorific_value` 等）通过 `order-info` 接口单向传递到煤场和化验系统：
- 修改合同基准后，新的 `order-info` 调用是否返回新值
- 历史入场单中的基准快照是否保持不变（不应受合同修订影响）

---

## 五、端到端测试缺口

现有的 `integration_smoke_test.py` 只覆盖了"煤场 ↔ 采购 ↔ 化验"这一条路径。以下两条主线完全缺乏端到端验证：

### 设备健康闭环（equipment-inspection → plant-safety）

```
触发：在 equipment-inspection 创建 CRITICAL 缺陷
验证：
  1. plant-safety 自动收到隐患推送（幂等键正确）
  2. equipment-inspection 缺陷的 safety_sync_status 更新为 SYNCED
  3. plant-safety 中隐患分区按设备编号前缀正确映射（-BL-→锅炉区）
  4. 整改完成后 equipment-inspection 能反查到隐患状态变化
```

### 排放合规闭环（emission-monitoring，v2 规划）

```
触发：注入超标的 CEMS 读数（持续 >30 分钟）
验证：
  1. 告警自动从 OPEN 升级到 ESCALATED
  2. plant-safety 收到环保隐患推送（v2 功能）
  3. equipment-inspection 收到 CEMS 设备缺陷（v2 功能）
  4. 月报草稿中的均值/合规率数据准确
```

---

## 六、燃气线特有的测试需求

gas-fuel-metering 有 97 条测试，但以下场景可能未覆盖：

- **气源切换测试**：从中石油切换到中石化气源时，热值基准和结算单价是否正确切换
- **GB/T 22634 温压补偿算法**：不同温度/压力组合下的标准体积（Nm³）计算准确性
- **0.5% 计量差异告警**：与上游结算单对比，差异恰好在 0.5% 边界时的处理
- **燃气线环保折算**：基准氧 15% 的折算公式，需与燃煤线的 6% 公式独立测试

---

## 七、改进优先级汇总

| 优先级 | 测试类型 | 预计影响 | 涉及系统 |
|---|---|---|---|
| 🔴 高 | 跨系统集成接口（9 条） | 业务闭环完整性 | 全部 |
| 🔴 高 | 状态机边界与无效跳转 | 数据一致性 | fuel-procurement, emission-monitoring, equipment-inspection |
| 🔴 高 | 基准氧折算公式 | 监管合规 | emission-monitoring |
| 🔴 高 | FIFO 出场扣减 | 库存准确性 | coal-yard-management |
| 🔴 高 | 供应商信用评分算法 | 采购决策准确性 | coal-quality-monitor |
| 🟡 中 | 幂等性测试 | 数据重复风险 | plant-safety, coal-yard-management |
| 🟡 中 | 角色权限边界 | 安全合规 | 全部 |
| 🟡 中 | APScheduler 定时任务 | 自动化业务流程 | equipment-inspection |
| 🟡 中 | 两票 HMAC 签名安全 | 审计合规 | equipment-inspection |
| 🟡 中 | 设备健康端到端闭环 | 安全管理 | equipment-inspection + plant-safety |
| 🟢 低 | WebSocket 实时推送 | 用户体验 | coal-transport-monitor, coal-quality-monitor |
| 🟢 低 | PWA 离线同步 | 移动端可靠性 | equipment-inspection |
| 🟢 低 | 合同煤质基准传导 | 数据一致性 | fuel-procurement, coal-yard-management |
