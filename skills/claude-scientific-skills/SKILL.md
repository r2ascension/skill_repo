---
name: claude-scientific-skills
description: Legacy alias for the K-Dense scientific-agent-skills pack. Trigger only as an alias or compatibility layer, then immediately route into `scientific-agent-skills` instead of treating it as a distinct collection.
---

# claude-scientific-skills

Use this collection router when:
- the user explicitly mentions `claude-scientific-skills`
- older notes or prompts refer to the Claude-branded name for the same scientific skill family

Routing guidance:
- Immediately route into `scientific-agent-skills` and choose the relevant child skill there.
- Do not maintain separate routing logic if the scientific-agent-skills child already covers the task.

Merge and precedence notes:
- This is effectively merged into `scientific-agent-skills`.

Examples in this collection:
- scientific-agent-skills/matlab
- scientific-agent-skills/plotly
- scientific-agent-skills/bgpt-paper-search
