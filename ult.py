import requests
import csv
import time
import random
import os

def get_response(url):
    headers = {
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "cookie": ("deviceId=s%3A2c0a1e44-3c6f-46ec-9ddd-1715a42517e3.i%2F%2FuUXFGsvnIIBdnezAGMjd4NjO1ehOZWuXI1%2F3vr9c; "
                "tid=s%3A8181cdfa-8bb0-4642-9263-0d7e9ee20de9.hA1iNSj0f6%2B9lzgp9Pm9lH%2FH0VIKMUaTiSX1UEd1dYM; "
                "sid=s%3Afna56d24-8b5a-443b-a3c0-14b306cd2734.UupBatXqK9IZ1WyspIKGsoffqO5Gph1gh75gSJCm%2Fe0; "
                "versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; "
                "ally-on=false; isNative=false; strId=; openIMHP=false; webBottomBarHeight=0; _gcl_au=1.1.379926304.1724174145; "
                "__SW=L2_DBFAVkCVErvoPDV8Aa0sT9AWHGeE6; _guest_tid=744434dd-3e19-400c-98d0-c3e8b16ddc10; _device_id=72068f96-28b0-8594-0b09-783d2569ae18; "
                "_sid=fnaca3b2-59b0-49ad-8b9d-a0e1370b7f87; fontsLoaded=1; _gid=GA1.2.1180604700.1724174157; location=%7B%22lat%22%3A19.2313448%2C%22lng%22%3A72.8635299%2C%22address%22%3A%22Mumbai%2C%20Maharashtra%20400066%2C%20India%22%2C%22area%22%3A%22mumbai%22%7D; "
                "lat=s%3A19.2313448.AlNkutWCpf%2BdQhE%2F86pY7DnkI%2BcntCWgqaBVLoFyJ3U; lng=s%3A72.8635299.%2FQoN8diQUBKtYBm%2BW3JzQWyDQ7RuLUTO%2Fe4XMaRhfgc; "
                "address=s%3AMumbai%2C%20Maharashtra%20400066%2C%20India.dvG8m1itEPxaojzQctu9x4m%2BvTZHIBSAdYcC6ik2MOA; "
                "addressId=s%3A.4Wx2Am9WLolnmzVcU32g6YaFDw0QbIBFRj2nkO7P25s; LocSrc=s%3AswgyUL.Dzm1rLPIhJmB3Tl2Xs6141hVZS0ofGP7LGmLXgQOA7Y; "
                "_ga_34JYJ0BCRN=GS1.1.1724174157.1.1.1724175930.0.0.0; userLocation=%7B%22address%22%3A%22Mumbai%2C%20Maharashtra%20400066%2C%20India%22%2C%22lat%22%3A19.2313448%2C%22lng%22%3A72.8635299%2C%22id%22%3A%22%22%2C%22annotation%22%3A%22%22%2C%22name%22%3A%22%22%7D; "
                "_ga=GA1.1.1460378741.1724174147; imOrderAttribution={%22entryId%22:null%2C%22entryName%22:null%2C%22entryContext%22:null%2C%22hpos%22:null%2C%22vpos%22:null%2C%22utm_source%22:null%2C%22utm_medium%22:null%2C%22utm_campaign%22:null}; "
                "_ga_8N8XRG907L=GS1.1.1724179005.2.1.1724180078.0.0.0"),
        "matcher": "a8gee8e9b8f77egdaecbc97",
        "origin": "https://www.swiggy.com",
        "priority": "u=1, i",
        "referer": "https://www.swiggy.com/instamart/search?categoryName=Atta%2C+Rice+and+Dals&custom_back=true&filterId=&query=maggi&storeId=1237261&taxonomyType=All+Listing",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    return data

def flatten_dict(dict_item):
    variation = dict_item["variations"][0]

    # Flatten the dictionary
    flat_data = {
        "id": variation["id"],
        "spin": variation["spin"],
        "mrp": variation["price"]["mrp"],
        "currency": variation["price"]["currency"],
        "store_price": variation["price"]["store_price"],
        "offer_price": variation["price"]["offer_price"],
        "unit_level_price": variation["price"]["unit_level_price"],
        "offer_id": variation["price"]["offer_applied"]["offer_id"],
        "listing_description": variation["price"]["offer_applied"]["listing_description"],
        "product_description": variation["price"]["offer_applied"]["product_description"],
        "super_offer": variation["price"]["offer_applied"]["super_offer"],
        "total_inventory": variation["inventory"]["total"],
        "remaining_inventory": variation["inventory"]["remaining"],
        "images" : str(variation.get("images", None)),
        "in_stock": variation["inventory"]["in_stock"],
        "quantity": variation["quantity"],
        "short_description": variation["meta"]["short_description"],
        "long_description": variation["meta"]["long_description"],
        "disclaimer": variation["meta"]["disclaimer"],
        "length_in_cm": variation["dimensions"]["length_in_cm"],
        "width_in_cm": variation["dimensions"]["width_in_cm"],
        "height_in_cm": variation["dimensions"]["height_in_cm"],
        "volume_in_cc": variation["dimensions"]["volume_in_cc"],
        "brand": variation["brand"],
        "category": variation["category"],
        "display_name": variation["display_name"],
        "super_saver": variation["super_saver"],
        "sku_quantity_with_combo": variation["sku_quantity_with_combo"],
        "max_allowed_quantity": variation["max_allowed_quantity"],
        "cart_allowed_quantity": variation["cart_allowed_quantity"]["total"],
        "weight_in_grams": variation["weight_in_grams"],
        "volumetric_weight": variation["volumetric_weight"],
        "alcohol_content_percentage": variation["alcohol_content_percentage"],
        "container_type": variation["container_type"],
        "sub_category_type": variation["sub_category_type"],
        "brand_id": variation["brand_id"],
        "product_name_without_brand": variation["product_name_without_brand"],
        "category_id": variation["category_id"],
        "sub_category": variation["sub_category"],
        "super_category": variation["super_category"],
        "store_id": variation["store_id"],
        "categoryId": dict_item["categoryId"],
        "brand": dict_item["brand"],
        "category": dict_item["category"],
        "retrievalRank": dict_item["retrievalRank"],
        "objectValue": dict_item["analytics"]["objectValue"],
        "context": dict_item["analytics"]["context"],
        "impressionObjectName": dict_item["analytics"]["impressionObjectName"],
        "clickObjectName": dict_item["analytics"]["clickObjectName"],
        "searchString": dict_item["analytics"]["extraFields"]["searchString"],
        "avail": dict_item["avail"],
        "adItem": dict_item["adItem"],
        "inStockAndSlotAvailable": dict_item["inStockAndSlotAvailable"],
        "product_id": dict_item["product_id"],
        "in_stock": dict_item["in_stock"],
        "badge_info": dict_item["badge_info"],
        "is_ad_item": dict_item["is_ad_item"],
        "search_result_type": dict_item["search_result_type"],
        "item_card_view": dict_item["item_card_view"],
        "super_category": dict_item["super_category"],
        "sub_category": dict_item["sub_category"]
    }
    return flat_data

def create_product_csv(query, data):
    query = query.replace("%20", "_")
    data = data["data"]["widgets"]
    product_ids = []
    for entry in data:
        if 'data' in entry:
            for item in entry['data']:
                if 'product_id' in item:
                    product_ids.append(item['product_id'])
                    # csv_filename = f"csvfiles/{query}_products_40.csv"
                    csv_filename = f"all_products.csv"
                    file_exists = os.path.isfile(csv_filename)
                    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
                        flat_data = flatten_dict(item)
                        writer = csv.DictWriter(file, fieldnames=flat_data.keys())
                        if not file_exists:
                            writer.writeheader()
                        writer.writerow(flat_data)
    return product_ids

def file_to_list(file_path):
    # Initialize an empty list to store sentences
    query_list = []
    # Open the file and read its content
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Strip leading/trailing spaces and add to the list if not empty
            stripped_line = line.strip()
            if stripped_line:
                query_list.append(stripped_line)
    return query_list

file_path = input(f"Enter a query file path: ")
query_list = file_to_list(file_path)

# Print the list of words
print("List of words:", query_list)

for query in query_list:

    page_num = 3
    limit = 100
    offset = 0
    store_id = 1237261
    time.sleep(random.randint(100, 1000)/ 1000.0)
    url = f"https://www.swiggy.com/api/instamart/search?pageNumber={page_num}&searchResultsOffset={offset}&limit={limit}&query={query}&ageConsent=false&layoutId=3990&pageType=INSTAMART_SEARCH_PAGE&isPreSearchTag=false&highConfidencePageNo=0&lowConfidencePageNo=0&voiceSearchTrackingId=&storeId={store_id}"

    data = get_response(url)
    product_ids = create_product_csv(query, data)