# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""App with multi-agent orchestration demonstrating sub-agents, plugins, and coordination.

This sample demonstrates:
1. Creating an App with root agent and sub-agents
2. Using plugins for application-wide capabilities
3. Agent coordination and task delegation
4. App-level configuration (context cache, resumability)
5. Complex multi-agent workflows
"""

from google.adk import Agent
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.tools.tool_context import ToolContext


# ============================================================================
# PLUGINS - Application-wide capabilities
# ============================================================================


class LoggerPlugin(BasePlugin):
    """A plugin that logs all agent interactions."""

    def __init__(self):
        super().__init__(name="logger_plugin")
        self.log_entries = []

    async def before_agent_turn(self, context):
        """Log before each agent turn."""
        agent_name = context.get("agent_name", "unknown")
        self.log_entries.append(f"[BEFORE] Agent '{agent_name}' starting turn")

    async def after_agent_turn(self, context):
        """Log after each agent turn."""
        agent_name = context.get("agent_name", "unknown")
        self.log_entries.append(f"[AFTER] Agent '{agent_name}' completed turn")

    def get_logs(self) -> list[str]:
        """Get all log entries."""
        return self.log_entries.copy()


class MetricsPlugin(BasePlugin):
    """A plugin that tracks metrics across all agents."""

    def __init__(self):
        super().__init__(name="metrics_plugin")
        self.metrics = {
            "total_turns": 0,
            "tool_calls": 0,
            "errors": 0,
        }

    async def before_agent_turn(self, context):
        """Increment turn counter."""
        self.metrics["total_turns"] += 1

    async def on_tool_call(self, context):
        """Track tool calls."""
        self.metrics["tool_calls"] += 1

    async def on_error(self, context):
        """Track errors."""
        self.metrics["errors"] += 1

    def get_metrics(self) -> dict:
        """Get current metrics."""
        return self.metrics.copy()


# ============================================================================
# TOOLS - Specialized tools for different agents
# ============================================================================


def research_topic(topic: str, depth: str, tool_context: ToolContext) -> str:
    """Research a topic with specified depth.

    Args:
        topic: The topic to research.
        depth: Depth level (basic, detailed, comprehensive).
        tool_context: Tool context for state access.

    Returns:
        Research findings.
    """
    # Track research history
    if "research_history" not in tool_context.state:
        tool_context.state["research_history"] = []

    research_data = {
        "python best practices": {
            "basic": "Use PEP 8 style guide, write docstrings, use type hints.",
            "detailed": "Follow PEP 8 for style. Write comprehensive docstrings "
            "using Google or NumPy format. Use type hints with mypy. "
            "Implement error handling with specific exceptions.",
            "comprehensive": "PEP 8 compliance, comprehensive documentation, "
            "type hints with mypy strict mode, error handling with custom "
            "exceptions, logging, unit tests with pytest, integration tests, "
            "CI/CD pipelines, code review processes.",
        },
        "machine learning": {
            "basic": "ML is about training models on data to make predictions.",
            "detailed": "ML involves supervised learning (classification, "
            "regression), unsupervised learning (clustering), and "
            "reinforcement learning. Key concepts: training/test split, "
            "feature engineering, model evaluation.",
            "comprehensive": "Comprehensive ML pipeline: data collection, EDA, "
            "feature engineering, model selection (linear models, tree-based, "
            "neural networks), hyperparameter tuning, cross-validation, "
            "ensemble methods, deployment, monitoring.",
        },
    }

    result = research_data.get(topic.lower(), {}).get(
        depth,
        f"Research on '{topic}' at {depth} level: [Simulated research results]",
    )

    tool_context.state["research_history"].append({
        "topic": topic,
        "depth": depth,
        "result": result,
    })

    return result


def write_document(title: str, content: str, tool_context: ToolContext) -> str:
    """Write a document with given title and content.

    Args:
        title: Document title.
        content: Document content.
        tool_context: Tool context for state access.

    Returns:
        Confirmation message.
    """
    if "documents" not in tool_context.state:
        tool_context.state["documents"] = []

    doc_id = len(tool_context.state["documents"]) + 1
    document = {"id": doc_id, "title": title, "content": content}

    tool_context.state["documents"].append(document)

    return f"Document '{title}' created (ID: {doc_id}). Length: {len(content)} chars"


def review_document(doc_id: int, tool_context: ToolContext) -> str:
    """Review a document and provide feedback.

    Args:
        doc_id: The document ID to review.
        tool_context: Tool context for state access.

    Returns:
        Review feedback.
    """
    documents = tool_context.state.get("documents", [])

    for doc in documents:
        if doc["id"] == doc_id:
            content_length = len(doc["content"])

            feedback = f"Document '{doc['title']}' Review:\n"
            feedback += f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            feedback += f"Length: {content_length} characters\n"

            if content_length < 100:
                feedback += "✅ Concise and focused\n"
            elif content_length < 500:
                feedback += "✅ Good level of detail\n"
            else:
                feedback += "⚠️  Very comprehensive\n"

            feedback += "✅ Structure looks good\n"
            feedback += "💡 Suggestion: Consider adding examples\n"

            return feedback

    return f"Document ID {doc_id} not found."


def format_final_output(content: str, format_type: str) -> str:
    """Format content for final output.

    Args:
        content: The content to format.
        format_type: Format type (markdown, html, plain).

    Returns:
        Formatted content.
    """
    if format_type == "markdown":
        return f"# Final Output\n\n{content}\n\n---\n*Generated by Multi-Agent System*"
    elif format_type == "html":
        return f"<html><body><h1>Final Output</h1><p>{content}</p></body></html>"
    else:
        return f"===== FINAL OUTPUT =====\n{content}\n======================="


# ============================================================================
# SUB-AGENTS - Specialized agents for different tasks
# ============================================================================


# Researcher Agent: Gathers information
researcher_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="researcher",
    description="Research specialist that gathers information on topics",
    instruction="""You are a research specialist. When asked to research a topic:
    1. Use the research_topic tool with appropriate depth
    2. Provide comprehensive findings
    3. Cite key points clearly
    4. Suggest areas for deeper investigation if needed

    Always be thorough and accurate.""",
    tools=[research_topic],
)


# Writer Agent: Creates content
writer_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="writer",
    description="Content writer that creates well-structured documents",
    instruction="""You are a professional content writer. When writing:
    1. Create clear, well-structured content
    2. Use appropriate tone and style
    3. Organize information logically
    4. Use the write_document tool to save your work

    Focus on clarity and engagement.""",
    tools=[write_document],
)


# Reviewer Agent: Reviews and provides feedback
reviewer_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="reviewer",
    description="Quality reviewer that provides feedback on documents",
    instruction="""You are a quality reviewer. When reviewing:
    1. Use the review_document tool to analyze documents
    2. Provide constructive feedback
    3. Highlight strengths and areas for improvement
    4. Be specific and actionable in your suggestions

    Maintain a supportive and professional tone.""",
    tools=[review_document],
)


# Editor Agent: Finalizes content
editor_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="editor",
    description="Editor that finalizes and formats content",
    instruction="""You are a professional editor. Your role:
    1. Review all previous work in the conversation
    2. Make final improvements
    3. Format the output using format_final_output tool
    4. Ensure consistency and quality

    Deliver polished, publication-ready content.""",
    tools=[format_final_output],
)


# ============================================================================
# ROOT AGENT - Coordinator
# ============================================================================


# Coordinator Agent: Orchestrates the workflow
coordinator_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="coordinator",
    description="Workflow coordinator that manages the document creation pipeline",
    instruction="""You are a workflow coordinator managing a team of specialists:
    - Researcher: Gathers information
    - Writer: Creates content
    - Reviewer: Provides feedback
    - Editor: Finalizes output

    When given a task:
    1. Analyze what needs to be done
    2. Delegate to appropriate sub-agents in sequence
    3. Ensure each step is completed before moving to the next
    4. Coordinate the overall workflow
    5. Provide status updates

    Example workflow for "Create a document about Python":
    1. Ask Researcher to research Python
    2. Ask Writer to create a document based on research
    3. Ask Reviewer to review the document
    4. Ask Editor to finalize and format

    Be proactive and keep the user informed of progress.""",
    sub_agents=[researcher_agent, writer_agent, reviewer_agent, editor_agent],
)


# ============================================================================
# APP - Complete application with configuration
# ============================================================================


# Create the App with all components
root_app = App(
    name="DocumentCreationPipeline",
    root_agent=coordinator_agent,
    plugins=[
        LoggerPlugin(),
        MetricsPlugin(),
    ],
    resumability_config=ResumabilityConfig(
        is_resumable=True,
    ),
)
