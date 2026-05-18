# Anthropic Multi-Agent Research — Applicable Patterns

Condensed from: https://www.anthropic.com/engineering/built-multi-agent-research-system (Jun 2025)

## Key Findings for Our Orchestrator

### Token Scaling = 80% Performance

- BrowseComp eval: 95% of performance variance explained by token usage (80%) + tool calls + model choice
- Multi-agent uses ~15x more tokens than chat; agents use ~4x
- **Implication for us**: Our 1-delegate budget for daily learning is correct. More delegates = more tokens = better results only for high-value tasks.

### Explicit Delegation Templates (validated)

Anthropic's lead agent must specify for each subagent:
1. Objective
2. Output format
3. Tools and sources to use
4. Task boundaries

Our instruction.md already does this (agent_goal, input evidence, output artifact, time budget, completion marker, fallback plan). **This is validated by Anthropic's production experience.**

### Scale Effort to Query Complexity

| Query type | Agents | Tool calls each |
|---|---:|---:|
| Simple fact-finding | 1 | 3-10 |
| Direct comparison | 2-4 | 10-15 |
| Complex research | 10+ | varies |

**Our equivalent**: Bounded subagent budget table (0-1 daily, 1-2 high-value, 2-3 major). Can consider adding explicit tool-call budget to instruction.md.

### Start Wide, Then Narrow

Agents default to overly specific queries that return few results. Counteract by:
1. Start with short, broad queries
2. Evaluate what's available
3. Progressively narrow focus

**Applicable to our GitHub discovery**: Start with trending API (broad), then deep-read specific repos (narrow).

### Tool Description Self-Improvement

- Tool-testing agent rewrites MCP tool descriptions after testing
- Result: 40% decrease in task completion time for future agents
- **Implication**: Periodically audit our tool/CLI descriptions for agent-friendliness

### Let Agents Improve Themselves

- Claude 4 models can diagnose why an agent fails and suggest prompt improvements
- **Implication**: When delegate_task fails, ask the model to diagnose and suggest template changes (don't just retry blindly)

## Anti-Patterns Observed

- Agents spawning 50 subagents for simple queries
- Agents scouring web for nonexistent sources
- Agents distracting each other with excessive updates
- Vague instructions like "research X" leading to duplicated work

## Not Applicable (Yet)

- Rainbow deployment — we don't have stateful long-running agents
- CitationAgent — not needed for our use case
- Asynchronous subagent execution — our delegate_task is synchronous by design
