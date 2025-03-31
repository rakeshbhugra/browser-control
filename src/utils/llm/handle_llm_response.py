from src.interfaces.llm_response import LLMResponse

async def handle_llm_response(llm_response: LLMResponse):
    if llm_response.function_name:
        function_name = llm_response.function_name
        function_args = llm_response.function_args
        # call the function
    else:
        return llm_response.text
