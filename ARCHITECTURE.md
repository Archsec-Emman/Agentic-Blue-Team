# Agentic Blue Team Architecture Reference

## 1. 平台核心设计目标

该平台的核心目标不是单纯做告警展示，而是围绕安全运营与应急响应流程，构建一个可以承载分析、富化、工单协同、自动化处置、知识沉淀与
AI 智能体编排的统一数据与执行平台。

平台设计上有几个明确的方向：

1. Case 是用户最常查看、最适合承载调查视角的核心对象。
2. Alert 是检测与分析之间的中间层，既保留 OCSF 风格的检测信息，又能汇总到 Case。
3. Artifact 是最小原子，是所有进一步查询、关联、情报匹配、资产定位、日志横向扩展的基础对象。
4. Enrichment 是可结构化挂载的信息层，可以附着在 Case、Alert、Artifact 上，用于保存外部分析结果、内部查询结果、威胁情报、业务上下文等。
5. Ticket 主要用于同步外部工单系统的数据，并与 Case 形成关联。
6. Playbook 用于对 Case、Alert、Artifact 执行自动化分析与处置逻辑，未来预期大量采用 LangGraph 风格的 AI Agent 编排。
7. Knowledge 是平台内部的高时效共享知识层，既服务人工分析，也服务 AI 分析。

---

## 2. 核心对象关系

### 2.1 Case

Case 是调查和处置层的主对象。

特征：

1. Case 是 Alert 的汇总视图，但不仅仅是 Alert 的简单集合。
2. Case 中会保留很多符合 OCSF 思路的字段，也会有 Case 独有字段，例如调查状态、处置结论、优先级、人工评论、AI 分析结果等。
3. 用户在平台中最常查看的是 Case，而不是底层 Alert。

Case 的主要关系：

1. 一个 Case 挂载一个或多个 Alert。
2. 一个 Case 可以挂载多个 Enrichment。
3. 一个 Case 可以关联多个 Ticket。
4. 一个 Case 可以触发或关联多个 Playbook 运行记录。

### 2.2 Alert

Alert 是检测层对象，也是 Case 汇总前的关键实体。

特征：

1. Alert 基本遵循 OCSF 风格，承载规则、检测来源、时间、风险、策略、处置状态等信息。
2. 多个 Alert 可以根据某些条件生成 Correlation UID。
3. 相同 Correlation UID 的 Alert 会被汇总到同一个 Case 中。

Alert 的主要关系：

1. 一个 Alert 可以关联到一个或多个 Case，但在业务设计上通常会汇总到某个目标 Case 中。
2. 一个 Alert 可以挂载多个 Artifact。
3. 一个 Alert 可以挂载多个 Enrichment。
4. 一个 Alert 也可以触发或关联 Playbook 执行。

### 2.3 Artifact

Artifact 是平台中的最小原子对象。

这是整个设计里最关键的建模层之一。

Artifact 的价值在于：

1. 它是情报查询、资产查询、CMDB 查询、历史日志回溯、关联告警扩展、内部规则识别等操作的天然输入对象。
2. 它比 Alert 更细粒度，比 Case 更可复用，更适合做跨系统 pivot。
3. 外部威胁情报、内部资产信息、用户信息、主机信息、网络画像等大多数富化，本质上都更适合围绕 Artifact 展开。

Artifact 常见内容包括：

1. IP
2. 域名
3. URL
4. 文件哈希
5. 主机名
6. 用户名
7. 邮箱
8. 进程名
9. 云资源标识

Artifact 的主要关系：

1. Artifact 挂载在 Alert 下。
2. Artifact 可以挂载多个 Enrichment。
3. Artifact 可以触发 Playbook。

### 2.4 Enrichment

Enrichment 是平台里的结构化富化层。

它的作用不是替代原始字段，而是给 Case、Alert、Artifact 增加可以独立维护、独立追踪、独立追加的分析结果与上下文。

Enrichment 的优势：

1. 支持结构化保存长文本、JSON、外部链接、提供方、摘要等信息。
2. 支持把多来源分析结果分层挂载，而不污染原始对象字段。
3. 适合保存 AI 分析结果、外部查询结果、内部资产查询结果、威胁情报结果、人工分析摘要等。

