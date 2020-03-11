import requests
from bs4 import BeautifulSoup
import re


def extract_url(url):
    if url.find("www.zalora.sg") != -1:
        index = url.find('/?')
        if index != -1:
            url = url.split('/?')[0]
        else:
            url = url

    else:
        url = None

    return url


# Read More About String Manipulation
def get_converted_price(price):

    replaced_price = re.sub(r'[^\d.]+', "", price)

    converted_price = float(replaced_price)

    return converted_price


def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
    details = {"name": "", "price": 0, "deal": True, "url": "", "sku": ""}
    _url = extract_url(url)
    if _url is None:
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        product_brand = soup.find("div", {"class": "product__brand"}).find("a")
        product_title = soup.find("div", {"class": "product__title"})
        product_sku = soup.find("td", {"itemprop": "sku"}).get_text().strip()
        full_product_name = f"{product_brand.get_text().strip()} {product_title.get_text().strip()}"
        price = soup.find(id="js-detail_specialPrice_without_selectedSize")
        if price is None:
            price = soup.find(id="js-detail_price_without_selectedSize")
            details["deal"] = False
        if full_product_name is not None and price is not None:
            details["name"] = full_product_name
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url
            details["sku"] = product_sku
        else:
            return None
    return details
