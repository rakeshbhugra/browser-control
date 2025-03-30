def get_browser_agent_system_prompt():
    with open("src/prompts/browse_agent_system_prompt.txt", "r") as f:
        browse_agent_system_prompt = f.read()
    return browse_agent_system_prompt


if __name__ == "__main__":
    print(get_browser_agent_system_prompt())