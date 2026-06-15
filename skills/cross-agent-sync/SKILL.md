---
name: cross-agent-sync
description: "Use when adding/modifying skills, memories, or MCP servers in this repository — ensures Claude Code and GitHub Copilot stay in sync. Trigger words: add skill, add memory, remember, add MCP, configure MCP, install plugin, share config, keep in sync."
---

# Cross-Agent Sync

Keep Claude Code and GitHub Copilot sharing the same skills, MCP servers, and persistent memories. When one agent adds something, this skill ensures the other can use it too.

## Current Sharing Architecture

| Resource | Sharing Method | Canonical Location |
|----------|---------------|-------------------|
| **Skills** | 🔗 Symlink (automatic) | `.copilot/skills/` ← `.claude/skills/` |
| **MCP Servers** | 🔄 Manual sync (both files) | `.claude/mcp.json` + `.vscode/mcp.json` |
| **Memory** | 📝 Agent writes to both | `.claude-mem/` (Claude) + `.agentmemory/` (Copilot) |

## Rules

### 1. Skills — Automatic (symlinked)

Skills are fully shared via symlink:
- `.claude/skills/` → `.copilot/skills/`
- `.github/skills/` → `.copilot/skills/` (for commit-shared skills)

**When adding a new skill:** put it in `.copilot/skills/<skill-name>/` — it's instantly available to both agents.

**When modifying a skill:** edit the file in `.copilot/skills/<skill-name>/` — both agents see the change.

**No copying needed.** The symlink handles everything.

### 2. MCP — Manual Sync (two configs)

Two separate MCP config files exist because the format differs slightly:
- `.claude/mcp.json` — Claude Code format (requires `"type": "stdio"` field)
- `.vscode/mcp.json` — VS Code / Copilot format (no `type` field)

**When adding a new MCP server:**

1. Add it to BOTH files with the same server name
2. In `.claude/mcp.json` include `"type": "stdio"`; in `.vscode/mcp.json` omit it
3. Use absolute paths (never `${workspaceFolder}`) for cross-agent compatibility
4. Ensure scripts are executable (`chmod +x`)

**When modifying or removing an MCP server:** update both files.

**Quick check for drift:**
```bash
# List servers in each
python3 -c "import json; d=json.load(open('.claude/mcp.json')); print(*d['mcpServers'].keys(), sep='\n')" | sort > /tmp/claude_mcp.txt
python3 -c "import json; d=json.load(open('.vscode/mcp.json')); print(*d['servers'].keys(), sep='\n')" | sort > /tmp/vscode_mcp.txt
diff /tmp/claude_mcp.txt /tmp/vscode_mcp.txt
```

### 3. Memory — Dual Write

Two memory systems coexist:

**Claude Code memory (claude-mem):**
- Storage: `.claude-mem/` (SQLite via Bun worker)
- Access: `mem-search` skill → `search` / `timeline` / `get_observations` MCP tools
- Worker requires Bun runtime (`~/.npm-global/bin/bun`)

**Copilot memory (agentmemory):**
- Storage: `.agentmemory/`
- Access: `agentmemory` MCP server at `http://127.0.0.1:3111`

**When asked to "remember" or "save" something:**
- Write to BOTH systems using the appropriate tools
- If one system is unavailable, write to the other and note the gap

**When asked to "recall" or "search memory":**
- Search BOTH systems and merge results
- claude-mem: use `search` → `timeline` → `get_observations` workflow
- agentmemory: use the agentmemory MCP tools

**Key memory shared between agents should cover:**
- Repository conventions and path rules
- Experiment status and results
- Parameter decisions and their rationale
- Known issues and workarounds
- Tool/script locations and usage patterns

## Anti-Patterns

- ❌ Adding a skill to `.claude/skills/` directly (it's a symlink — use `.copilot/skills/`)
- ❌ Adding MCP to only one config file
- ❌ Using `${workspaceFolder}` in MCP paths (Claude Code doesn't resolve it)
- ❌ Writing memories to only one system
- ❌ Duplicating skill content instead of updating the shared copy

## Verification Checklist

After any change to skills, MCP, or memory:
- [ ] New skill is in `.copilot/skills/` and visible via `.claude/skills/`
- [ ] Both `.claude/mcp.json` and `.vscode/mcp.json` have the new server
- [ ] MCP scripts are executable
- [ ] Memory entries are accessible from both Claude and Copilot
