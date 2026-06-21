[English](README.md) · **中文**

<h1 align="center">Meeting to Action</h1>

<p align="center">
  <em>「开完会只问三件事：谁干、什么时候交、怎么算完。」</em><br>
  <em>"Every meeting ends with three things: who does what, by when, and how we'll know it's done."</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://skills.sh"><img src="https://img.shields.io/badge/skills.sh-Compatible-brightgreen" alt="skills.sh"></a>
  <a href="#"><img src="https://img.shields.io/badge/Agent-Agnostic-blueviolet" alt="Agent Agnostic"></a>
</p>

**录完会，一条指令：结构化纪要 + 可追踪待办 + 自动通知责任人。** 不再"大家跟进一下"然后石沉大海。

```
npx skills add quzhi-ai/meeting-to-action
```

[为什么需要](#为什么需要) · [怎么运作](#怎么运作) · [安装](#安装) · [三件套框架](#三件套框架) · [使用方法](#使用方法)

---

## 为什么需要

开完会，你做了什么？

大多数人：打开备忘录，抄几个要点，发到群里。下周呢？忘了。

问题不在记录，在于**普通会议笔记缺三样东西**：

| 缺什么 | 后果 |
|--------|------|
| 没有明确**负责人** | "大家跟进一下" = 没人跟进 |
| 没有**截止日期** | "尽快处理" = 永远不处理 |
| 没有**完成标准** | "把这事搞定" = 没法验收 |

Meeting to Action 用**三件套框架**提取每条待办：**负责人 + 截止日期 + 完成标准（产出物 + 验收人）**。让每个会议决定变成可追踪的承诺。

---

## 怎么运作

```
会议录音（飞书妙记 / 任意转写文本）
    │
    ▼
Claude Code 处理
    │
    ├─→ 结构化纪要    → 飞书文档（给你链接）
    ├─→ 待办事项      → 飞书多维表格（可追踪）
    └─→ 通知负责人    → 飞书 IM / 邮件
```

完整流程：

1. **你** — 把会议转写文本丢给 Claude Code
2. **Skill** — 生成结构化纪要 → 创建飞书文档 → 给你链接
3. **Skill** — 用三件套框架提取待办 → 列出来让你确认
4. **你** — 确认（或修改）
5. **Skill** — 写入飞书多维表格 + 给每个负责人发通知

全程你只需要两个动作：丢文件 + 点确认。

---

## 三件套框架

这是整个 Skill 的核心方法论。每条待办必须满足三件套，否则不算待办：

| 要素 | 要求 | 正例 | 反例 |
|------|------|------|------|
| **负责人** | 具体到人（不模糊到部门） | 张三 | "销售部跟进" |
| **截止日期** | 具体日期 | 2026-07-01 | "尽快" / "本周" |
| **完成标准** | 产出物 + 验收人 | 竞品分析 PPT，李总确认 | "把这事搞定" |

### 怎么判断谁是负责人（归口三问）

会议里经常出现"大家一起推进"。判断真正的负责人，问三个问题：

| 问题 | 逻辑 |
|------|------|
| **谁有执行权？** | 谁能把这事推到"完成"？ |
| **谁有信息权？** | 谁掌握执行所需的关键信息？ |
| **谁提出的？** | 仅作参考。提出者 ≠ 执行者 |

**主责人 = 执行权 ∩ 信息权**。提出者如果不是主责，标为"协同方"。

### 完成标准怎么写

完成标准 = **交什么** + **谁来验收**

| 交什么（产出物） | 谁验收 |
|-----------------|--------|
| 竞品分析 PPT | 产品总监 |
| 报价方案 Excel | 客户确认 |
| 流程 SOP 文档 | 部门经理 |
| 原型设计稿 | 产品经理 |

没有产出物的"待办"不是待办——"了解一下""跟进一下"要么转成具体产出物，要么不列。

---

## 安装

### 一键安装

```bash
npx skills add quzhi-ai/meeting-to-action
```

### 手动安装

```bash
git clone https://github.com/quzhi-ai/meeting-to-action.git
cp -r meeting-to-action /your/project/.claude/skills/
```

### 5 步配置

#### 1. 安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

#### 2. 安装 lark-cli

```bash
npm install -g lark-cli

# 添加你的飞书应用 profile
lark-cli profile add
```

> 飞书应用需要的权限：`bitable:app`（多维表格）、`docs:doc`（文档）、`im:message`（消息）
>
> 在[飞书开放平台](https://open.feishu.cn) → 创建应用 → 权限管理中开启

#### 3. 创建飞书多维表格

在飞书中新建一个多维表格，按照 [docs/bitable-setup.md](docs/bitable-setup.md) 创建字段结构。

#### 4. 填写配置

```bash
cp config.example.yaml config.yaml
# 编辑 config.yaml，填入：
# - 飞书 profile 名称
# - 文档文件夹 token
# - 多维表格 token 和 table_id
# - 通知联系人（飞书 IM 或邮箱）
```

#### 5. 验证

```bash
pip install -r requirements.txt
python3 scripts/check_setup.py --config config.yaml
```

全部 PASS 就可以用了。

---

## 使用方法

在 Claude Code 中，把会议转写丢过来：

```
帮我整理这个会议 @transcript.txt
```

或者直接粘贴：

```
整理一下这个会议：

[粘贴会议转写内容]
```

触发词：`整理会议` / `会议记录` / `开完会` / `出纪要` / `处理会议` / `整理一下`

---

## 通知方式

支持两种通知渠道，在 `config.yaml` 中配置：

| 方式 | 优势 | 配置复杂度 |
|------|------|-----------|
| **飞书 IM**（推荐） | 消息即时到达，点开就看 | 低（只需 open_id） |
| **邮件** | 正式，可追溯 | 中（需 SMTP 凭证） |

两种可以同时开启。

---

## 项目结构

```
meeting-to-action/
├── SKILL.md              # Skill 定义（Claude / 任意 agent 读取）
├── config.example.yaml   # 配置模板
├── requirements.txt      # Python 依赖
├── scripts/
│   ├── write_todos.py    # 写入飞书多维表格
│   ├── notify.py         # 发通知（IM / 邮件）
│   └── check_setup.py    # 环境检查
├── templates/
│   └── email_todo.html   # 邮件通知模板
└── docs/
    └── bitable-setup.md  # 多维表格配置指南
```

---

## 支持项目

如果这个 Skill 对你有帮助，可以请作者喝杯咖啡：

| 微信支付 | 支付宝 |
|:---:|:---:|
| <img src="demos/donate/wechat-pay.jpg" width="200"> | <img src="demos/donate/alipay.jpg" width="200"> |

## Star History

<p align="center">
  <a href="https://star-history.com/#quzhi-ai/meeting-to-action&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=quzhi-ai/meeting-to-action&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=quzhi-ai/meeting-to-action&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=quzhi-ai/meeting-to-action&type=Date" width="600" />
    </picture>
  </a>
</p>

## 许可证

MIT — 见 [LICENSE](LICENSE)

---

<p align="center">
  <a href="https://x.com/quzhiai"><img src="https://img.shields.io/badge/X%20%2F%20Twitter-@quzhiai-black?logo=x&logoColor=white" alt="X / Twitter"></a>
</p>

<p align="center">
  <em>开完会留下的应该是承诺，不是口水。</em><br>
  <em>Every meeting should end with commitments, not just conversations.</em>
</p>
