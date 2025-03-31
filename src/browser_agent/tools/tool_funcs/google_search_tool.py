from src.interfaces.tool_response import ToolResponse
from src.interfaces.context import Context
from crawl4ai import AsyncWebCrawler
import os
async def crawl_raw_html(raw_html: str):
    raw_html_url = f"raw:{raw_html}"
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=raw_html_url)
        if result.success:
            return result.markdown
        else:
            return None

async def google_search_tool(query: str, context: Context) -> ToolResponse:
    # Implement Google search functionality
    # This would typically use a search API or web scraping
    print(f"Searching Google for: {query}")
    
    await context.page.goto("https://www.bing.com")
    await context.page.wait_for_timeout(1000)
    await context.page.fill("textarea", query)
    await context.page.keyboard.press("Enter")
    await context.page.wait_for_timeout(10000)

    # wait for page to load
    await context.page.wait_for_selector("body")
    
    # read page html
    raw_html = await context.page.content()
    ignored_dir = 'data/gitignored'
    with open(os.path.join(ignored_dir, "raw.html"), "w") as f:
        f.write(raw_html)
    search_markdown = await crawl_raw_html(raw_html)
    with open(os.path.join(ignored_dir, "search_results.md"), 'w') as f:
        f.write(search_markdown)

    return ToolResponse(text_response=search_markdown, tool_output=search_markdown)