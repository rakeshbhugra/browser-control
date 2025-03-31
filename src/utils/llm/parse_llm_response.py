from src.interfaces.llm_response import LLMResponse
import json

async def parse_llm_response(response):
    function_name = None
    function_args = None
    text = None
    
    if response[0].type == "function_call":
        function_name = response[0].name
        function_args = json.loads(response[0].arguments)
        print(function_name, function_args)
    else:
        text = response[0].content[0].text
        print(text)
    return LLMResponse(
        function_name=function_name, 
        function_args=function_args, 
        text=text
        )