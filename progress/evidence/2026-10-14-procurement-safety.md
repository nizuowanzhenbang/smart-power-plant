# PP-030 / PP-040 / PP-041 采购与安全可靠交付证据

批次B-20261012-01，2026-10-12启动、13/14接续；owner codex-batch-20261012-01。三项已合并并分别签收，文档最新CI另行核对；代码/进度/文档SHA分开保存。

## 固定范围与实现

设备基线8047049bb3158959172edc5a7148dd5f35be4217；安全基线e5e62e77ea0d01c7c24bea790d79e51a3b3f18d1。

PP-030四个单元：创建数量/金额Decimal与容量、原子日编号及0003到0004增量迁移、API/调度共用补货与锁序/跳过原因、拒绝超量收货且保留合法身份重放。PP-040：缺陷同事务不可变outbox，严格200/业务code/正整数ID/有效引用/来源/单号ACK，网络失败及本地ACK保存失败都可用原消息恢复，正常历史成功不重发。PP-041：原始消息收据和隐患同事务、唯一自然键、同键异内容409、规范化时间/空值、历史投影核对、人工处置不被重放覆盖；三个创建入口共享日编号。

代码规范与计划在各代码仓库docs/superpowers中，失败回归随业务代码保存。真正两个独立应用、数据库和进程通过HTTP代理，安全提交后故意丢第一ACK，停止发送进程、改变源内容/设备名、重启后仍重发原事件，只有一张隐患和收据。旧接收候选实际2失败，新实现2通过；不是只给mock成功结果。

## 验证阶段

采购初始48项双库40失败/8通过；旧0003升级1失败。实现采购后完整542通过；发送目标初始30失败/4通过、附加本地保存/无URL4失败，实现后目标38通过，完整设备582通过。加真正配对后完整584通过（SQLite、真实PostgreSQL16及同版本备份客户端），前端16通过/构建通过。

安全初始42项40失败/2通过；附加原子写入/映射及期限冲突4失败/1刻意跳过，实现后完整113通过/1刻意跳过。跳过是PG外键已阻止的人工孤立映射损坏，SQLite真实覆盖该拒绝。

## 唯一整批审查与裁定

fresh-context范围：设备8047049..57816f8、安全e5e62e7..56f494a。审查者目标设备88通过、安全45通过/1刻意跳过；两范围diff检查通过。完整584/113是父代理另行运行。Critical 0、Important 3、Minor 3。完整审查结论已返回；无再次审查。

- R1接受Important：接收max(ID)编号遇PG回滚空洞，与人工/检查count+1冲突。真实JWT请求复现500，另有原审查真实并发证据。仓库新增确定性回滚ID空洞回归先PG两入口2失败、SQLite2通过（失败提交安全9752f18），随后修正。采用独立日序号表、三个入口共用事务内分配，按旧合法最大后缀初始化；代价是新表和同日编号串行，升级要维护窗口统一切换旧写入进程。
- R2接受Important：采购嵌套数组/对象或urgency/spare_part_id中的1e309令422序列化失败成500，双库8失败。模型前递归规范非法值；代价为遍历请求结构，不改变合法数值口径。
- R3接受Important：历史SYNCED的tab/newline/内部控制字符无法被SQL trim扫描且界面误绿。分段扫描并复用有效引用判断；正常成功不占limit、不重发。页面采用一致控制字符/空白/码点长度判断。代价是读历史行及ID升序处理，容量/性能尚未验收。

设备新增回归首轮18失败/6通过，其中17业务失败、1为试图向PG varchar(50)写51字的非法夹具。PG本就禁止该状态，改为双库超长ACK拒绝测试；不将夹具错误当业务RED。失败提交设备e17b69d。安全修正6ff90cac638d88b7109dba5bfaf4cefad95ffc05，完整119通过/1刻意跳过（含新表增建/重复启动/旧9000高号/删除不复用）。设备最终完整608通过，无环境跳过，前端新增后18通过/构建通过；ruff、依赖一致性、interview_demo通过。

所有其他Ruling：沿用户明确自主批量授权不重复阶段许可（成本是范围误判时需回退）；累计到货不超原申请（合法额外到货需另行处理）；金额HALF_UP两位且溢出跳过（旧浮点边界可能差0.01，异常建议需人工核对）；历史没有原消息只能核对已存投影（无法证明原location/sla等未存字段，冲突需人工处理）；DB确认失败保留消息、返回非成功（已提交尝试数不等于全部网络次数）。

