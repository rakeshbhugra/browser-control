import asyncio

from src.utils.get_browser_agent_system_prompt import get_browser_agent_system_prompt
from src.utils.llm.litellm_calls import tool_response
from src.utils.parse_function import parse_function

class BrowserAgent:
    def __init__(self):
        self.system_prompt = get_browser_agent_system_prompt()

    async def run(self, user_input):
        response = await tool_response(self.system_prompt, user_input, {}, 0, "gpt-4o-mini", False)
        return response

async def main():
    agent = BrowserAgent()
    response = await agent.run("What is latest news in India?")
    print(response)
    function_name, function_args = await parse_function(response)
    print(function_name)
    print(function_args)

if __name__ == "__main__":
    asyncio.run(main())
