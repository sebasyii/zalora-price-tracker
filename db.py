import datetime
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["zalora"]


def add_product_details(details):

    new = db["products"]
    product_id = details["sku"]
    details["date"] = datetime.datetime.utcnow()

    try:
        new.update_one(
            {
                "product_id": product_id
            },
            {
                "$set": {
                    "product_id": product_id
                },
                "$push": {
                    "details": details
                }
            },
            upsert=True
        )
        return True
    except Exception as identifier:
        print(identifier)
        return False


def get_product_history(product_id):
    new = db["products"]
    try:
        find = new.find_one({"product_id": product_id}, {"_id": 0})
        if find:
            return find
    except Exception as identifier:
        print(identifier)
        return None
