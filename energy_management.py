import requests


def setze_energie(limits):
    requests.put("http://10.255.255.254:2032/limits", json=limits)
    requests.put("http://10.255.255.254:2033/limits", json=limits)


def fliegen_ein(matter_stabilizer=0):
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
    })


def mining_ein(matter_stabilizer=0, laser_amplifier=0, laser=1):
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
    })


def cargo_bot_ein(matter_stabilizer=0):
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
        "jumpdrive":1,
    })