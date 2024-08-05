import json

from config_manager import read_effect_config
from forms import setup_config


def send_config_factory():
    old_config = read_effect_config()
    
    def send_config():
        nonlocal old_config
        new_effect_config = read_effect_config()

        for element_index in setup_config["elements"]:
            for config_type in old_config["elements"][element_index].keys():
                data_to_send = {}
                for parameter in old_config["elements"][element_index][config_type].keys():
                    if old_config["elements"][element_index][config_type][parameter] != new_effect_config["elements"][element_index][config_type][parameter]:
                        data_to_send[parameter] = new_effect_config["elements"][element_index][config_type][parameter]

                if len(data_to_send) > 0:
                    json_to_send = {"target": "element", "index": element_index, "type": config_type, "data": data_to_send}
                    print(json.dumps(json_to_send))

        old_config = new_effect_config

    return send_config

