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

def get_last_row_where_no_item():
    last_empty_row = 0
    for i, row in enumerate(cargo.get_structure().json()["hold"]):
        if all(cell is None for cell in row):
            last_empty_row = i
    return last_empty_row

def bewege_magnon():
    last_row = get_last_row_where_no_item()
    for y in range(last_row):
        for x in range(6):
            print(bewege_structure({
                "a": {
                    "x": x*2+last_row%2,
                    "y": y
                },
                "b": {
                    "x": x*2+last_row%2,
                    "y": y + 1
                }
            }).json())
            time.sleep(.5)
    for x in range(6):
        print(bewege_structure({
            "a": {
                "x": x*2,
                "y": 0
            },
            "b": {
                "x": x*2+1,
                "y": 0
            }
        }).json())
        print(x,0," ", x*2+magnon_erste_zeile_richtung(last_row), 0)
        time.sleep(.5)

def magnon_erste_zeile_richtung(last_row):
    if last_row%1:
        return -1
    return 1
