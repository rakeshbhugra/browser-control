from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

with sync_playwright() as p:
    proxy_url = os.getenv("PROXY_URL")
    parsed_url = urlparse(proxy_url)
    proxy_server = f"{parsed_url.scheme}://{parsed_url.netloc}"
    proxy_username = parsed_url.username
    proxy_password = parsed_url.password

    # Create browser context with more realistic settings
    browser = p.chromium.launch(
        headless=False,
        proxy={
            "server": proxy_server,
            "username": proxy_username,
            "password": proxy_password,
        },
    )
    
    # Create a context with more realistic browser settings
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        locale='en-US',
        timezone_id='America/New_York',
        permissions=['geolocation']
    )
    
    page = context.new_page()
    
    try:
        page.goto("https://www.bing.com", wait_until="networkidle", timeout=30000)
        page.wait_for_load_state("domcontentloaded")
        
        # Wait for a common Google element to ensure the page loaded properly
        page.wait_for_selector('input[name="q"]', timeout=10000)
        
        input("Press Enter to continue...")
        print(page.content())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        context.close()
        browser.close()