Enrichment 可以挂载在：

1. Case
2. Alert
3. Artifact

推荐理解方式：

1. Artifact 的 Enrichment 更偏情报、资产、实体画像、外部查询结果。
2. Alert 的 Enrichment 更偏规则分析结果、告警解释、跨源关联结果、外部分析结论。
3. Case 的 Enrichment 更偏调查阶段结论、整体态势判断、跨 Alert 汇总结果、复盘材料。

Alert 上适合挂载的 Enrichment 示例：

1. 告警规则解释与误报分析
2. 跨日志源的二次验证结果
3. AI 对告警上下文的结构化分析
4. 关联同类告警的统计摘要
5. 外部平台对该 Alert 的补充判定

Case 上适合挂载的 Enrichment 示例：

1. 整体调查过程摘要
2. 多个 Alert 汇总后的攻击链判断
3. 事件分级依据
4. 复盘材料与结构化结论
5. 面向管理层或值班交接的结构化说明

### 2.5 Ticket

Ticket 主要用于同步外部工单系统的数据，而不是取代外部工单系统本身。

特点：

1. Ticket 相对独立。
2. Ticket 主要与 Case 关联。
3. Ticket 的存在使平台能够追踪外部系统中的工单状态、编号、链接与类型。

Ticket 的设计定位是“同步与关联”，不是“平台内部替代工单”。

### 2.6 Playbook

Playbook 对应 SOAR 的 playbook 理念。

当前设计里，用户可以针对不同对象编写 Python 脚本，脚本位于 PLAYBOOKS 目录。未来这部分很适合逐步演进为以 LangGraph 为主的 AI
分析/处置智能体执行层。

Playbook 可以面向：

1. Case
2. Alert
3. Artifact

Playbook 在平台中的职责包括：

1. 自动化分析
2. 自动化富化
3. 风险判断
4. 规则化处置
5. AI 智能体流程编排
6. 将结果回写为 Enrichment、Knowledge、Comment、Status 等

### 2.7 Knowledge

Knowledge 是平台内部维护的高时效共享知识层。

它和传统静态文档库不同，更偏面向 SOC/IR 的实时业务知识。

典型知识包括：

1. 哪些资产是内部扫描器
2. 哪些主机或账户属于红队演练范围
3. 某些时间窗口内哪些告警应降低优先级
4. 某些业务系统的特殊行为基线
5. 某些已知例外情况或临时豁免规则

Knowledge 的关键价值在于：

1. 给人工分析员提供统一上下文
2. 给 AI Agent 提供高时效、可更新、可共享的内部知识
3. 作为一种轻量的、运营团队可直接维护的 RAG 输入层

现有实现中，AGENTS/agent_knowledge.py 已体现出这种定位：

1. 通过向量检索和 rerank 获取内部知识条目
2. 可结合 Mem0 作为额外记忆层
3. 最终返回适合分析智能体消费的知识结果集合

Knowledge 的 Action 字段很重要，因为它天然适合承载“待存储”“待移除”“已生效”等知识生命周期状态。

---

## 3. Correlation UID 与汇总逻辑

平台的一个关键聚合机制是 Correlation UID。

核心思想：

1. 多个 Alert 会根据一定规则生成 Correlation UID。
2. 相同 Correlation UID 的 Alert 被归并到同一个 Case。
3. Case 可以理解为“相关 Alert 的调查汇总对象”。

这样做的价值：

1. 减少告警风暴对分析员的干扰
2. 让用户从事件而不是从单条规则告警进行调查
3. 更容易把 AI 分析能力放在更高层级的 Case 上

这也意味着：

1. Alert 是检测层事实对象
2. Case 是调查层视图对象
3. Artifact 是原子 pivot 对象
4. Enrichment 是结构化结果对象

---

## 4. MCP 设计原则

MCP 层应尽量遵守以下原则：

1. MCP 主要暴露工具，不承载复杂业务逻辑。
2. 业务逻辑应尽量下沉到 sirpapi.py 这类领域层。
3. MCP 层只做参数 schema、对象路由、最小封装和返回格式整理。
4. 对象关系和回写逻辑要以领域模型真实结构为基础，不能在 MCP 层假设不存在的关系。

---