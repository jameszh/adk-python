# Advanced ADK Samples: Runner and App Usage

This document provides an overview of the advanced samples demonstrating core ADK concepts: **Runner**, **App**, **tools**, **sub-agents**, and **event loop processing**.

## Overview

These samples bridge the gap between basic examples and production usage by showing:

1. How `adk run` and `adk web` abstract the Runner pattern
2. Manual Runner setup for fine-grained control
3. App usage for complex multi-agent systems
4. Event loop processing for custom workflows
5. State management and session handling

## Samples

### 1. Runner with Tools Advanced
📁 `contributing/samples/runner_with_tools_advanced/`

**What it demonstrates:**
- Manual Runner setup with custom services
- Event loop processing with different event types
- Custom tools with ToolContext for state management
- Multi-turn conversations with state persistence
- Multiple isolated user sessions

**Key concepts:**
- `Runner` class and its role
- Event stream processing (`run_async()`)
- `ToolContext` for accessing session state
- Session service integration

**When to use this pattern:**
- Building custom CLI tools
- Creating specialized workflows
- Fine-grained control over execution
- Custom event processing logic

**Try it:**
```bash
# Interactive mode
adk run contributing/samples/runner_with_tools_advanced

# Run all examples
python -m contributing.samples.runner_with_tools_advanced.main
```

---

### 2. App with Multi-Agent Orchestration
📁 `contributing/samples/app_multi_agent_orchestration/`

**What it demonstrates:**
- App as a container for agents and configuration
- Multi-agent coordination with coordinator pattern
- Plugins for application-wide capabilities
- Sub-agent specialization and task delegation
- App-level configuration (resumability)

**Key concepts:**
- `App` class structure
- Coordinator pattern for multi-agent systems
- Plugins for cross-cutting concerns
- Sub-agents and task delegation
- App-wide configuration

**When to use this pattern:**
- Complex multi-agent systems
- Production applications
- Shared capabilities across agents
- Application-wide settings

**Try it:**
```bash
# Interactive mode
adk run contributing/samples/app_multi_agent_orchestration

# Run all examples
python -m contributing.samples.app_multi_agent_orchestration.main
```

---

## Conceptual Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Manual Code                          │
│  session_service = InMemorySessionService()                  │
│  agent = LlmAgent.builder().build()                          │
│  runner = Runner(agent, session_service, ...)                │
│  events = runner.run(user_id, session_id, new_message)       │
└─────────────────────────────────────────────────────────────┘
                         ↑
                    Abstracted by
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              Sample 1: runner_with_tools_advanced            │
│  Shows HOW the Runner works internally                       │
│  - Event loop processing                                     │
│  - State management                                          │
│  - Tool integration                                          │
└─────────────────────────────────────────────────────────────┘
                         ↑
                  Used by / Wrapped by
                         ↓
