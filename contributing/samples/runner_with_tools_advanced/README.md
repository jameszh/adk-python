# Advanced Runner with Tools and Event Loop

This sample demonstrates advanced usage of the ADK `Runner` class with custom tools, event processing, and state management.

## What You'll Learn

1. **Manual Runner Setup**: How to create and configure a Runner with custom services
2. **Event Loop Processing**: Processing different event types in the runner's event stream
3. **State Management**: Using ToolContext to persist state across conversation turns
4. **Session Handling**: Managing multiple users with isolated sessions
5. **Error Handling**: Gracefully handling errors in the event loop

## Features Demonstrated

### Custom Tools with State
- Task management tools that persist state across turns
- Calculator with calculation history tracking
- Tools using `ToolContext` to access and modify session state

### Event Loop Processing
- Handling different event types (text, function calls, function responses)
- Counting and categorizing events
- Processing events in real-time

### Multi-Turn Conversations
- State persistence across multiple queries
- Session inspection and debugging
- Multiple isolated user sessions

## Running the Sample

### Using the CLI
```bash
# Run interactively
adk run contributing/samples/runner_with_tools_advanced

# Run all examples programmatically
python -m contributing.samples.runner_with_tools_advanced.main
```

### Using the Web UI
```bash
# Start the dev server
adk web contributing/samples/

# Navigate to http://localhost:8000/dev-ui/
# Select "runner_with_tools_advanced" from the agents list
```

## Code Structure

```
runner_with_tools_advanced/
├── agent.py       # Agent definition with custom tools
├── main.py        # Five comprehensive examples
├── __init__.py    # Package initialization
└── README.md      # This file
```

## Example Outputs

### Example 1: Basic Runner Setup
Shows the fundamental pattern of creating services, app, runner, and processing events.

### Example 2: Event Loop Processing
Demonstrates detailed event handling with statistics on tool calls and responses.

### Example 3: State Persistence
Shows how state persists across multiple turns:
- Add tasks
- List tasks
- Complete tasks
- View statistics

### Example 4: Error Handling
Demonstrates graceful error handling when tools encounter issues.

### Example 5: Multiple Sessions
Shows how different users maintain isolated sessions.

## Key Concepts

### Runner
The `Runner` class is the execution engine that:
- Coordinates agent execution
- Manages services (session, artifact, credential)
- Provides the event loop for processing

### ToolContext
Allows tools to:
- Access session state
- Modify state that persists across turns
- Share data between tool calls

### Event Stream
The `run_async()` method returns an async generator of events:
```python
async with Aclosing(runner.run_async(...)) as event_stream:
    async for event in event_stream:
        # Process event
```

## Related Samples

- `runner_debug_example` - Simplified runner usage with `run_debug()`
- `app_multi_agent_orchestration` - Using App with sub-agents
- `multi_agent_loop_config` - Multi-agent coordination patterns

## Learn More

- [ADK Runners Documentation](https://google.github.io/adk-docs/core-concepts/runners/)
- [Custom Tools Guide](https://google.github.io/adk-docs/tools/custom-tools/)
- [State Management](https://google.github.io/adk-docs/core-concepts/state/)
