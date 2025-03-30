import asyncio

from src.utils.get_browser_agent_system_prompt import get_browser_agent_system_prompt
from src.utils.llm.openai_call import get_openai_completion
from src.utils.parse_function import parse_function
from src.interfaces.user import User
from src.interfaces.messages import Messages
from src.browser_agent.tools.tools import get_all_tools

class BrowserAgent:
    def __init__(self):
        self.system_prompt = get_browser_agent_system_prompt()

    async def run(self, user_input):
        while True:
            response = await get_openai_completion(
                system_prompt=self.system_prompt,
                user_prompt=user_input,
                model="gpt-4o-mini",
                temperature=0,
                stream=False,
                tools=await get_all_tools()
            )
            print(response)
            function_name = response[0].name
            function_args = response[0].arguments
            print(function_name, function_args)
            break
        return response

async def main():
    agent = BrowserAgent()
    # response = await agent.run("How are you doing?")
    response = await agent.run("What is latest news in India?")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
