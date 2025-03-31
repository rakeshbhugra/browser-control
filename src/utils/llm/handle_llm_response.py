from src.interfaces.llm_response import LLMResponse
from src.sqlite_manager.manager import sqlite_manager

async def handle_llm_response(llm_response: LLMResponse, user_id: str):

    # get history for this user_id
    history = await sqlite_manager.get_previous_events(user_id)

    if llm_response.function_name:
        function_name = llm_response.function_name
        function_args = llm_response.function_args
        # call the function
    else:
        pass