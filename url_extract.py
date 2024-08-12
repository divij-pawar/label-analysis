import asyncio
from playwright.async_api import async_playwright

async def get_target_urls(url, selector):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        # Get all elements that match the selector
        elements = await page.query_selector_all(selector)

        # print(elements)
        target_urls = []
        for element in elements:
            # Click the element
            await element.click()
            
            # Wait for the navigation to finish
            await page.wait_for_load_state('networkidle')
            
            # Get the current URL
            current_url = page.url
            target_urls.append(current_url)
            
            # Go back to the original page
            await page.go_back()
            await page.wait_for_load_state('networkidle')
        
        await browser.close()
        return target_urls

url = 'https://www.swiggy.com/instamart/category-listing?categoryName=Dairy%2C+Bread+and+Eggs'
selector = '[data-testid="ItemWidgetContainer"]'
# selector = '[data-testid="image-card-div"]'

target_urls = asyncio.run(get_target_urls(url, selector))
print(target_urls)
