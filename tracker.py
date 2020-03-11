import db
import scraper
import time

URL = 'https://www.zalora.sg/adidas-adidas-sensebounce-m-shoes-white-1336685.html'


def track():

    details = scraper.get_product_details(URL)
    result = ""
    if details is None:
        result = "not done"
    else:
        inserted = db.add_product_details(details)
        if inserted:
            result = "done"
        else:
            result = "not done"
        return result


while True:
    print(track())
    time.sleep(60)
