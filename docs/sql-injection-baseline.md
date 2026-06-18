# SQL 注入防护基线 · 8 个子系统统一规范

> 适用范围：燃煤线 7 个子系统 + 燃气线 gas-fuel-metering，以及后续按同一基线开发的新子系统。
>
> 技术栈前提：**FastAPI + SQLAlchemy 2 + Pydantic 2**，数据库 SQLite（开发）/ PostgreSQL（生产）。
>
> 一句话原则：**所有进数据库的值都必须走绑定参数（bound parameters），所有进 SQL 文本的"标识符"都必须走白名单。**

---

## 1. 为什么 ORM 不等于"天然免疫"

SQLAlchemy 默认确实用绑定参数，但实践中下面几类写法会绕过保护，把用户输入直接拼进 SQL：

```python
# ❌ 危险：f-string 把用户输入拼进 SQL 文本
session.execute(text(f"SELECT * FROM coal_order WHERE supplier_name = '{name}'"))

# ❌ 危险：order_by(text(...)) 直接接收前端传入的字段名
query.order_by(text(f"{sort_field} {sort_dir}"))

# ❌ 危险：动态列名也是字符串拼接，绑定参数不覆盖标识符
session.execute(text(f"SELECT {col} FROM lab_result"))

# ❌ 危险：LIKE 模糊查询未转义 % _ \
query.filter(Supplier.name.like(f"%{q}%"))   # q="100%" 会破坏匹配语义；q="\\" 在 PG 上更危险

# ❌ 危险：raw SQL + executescript（SQLite）会执行多语句
conn.executescript(f"UPDATE x SET y=1 WHERE z='{user_input}'")   # 用户传 "'; DROP TABLE ...--" 直接拖库
```

---

## 2. 强制规范（必须做）

### 2.1 写查询：优先 ORM 表达式，其次 text() + bindparam

```python
# ✅ 首选：ORM 表达式
stmt = select(CoalOrder).where(CoalOrder.supplier_name == name)
session.execute(stmt)

# ✅ 次选：必须用 text() 时，参数走命名占位符
stmt = text("SELECT * FROM coal_order WHERE supplier_name = :name")
session.execute(stmt, {"name": name})
```

### 2.2 动态字段 / 排序 / 表名：白名单，不接受任意字符串

```python
# ✅ 排序字段白名单
SORTABLE = {
    "created_at": CoalOrder.created_at,
    "delivered_quantity": CoalOrder.delivered_quantity,
    "supplier_name": CoalOrder.supplier_name,
}
col = SORTABLE.get(sort_field)
if col is None:
    raise HTTPException(400, "invalid sort field")
direction = asc if sort_dir == "asc" else desc   # 只允许两个值
query = query.order_by(direction(col))
```

### 2.3 LIKE 模糊查询：转义 + 显式 escape

```python
# ✅ 把 % _ \ 全部转义
def escape_like(s: str) -> str:
    return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

query.filter(Supplier.name.like(f"%{escape_like(q)}%", escape="\\"))
```

### 2.4 入口处用 Pydantic 收紧类型

数字、枚举、日期、UUID 全部用 Pydantic 的强类型；字符串字段必加 `max_length` 与正则约束（如供应商编码 `^[A-Z0-9_-]{1,32}$`）。这一层是 SQL 注入的第一道防线。

### 2.5 跨系统调用同样适用

`httpx` 调下游系统时拼接的 URL/参数走 `params=`，**绝不把用户输入直接拼到 path 里**；下游系统接到值之后仍然要按上面的规矩进库。

### 2.6 禁令清单

| 写法 | 状态 |
|---|---|
| `session.execute(text(f"...{var}..."))` | ❌ 禁止 |
| `query.filter(text(f"...{var}..."))` | ❌ 禁止 |
| `query.order_by(text(user_input))` | ❌ 禁止 |
| `session.execute("string sql", {...})`（不走 text/select） | ❌ 禁止 |
| `connection.executescript(...)` 含用户输入 | ❌ 禁止 |
| 把前端传来的字段名直接当列名/表名 | ❌ 禁止 |
| 给前端开"自由 SQL"导出/报表接口 | ❌ 禁止（除非走只读账号 + 解析白名单 AST） |

---

## 3. 一键自查脚本（在任意子仓库根目录执行）

把下面这段保存为 `scripts/sqli_scan.sh`，每次提交前 / CI 里跑一次：

