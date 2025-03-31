import asyncio

from src.utils.get_browser_agent_system_prompt import get_browser_agent_system_prompt
from src.utils.llm.openai_call import get_openai_completion
from src.browser_agent.tools.get_all_tools import get_all_tools
from src.utils.llm.parse_llm_response import parse_llm_response
from src.interfaces.llm_response import LLMResponse
from src.utils.get_this_from_config import get_this_from_runtime_config
from src.utils.llm.handle_llm_response import handle_llm_response
from src.utils.prepare_user_prompt import prepare_user_prompt
from uuid import uuid4
from src.utils.print_helper import print_helper
from src.utils.launch_pywright_browser import launch_pywright_browser
from src.utils.print_history import print_history
from src.interfaces.context import Context

class BrowserAgent:
    def __init__(self):
        self.system_prompt = get_browser_agent_system_prompt()
        self.user_id = str(uuid4())

    async def run(self):
        print_helper.line_print(color='cyan')

        # initiate browser
        playwright_instance, browser, page = await launch_pywright_browser(use_proxy=False)
        self.context: Context = Context(
                user_id=self.user_id,
                page=page,
                page_content=None,
                element_index_dict=None,
                messages_for_llm="",
                plan=None
            )
        print_helper.green_print("Welcome to the browser agent!\n")
        
        # user_input = input("What can I do for you today?\n")
        user_input = "search for latest news in india"

        # TODO: we'll add planning later
        # if not self.context.plan:

        if self.context.page_content and self.context.element_index_dict:
            user_input += f'\n<page_text>{self.context.page_content}</page_text>\n'
            user_input += f'\n<element_index>{self.context.element_index_dict}</element_index>\n'

        while True:
            user_prompt = self.context.messages_for_llm
            response = await get_openai_completion(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                model=await get_this_from_runtime_config("llm_model"),
                temperature=0,
                stream=False,
                tools=await get_all_tools()
            )
            llm_response: LLMResponse = await parse_llm_response(response)
            await handle_llm_response(llm_response, self.context)

            # print history for debugging
            await print_history(self.user_id)

