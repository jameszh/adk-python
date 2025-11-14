# ADK Samples Reorganization Plan

## Current State
- 114 samples in flat directory structure
- Hard to navigate and find relevant examples
- No clear learning path

## Proposed Organization

### 1. **01-getting-started/** (Quick wins for new users)
- hello_world
- hello_world_app
- quickstart
- core_basic_config
- runner_debug_example

### 2. **02-core-concepts/** (Fundamental ADK concepts)
- callbacks
- core_callback_config
- core_custom_agent_config
- core_generate_content_config_config
- session_state_agent
- history_management
- token_usage
- telemetry

### 3. **03-tools/** (Tool integration and usage)
**03-tools/builtin/**
- tool_builtin_config
- built_in_multi_tools
- code_execution
- custom_code_execution
- agent_engine_code_execution
- vertex_code_execution

**03-tools/custom/**
- tool_functions_config
- pydantic_argument
- tool_agent_tool_config
- parallel_functions

**03-tools/human-in-loop/**
- human_in_loop
- human_tool_confirmation
- tool_human_in_the_loop_config

**03-tools/integrations/**
- langchain_structured_tool_agent
- langchain_youtube_search_agent
- crewai_tool_kwargs

### 4. **04-mcp-integrations/** (Model Context Protocol)
- mcp_stdio_server_agent
- mcp_stdio_notion_agent
- mcp_tool_mcp_stdio_notion_config
- mcp_sse_agent
- mcp_streamablehttp_agent
- mcp_dynamic_header_agent
- mcp_in_agent_tool_remote
- mcp_in_agent_tool_stdio
- mcp_postgres_agent
- mcp_server_side_sampling
- mcp_service_account_agent

### 5. **05-multi-agent/** (Multi-agent orchestration)
- multi_agent_basic_config
- multi_agent_llm_config
- multi_agent_loop_config
- multi_agent_seq_config
- sub_agents_config
- simple_sequential_agent
- non_llm_sequential
- workflow_agent_seq
- workflow_triage
- live_bidi_streaming_multi_agent

### 6. **06-live-streaming/** (Live API and streaming)
- live_agent_api_server_example
- live_bidi_streaming_single_agent
- live_bidi_streaming_tools_agent
- live_bidi_debug_utils
- live_tool_callbacks_agent

### 7. **07-plugins/** (Plugin system)
- plugin_basic
- plugin_reflect_tool_retry

### 8. **08-llm-providers/** (Different LLM backends)
- hello_world_anthropic
- hello_world_gemma
- hello_world_litellm
- hello_world_litellm_add_function_to_prompt
- hello_world_ollama
- hello_world_apigeellm
- litellm_inline_tool_call
- litellm_structured_output
- litellm_with_fallback_models
- hello_world_ma

### 9. **09-data-storage/** (Database and storage integrations)
- bigquery
- bigtable
- spanner
- spanner_rag_agent
- memory

### 10. **10-google-cloud/** (GCP integrations)
- google_api
- google_search_agent
- gepa
- gke_agent_sandbox
- application_integration_agent
- integration_connector_euc_agent

### 11. **11-authentication/** (Auth patterns)
- oauth2_client_credentials
- oauth_calendar_agent
- authn-adk-all-in-one
- a2a_auth

### 12. **12-a2a-protocol/** (Agent-to-Agent)
- a2a_basic
- a2a_human_in_loop
- a2a_root

### 13. **13-advanced-features/** (Advanced capabilities)
- context_offloading_with_artifact
- artifact_save_text
- cache_analysis
- rewind_session
- generate_image
- multimodal_tool_results
- output_schema_with_tools
- fields_output_schema
- fields_planner
- logprobs
- static_instruction
- static_non_text_content
- computer_use
- json_passing_agent

### 14. **14-rag-examples/** (RAG and knowledge)
- rag_agent
- spanner_rag_agent

### 15. **15-production/** (Production-ready examples)
- toolbox_agent
- jira_agent
- adk_agent_builder_assistant
- adk_answering_agent
- adk_documentation
- adk_issue_formatting_agent
- adk_knowledge_agent
- adk_pr_agent
- adk_pr_triaging_agent
- adk_triaging_agent

### 16. **utils/** (Utilities and services)
- dummy_services.py
- services.py
- services.yaml
- migrate_session_db

## Benefits
1. **Clear learning path**: Start with 01, progress to 15
2. **Easy discovery**: Find samples by feature category
3. **Better organization**: Related samples grouped together
4. **Scalable**: Easy to add new samples to appropriate categories

## Implementation
- Move samples to new structure
- Create README.md in each category
- Create master INDEX.md with navigation
- Update references in docs