┌─────────────────────────────────────────────────────────────┐
│         Sample 2: app_multi_agent_orchestration              │
│  Shows HOW to structure complex applications                 │
│  - App wraps Runner usage                                    │
│  - Multi-agent coordination                                  │
│  - Plugins and shared capabilities                           │
└─────────────────────────────────────────────────────────────┘
                         ↑
                   Used by
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  adk run / adk web                           │
│  Commands that use App + Runner automatically                │
└─────────────────────────────────────────────────────────────┘
```

## Comparison Matrix

| Feature | Runner Sample | App Sample | `adk run/web` |
|---------|--------------|------------|---------------|
| **Setup Complexity** | Manual | Moderate | Automatic |
| **Control Level** | Full | High | Minimal |
| **Multi-Agent** | Manual coordination | Built-in coordinator | Automatic |
| **Plugins** | Manual | Built-in | Configurable |
| **Use Case** | Custom workflows | Production apps | Quick testing |
| **Event Processing** | Full access | Full access | Abstracted |
| **State Management** | Manual | Managed | Managed |

## Key Classes and Their Relationships

### Runner
- **Purpose**: Execution engine that runs agents
- **Manages**: Services (session, artifact, credential)
- **Provides**: Event loop for processing
- **Used by**: Both samples and CLI commands

### App
- **Purpose**: Container for application configuration
- **Contains**: Root agent, plugins, app-wide config
- **Benefits**: Encapsulation, shared configuration
- **Used by**: App sample and production systems

### Event Loop
- **Purpose**: Process agent execution events
- **Provides**: Fine-grained control
- **Types**: User messages, tool calls, tool responses, agent text
- **Used by**: Custom processing logic

### ToolContext
- **Purpose**: Provides tools access to session state
- **Enables**: Stateful tools, data persistence
- **Scoped to**: Current session
- **Used by**: Tools that need state

## Learning Path

1. **Start here**: Basic samples (hello_world, etc.)
2. **Then**: `runner_with_tools_advanced` to understand Runner internals
3. **Next**: `app_multi_agent_orchestration` to see App usage
4. **Finally**: Build your own production application

## Example Workflows

### Custom CLI Tool (Use Runner Sample Pattern)
```python
# You have full control over event processing
session_service = InMemorySessionService()
runner = Runner(agent=agent, session_service=session_service)

async for event in runner.run_async(...):
    # Custom event processing
    if event.content:
        # Do something specific with events
        pass
```

### Production Application (Use App Sample Pattern)
```python
# App provides structure and configuration
app = App(
    name="MyApp",
    root_agent=coordinator,
    sub_agents=[specialist1, specialist2],
    plugins=[logger, metrics],
    resumability_config=ResumabilityConfig(is_resumable=True),
)

runner = Runner(app=app, session_service=session_service)
# App configuration automatically applies to all agents
```

### Quick Testing (Use CLI)
```bash
# Just use the CLI for quick iteration
adk run path/to/agent
```

## Common Patterns

### Pattern 1: Stateful Tools
```python
def my_tool(arg: str, tool_context: ToolContext) -> str:
    # Access session state
    if "history" not in tool_context.state:
        tool_context.state["history"] = []

    # Modify state
    tool_context.state["history"].append(arg)

    return f"Processed {arg}"
```

### Pattern 2: Event Filtering
```python
async for event in runner.run_async(...):
    if event.content and event.content.parts:
        for part in event.content.parts:
            if part.function_call:
                # Process only tool calls
                handle_tool_call(part.function_call)
```

### Pattern 3: Multi-Agent Coordination
```python
coordinator = Agent(
    name="coordinator",
    sub_agents=[researcher, writer, reviewer],
    instruction="Delegate to specialists based on task type"
)

app = App(name="Pipeline", root_agent=coordinator)
```

## FAQs

**Q: When should I use Runner directly vs App?**
A: Use Runner for simple agents or custom workflows. Use App when you have multiple agents, need plugins, or want app-wide configuration.

**Q: Can I use both patterns together?**
A: Yes! App wraps agents, and Runner executes the App. They work together.

**Q: Do I need to understand Runner to use App?**
A: Not necessarily, but understanding Runner helps when debugging or building custom workflows.

**Q: How does this relate to `adk run` and `adk web`?**
A: Those commands use these patterns internally. They're convenience wrappers around Runner and App.

**Q: Which pattern should production apps use?**
A: Production apps should typically use the App pattern with proper service configuration (database session service, etc.)

## Next Steps

1. **Try the samples** in order (Runner → App)
2. **Modify the samples** to understand the patterns
3. **Read the inline documentation** in each sample
4. **Build your own** using these patterns as templates

## Additional Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Core Concepts](https://google.github.io/adk-docs/core-concepts/)
- [Runners Guide](https://google.github.io/adk-docs/core-concepts/runners/)
- [Apps Guide](https://google.github.io/adk-docs/core-concepts/app/)
- [Multi-Agent Systems](https://google.github.io/adk-docs/guides/multi-agent/)

## Contributing

Found issues or have improvements? See [CONTRIBUTING.md](./CONTRIBUTING.md)
