import json

from config_manager import read_effect_config, read_spatial_config
from forms import setup_config
from time import sleep

import serial

connected = False
attempts_left = 60
while not connected and attempts_left > 1:
    try:
        sleep(5)
        ser = serial.Serial('/dev/serial0', 9600, timeout=2)
        ser.flush()
        connected = True
        print("connected!")
    except serial.serialutil.SerialException:
        attempts_left -= 1

if not connected:
    exit(1)


def write_to_serial(json_dict):
    line = (json.dumps(json_dict) + "\n").encode('utf-8')
    ser.write(line)
    ser.flush()
    print("written:", line)
    if ser.in_waiting:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)


## DUMMY METHOD FOR TESTING ON DEVELOPMENT MACHINE
# def write_to_serial(json_dict):
#     line = (json.dumps(json_dict) + "\n").encode('utf-8')
#     print(line)


def send_config_factory():
    old_effect_config = read_effect_config()
    old_spatial_config = read_spatial_config()
    
    def send_config():
        nonlocal old_effect_config
        nonlocal old_spatial_config

        new_effect_config = read_effect_config()
        new_spatial_config = read_spatial_config()

        for element_index in setup_config["elements"]:
            for config_type in old_effect_config["elements"][element_index].keys():
                data_to_send = {}
                for parameter in old_effect_config["elements"][element_index][config_type].keys():
                    if old_effect_config["elements"][element_index][config_type][parameter] != new_effect_config["elements"][element_index][config_type][parameter]:
                        data_to_send[parameter] = new_effect_config["elements"][element_index][config_type][parameter]

                if len(data_to_send) > 0:
                    json_to_send = {"target": "element", "index": element_index, "type": config_type, "data": data_to_send}
                    write_to_serial(json_to_send)

        old_effect_config = new_effect_config

        for container_index in setup_config["containers"]:
            for config_type in old_spatial_config["containers"][container_index].keys():
                data_to_send = {}
                for parameter in old_spatial_config["containers"][container_index][config_type].keys():
                    if old_spatial_config["containers"][container_index][config_type][parameter] != new_spatial_config["containers"][container_index][config_type][parameter]:
                        data_to_send[parameter] = new_spatial_config["containers"][container_index][config_type][parameter]

                if len(data_to_send) > 0:
                    json_to_send = {"target": "container", "index": container_index, "type": config_type, "data": data_to_send}
                    write_to_serial(json_to_send)

        old_spatial_config = new_spatial_config

    return send_config


send_config = send_config_factory()


def send_entire_config():
    effect_config = read_effect_config()
    spatial_config = read_spatial_config()

    for element_index in setup_config["elements"]:
        for config_type in effect_config["elements"][element_index].keys():
            data_to_send = effect_config["elements"][element_index][config_type]

            json_to_send = {"target": "element", "index": element_index, "type": config_type, "data": data_to_send}
            write_to_serial(json_to_send)

    for container_index in setup_config["containers"]:
        for config_type in spatial_config["containers"][container_index].keys():
            data_to_send = spatial_config["containers"][container_index][config_type]

            json_to_send = {"target": "container", "index": container_index, "type": config_type, "data": data_to_send}
            write_to_serial(json_to_send)


if __name__ == "__main__":
    send_entire_config()
