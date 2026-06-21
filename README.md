**English** · [中文](README.zh.md)

<h1 align="center">Meeting to Action</h1>

<p align="center">
  <em>"Every meeting ends with three things: who does what, by when, and how we'll know it's done."</em><br>
  <em>「开完会只问三件事：谁干、什么时候交、怎么算完。」</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="https://skills.sh"><img src="https://img.shields.io/badge/skills.sh-Compatible-brightgreen" alt="skills.sh"></a>
  <a href="#"><img src="https://img.shields.io/badge/Agent-Agnostic-blueviolet" alt="Agent Agnostic"></a>
</p>

**Record a meeting → get structured minutes + trackable action items + automatic notifications to every owner.** One command. No more "let's follow up on that" → nobody follows up.

```
npx skills add quzhi-ai/meeting-to-action
```

[Why](#why) · [How it works](#how-it-works) · [Install](#install) · [The Three-Piece Framework](#the-three-piece-framework)

---

## Why

After every meeting, most people: open a note app, jot some bullet points, send to the group chat. Next week? Forgotten.

The problem isn't the note-taking. It's that **normal meeting notes are missing three things**:

| Missing | Consequence |
|---------|-------------|
| No clear **owner** | "Everyone follow up" = nobody follows up |
| No **deadline** | "ASAP" = never |
| No **done criteria** | "Get it done" = can't verify |

Meeting to Action uses a **Three-Piece Framework** to extract every action item with: **Owner + Deadline + Done Criteria (deliverable + reviewer)**. Every meeting decision becomes a trackable commitment.

---

## How It Works

```
Meeting recording (Feishu Minutes / any transcript)
    │
    ▼
Claude Code processes it
    │
    ├─→ Structured minutes    → Feishu Doc (with link)
    ├─→ Action items          → Feishu Bitable (spreadsheet)
    └─→ Notifications         → Feishu IM / Email to each owner
```

The flow:

1. **You** — drop a meeting transcript into Claude Code
2. **Skill** — generates structured minutes → creates a Feishu doc → gives you the link
3. **Skill** — extracts action items using the Three-Piece Framework → shows you for confirmation
4. **You** — confirm (or edit)
5. **Skill** — writes to Feishu Bitable + notifies each responsible person

---

## The Three-Piece Framework

The core methodology. Every action item must have all three — or it's not an action item:

| Piece | Requirement | Good | Bad |
|-------|-------------|------|-----|
| **Owner** | One specific person | Zhang San | "Sales team follows up" |
| **Deadline** | Specific date | 2026-07-01 | "ASAP" / "this week" |
| **Done criteria** | Deliverable + Reviewer | Competitor analysis PPT, approved by Director Li | "Get it done" |

### How to determine the owner (Three Questions)

| Question | Logic |
|----------|-------|
| Who has **execution authority**? | Who can push this to "done"? |
| Who has **information authority**? | Who holds the key context? |
| Who raised it? | Reference only. Raiser ≠ doer. |

**Owner = execution authority ∩ information authority.**

---

## Install

### Quick install

```bash
npx skills add quzhi-ai/meeting-to-action
```

### Manual install

```bash
git clone https://github.com/quzhi-ai/meeting-to-action.git
cp -r meeting-to-action /your/project/.claude/skills/
```

### Setup (5 steps)

1. **Install Claude Code** — `npm install -g @anthropic-ai/claude-code`
2. **Install lark-cli** — `npm install -g lark-cli && lark-cli profile add`
3. **Create a Feishu Bitable** — see [docs/bitable-setup.md](docs/bitable-setup.md) for the column structure
4. **Fill in config** — `cp config.example.yaml config.yaml` and edit
5. **Verify** — `pip install -r requirements.txt && python3 scripts/check_setup.py`

---

## Usage

```
Help me process this meeting @transcript.txt
```

Or paste the transcript directly:

```
Process this meeting:

[paste transcript here]
```

---

## Project Structure

```
meeting-to-action/
├── SKILL.md              # The skill definition (read by Claude / any agent)
├── config.example.yaml   # Configuration template
├── requirements.txt      # Python dependencies (pyyaml)
├── scripts/
│   ├── write_todos.py    # Write action items to Feishu Bitable
│   ├── notify.py         # Send notifications (IM / email)
│   └── check_setup.py    # Environment check
├── templates/
│   └── email_todo.html   # Email notification template
└── docs/
    └── bitable-setup.md  # Bitable column setup guide
```

---

## Support

If this skill helps you, buy the author a coffee:

| WeChat Pay | Alipay |
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

## License

MIT — see [LICENSE](LICENSE)

---

<p align="center">
  <a href="https://x.com/quzhiai"><img src="https://img.shields.io/badge/X%20%2F%20Twitter-@quzhiai-black?logo=x&logoColor=white" alt="X / Twitter"></a>
</p>

<p align="center">
  <em>Every meeting should end with commitments, not just conversations.</em><br>
  <em>开完会留下的应该是承诺，不是口水。</em>
</p>
