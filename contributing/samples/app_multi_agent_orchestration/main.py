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

"""Examples demonstrating App usage with multi-agent orchestration.

This sample shows:
1. Using App to wrap agents with app-wide configuration
2. Sub-agent coordination through a coordinator agent
3. Plugin usage for cross-cutting concerns
4. Accessing plugin data after execution
5. Complex multi-agent workflows
"""

import asyncio

from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.utils.context_utils import Aclosing
from google.genai import types

from . import agent


APP_NAME = "DocumentPipeline"
USER_ID = "demo_user"


async def example_basic_app_usage():
    """Example 1: Basic App usage with Runner."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic App Usage")
    print("=" * 70)

    # Create runner with the App
    # The App already contains the root agent and plugins
    session_service = InMemorySessionService()
    runner = Runner(
        app=agent.root_app,  # ← Pass the complete App
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name=agent.root_app.name,  # Use app name from App
        user_id=USER_ID,
    )

    query = "Hello! What can you help me with?"
    print(f"\n[User]: {query}")
    print("[Coordinator]:")

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

    await runner.close()
    print("\n✅ Basic app usage completed")


async def example_multi_agent_workflow():
    """Example 2: Complete multi-agent workflow with task delegation."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Multi-Agent Workflow")
    print("=" * 70)

    session_service = InMemorySessionService()
    runner = Runner(app=agent.root_app, session_service=session_service)

    session = await session_service.create_session(
        app_name=agent.root_app.name,
        user_id=USER_ID,
    )

    query = "Create a comprehensive document about Python best practices"
    print(f"\n[User]: {query}")
    print("\n[Multi-Agent Workflow]:\n")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    current_agent = None
    async with Aclosing(
        runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=content,
        )
    ) as event_stream:
        async for event in event_stream:
            # Track which agent is speaking
            if event.author and event.author != current_agent:
                current_agent = event.author
                print(f"\n>>> {current_agent.upper()} <<<")

            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        # Truncate long responses for readability
                        text = part.text
                        if len(text) > 200:
                            text = text[:200] + "..."
                        print(f"  {text}")
                    elif part.function_call:
                        print(f"  🔧 Calling: {part.function_call.name}")

    await runner.close()
    print("\n✅ Multi-agent workflow completed")


async def example_plugin_access():
    """Example 3: Accessing plugin data after execution."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Plugin Data Access")
    print("=" * 70)

    session_service = InMemorySessionService()
    runner = Runner(app=agent.root_app, session_service=session_service)

    session = await session_service.create_session(
        app_name=agent.root_app.name,
        user_id=USER_ID,
    )

    # Run a simple query
    query = "Research machine learning basics"
    print(f"\n[User]: {query}")

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
                        # Only print first 100 chars
                        print(f"  {part.text[:100]}...")

    # Access plugin data
    print("\n[Plugin Data]:")

    # Access logger plugin
    logger_plugin = agent.root_app.plugins[0]
    logs = logger_plugin.get_logs()
    print(f"\nLogger Plugin - Total Log Entries: {len(logs)}")
    print("Recent logs:")
    for log in logs[-5:]:  # Last 5 logs
        print(f"  {log}")

    # Access metrics plugin
    metrics_plugin = agent.root_app.plugins[1]
    metrics = metrics_plugin.get_metrics()
    print(f"\nMetrics Plugin:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    await runner.close()
    print("\n✅ Plugin access completed")


async def example_session_state_inspection():
    """Example 4: Inspecting session state with documents and research."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Session State Inspection")
    print("=" * 70)

    session_service = InMemorySessionService()
    runner = Runner(app=agent.root_app, session_service=session_service)

    session = await session_service.create_session(
        app_name=agent.root_app.name,
        user_id=USER_ID,
    )

    # Execute a workflow that creates artifacts
    query = "Research Python and create a short document about it"
    print(f"\n[User]: {query}\n")

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
                    if part.text and len(part.text) > 0:
                        # Print shortened responses
                        text = part.text[:150]
                        if len(part.text) > 150:
                            text += "..."
                        print(f"[{event.author}]: {text}")

    # Inspect final session state
    final_session = await session_service.get_session(
        app_name=agent.root_app.name,
        user_id=USER_ID,
        session_id=session.id,
    )

    print("\n[Final Session State]:")
    print(f"  Total Events: {len(final_session.events)}")
    print(f"  State Keys: {list(final_session.state.keys())}")

    if "research_history" in final_session.state:
        research = final_session.state["research_history"]
        print(f"\n  Research History ({len(research)} entries):")
        for i, item in enumerate(research, 1):
            print(f"    {i}. Topic: {item['topic']} (Depth: {item['depth']})")

    if "documents" in final_session.state:
        docs = final_session.state["documents"]
        print(f"\n  Documents Created ({len(docs)} total):")
        for doc in docs:
            print(f"    - ID {doc['id']}: {doc['title']} ({len(doc['content'])} chars)")

    await runner.close()
    print("\n✅ Session state inspection completed")


async def example_resumability():
    """Example 5: Demonstrate resumability configuration."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Resumability (Experimental)")
    print("=" * 70)

    print("\nApp Configuration:")
    print(f"  App Name: {agent.root_app.name}")
    print(f"  Root Agent: {agent.root_app.root_agent.name}")
    print(f"  Sub-Agents: {len(agent.root_app.root_agent.sub_agents)}")
    print(f"  Plugins: {[p.name for p in agent.root_app.plugins]}")
    print(f"  Resumability Enabled: {agent.root_app.resumability_config.is_resumable}")

    print("\nResumability allows the app to:")
    print("  1. Pause execution on long-running function calls")
    print("  2. Resume from the last event if paused/failed")
    print("  3. Handle idempotent operations gracefully")

    session_service = InMemorySessionService()
    runner = Runner(app=agent.root_app, session_service=session_service)

    session = await session_service.create_session(
        app_name=agent.root_app.name,
        user_id=USER_ID,
    )

    query = "Start researching AI, but I'll need to pause and resume"
    print(f"\n[User]: {query}")

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
                        print(f"  {part.text[:100]}...")

    await runner.close()
    print("\n✅ Resumability example completed")


async def main():
    """Run all examples."""
    print("\n" + "🚀" * 35)
    print("APP WITH MULTI-AGENT ORCHESTRATION - ALL EXAMPLES")
    print("🚀" * 35)

    await example_basic_app_usage()
    await example_multi_agent_workflow()
    await example_plugin_access()
    await example_session_state_inspection()
    await example_resumability()

    print("\n" + "=" * 70)
    print("✨ All examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. App wraps agent(s) with app-wide configuration")
    print("2. Sub-agents enable task specialization and delegation")
    print("3. Plugins provide cross-cutting concerns (logging, metrics)")
    print("4. Coordinator pattern enables complex workflows")
    print("5. App-level configs (resumability, context cache) apply to all agents")


if __name__ == "__main__":
    asyncio.run(main())
