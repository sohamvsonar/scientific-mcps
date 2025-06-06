import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Optional
import argparse
from pathlib import Path
import sys

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client with API key
client = genai.Client(api_key=GEMINI_API_KEY)


def find_server_py(server_name: str) -> str:
    """
    Recursively find server.py for a given server name in the repo.
    Looks under <repo_root>/<server_name>/src/ for any server.py.
    """
    repo_root = Path(__file__).resolve().parent.parent
    server_src = repo_root / server_name / "src"
    if not server_src.exists():
        raise FileNotFoundError(f"src directory not found for {server_name} at {server_src}")
    matches = list(server_src.rglob("server.py"))
    if not matches:
        raise FileNotFoundError(f"Could not find server.py for {server_name} under {server_src}")
    return str(matches[0])


class MCPClient:
    """Handles connection and communication with an MCP server."""
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect(self, server_script: str):
        print(f"Starting server with stdio: {server_script}")
        command = sys.executable
        args = [server_script]
        params = StdioServerParameters(command=command, args=args, env=os.environ)
        reader, writer = await self.exit_stack.enter_async_context(
            stdio_client(params)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(reader, writer)
        )
        await self.session.initialize()
        tools = await self.session.list_tools()
        print("\nConnected. Tools available 📦:\n")
        for t in tools.tools:
            print(f" * {t.name}: {t.description}")

    async def process_query(self, query: str) -> dict:
        resp_tools = await self.session.list_tools()
        tool_descs = []
        for t in resp_tools.tools:
            tool_descs.append({
                "name": t.name,
                "description": t.description,
                "parameters": {
                    "type": t.inputSchema.get("type", "object"),
                    "properties": {
                        k: {"type": v.get("type", "string"), "description": v.get("description", "")}
                        for k, v in t.inputSchema.get("properties", {}).items()
                    },
                    "required": t.inputSchema.get("required", [])
                }
            })
        tools_schema = types.Tool(function_declarations=tool_descs)
        config = types.GenerateContentConfig(tools=[tools_schema])
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[query],
            config=config,
        )
        um = response.usage_metadata
        prompt_tokens = um.prompt_token_count
        completion_tokens = um.candidates_token_count
        final_parts = []
        for cand in response.candidates:
            parts = getattr(cand.content, 'parts', None)
            if parts:
                for part in parts:
                    if getattr(part, 'function_call', None):
                        name = part.function_call.name
                        raw = part.function_call.args
                        args = json.loads(raw) if isinstance(raw, str) else raw
                        print(f"[Calling tool {name} with args {args}]")
                        tr = await self.session.call_tool(name, args)
                        raw_txt = tr.content[0].text
                        final_parts.append(f"[Called {name}: {raw_txt}]")
                    elif getattr(part, 'text', None):
                        final_parts.append(part.text)
            else:
                txt = getattr(cand.content, 'text', '')
                if txt:
                    final_parts.append(txt)
        return {
            "text": "\n".join(final_parts).strip(),
            "usage_metadata": {
                "prompt_token_count": prompt_tokens,
                "response_token_count": completion_tokens
            }
        }

    async def chat_loop(self):
        print("\nMCP Client Started! (type 'quit' to exit)")
        while True:
            q = input("\nQuery: ").strip()
            if q.lower() in ('quit', 'exit'):
                break
            out = await self.process_query(q)
            um = out["usage_metadata"]
            total = um["prompt_token_count"] + um["response_token_count"]
            print(f"\n{out['text']}")
            print(f"[Tokens: {total} (prompt {um['prompt_token_count']}, response {um['response_token_count']})]")

    async def cleanup(self):
        await self.exit_stack.aclose()


async def async_main(server_names):
    for server_name in server_names:
        print(f"\n=== Connecting to {server_name} ===")
        server_py = find_server_py(server_name)
        client = MCPClient()
        try:
            await client.connect(server_py)
            await client.chat_loop()
        finally:
            await client.cleanup()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--servers",
        required=True,
        help="Comma-separated list of server names (e.g. HDF5,Arxiv)"
    )
    args = parser.parse_args()
    server_names = [name.strip() for name in args.servers.split(",")]
    asyncio.run(async_main(server_names))


if __name__ == "__main__":
    main()