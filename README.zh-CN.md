# Governed Research Skills

> 面向 AI 智能体的可审计科研工作流。

Governed Research Skills 是一套版本化的科研 Skill 运行时，将统一控制路由与
文献综合、学术检索、论文阅读、科研写作及领域委派能力组织在一个可复现载荷中。

项目重点关注：

- 确定性的路由合同；
- 明确的所有权和委派边界；
- 必要能力缺失时失败关闭；
- 可逐字节复现的发布载荷；
- 尽可能离线的验证；
- 基于证据和独立审核的治理流程。

## 稳定基线

当前稳定版本为 `v1.0.1`；不可变的 `v1.0.0` 标签仍是首个稳定基线。

| 属性 | 值 |
|---|---|
| 载荷目录 | `payload/runtime-receiver` |
| 文件数 | 110 |
| 规范化 SHA-256 | `93b1432db6589793a4e221b9357a4ac45bc923c3cc8b661582e3f748fddcc839` |
| 已部署 Router SHA-256 | `6f8691c439657bf587ba2b20c61a00e935010927b739e3ec0f97c087aa9d2e3c` |
| 治理基线 | R79 运行时基线；R81 打包与许可证审核 |
| 运行时合同 | 继承 `v1.0.0` 的七会话 PASS 证据；本次仅替换夹具，未重跑模型会话 |

规范化摘要只覆盖 `payload/runtime-receiver` 下的 110 个文件，不包含仓库说明、
工作流或发布元数据。

## 包含的组件

- `research-workflow-router`：唯一隐式科研控制 Router；
- `nature-research-router`：Nature 风格多阶段科研任务的显式 Router；
- `quant-workflow-router`：量化研究任务的显式 Router；
- `stats-experiment-router`：实验设计和统计任务的显式 Router；
- `literature-synthesis`：基于已提供或合法可访问来源的跨论文证据综合；
- `nature-academic-search`：学术检索、引文核验和引用文件管理；
- `nature-literature-pipeline`：显式调用的文献监测流程合同；
- `nature-reader`：保留来源锚点和图表位置的双语论文阅读；
- `researchwrite`：基于用户证据的研究计划和科研写作。

部分 Router 会描述本版本未打包的可选 specialist。能力缺失时不得模拟执行，必须
明确披露或失败关闭。

## 验证

```bash
python tools/verify_payload.py
python tools/audit_release.py
```

或：

```powershell
pwsh -NoProfile -File tools/verify-payload.ps1
```

载荷验证器会检查文件集合、大小、逐文件 SHA-256 和规范化摘要；发布审核器会
检查 Apache-2.0 原文、许可元数据、出版方内容残留和合成夹具转换一致性。

## 安装边界

需要安装的 Skill 位于：

```text
payload/runtime-receiver/.agents/skills/<skill-name>
```

只复制实际需要的 Skill 目录。不要把 `payload/runtime-receiver/AGENTS.md` 安装成
全局配置；它只是用于复现运行时合同的只读隔离验收 envelope。

仓库不会自动安装依赖、注册 MCP、开放网络、修改 Skill Manager、接入 Kimi 或
启用系统 Default。

## 平台边界

大部分内容由平台无关的 Markdown 和 Python 构成。`nature-academic-search` 的受控
引用文件 writer 仅支持 Windows；在非 Windows 平台明确失败关闭，不得用普通文件
写入绕过。

## 限制与声明

- 不提供投资建议或交易建议；
- 不保证科研结论、创新性或发表结果；
- 不代表所有可委派 specialist 均已打包；
- 不代表与 OpenAI、Nature Portfolio、AAAS、Cell Press 或其他平台存在官方关系；
- R79 的本机路径、原始模型响应、回滚备份和内部治理报告不进入本仓库。

## 许可证

`v1.0.1` 采用 Apache License 2.0。先前的 `v1.0.0` 标签仍适用该标签中提交的
许可证文本。详见根目录 `LICENSE`、`NOTICE`、`THIRD_PARTY_NOTICES.md` 和
`governance/LICENSE-AUDIT.md`。仓库当前仍保持 private；许可证与可见性是两个
独立设置。
