async def parse_function(response):
    function = response.split("```python")[1].split("```")[0]
    function_name = function.split("(")[0].strip()
    function_args = function.split("(")[1].split(")")[0].strip()
    return function_name, function_args
