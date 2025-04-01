from crawl4ai import AsyncWebCrawler

async def crawl_raw_html(raw_html: str):
    raw_html_url = f"raw:{raw_html}"
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=raw_html_url)
        if result.success:
            return result.markdown
        else:
            return None
