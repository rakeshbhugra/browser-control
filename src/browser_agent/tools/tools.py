import json
import os
import asyncio
async def get_all_tools():
    tools_definitions_dir = 'src/browser_agent/tools/tool_definitions'
    tools = []
    for file in os.listdir(tools_definitions_dir):
        if file.endswith('_tool.json'):
            with open(os.path.join(tools_definitions_dir, file), 'r') as f:
                tools.append(json.load(f))
    return tools

async def main():
    tools = await get_all_tools()
    for tool in tools:
        print(tool)

if __name__ == "__main__":
    asyncio.run(main())