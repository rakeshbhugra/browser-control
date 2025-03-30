# import statements
from src.utils.launch_pywright_browser import launch_pywright_browser
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

# Add this class for request validation
class SearchQuery(BaseModel):
    query: str

app = FastAPI()

# Global variables
page = None
playwright_instance = None
browser = None

@asynccontextmanager
async def lifespan(app):
    # Startup
    global page, playwright_instance, browser
    playwright_instance, browser, page = await launch_pywright_browser()
    yield
    # Shutdown
    await browser.close()
    await playwright_instance.stop()

app = FastAPI(lifespan=lifespan)

# routes
@app.post('/google_search')
async def google_search(search_query: SearchQuery):
    try:
        print(f"Attempting to search for: {search_query.query}")
        # First navigate to Google
        await page.goto("https://www.google.com", wait_until="networkidle")
        print("Navigated to Google")
        
        # Use the actual query from the request
        await page.fill("textarea", search_query.query)
        print("Filled search query")
        
        await page.keyboard.press("Enter")
        print("Pressed Enter")
        
        return {"message": f"Google search started for: {search_query.query}"}
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {"error": str(e)}

# main
if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=4000,
    )
    