# ADK Samples Index

Welcome to the ADK samples directory! This organized collection of 125+ examples helps you learn ADK from basics to advanced production use cases.

## 📚 Learning Path

**New to ADK?** Follow this recommended path:

1. Start with **[01-getting-started](./01-getting-started/)** - Hello World and basics
2. Explore **[02-core-concepts](./02-core-concepts/)** - Fundamental ADK concepts
3. Learn **[03-tools](./03-tools/)** - Tool integration and custom tools
4. Try **[05-multi-agent](./05-multi-agent/)** - Multi-agent orchestration
5. Explore advanced categories based on your needs

## 🗂️ Categories

### Beginner-Friendly

#### [01-getting-started/](./01-getting-started/) (5 samples)
Start here! Basic hello world examples and quickstart guides.
- `hello_world` - Simplest ADK agent
- `hello_world_app` - Using the App abstraction
- `quickstart` - Quick introduction to key features
- `core_basic_config` - Basic configuration patterns
- `runner_debug_example` - Debugging with Runner

#### [02-core-concepts/](./02-core-concepts/) (8 samples)
Essential ADK concepts every developer should know.
- Callbacks and lifecycle hooks
- Session state management
- History management
- Token usage tracking
- Telemetry and monitoring

### Tools & Integrations

#### [03-tools/](./03-tools/) (23 samples across 4 subcategories)
Everything about tools - from built-in to custom integrations.

**[builtin/](./03-tools/builtin/)** - Built-in tool types (6 samples)
- Code execution (built-in, custom, vertex, agent engine)
- Multi-tool usage patterns

**[custom/](./03-tools/custom/)** - Custom tool development (4 samples)
- Function-based tools
- Pydantic arguments
- Parallel function calling

**[human-in-loop/](./03-tools/human-in-loop/)** - Human interaction (3 samples)
- Human-in-the-loop patterns
- Tool confirmation flows

**[integrations/](./03-tools/integrations/)** - Third-party integrations (3 samples)
- LangChain tools
- CrewAI integration

#### [04-mcp-integrations/](./04-mcp-integrations/) (14 samples)
Model Context Protocol integrations for extended capabilities.
- Various MCP transports (stdio, SSE, HTTP)
- MCP server examples
- Cloud service integrations via MCP
- BigQuery via MCP endpoint
- MCP progress callbacks
- MCP toolset authentication

### Multi-Agent Systems

#### [05-multi-agent/](./05-multi-agent/) (9 samples)
Orchestrating multiple agents for complex workflows.
- Basic multi-agent patterns
- Sequential vs loop-based coordination
- Sub-agent configuration
- Workflow patterns

#### [06-live-streaming/](./06-live-streaming/) (7 samples)
Real-time streaming with Live API.
- Bidirectional streaming
- Single vs multi-agent streaming
- Tool callbacks in streaming
- Streaming function call arguments
- Debug utilities

### Advanced Features

#### [07-plugins/](./07-plugins/) (3 samples)
Plugin system for extensibility.
- Basic plugin usage
- Plugin retry mechanisms
- Debug logging plugin

#### [08-llm-providers/](./08-llm-providers/) (13 samples)
Different LLM backend integrations.
- Anthropic, Gemma, Ollama variants
- Gemma3 via Ollama
- LiteLLM integration, streaming, and patterns
- Multi-provider examples

#### [09-data-storage/](./09-data-storage/) (6 samples)
Database and storage integrations.
- BigQuery, Bigtable, Spanner
- PostgreSQL session persistence
- Memory management
- RAG with databases

#### [10-google-cloud/](./10-google-cloud/) (10 samples)
Google Cloud Platform integrations.
- Google APIs usage
- Search integration
- GKE deployment
- Application Integration
- Agent Registry and API Registry
- Conversational Analytics (Data Agent)
- Cloud Pub/Sub

#### [11-authentication/](./11-authentication/) (4 samples)
Authentication and authorization patterns.
- OAuth2 flows
- Service accounts
- All-in-one auth examples

#### [12-a2a-protocol/](./12-a2a-protocol/) (3 samples)
Agent-to-Agent communication protocol.
- Basic A2A setup
- Human-in-loop with A2A
- Root agent patterns

#### [13-advanced-features/](./13-advanced-features/) (16 samples)
Advanced capabilities and optimizations.
- Context caching and offloading
- Artifacts and state management
- Rewind/resume functionality
- Interactions API
- Skills and SkillToolset
- Multimodal outputs
- Structured outputs and schemas
- Computer use
- Static instructions

#### [14-rag-examples/](./14-rag-examples/) (1 sample)
Retrieval-Augmented Generation patterns.
- Basic RAG implementation
- (See also 09-data-storage for database-backed RAG)

#### [15-production/](./15-production/) (10 samples)
Production-ready real-world examples.
- Complete applications (Jira agent, toolbox)
- ADK internal tools (PR agents, triage, stale issue bot, docs)
- Production patterns and best practices

#### [16-utils/](./16-utils/) (4 items)
Utilities and helper scripts.
- Service registration helpers
- Migration tools
- Shared utilities

## 🎯 Find Samples By Use Case

### I want to...

**Get started quickly**
→ [01-getting-started/](./01-getting-started/)

**Build a chatbot with tools**
→ [03-tools/custom/](./03-tools/custom/) + [02-core-concepts/](./02-core-concepts/)

**Connect to external APIs/services**
→ [04-mcp-integrations/](./04-mcp-integrations/) or [10-google-cloud/](./10-google-cloud/)

**Coordinate multiple specialized agents**
→ [05-multi-agent/](./05-multi-agent/)

**Implement real-time streaming**
→ [06-live-streaming/](./06-live-streaming/)

**Use different LLM providers**
→ [08-llm-providers/](./08-llm-providers/)

**Store and retrieve data**
→ [09-data-storage/](./09-data-storage/)

**Build a RAG application**
→ [14-rag-examples/](./14-rag-examples/) + [09-data-storage/](./09-data-storage/)

**Add authentication**
→ [11-authentication/](./11-authentication/)

**Deploy to production**
→ [15-production/](./15-production/)

**Execute code safely**
→ [03-tools/builtin/](./03-tools/builtin/)

**Implement human approval flows**
→ [03-tools/human-in-loop/](./03-tools/human-in-loop/)

## 📊 Statistics

- **Total Samples**: 126
- **Categories**: 16
- **Difficulty Levels**: Beginner (13) → Intermediate (55+) → Advanced (55+)

## 🚀 Running Samples

### Using CLI
```bash
# Run any sample interactively
adk run contributing/samples/<category>/<sample-name>

# Example
adk run contributing/samples/01-getting-started/hello_world
```

### Using Web UI
```bash
# Start web server
adk web contributing/samples

# Navigate to http://localhost:8000/dev-ui/
# Select sample from the categorized list
```

### Using Python
```python
# Import and use directly
from contributing.samples.<category>.<sample_name> import root_agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=root_agent)
await runner.run_debug("Hello!")
```

## 📖 Additional Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [API Reference](https://google.github.io/adk-docs/api/)
- [GitHub Repository](https://github.com/google/adk-python)
- [Community Samples](https://github.com/google/adk-python-community)

## 🤝 Contributing

Want to add a new sample? See [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

*Happy coding! If you have questions, check the [docs](https://google.github.io/adk-docs/) or open an issue.*
