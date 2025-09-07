import time
import cargo
import energy_management
import requests

url = "http://10.255.255.254:2018/"


def mine(matter_stabilizer=0, laser_amplifier=0, laser=1):
    energy_management.mining_ein(matter_stabilizer, laser_amplifier, laser)
    response = activate()
    while cargo.get_free_hold() > 0:
        s = state()
        print(s)
        if cargo.muss_bewegt_werden():
            deactivate()
            energy_management.cargo_bot_ein(matter_stabilizer)
            cargo.bewege_alle_nach_hinten_structure(.5)
            energy_management.mining_ein(matter_stabilizer, laser_amplifier, laser)
        if response.status_code == 403:
            print("cooling down")
            time.sleep(30)
            find_correct_angle()
        elif (not bool(s["is_active"])):
            response = activate()
            print("activate: " + str(response.json()))
        elif (not bool(s["is_mining"])):
            print("coorect angle")
            find_correct_angle()
        time.sleep(1)
    deactivate()
    energy_management.mining_aus(matter_stabilizer)

def find_correct_angle():
    a = 0
    while not bool(state()["is_mining"]):
        if (not bool(state()["is_active"])):
            response = activate()
            print("activate: " + str(response.json()))
        a = (a + 22) % 360
        print(state())
        angle(a)
        time.sleep(1)
    return a


def state():
    return requests.get(url + "state").json()


def angle(angle):
    payload = {
        "angle": angle
    }
    return requests.put(url + "angle", json=payload)


def deactivate():
    return requests.post(url + "deactivate")


def activate():
    return requests.post(url + "activate")
