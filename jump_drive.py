from opcua import Client
import energy_management
url = "opc.tcp://10.255.255.254:2035/"
client = Client(url)

def springe_zu(x, y):
    energy_management.jumpdrive_ein()
    try:
        client.connect()
        print("Verbunden mit Jumpdrive OPC UA Server")

        root = client.get_root_node()

        jump_to_method = client.get_node("i=20002")

        result = jump_to_method.call(x, y)
        print("JumpTo-Ergebnis:", result)

        get_charge_method = client.get_node("i=20005")
        charge_percent = get_charge_method.call()
        print("Akkuladung:", charge_percent, "%")

    finally:
        client.disconnect()
    energy_management.fliegen_ein()
