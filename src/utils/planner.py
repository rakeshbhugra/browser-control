from src.interfaces.context import Context
from src.utils.llm.openai_call import get_openai_completion
from src.utils.get_this_from_config import get_this_from_runtime_config

system_prompt = """
You are a helpful assistant that helps with planning tasks. You are creating a plan for web agent that can do google search, navigate to different pages, etc.
Keep the plan simple and have steps.
"""

async def get_plan(user_input: str) -> str:
    response = await get_openai_completion(
        system_prompt = system_prompt,
        user_prompt = user_input,
        model = await get_this_from_runtime_config("llm_model"),
        temperature = 0,
        stream = False,
    )
    return response[0].content[0].text