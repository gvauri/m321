import time

from opcua import Client, ua
import energy_management

url = "opc.tcp://10.255.255.254:2035/"
client = Client(url)


def springe_zu(x, y):
    energy_management.jumpdrive_ein()
    time.sleep(20)
    client.connect()
    node = client.get_node("ns=0;i=20001")
    print(f"Node Name: {node.get_browse_name()}")


    result = node.call_method(
        "0:JumpTo",
        ua.Variant(x, ua.VariantType.Int32),
        ua.Variant(y, ua.VariantType.Int32)
    )

    print("JumpTo-Ergebnis:", result)
    client.disconnect()
    energy_management.fliegen_ein()


springe_zu(1000, 1000)
