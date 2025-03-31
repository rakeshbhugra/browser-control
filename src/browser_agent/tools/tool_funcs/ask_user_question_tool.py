from src.interfaces.tool_response import ToolResponse

async def ask_user_question_tool(question: str) -> ToolResponse:
    # Implement user questioning functionality
    # This would typically involve a UI element to prompt the user
    print(f"Asking user: {question}")
    # Placeholder - in a real implementation, this would wait for and return the user's response
    user_response = f"User response to question: {question}"
    return ToolResponse(text_response=user_response, tool_output=user_response) 