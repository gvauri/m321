import requests
import time
import threading

import cargo

url = "http://10.255.255.254:2012/"


def get_free_hold():
    return get_cargo_hold().json()["hold"]["hold_free"]

def get_hold_size():
    return get_cargo_hold().json()["hold"]["hold_size"]


def get_cargo_hold():
    return requests.get(url + "hold")


def get_structure():
    return requests.get(url + "structure")


def bewege_structure(payload):
    return requests.post(url + "swap_adjacent", json=payload)


def bewege_nach_hinten_wenn_voll(sleep=.5):
    muss_bewegt_werden_ = muss_bewegt_werden()
    print("bewege nachhinten wenn voll: " + str(muss_bewegt_werden_))
    if muss_bewegt_werden_:
        bewege_alle_nach_hinten_structure(sleep)


def muss_bewegt_werden():
    return all(item is not None for item in get_structure().json()["hold"][0])


def bewege_alle_nach_hinten_structure(sleep):
    for y in range(get_last_none_row()):
        for x in range(12):
            print(bewege_structure({
                "a": {
                    "x": x,
                    "y": y
                },
                "b": {
                    "x": x,
                    "y": y + 1
                }
            }).json())
            time.sleep(sleep)

def get_last_none_row():
    last_none_row = 0
    for i, row in enumerate(cargo.get_structure().json()["hold"]):
        if any(cell is None for cell in row):
            last_none_row = i
    return last_none_row
