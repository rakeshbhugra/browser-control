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
    browser = p.chromium.launch(
        headless=False,
        proxy={
            "server": proxy_server,
            "username": proxy_username,
            "password": proxy_password,
        },
    )
    page = browser.new_page()
    page.wait_for_load_state("networkidle")
    page.goto("https://www.booking.com/")
    print(page.content())
    browser.close()
