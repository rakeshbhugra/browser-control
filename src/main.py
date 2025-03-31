import asyncio
from src.browser_agent.agent import BrowserAgent

async def main():
    agent = BrowserAgent()
    await agent.run()

asyncio.run(main())