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

"""Advanced Runner example with custom tools, event processing, and state management.

This sample demonstrates:
1. Creating custom tools with ToolContext for state management
2. Using Runner with event loop processing
3. Handling different event types (user messages, tool calls, tool responses)
4. Session state persistence across multiple turns
5. Error handling in the event loop
"""

from typing import Any
from google.adk import Agent
from google.adk.tools.tool_context import ToolContext


class TaskManager:
    """A stateful task manager tool that demonstrates persistent state."""

    @staticmethod
    def add_task(task: str, priority: str, tool_context: ToolContext) -> str:
        """Add a task to the task list with priority.

        Args:
            task: The task description.
            priority: Priority level (high, medium, low).
            tool_context: Tool context for accessing session state.

        Returns:
            Confirmation message with task ID.
        """
        # Initialize task list in state if not exists
        if "tasks" not in tool_context.state:
            tool_context.state["tasks"] = []
            tool_context.state["next_task_id"] = 1

        task_id = tool_context.state["next_task_id"]
        task_entry = {
            "id": task_id,
            "description": task,
            "priority": priority,
            "status": "pending",
        }

        tool_context.state["tasks"].append(task_entry)
        tool_context.state["next_task_id"] = task_id + 1

        return f"Task #{task_id} added: '{task}' (Priority: {priority})"

    @staticmethod
    def list_tasks(tool_context: ToolContext) -> str:
        """List all tasks with their current status.

        Args:
            tool_context: Tool context for accessing session state.

        Returns:
            Formatted list of all tasks.
        """
        tasks = tool_context.state.get("tasks", [])

        if not tasks:
            return "No tasks found. Add some tasks to get started!"

        result = "Current Tasks:\n"
        for task in tasks:
            status_icon = {
                "pending": "⏳",
                "completed": "✅",
                "in_progress": "🔄",
            }.get(task["status"], "❓")

            result += (
                f"\n{status_icon} Task #{task['id']}: {task['description']}\n"
            )
            result += f"   Priority: {task['priority']} | Status: {task['status']}"

        return result

    @staticmethod
    def complete_task(task_id: int, tool_context: ToolContext) -> str:
        """Mark a task as completed.

        Args:
            task_id: The ID of the task to complete.
            tool_context: Tool context for accessing session state.

        Returns:
            Confirmation or error message.
        """
        tasks = tool_context.state.get("tasks", [])

        for task in tasks:
            if task["id"] == task_id:
                if task["status"] == "completed":
                    return f"Task #{task_id} is already completed!"
                task["status"] = "completed"
                return f"Task #{task_id} marked as completed: '{task['description']}'"

        return f"Task #{task_id} not found."

    @staticmethod
    def get_statistics(tool_context: ToolContext) -> str:
        """Get task statistics from session state.

        Args:
            tool_context: Tool context for accessing session state.

        Returns:
            Statistics about tasks.
        """
        tasks = tool_context.state.get("tasks", [])

        if not tasks:
            return "No tasks to analyze."

        total = len(tasks)
        completed = sum(1 for t in tasks if t["status"] == "completed")
        pending = sum(1 for t in tasks if t["status"] == "pending")
        in_progress = sum(1 for t in tasks if t["status"] == "in_progress")

        high_priority = sum(1 for t in tasks if t["priority"] == "high")

        stats = f"""Task Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Tasks: {total}
✅ Completed: {completed}
⏳ Pending: {pending}
🔄 In Progress: {in_progress}
🔴 High Priority: {high_priority}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completion Rate: {(completed/total*100):.1f}%"""

        return stats


def calculate_with_history(
    expression: str, tool_context: ToolContext
) -> str:
    """Calculate mathematical expressions and maintain calculation history.

    Args:
        expression: Mathematical expression to evaluate.
        tool_context: Tool context for state access.

    Returns:
        Calculation result with history count.
    """
    import ast
    import operator

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
    }

    def _eval(node: Any) -> float:
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            op = operators.get(type(node.op))
            if op:
                return op(_eval(node.left), _eval(node.right))
            raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree)

        # Track calculation history
        if "calc_history" not in tool_context.state:
            tool_context.state["calc_history"] = []

        tool_context.state["calc_history"].append({
            "expression": expression,
            "result": result,
        })

        history_count = len(tool_context.state["calc_history"])

        return (
            f"Result: {result}\n"
            f"(This is calculation #{history_count} in this session)"
        )
    except Exception as e:
        return f"Error: {str(e)}"


# Create the agent with all tools
root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="task_manager_agent",
    description="Advanced task management assistant with persistent state",
    instruction="""You are an intelligent task management assistant that helps users:
    1. Add and organize tasks with priorities
    2. Track task completion
    3. Provide statistics and insights about productivity
    4. Perform calculations and maintain history

    You have access to task management tools and a calculator.
    Always be helpful, provide clear feedback, and suggest next actions.

    When users add tasks, confirm the details.
    When users ask about their progress, provide statistics and encouragement.""",
    tools=[
        TaskManager.add_task,
        TaskManager.list_tasks,
        TaskManager.complete_task,
        TaskManager.get_statistics,
        calculate_with_history,
    ],
)
