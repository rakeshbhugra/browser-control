import importlib
import os
import inspect
import asyncio
from src.interfaces.tool_response import ToolResponse
from src.utils.print_helper import print_helper
from playwright.sync_api import Page

class ToolFuncsManager:
    def __init__(self):
        self.tool_mapping = {}
        self._load_tools()

    def _load_tools(self):
        # Get the directory containing the tool functions
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Dynamically import all tool modules
        for filename in os.listdir(current_dir + "/tool_funcs"):
            if filename.endswith('_tool.py') and filename != '__init__.py':
                module_name = filename[:-3]  # Remove .py extension
                
                # Import the module
                module_path = f"src.browser_agent.tools.tool_funcs.{module_name}"
                try:
                    module = importlib.import_module(module_path)
                    
                    # Find the tool function in the module
                    for name, obj in inspect.getmembers(module):
                        if name.endswith('_tool') and asyncio.iscoroutinefunction(obj):
                            # Extract the tool name (remove '_tool' suffix)
                            tool_name = name[:-5] if name.endswith('_tool') else name
                            self.tool_mapping[tool_name] = obj
                            print_helper.cyan_print(f"Loaded tool: {tool_name}")
                except ImportError as e:
                    print_helper.red_print(f"Error importing {module_path}: {e}")

    async def tool_call(self, tool_name: str, tool_args: dict, page: Page) -> ToolResponse:
        if tool_name not in self.tool_mapping:
            return f"Error: Tool '{tool_name}' not found"
        
        tool_func = self.tool_mapping[tool_name]
        try:
            # TODO: add error handling here
            tool_response = await tool_func(**tool_args, page=page)
            # validate pydantic model
            assert isinstance(tool_response, ToolResponse)
            return tool_response
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

# use this if u want to use cached tools, otherwise create the class instance again
tool_funcs_manager = ToolFuncsManager()