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

## 首个稳定基线

首个稳定版本为 `v1.0.0`。

| 属性 | 值 |
|---|---|
| 载荷目录 | `payload/runtime-receiver` |
| 文件数 | 110 |
| 规范化 SHA-256 | `5fe9a8a3e56398debdb2b4ed2799541954b4a10bb8e3e704f044c998ed8cf4a2` |
| 已部署 Router SHA-256 | `6f8691c439657bf587ba2b20c61a00e935010927b739e3ec0f97c087aa9d2e3c` |
| 治理基线 | R79，封存于 2026-09-04 |
| 运行时合同 | P00、D01、C13、L01、C03、C04、C05 全部通过，重试 0 |

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
```

或：

```powershell
pwsh -NoProfile -File tools/verify-payload.ps1
```

验证器会检查文件集合、大小、逐文件 SHA-256 和规范化载荷摘要。

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

`v1.0.0` 暂不授予开源许可。仓库首先以 private、all-rights-reserved 基线发布，待
后续单独完成许可证和第三方测试夹具审核后，再决定是否公开。
