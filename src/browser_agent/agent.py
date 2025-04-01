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
from src.sqlite_manager.create_event import create_event
from src.interfaces.events import Event
from datetime import datetime
from src.utils.draw_bounding_boxes_around_elements import draw_bounding_boxes_around_elements, DrawBoundingBoxesAroundElementsResponse
import os

class BrowserAgent:
    def __init__(self):
        self.default_system_prompt = get_browser_agent_system_prompt()
        self.user_id = str(uuid4())
        
        # create ignored output dir
        os.makedirs("data/gitignored", exist_ok=True)

    async def _init_browser(self):
        playwright_instance, browser, page = await launch_pywright_browser(use_proxy=False)
        self.context: Context = Context(
                user_id=self.user_id,
                page=page,
                page_content=None,
                element_index_dict=None,
                messages_for_llm="",
                plan=None
            )

    async def run(self):
        await self._init_browser()
        
        print_helper.line_print(color='cyan')

        # initiate browser
        print_helper.green_print("Welcome to the browser agent!\n")
        
        # user_input = input("What can I do for you today?\n")
        user_input = "search for latest news in india"

        # create user event and save
        user_event = Event(
            user_id=self.user_id,
            role="user",
            content=user_input,
            message_type="text",
            event_timestamp=datetime.now()
        )
        await create_event(user_event)

        self.context.messages_for_llm = f'User: {user_input}\n'

        # TODO: we'll add planning later
        # if not self.context.plan:

        while True:
            system_prompt = await self.prepare_system_prompt()
            user_prompt = await prepare_user_prompt(self.context)
            response = await get_openai_completion(
                system_prompt = system_prompt,
                user_prompt = user_prompt,
                model = await get_this_from_runtime_config("llm_model"),
                temperature = 0,
                stream = False,
                tools = await get_all_tools(),
            )
            llm_response: LLMResponse = await parse_llm_response(response)
            await handle_llm_response(llm_response, self.context)

            # print history for debugging
            # await print_history(self.user_id)

    async def prepare_system_prompt(self):
        system_prompt = self.default_system_prompt

        draw_bounding_boxes_around_elements_response: DrawBoundingBoxesAroundElementsResponse = await draw_bounding_boxes_around_elements(self.context.page, need_screenshot=False)
        self.context.element_index_dict = draw_bounding_boxes_around_elements_response.element_index_dict
        self.context.page_content = await self.context.page.evaluate("document.body.innerText")
        
        if self.context.page_content and self.context.element_index_dict:
            system_prompt += f'\n\n\n<current_url>\n{self.context.page.url}\n</current_url>\n\n\n'
            system_prompt += f'\n\n\n<page_text>\n{self.context.page_content}\n</page_text>\n\n\n'
            system_prompt += f'\n\n\n<element_index>\n{self.context.element_index_dict}\n</element_index>\n\n\n'
        with open(os.path.join("data/gitignored", "system_prompt.txt"), 'w') as f:
            f.write(system_prompt)
        return system_prompt