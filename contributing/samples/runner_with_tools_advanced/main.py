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

"""Advanced Runner usage examples demonstrating event loop processing.

This sample shows:
1. Manual Runner setup with services
2. Event loop processing and event type handling
3. State management across multiple turns
4. Error handling and graceful degradation
5. Session inspection and debugging
"""

import asyncio
from typing import Optional

from google.adk.apps.app import App
from google.adk.artifacts.in_memory_artifact_service import (
    InMemoryArtifactService,
)
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.utils.context_utils import Aclosing
from google.genai import types

from . import agent


# Constants for session management
APP_NAME = "TaskManagerApp"
USER_ID = "demo_user"


async def example_basic_runner():
    """Example 1: Basic Runner setup and single query."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Runner Setup")
    print("=" * 70)

    # Step 1: Create services (like your manual code)
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    credential_service = InMemoryCredentialService()

    # Step 2: Create an App (wraps agent with configuration)
    app = App(
        name=APP_NAME,
        root_agent=agent.root_agent,
    )

    # Step 3: Create Runner with services
    runner = Runner(
        app=app,
        session_service=session_service,
        artifact_service=artifact_service,
        credential_service=credential_service,
    )

    # Step 4: Create a session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # Step 5: Run a query
    content = types.Content(
        role="user",
        parts=[types.Part(text="Add a task: Finish the project report with high priority")],
    )

    print(f"\n[User]: {content.parts[0].text}")
    print(f"[Session ID]: {session.id}")
    print("\n[Agent Response]:")

    # Step 6: Process events from the runner
    async with Aclosing(
        runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=content,
        )
    ) as event_stream:
        async for event in event_stream:
            # Print agent's text responses
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"  {part.text}")

    await runner.close()
    print("\n✅ Basic runner example completed")


async def example_event_loop_processing():
    """Example 2: Detailed event loop processing with event type handling."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Event Loop Processing")
    print("=" * 70)

    session_service = InMemorySessionService()
    app = App(name=APP_NAME, root_agent=agent.root_agent)
    runner = Runner(app=app, session_service=session_service)

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    query = "Add three tasks: 1) Code review (high), 2) Team meeting (medium), 3) Email responses (low)"
    print(f"\n[User]: {query}")
    print("\n[Processing Events]:")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    event_count = 0
    tool_calls = 0
    agent_responses = 0

    async with Aclosing(
        runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=content,
        )
    ) as event_stream:
        async for event in event_stream:
            event_count += 1

            # Process different event types
            if event.content and event.content.parts:
                for part in event.content.parts:
                    # Text response from agent
                    if part.text:
                        agent_responses += 1
                        print(f"\n  📝 Agent: {part.text}")

                    # Tool call (function call)
                    elif part.function_call:
                        tool_calls += 1
                        print(
                            f"  🔧 Tool Call: {part.function_call.name}("
                            f"{dict(part.function_call.args)})"
                        )

                    # Tool response
                    elif part.function_response:
                        response_text = str(part.function_response.response.get("result", ""))
                        print(f"  ✅ Tool Result: {response_text[:100]}...")

    print(f"\n[Statistics]:")
    print(f"  Total Events: {event_count}")
    print(f"  Tool Calls: {tool_calls}")
    print(f"  Agent Responses: {agent_responses}")

    await runner.close()
    print("\n✅ Event loop processing completed")


