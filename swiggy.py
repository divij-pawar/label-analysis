import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

itemid="CNP270FMTW" #swiggy item ID
service = webdriver.ChromeService()
service = webdriver.ChromeService(executable_path="C:\\Users\\divij\\Music\\nutr-analysis\\chromedriver.exe")
def download_images(url, folder):
    # Set up Selenium WebDriver with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # driver = webdriver.Chrome(service=Service('/path/to/chromedriver'), options=chrome_options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(url)
    
    # Get page source after JavaScript is executed
    html = driver.page_source
    driver.quit()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    div_tags = soup.find_all('div', {'data-testid': 'image-card-div'})

    # # Find all image tags
    # img_tags = soup.find_all('img')

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download each image
    for div in div_tags:
        img_tags = div.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                # Ensure the URL is absolute
                img_url = urljoin(url, img_url)
                # Get the image response
                img_response = requests.get(img_url)

                # Get the image name and save it
                img_name = os.path.join(folder, os.path.basename(img_url))
                img_name += ".jpg"
                with open(img_name, 'wb') as f:
                    f.write(img_response.content)
                print(f'Downloaded {img_name}')

url = f'https://www.swiggy.com/instamart/item/{itemid}'
folder = 'swiggy/'+itemid
download_images(url, folder)




