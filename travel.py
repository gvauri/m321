import requests
import communication as c
import cargo
import time
import mining

url = "http://10.255.255.254:2009/set_target"


def travel_station(station):
    payload = {"target": station}
    return requests.post(url, json=payload)


def travel_position(x, y):
    payload = {"target": {"x": x, "y": y}}
    return requests.post(url, json=payload)


def position():
    return requests.get("http://10.255.255.254:2010/pos")


def travel_and_buy(station="Vesta Station", what="IRON", amount=cargo.get_free_hold()):
    travel_station_wait_until_recive(station)
    c.buy(station, what, amount)

def travel_position_and_buy(x, y, what="IRON", amount=cargo.get_free_hold()):
    travel_position_until_recive(x, y)
    time.sleep(5)
    c.buy(list(c.get_near_station().json()["stations"])[0], what, amount)

def travel_and_sell(station="Core Station", what="IRON", amount=cargo.get_free_hold()):
    travel_station_wait_until_recive(station)
    c.sell(station, what, amount)


def travel_station_wait_until_recive(station):
    travel_station(station)
    while not c.is_ship_at_station(station):
        time.sleep(1)
    print(station)


def travel_position_until_recive(x, y):
    travel_position(x, y)
    while not recived_position(x, y):
        time.sleep(1)
    time.sleep(.5)
    print("coords erreicht x:" + str(x) + ", y:" + str(y))


def recived_position(x, y):
    pos = position().json()["pos"]
    return x + 100 > pos["x"] > x - 100 and y + 100 > pos["y"] > y - 100

def travel_position_and_mine(x, y):
    travel_position_until_recive(x, y)
    time.sleep(2)
    mining.mine()