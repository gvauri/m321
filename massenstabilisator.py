import requests
from flask import Flask
import energy_management as e

app = Flask(__name__)


@app.route(rule="/", methods=["GET"])
def massenstabilisator():
    response = requests.get("http://10.255.255.254:2038/data")
    json = response.json()
    print(json)
    return {"data": json.get("measurement")}


def run():
    e.setze_energie({
    "sensor_atomic_field": 1,
    "matter_stabilizer": 1,
    })
    app.run(host='0.0.0.0', port=2101)


run()