async def example_state_persistence():
    """Example 3: Demonstrate state persistence across multiple turns."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: State Persistence Across Turns")
    print("=" * 70)

    session_service = InMemorySessionService()
    app = App(name=APP_NAME, root_agent=agent.root_agent)
    runner = Runner(app=app, session_service=session_service)

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    queries = [
        "Add a task: Write documentation with high priority",
        "Add a task: Review pull requests with medium priority",
        "List all my tasks",
        "Complete task 1",
        "Show me my task statistics",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n[Turn {i}] User: {query}")
        print("[Agent]:")

        content = types.Content(role="user", parts=[types.Part(text=query)])

        async with Aclosing(
            runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=content,
            )
        ) as event_stream:
            async for event in event_stream:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"  {part.text}")

        # Small delay for readability
        await asyncio.sleep(0.5)

    # Inspect session state
    print("\n[Final Session State]:")
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session.id,
    )
    if session:
        print(f"  Session ID: {session.id}")
        print(f"  Total Events: {len(session.events)}")
        print(f"  State Keys: {list(session.state.keys())}")
        if "tasks" in session.state:
            print(f"  Total Tasks Created: {len(session.state['tasks'])}")

    await runner.close()
    print("\n✅ State persistence example completed")


async def example_error_handling():
    """Example 4: Error handling in the event loop."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Error Handling")
    print("=" * 70)

    session_service = InMemorySessionService()
    app = App(name=APP_NAME, root_agent=agent.root_agent)
    runner = Runner(app=app, session_service=session_service)

    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # Try to complete a non-existent task
    query = "Complete task 999"
    print(f"\n[User]: {query}")
    print("[Agent Response]:")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    try:
        async with Aclosing(
            runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=content,
            )
        ) as event_stream:
            async for event in event_stream:
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            print(f"  {part.text}")
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

    await runner.close()
    print("\n✅ Error handling example completed")


async def example_multiple_sessions():
    """Example 5: Multiple users with separate sessions."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Multiple Users with Separate Sessions")
    print("=" * 70)

    session_service = InMemorySessionService()
    app = App(name=APP_NAME, root_agent=agent.root_agent)
    runner = Runner(app=app, session_service=session_service)

    # Alice's session
    alice_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="alice",
    )

    # Bob's session
    bob_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id="bob",
    )

    # Alice adds a task
    print("\n[Alice's Session]")
    content = types.Content(
        role="user",
        parts=[types.Part(text="Add a task: Prepare presentation with high priority")],
    )

    async with Aclosing(
        runner.run_async(
            user_id="alice",
            session_id=alice_session.id,
            new_message=content,
        )
    ) as event_stream:
        async for event in event_stream:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"  Alice's Agent: {part.text}")

    # Bob adds a different task
    print("\n[Bob's Session]")
    content = types.Content(
        role="user",
        parts=[types.Part(text="Add a task: Bug fix in module X with high priority")],
    )

    async with Aclosing(
        runner.run_async(
            user_id="bob",
            session_id=bob_session.id,
            new_message=content,
        )
    ) as event_stream:
        async for event in event_stream:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"  Bob's Agent: {part.text}")

    # Verify sessions are separate
    alice_final = await session_service.get_session(
        app_name=APP_NAME,
        user_id="alice",
        session_id=alice_session.id,
    )
    bob_final = await session_service.get_session(
        app_name=APP_NAME,
        user_id="bob",
        session_id=bob_session.id,
    )

    print("\n[Session Isolation Verified]:")
    print(f"  Alice's tasks: {len(alice_final.state.get('tasks', []))}")
    print(f"  Bob's tasks: {len(bob_final.state.get('tasks', []))}")

    await runner.close()
    print("\n✅ Multiple sessions example completed")


async def main():
    """Run all examples."""
    print("\n" + "🚀" * 35)
    print("ADVANCED RUNNER WITH TOOLS - ALL EXAMPLES")
    print("🚀" * 35)

    await example_basic_runner()
    await example_event_loop_processing()
    await example_state_persistence()
    await example_error_handling()
    await example_multiple_sessions()

    print("\n" + "=" * 70)
    print("✨ All examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Runner coordinates agent execution with services")
    print("2. Event loop provides fine-grained control over processing")
    print("3. State persists across turns within a session")
    print("4. Multiple users can have isolated sessions")
    print("5. Tools can access and modify session state via ToolContext")


if __name__ == "__main__":
    asyncio.run(main())
