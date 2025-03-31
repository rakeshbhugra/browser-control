import asyncio

from src.utils.get_browser_agent_system_prompt import get_browser_agent_system_prompt
from src.utils.llm.openai_call import get_openai_completion
from src.browser_agent.tools.tools import get_all_tools
from src.utils.llm.parse_llm_response import parse_llm_response
from src.interfaces.llm_response import LLMResponse
from src.utils.get_this_from_config import get_this_from_runtime_config
from src.utils.llm.handle_llm_response import handle_llm_response
from uuid import uuid4

class BrowserAgent:
    def __init__(self):
        self.system_prompt = get_browser_agent_system_prompt()
        self.user_id = str(uuid4())

    async def run(self, user_input):
        while True:
            response = await get_openai_completion(
                system_prompt=self.system_prompt,
                user_prompt=user_input,
                model=await get_this_from_runtime_config("llm_model"),
                temperature=0,
                stream=False,
                tools=await get_all_tools()
            )
            llm_response: LLMResponse = await parse_llm_response(response)
            await handle_llm_response(llm_response, self.user_id)
            break

        return llm_response

async def main():
    agent = BrowserAgent()
    # response = await agent.run("How are you doing?")
    # response = await agent.run("Thank you you were very helpful")
    response = await agent.run("What is the best selling product in India?")
    # print(response)

if __name__ == "__main__":
    asyncio.run(main())