```bash
#!/usr/bin/env bash
# SQL injection static scan · 适用于 FastAPI + SQLAlchemy 2 子系统
# 用法：bash scripts/sqli_scan.sh [path]，默认扫 backend/
set -u
ROOT="${1:-backend}"
EXIT=0

echo "== [1] text() / execute() 内出现 f-string 或 .format() =="
if grep -rnE "(text|execute)\s*\(\s*(f\"|f')" "$ROOT" --include='*.py'; then EXIT=1; fi
if grep -rnE "(text|execute)\s*\([^)]*\.format\(" "$ROOT" --include='*.py'; then EXIT=1; fi

echo "== [2] text() / execute() 内出现 % 字符串格式化或 + 拼接 =="
if grep -rnE "(text|execute)\s*\([^)]*%[^)]*\)" "$ROOT" --include='*.py'; then EXIT=1; fi
if grep -rnE "(text|execute)\s*\([^)]*\+[^)]*\)" "$ROOT" --include='*.py' | grep -v "execute(stmt"; then EXIT=1; fi

echo "== [3] order_by / filter / where 内出现 text(f...) 拼接 =="
if grep -rnE "(order_by|filter|where)\s*\(\s*text\s*\(\s*(f\"|f')" "$ROOT" --include='*.py'; then EXIT=1; fi

echo "== [4] executescript / executemany 出现 f-string =="
if grep -rnE "execute(script|many)\s*\(\s*(f\"|f')" "$ROOT" --include='*.py'; then EXIT=1; fi

echo "== [5] LIKE 查询未带 escape 参数（人工复核） =="
grep -rnE "\.like\s*\(" "$ROOT" --include='*.py' | grep -v "escape=" || echo "  （以上若有结果需人工确认是否处理了 % _ \\）"

echo "== [6] 直接把请求参数拼到 SQL 文本（高危关键字） =="
grep -rnE "f\"(SELECT|INSERT|UPDATE|DELETE)\b" "$ROOT" --include='*.py' -i && EXIT=1
grep -rnE "f'(SELECT|INSERT|UPDATE|DELETE)\b" "$ROOT" --include='*.py' -i && EXIT=1

if [ "$EXIT" = "0" ]; then
  echo "✅ 静态扫描未发现常见注入模式（仍需人工复核 LIKE 与白名单）"
else
  echo "❌ 发现可疑模式，请按基线整改"
fi
exit "$EXIT"
```

> 这个脚本不是"全部找到才算"，而是把人最容易出错的几类高危模式拦掉。**它通过 ≠ 代码安全**，业务里出现"动态列名 / 表名 / 排序字段"时仍然必须人工核对白名单是否落实。

---

## 4. 每个子系统必须自查的接口清单

下面几类接口是注入高发区，每个子系统至少要逐一确认：

| 接口形态 | 典型出现位置 | 注入关注点 |
|---|---|---|
| 列表查询带 `sort` / `order` 参数 | 各子系统的 `GET /xxx/list` | 排序字段白名单、方向枚举 |
| 列表查询带 `q` / `keyword` 模糊搜索 | 供应商、设备、缺陷、隐患列表 | LIKE 转义 + escape="\\" |
| 列表查询带 `filters` JSON | 任意"高级查询"接口 | 字段名白名单、操作符白名单 |
| 报表/导出接口 | 月度合规、煤场盘点、缺陷台账 | 时间范围用 Pydantic `datetime`；分组字段白名单 |
| 跨系统回写接口 | 信用回写、隐患联动、入场回执 | 共享密钥头 + Pydantic 强类型；不要根据请求体拼 SQL |
| 原生 SQL 报表 | `text(...)` 类的统计接口 | 全部参数走 `:name` 绑定；不出现 f-string |

---

## 5. 复审节奏

1. **每个 PR**：CI 跑 `sqli_scan.sh`，非零退出阻塞合并。
2. **每个 release**：在每个子系统的 release notes 里追加一行"SQL 注入扫描结果：通过 / 风险点 N 处已整改"。
3. **每季度**：在 `smart-power-plant` 总览仓库开一个 Issue，链接 8 个子系统的最新扫描结果，作为集团级合规凭证。
4. **新子系统准入**：燃气线后续两个规划中的子系统（gas-turbine-performance、gas-emission-monitoring）首次合入主干前，必须先跑过本基线。

---

## 6. 不在本文档范围内的安全项

下面这些重要，但**不是本文档的主题**，请在各自专门的安全基线里覆盖：

- 认证授权（JWT 过期、刷新、角色越权）
- 跨系统调用的共享密钥轮换
- 前端 XSS、CSRF
- 文件上传（设备点检的二维码 / 巡检照片）的类型与大小校验
- 对象存储（boto3）的预签名 URL 时限
- 密码哈希算法与默认账户清理（README 里那批 `admin/admin123` 上生产前必须改）
