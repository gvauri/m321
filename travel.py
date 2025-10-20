import requests
import communication as c
import cargo
import time
import mining
import energy_management

url = "http://10.255.255.254:2009/set_target"


def travel_station(station):
    energy_management.fliegen_ein()
    payload = {"target": station}
    return requests.post(url, json=payload)


def travel_position(x, y, matter_stabilizer=0, schild=0):
    energy_management.fliegen_ein(matter_stabilizer, schild)
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


def travel_and_sell(station="Core Station", what="IRON", amount=cargo.get_hold_size() - cargo.get_free_hold()):
    travel_station_wait_until_recive(station)
    print(amount)
    for i in range(int(amount / 10) + 1):
        c.sell(station, what, 12)
        time.sleep(.1)


def travel_position_and_sell(x, y, station, what, amount=cargo.get_hold_size() - cargo.get_free_hold()):
    travel_position_until_recive(x, y)
    print(amount)
    for i in range(int(amount / 10) + 1):
        c.sell(station, what, 12)
        time.sleep(.1)


def travel_station_wait_until_recive(station):
    travel_station(station)
    while not c.is_ship_at_station(station):
        time.sleep(1)
    print(station)


def travel_position_until_recive(x, y, matter_stabilizer=1, schild=0):
    travel_position(x, y, matter_stabilizer=matter_stabilizer, schild=schild)
    while not recived_position(x, y):
        time.sleep(1)
    time.sleep(.5)
    print("coords erreicht x:" + str(x) + ", y:" + str(y))


def recived_position(x, y):
    pos = position().json()["pos"]
    return x + 100 > pos["x"] > x - 100 and y + 100 > pos["y"] > y - 100


def travel_position_and_mine(x, y, laser_amplifier=0, matter_stabilizer=0, laser=1, shield=0, magnon=False):
    travel_position_until_recive(x, y + 200, matter_stabilizer=matter_stabilizer, schild=shield)
    time.sleep(2)
    mining.mine(matter_stabilizer, laser_amplifier, laser, shield, magnon)


def travell_and_sell_all_until_empty():
    while cargo.get_free_hold() != cargo.get_hold_size():
        resources = cargo.get_cargo_hold().json()["hold"]["resources"]
        print(resources)
        for resource, amount in resources.items():
            travel_and_sell(what=resource, amount=amount)


def travell_position_and_sell_all_until_empty(x, y, station):
    while cargo.get_free_hold() != cargo.get_hold_size():
        resources = cargo.get_cargo_hold().json()["hold"]["resources"]
        for resource, amount in resources.items():
            travel_position_and_sell(x, y, station, what=resource, amount=amount)


def travell_and_sell_all(station="Core Station"):
    resources = cargo.get_cargo_hold().json()["hold"]["resources"]
    print(resources)
    for resource, amount in resources.items():
        travel_and_sell(what=resource, amount=amount, station=station)


def travell_position_and_sell_all(x, y, station):
    resources = cargo.get_cargo_hold().json()["hold"]["resources"]
    for resource, amount in resources.items():
        travel_position_and_sell(x, y, station, what=resource, amount=amount)
