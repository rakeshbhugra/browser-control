from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.async_api import async_playwright
import uvicorn

app = FastAPI()

# Global variables to hold Playwright instances.
playwright_instance = None
browser = None
page = None

# --- Pydantic models for inputs and outputs ---

class GoogleSearchRequest(BaseModel):
    query: str

class GoogleSearchResponse(BaseModel):
    results: str  # In a real scenario, you might structure these results better.

class ReadPageRequest(BaseModel):
    url: str

class ReadPageResponse(BaseModel):
    content: str

class ScreenshotResponse(BaseModel):
    file_path: str

# --- FastAPI Startup and Shutdown Events ---

@app.on_event("startup")
async def startup_event():
    global playwright_instance, browser, page
    playwright_instance = await async_playwright().start()
    # Launch the browser (non-headless mode to see the browser)
    browser = await playwright_instance.chromium.launch(headless=False)
    page = await browser.new_page()
    # Optionally, navigate to a default page
    await page.goto("https://www.google.com")
    print("Browser started and navigated to https://www.google.com")

@app.on_event("shutdown")
async def shutdown_event():
    global playwright_instance, browser
    await browser.close()
    await playwright_instance.stop()
    print("Browser and Playwright have been shut down.")

# --- Endpoint Implementations ---

@app.post("/google_search", response_model=GoogleSearchResponse)
async def google_search(request: GoogleSearchRequest):
    global page
    # Navigate to Google search with the provided query
    search_url = f"https://www.google.com/search?q={request.query}"
    await page.goto(search_url)
    await page.wait_for_load_state("networkidle")
    # For simplicity, return the full HTML content.
    # In a production scenario, you might parse the HTML to extract specific search result snippets.
    content = await page.content()
    return GoogleSearchResponse(results=content)

@app.post("/read_page", response_model=ReadPageResponse)
async def read_page(request: ReadPageRequest):
    global page
    await page.goto(request.url)
    await page.wait_for_load_state("networkidle")
    content = await page.content()
    return ReadPageResponse(content=content)

@app.post("/screenshot", response_model=ScreenshotResponse)
async def take_screenshot():
    global page
    file_path = "screenshot.png"
    await page.screenshot(path=file_path)
    return ScreenshotResponse(file_path=file_path)

# --- Running the FastAPI Server ---
if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=4000,
    )