Minor全部延期：M1接收升级备份/维护窗口具体操作文档；M2采购页面显式剩余数量；M3读取响应/日常界面展示已存SKIPPED/失败原因。成本分别为操作需维护者另备步骤、余量由已到/总数自行理解、日常排错需手动重试/查记录。各有后续任务，未声称全部规范完成。

Declined-to-judge接受：现场有效性、容量/性能、真实第三方运行、任意篡改后的完整恢复、跨库exactly-once超范围；成本是本次只证明版本化软件原型与明确故障契约。未证明现场收益或全厂联合优化。

[无聊天恢复实录](../docs/RECOVERY-EXERCISE-20261013.md)。本地scratch路径仅本执行环境有效；GitHub版本化用例、规范、固定SHA和本证据才是持久接续依据。


## 接收端发布

安全固定6ff90cac638d88b7109dba5bfaf4cefad95ffc05候选CI [38627582408](https://github.com/nizuowanzhenbang/plant-safety/actions/runs/38627582408)三项成功，PR #4合并为6f12503f00fdd485a55e737f17d08e8ff8b833f0，合并树与受测树一致；[main CI 38628086080](https://github.com/nizuowanzhenbang/plant-safety/actions/runs/38628086080)三项成功。文档关闭计划签收aed22d627120c6c902878f6c6b8a28b50fef72c5，[main CI 38628257397](https://github.com/nizuowanzhenbang/plant-safety/actions/runs/38628257397)三项成功。真实merged检查点de1b520、release9254a4e；已录入RELEASES。设备配对CI固定实际接收发布6f12503。

设备完整最终608通过、前端18/构建通过。固定修正候选d412845a2c38d5e4b60af1401a174f7d3f6021da已推送，reviewed检查点d0a64df，PR #15当前CI中，不能写为已合并。接续工具本轮完整25项通过。


最后CI范围核对发现根目录发送测试的PG参数未被原PG目录命令选中，追加CI专门覆盖；最终候选3211e6602915483b479d1d638ada80af6b87f6a8仅改CI命令/台账，业务树与完整608通过的d412一致。对应pr_open检查点2482a47。等待CI期间完成[PP050只读准备](../docs/PP050-DISCOVERY-20261014.md)，未将身份映射或适配器计为实施。


## 设备发布与整批签收

最终3211e6602915483b479d1d638ada80af6b87f6a8的[质量CI38628696787](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/38628696787)四项及[Compose38628696609](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/38628696609)成功。按固定SHA合并[PR #15](https://github.com/nizuowanzhenbang/equipment-inspection/pull/15)为2312540c6d4c85ac0b921100937476067f87a506；合并树与候选一致。[main质量38629494445](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/38629494445)四项成功，[手动main Compose38629717040](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/38629717040)成功。浏览器场景为既有登录/鉴权/库存/部署场景，不能扩大为新增控制字符标签的浏览器测试；该标签的共享谓词由前端18项中的新增单元与构建核对。

PP030 merged检查点2e3b061、release6d0eb2b；PP040 claim2a483ce、merged797e71c、releaseca30b20，SESSION.active=null且last为PP040的真实业务mergeSHA/PR15。RELEASES以两任务同一实际PR分别索引，不把后来文档SHA冒充业务merge。设备文档55a32758036dc0b7503b5d4fcb22f281c9fedd31关闭计划，[质量CI38630239143](https://github.com/nizuowanzhenbang/equipment-inspection/actions/runs/38630239143)四项成功；安全文档aed22d6已main绿。自有临时PG测试容器已停止并移除，没有后台模型开发服务；工作分支和检出保留，不强推或清理他人工作。


最终离线结构/本地链接及8条真实发布索引远端核验通过，接续本轮25项完整通过。SESSION最后下一动作在签收文档中改为下一批入口，保留真实merged/release的SHA/PR/执行者/时间，不让旧合并时动作引发再次释放。三任务、两个业务基线、两份代码计划、下一批入口一致；最终中央签收提交与同SHA远端核心文件复读在收尾核对。
