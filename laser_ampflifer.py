import time
import threading
import requests
from flask import Flask
import energy_management as e

app = Flask(__name__)

last_measure = ""

@app.route("/data", methods=["GET"])
def laser_ampflifer():
    global last_measure
    print(last_measure)
    return last_measure

def update_measure_loop():
    global last_measure
    while True:
        try:
            response = requests.post("http://10.255.255.254:2042/measure", timeout=10)
            print("Messdaten empfangen:", response.text)
            last_measure = response.json().get("rad", "")
            print("last_measure:", last_measure)
        except Exception as ex:
            print("Fehler beim Abrufen der Messdaten:", ex)
        time.sleep(5)

def start_flask():
    app.run(host='0.0.0.0', port=2104, use_reloader=False)

def run():
    e.setze_energie({
        "laser_amplifier": 1,
        "sensor_plasma_radiation": 1,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_front_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_left": 0,
        "thruster_bottom_right": 0,
        "scanner":0
    })

    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    update_measure_loop()

if __name__ == '__main__':
    run()
