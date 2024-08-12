from playwright.sync_api import sync_playwright

def extract_all_urls(url):
    with sync_playwright() as p:
        # Launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        # Get the page content
        html = page.content()

        # Extract all URLs from the page
        urls = page.query_selector_all('a')
        all_urls = [url.get_attribute('href') for url in urls if url.get_attribute('href')]

        # Print all URLs
        for link in all_urls:
            print(link)

        browser.close()

# URL to extract URLs from
url = 'https://www.swiggy.com/instamart/category-listing?categoryName=Dairy%2C+Bread+and+Eggs&custom_back=true&taxonomyType=All+Listing'
extract_all_urls(url)
