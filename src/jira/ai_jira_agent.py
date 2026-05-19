"""
AI Jira MCP Agent – Dùng AI (Claude/OpenAI) kết hợp Jira MCP Server
để fetch ticket và phân tích precondition/steps/expected

Kiến trúc:
  ┌─────────────┐     stdio/sse      ┌──────────────────────┐
  │  Python App │ ◄────MCP────────► │  mcp-atlassian server │
  │  (AI Agent) │                   │  (npx mcp-atlassian)  │
  └──────┬──────┘                   └──────────────────────┘
         │ AI calls MCP tools
         ▼
  Claude / OpenAI với tool_use

Tools được expose bởi mcp-atlassian:
  - jira_get_issue          → Lấy ticket theo ID
  - jira_search             → JQL search
  - jira_get_issue_comments → Lấy comments
  - jira_get_transitions    → Lấy workflow states

Usage:
    agent = JiraMCPAgent()
    ticket_data = await agent.fetch_and_analyze("PROJ-1234")
"""
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class JiraMCPAgent:
    """
    AI Agent kết hợp Jira MCP Server để fetch và phân tích ticket.

    Cấu hình trong .env:
        JIRA_MCP_URL       = https://your-company.atlassian.net
        JIRA_EMAIL         = your@email.com
        JIRA_API_TOKEN     = your_jira_api_token
        AI_PROVIDER        = anthropic | openai
        AI_API_KEY         = your_ai_api_key
        AI_MODEL           = claude-3-5-sonnet-20241022 | gpt-4o
    """

    def __init__(self) -> None:
        # mcp-atlassian dùng ATLASSIAN_* (không phải JIRA_*)
        self.jira_url   = os.getenv("ATLASSIAN_BASE_URL") or os.getenv("JIRA_MCP_URL", "")
        self.jira_email = os.getenv("ATLASSIAN_EMAIL")    or os.getenv("JIRA_EMAIL", "")
        self.jira_token = os.getenv("ATLASSIAN_API_TOKEN") or os.getenv("JIRA_API_TOKEN", "")
        self.provider   = os.getenv("AI_PROVIDER", "anthropic").lower()
        self.api_key    = os.getenv("AI_API_KEY", "")
        self.model      = os.getenv("AI_MODEL", "claude-3-5-sonnet-20241022")

        if not all([self.jira_url, self.jira_email, self.jira_token]):
            raise ValueError(
                "Thiếu Jira credentials. Cần set trong .env:\n"
                "  ATLASSIAN_BASE_URL   = https://your-company.atlassian.net\n"
                "  ATLASSIAN_EMAIL      = your@email.com\n"
                "  ATLASSIAN_API_TOKEN  = your_token"
            )
        if not self.api_key:
            raise ValueError(
                "Thiếu AI API key. Cần set trong .env:\n"
                "  AI_API_KEY = your_key"
            )

    # ── Public API ────────────────────────────────────────────────

    def fetch_and_analyze(self, ticket_id: str) -> dict[str, Any]:
        """
        Fetch ticket từ Jira qua MCP và phân tích bằng AI.
        Synchronous wrapper cho async implementation.

        Args:
            ticket_id: Jira ticket ID, ví dụ 'PROJ-1234'

        Returns:
            dict: Structured ticket + analysis data
        """
        return asyncio.run(self._run(ticket_id))

    # ── Core async flow ───────────────────────────────────────────

    async def _run(self, ticket_id: str) -> dict[str, Any]:
        """Main async flow: connect MCP → AI fetch → AI analyze."""
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        # Khởi động mcp-atlassian server qua npx/global install
        server_params = StdioServerParameters(
            command="mcp-atlassian",   # global install → gọi trực tiếp
            args=[],
            env={
                **os.environ,
                "ATLASSIAN_BASE_URL":  self.jira_url,
                "ATLASSIAN_EMAIL":     self.jira_email,
                "ATLASSIAN_API_TOKEN": self.jira_token,
            },
        )

        logger.info(f"[MCP] Connecting to mcp-atlassian server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Liệt kê tools available
                tools_result = await session.list_tools()
                tool_names = [t.name for t in tools_result.tools]
                logger.info(f"[MCP] Available tools: {tool_names}")

                # Dùng AI để fetch + analyze ticket
                result = await self._ai_fetch_and_analyze(session, ticket_id, tools_result.tools)
                return result

    # ── AI Agent Logic ────────────────────────────────────────────

    async def _ai_fetch_and_analyze(
        self,
        session: Any,
        ticket_id: str,
        tools: list,
    ) -> dict[str, Any]:
        """
        AI agent loop:
        1. Gửi request cho AI với MCP tools
        2. AI gọi tool jira_get_issue
        3. Trả kết quả tool về AI
        4. AI parse và trả structured analysis
        """
        if self.provider == "anthropic":
            return await self._claude_agent(session, ticket_id, tools)
        else:
            return await self._openai_agent(session, ticket_id, tools)

    # ── Claude Agent ──────────────────────────────────────────────

    async def _claude_agent(
        self,
        session: Any,
        ticket_id: str,
        tools: list,
    ) -> dict[str, Any]:
        import anthropic

        client = anthropic.Anthropic(api_key=self.api_key)

        # Convert MCP tools → Claude tools format
        claude_tools = self._mcp_tools_to_claude(tools)

        messages = [
            {
                "role": "user",
                "content": (
                    f"Hãy lấy thông tin Jira ticket '{ticket_id}' và phân tích nó. "
                    f"Sau khi có dữ liệu, trả về JSON với format:\n"
                    f"{self._analysis_json_schema()}"
                ),
            }
        ]

        logger.info(f"[AI] Claude bắt đầu fetch ticket {ticket_id}...")

        # Agentic loop – AI gọi tools cho đến khi xong
        while True:
            response = client.messages.create(
                model=self.model,
                max_tokens=4096,
                tools=claude_tools,
                messages=messages,
            )

            logger.debug(f"[AI] Claude stop_reason: {response.stop_reason}")

            # AI muốn gọi tool
            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        logger.info(f"[MCP] AI calling tool: {block.name}({block.input})")
                        result = await session.call_tool(block.name, block.input)
                        tool_content = result.content[0].text if result.content else ""
                        logger.debug(f"[MCP] Tool result length: {len(tool_content)} chars")
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_content,
                        })

                # Thêm response của AI + kết quả tools vào messages
                messages.append({"role": "assistant", "content": response.content})
                messages.append({"role": "user", "content": tool_results})

            # AI đã xong – parse kết quả
            elif response.stop_reason == "end_turn":
                final_text = "".join(
                    block.text for block in response.content
                    if hasattr(block, "text")
                )
                logger.info(f"[AI] Claude hoàn thành phân tích")
                return self._parse_ai_response(final_text, ticket_id)

            else:
                logger.warning(f"[AI] Unexpected stop_reason: {response.stop_reason}")
                break

        return self._empty_analysis(ticket_id)

    # ── OpenAI Agent ──────────────────────────────────────────────

    async def _openai_agent(
        self,
        session: Any,
        ticket_id: str,
        tools: list,
    ) -> dict[str, Any]:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)

        # Convert MCP tools → OpenAI function format
        openai_tools = self._mcp_tools_to_openai(tools)

        messages = [
            {
                "role": "system",
                "content": "You are a QA expert. Fetch Jira tickets and analyze them for test case generation. Always respond with valid JSON.",
            },
            {
                "role": "user",
                "content": (
                    f"Fetch Jira ticket '{ticket_id}' and analyze it. "
                    f"Return JSON with this schema:\n{self._analysis_json_schema()}"
                ),
            },
        ]

        logger.info(f"[AI] OpenAI bắt đầu fetch ticket {ticket_id}...")

        # Agentic loop
        while True:
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto",
            )

            choice = response.choices[0]
            message = choice.message

            # AI muốn gọi tool
            if choice.finish_reason == "tool_calls" and message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    logger.info(f"[MCP] AI calling: {tool_call.function.name}")
                    args = json.loads(tool_call.function.arguments)
                    result = await session.call_tool(tool_call.function.name, args)
                    tool_content = result.content[0].text if result.content else ""
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_content,
                    })

            # AI đã xong
            elif choice.finish_reason == "stop":
                final_text = message.content or ""
                logger.info("[AI] OpenAI hoàn thành phân tích")
                return self._parse_ai_response(final_text, ticket_id)
            else:
                break

        return self._empty_analysis(ticket_id)

    # ── Tool Format Converters ────────────────────────────────────

    def _mcp_tools_to_claude(self, tools: list) -> list[dict]:
        """Convert MCP tool definitions → Claude tools format."""
        claude_tools = []
        for t in tools:
            tool = {
                "name": t.name,
                "description": t.description or "",
                "input_schema": t.inputSchema if hasattr(t, "inputSchema") else {"type": "object", "properties": {}},
            }
            claude_tools.append(tool)
        return claude_tools

    def _mcp_tools_to_openai(self, tools: list) -> list[dict]:
        """Convert MCP tool definitions → OpenAI function tools format."""
        openai_tools = []
        for t in tools:
            tool = {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or "",
                    "parameters": t.inputSchema if hasattr(t, "inputSchema") else {"type": "object", "properties": {}},
                },
            }
            openai_tools.append(tool)
        return openai_tools

    # ── Parse AI Response ─────────────────────────────────────────

    def _parse_ai_response(self, text: str, ticket_id: str) -> dict[str, Any]:
        """Parse JSON từ AI response."""
        import re
        # Tìm JSON block trong response
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1)
        else:
            # Thử parse toàn bộ text như JSON
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                text = text[start:end]

        try:
            data = json.loads(text)
            data.setdefault("ticket_id", ticket_id)
            return data
        except json.JSONDecodeError as e:
            logger.error(f"[AI] Cannot parse JSON response: {e}")
            logger.debug(f"[AI] Raw response: {text[:500]}")
            return self._empty_analysis(ticket_id)

    # ── Helpers ───────────────────────────────────────────────────

    def _analysis_json_schema(self) -> str:
        return json.dumps({
            "ticket_id": "PROJ-1234",
            "title": "Tóm tắt ticket",
            "description": "Mô tả đầy đủ",
            "priority": "High|Medium|Low",
            "status": "Open|In Progress|...",
            "components": ["component1"],
            "labels": ["label1"],
            "assignee": "email",
            "reporter": "email",
            "preconditions": ["Điều kiện tiên quyết 1", "..."],
            "test_steps": ["Bước test 1", "Bước test 2", "..."],
            "expected_results": ["Kết quả mong đợi 1", "..."],
            "test_type": "functional|regression|smoke",
            "platforms": ["android", "ios"],
            "acceptance_criteria": ["AC 1", "..."],
        }, indent=2, ensure_ascii=False)

    def _empty_analysis(self, ticket_id: str) -> dict[str, Any]:
        return {
            "ticket_id": ticket_id,
            "title": "",
            "description": "",
            "priority": "Medium",
            "status": "",
            "components": [],
            "labels": [],
            "assignee": "",
            "reporter": "",
            "preconditions": [],
            "test_steps": [],
            "expected_results": [],
            "test_type": "functional",
            "platforms": ["android"],
            "acceptance_criteria": [],
        }

