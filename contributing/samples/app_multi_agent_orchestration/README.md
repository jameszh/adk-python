# App with Multi-Agent Orchestration

This sample demonstrates advanced usage of the ADK `App` class with multi-agent orchestration, plugins, and app-wide configuration.

## What You'll Learn

1. **App Structure**: How to create an App with root agent and sub-agents
2. **Sub-Agent Orchestration**: Coordinator pattern for managing specialized agents
3. **Plugins**: Application-wide capabilities shared across all agents
4. **App-Level Configuration**: Resumability and other app-wide settings
5. **Complex Workflows**: Real-world multi-step task delegation

## Architecture

```
App (DocumentCreationPipeline)
├── Root Agent: Coordinator
│   └── Sub-Agents:
│       ├── Researcher  (gathers information)
│       ├── Writer      (creates content)
│       ├── Reviewer    (provides feedback)
│       └── Editor      (finalizes output)
├── Plugins:
│   ├── LoggerPlugin    (logs all interactions)
│   └── MetricsPlugin   (tracks metrics)
└── Config:
    └── ResumabilityConfig (enables pause/resume)
```

## Features Demonstrated

### Multi-Agent Coordination
- **Coordinator Agent**: Routes tasks to appropriate specialists
- **Specialized Sub-Agents**: Each agent has specific tools and responsibilities
- **Sequential Workflow**: Tasks flow through agents in logical order

### Plugins
- **LoggerPlugin**: Tracks all agent interactions
- **MetricsPlugin**: Collects metrics (turns, tool calls, errors)
- **Shared Access**: All agents can use plugin capabilities

### App-Wide Configuration
- **Resumability**: Pause and resume long-running operations
- **Consistent Settings**: Configuration applies to all agents in the hierarchy

### State Management
- Research history tracked across agents
- Documents created and stored in session state
- Shared context maintained throughout workflow

## Running the Sample

### Using the CLI
```bash
# Run interactively
adk run contributing/samples/app_multi_agent_orchestration

# Run all examples programmatically
python -m contributing.samples.app_multi_agent_orchestration.main
```

### Using the Web UI
```bash
# Start the dev server
adk web contributing/samples/

# Navigate to http://localhost:8000/dev-ui/
# Select "app_multi_agent_orchestration"
```

## Code Structure

```
app_multi_agent_orchestration/
├── agent.py       # App with coordinator, sub-agents, and plugins
├── main.py        # Five comprehensive examples
├── __init__.py    # Package initialization
└── README.md      # This file
```

## Workflow Example

When you ask: "Create a document about Python best practices"

1. **Coordinator** analyzes the task
2. **Researcher** gathers information about Python best practices
3. **Writer** creates a document based on research findings
4. **Reviewer** reviews the document and provides feedback
5. **Editor** finalizes and formats the output

Each agent has specialized tools and instructions for their role.

## Key Concepts

### App vs Agent

| Concept | Purpose | Contains |
|---------|---------|----------|
| **Agent** | Specific task executor | Model, tools, instructions, sub-agents |
| **App** | Application container | Root agent + plugins + config |

### Why Use App?

```python
# Without App - verbose
runner = Runner(
    app_name="MyApp",
    agent=coordinator,
    plugins=[logger, metrics],
    session_service=session_service,
)

# With App - cleaner
app = App(
    name="MyApp",
    root_agent=coordinator,
    plugins=[logger, metrics],
)
runner = Runner(app=app, session_service=session_service)
```

### Plugin Benefits

Plugins provide cross-cutting concerns:
- ✅ Logging all agent interactions
- ✅ Collecting metrics across agents
- ✅ Authentication/authorization
- ✅ Rate limiting
- ✅ Custom telemetry

### Coordinator Pattern

The coordinator agent:
1. Receives high-level user requests
2. Breaks down into subtasks
3. Delegates to specialized sub-agents
4. Aggregates results
5. Provides final response

## Example Outputs

### Example 1: Basic App Usage
Shows how to create and use an App with Runner.

### Example 2: Multi-Agent Workflow
Demonstrates a complete workflow with task delegation across multiple agents.

### Example 3: Plugin Access
Shows how to access plugin data (logs, metrics) after execution.

### Example 4: Session State Inspection
Inspects session state to see research history and created documents.

### Example 5: Resumability
Demonstrates app-level resumability configuration.

## Related Samples

- `runner_with_tools_advanced` - Advanced Runner usage with tools
- `multi_agent_loop_config` - Multi-agent loop patterns
- `plugin_basic` - Basic plugin usage
- `sub_agents_config` - Sub-agent configuration patterns

## Best Practices

1. **Use App for Complex Systems**: When you have multiple agents and plugins
2. **Coordinator Pattern**: Use a coordinator agent to manage sub-agents
3. **Specialized Agents**: Give each agent a specific role and tools
4. **Plugins for Cross-Cutting**: Use plugins for capabilities shared across agents
5. **App-Level Config**: Set configurations that apply to all agents

## Learn More

- [ADK App Documentation](https://google.github.io/adk-docs/core-concepts/app/)
- [Multi-Agent Systems](https://google.github.io/adk-docs/guides/multi-agent/)
- [Plugins Guide](https://google.github.io/adk-docs/plugins/)
- [Sub-Agents](https://google.github.io/adk-docs/core-concepts/sub-agents/)
