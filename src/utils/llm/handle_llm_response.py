from src.interfaces.llm_response import LLMResponse
from src.sqlite_manager.manager import sqlite_manager
from src.browser_agent.tools.manager import tool_funcs_manager
from src.interfaces.tool_response import ToolResponse
from src.interfaces.events import Event, FunctionDetails
from playwright.sync_api import Page
from datetime import datetime
from src.interfaces.context import Context

async def handle_llm_response(llm_response: LLMResponse, context: Context):

    if llm_response.function_name:
        function_name = llm_response.function_name
        function_args = llm_response.function_args
        # call the function
        tool_response: ToolResponse = await tool_funcs_manager.tool_call(function_name, function_args, context)
        # print(tool_response)
        
        function_details = FunctionDetails(
            name=function_name,
            args=function_args,
            response=tool_response.text_response
        )
        
        event = Event(
            user_id=context.user_id,
            role="agent_action",
            content=tool_response.text_response,
            message_type="function_call",
            function_details=function_details,
            event_timestamp=datetime.now()
        )
    else:
        event = Event(
            user_id=context.user_id,
            role="agent_response",
            content=llm_response.text,
            message_type="text",
            event_timestamp=datetime.now()
        )

    # save the event
    await sqlite_manager.create_event(event)

    return event