from src.interfaces.tool_response import ToolResponse
from playwright.sync_api import Page
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import CrawlerRunConfig

async def crawl_raw_html(raw_html: str):
    raw_html_url = f"raw:{raw_html}"
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=raw_html_url)
        if result.success:
            return result.markdown
        else:
            return None

async def google_search_tool(query: str, page: Page) -> ToolResponse:
    # Implement Google search functionality
    # This would typically use a search API or web scraping
    print(f"Searching Google for: {query}")
    
    await page.goto("https://www.google.com", wait_until="networkidle")
    await page.fill("textarea", query)
    await page.keyboard.press("Enter")

    # wait for page to load
    await page.wait_for_selector("body")
    
    # read page html
    raw_html = await page.content()
    with open("raw_html.txt", "w") as f:
        f.write(raw_html)
    search_results = await crawl_raw_html(raw_html)

    return ToolResponse(text_response=search_results, tool_output=search_results)