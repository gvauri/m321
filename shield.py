import time
import uuid

from pymongo import MongoClient
import requests

import energy_management

vakuumsensor_url = "http://10.255.255.254:2037"

def get_measure_data():
    id = str(uuid.uuid4())
    payload = {"request_id": id}
    requests.post(vakuumsensor_url+"/trigger_measurement", json=payload)
    while requests.get(vakuumsensor_url+"/measurements/" + id).json()["state"] != "measured":
        time.sleep(2)
    result = requests.get(vakuumsensor_url+"/measurements/" + id).json()["result"]
    requests.delete(vakuumsensor_url+"/measurements/" + id)
    return result

def speicher_in_db():
    while True:
        result = get_measure_data()
        print(result)
        client = MongoClient("mongodb://theship:theship1234@10.255.255.254:2021/theshipdb")
        db = client["theshipdb"]
        collection = db["vacuum-energy"]
        collection.delete_many({})
        result_to_return = result
        collection.insert_one({
            "data": result_to_return
        })
        client.close()

def schild_ein():
    energy_management.fliegen_ein(schild=1)
    speicher_in_db()
schild_ein()