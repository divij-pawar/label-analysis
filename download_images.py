import requests
import os
from urllib.parse import urljoin
import csv
import ast


url = "https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto/"



def read_csv(file_path):
    rows = []
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append({
                'product_id': row['product_id'],
                'images': row['images'],
                'display_name': row['display_name']
            })
    return rows



def download_image_from_url(product_name, img_url):
    folder = f"/mnt/c/Users/divij/Music/nutr-analysis/product_images/{product_name.replace(' ', '_')}"
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    img_url = urljoin(url, img_url)
    # Get the image response
    img_response = requests.get(img_url)

    # Get the image name and save it
    img_name = os.path.join(folder, os.path.basename(img_url))
    img_name += ".jpg"
    with open(img_name, 'wb') as f:
        f.write(img_response.content)
    print(f'Downloaded {img_name}')


file_path = 'all_products.csv'
results = read_csv(file_path)
for row in results:
    for image_id in ast.literal_eval(row['images']):
        download_image_from_url(row['product_id'], url+str(image_id))