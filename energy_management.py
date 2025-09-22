import requests


def setze_energie(limits):
    try:
        requests.put("http://10.255.255.254:2032/limits", json=limits)
    except Exception as e:
        print("Exception occured: " + str(e))
    try:
        requests.put("http://10.255.255.254:2033/limits", json=limits)
    except Exception as e:
        print("Exception occured: " + str(e))


def fliegen_ein(matter_stabilizer=0, schild=0):
    setze_energie({
        "laser": 0,
        "cargo_bot": 0,
        "laser_amplifier": 0,
        "sensor_plasma_radiation": 0,
        "thruster_back": 1,
        "thruster_front": 1,
        "thruster_front_left": 1,
        "thruster_front_right": 1,
        "thruster_bottom_left": 1,
        "thruster_bottom_right": 1,
        "scanner": 1,
        "sensor_atomic_field": matter_stabilizer,
        "matter_stabilizer": matter_stabilizer,
        "nuclear_reactor": 0,
        "sensor_void_energy": schild,
        "shield_generator": schild,
    })


def mining_ein(matter_stabilizer=0, laser_amplifier=0, laser=1, shield=0):
    setze_energie({
        "laser": laser,
        "cargo_bot": 0,
        "laser_amplifier": laser_amplifier,
        "sensor_plasma_radiation": laser_amplifier,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_front_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_left": 0,
        "thruster_bottom_right": 0,
        "scanner": 0,
        "sensor_atomic_field": matter_stabilizer,
        "matter_stabilizer": matter_stabilizer,
        "nuclear_reactor": 0,
        "analyzer_beta": 0,
        "sensor_void_energy": shield,
        "shield_generator": shield,
    })


def cargo_bot_ein(matter_stabilizer=0, shield=0):
    setze_energie({
        "laser": 0,
        "cargo_bot": 1,
        "laser_amplifier": 0,
        "sensor_plasma_radiation": 0,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_front_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_left": 0,
        "thruster_bottom_right": 0,
        "scanner": 0,
        "sensor_atomic_field": matter_stabilizer,
        "matter_stabilizer": matter_stabilizer,
        "nuclear_reactor": 0,
        "analyzer_beta": 0,
        "sensor_void_energy": shield,
        "shield_generator": shield,
    })


def get_energie():
    return requests.get("http://10.255.255.254:2033/limits").json()


def jumpdrive_ein():
    setze_energie({
        "laser": 0,
        "cargo_bot": 0,
        "laser_amplifier": 0,
        "sensor_plasma_radiation": 0,
        "thruster_back": 0,
        "thruster_front": 0,
        "thruster_front_left": 0,
        "thruster_front_right": 0,
        "thruster_bottom_left": 0,
        "thruster_bottom_right": 0,
        "scanner": 0,
        "sensor_atomic_field": 0,
        "matter_stabilizer": 0,
        "jumpdrive": 1,
        "nuclear_reactor": 1
    })
