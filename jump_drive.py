import math
import time

from opcua import Client, ua
import energy_management
import requests

maximale_sprung_laenge = 19999
url = "opc.tcp://10.255.255.254:2035/"
client = Client(url)


def springe_zu(x, y, matter_stabilizer=0):
    client.connect()
    while not ist_punkt_erreicht(x, y):
        energy_management.jumpdrive_ein(matter_stabilizer)
        node = client.get_node("ns=0;i=20001")
        print(f"Node Name: {node.get_browse_name()}")

        wait_until_full_charged(node)
        next_x, next_y = berechne_naechster_punkt(x, y)
        print(f"Springe zu, x: {next_x}, y: {next_y}")
        result = node.call_method(
            "0:JumpTo",
            ua.Variant(next_x, ua.VariantType.Int32),
            ua.Variant(next_y, ua.VariantType.Int32)
        )

        print("JumpTo-Ergebnis:", result)
        energy_management.setze_energie({"nuclear_reactor":0})
    client.disconnect()


def ist_punkt_erreicht(x, y):
    pos = position().json()["pos"]
    return x + 100 > pos["x"] > x - 100 and y + 100 > pos["y"] > y - 100


def wait_until_full_charged(node):
    while True:
        result = node.call_method("0:GetChargePercent")
        print("Jumpdrive Percentage:", result)
        if result == 1:
            break
        time.sleep(5)


def berechne_naechster_punkt(x_ziel, y_ziel):
    pos = position()
    x_position, y_position = pos.json()["pos"]["x"], pos.json()["pos"]["y"]
    x_strecke, y_strecke = x_ziel - x_position, y_ziel - y_position
    strecke = math.sqrt(x_strecke ** 2 + y_strecke ** 2)
    if strecke < maximale_sprung_laenge:
        return x_ziel, y_ziel
    vx, vy = x_strecke / strecke, y_strecke / strecke
    print(vx, vy)
    return round(x_position + vx * maximale_sprung_laenge), round(y_position + vy * maximale_sprung_laenge)


def position():
    return requests.get("http://10.255.255.254:2010/pos")

