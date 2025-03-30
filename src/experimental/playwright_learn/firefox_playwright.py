from playwright.sync_api import sync_playwright
import os

def run():
    ignored_dir = "data/gitignored"
    os.makedirs(ignored_dir, exist_ok=True)
    with sync_playwright() as p:
        # Launch with more realistic browser settings
        browser = p.firefox.launch(
            headless=False,
            args=[
                '--window-size=1920,1080',
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/123.0'
            ]
        )
        
        # Create context with more human-like characteristics
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/123.0',
            geolocation={'latitude': 40.712776, 'longitude': -74.005974},
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['geolocation']
        )
        
        page = context.new_page()
        
        # Add some random delay to seem more human-like
        page.set_default_timeout(30000)  # 30 seconds
        page.set_default_navigation_timeout(30000)
        
        # navigate to google
        url = "https://www.google.com"
        page.goto(url)
        
        # Add slight delay before typing
        page.wait_for_timeout(1000)
        
        # search for something
        search_query = "Playwright Python tutorial"
        page.fill("textarea", search_query)
        page.wait_for_timeout(500)  # Small delay before pressing Enter
        page.keyboard.press("Enter")

        # wait for navigation
        page.wait_for_load_state("networkidle")

        # get html
        html = page.content()
        with open(os.path.join(ignored_dir, "google_home.html"), "w") as f:
            f.write(html)

        # Handle reCAPTCHA
        # First locate the iframe
        recaptcha_frame = page.frame_locator('iframe[title="reCAPTCHA"]')
        # Click the checkbox inside the iframe
        recaptcha_frame.locator('.recaptcha-checkbox-border').click()
        
        # Wait a moment to see if the captcha is solved
        page.wait_for_timeout(2000)  # 2 seconds

        # Keep the browser window open until user input
        input("Press Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    run()
