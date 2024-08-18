import forms
from forms import *


effect_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "effect_config.json")
spatial_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spatial_config.json")
presets_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets.json")
preset_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presets")


def read_effect_config():
    with open(effect_config_file_path, "r") as fin:
        config = json.load(fin)

    return config


def read_spatial_config():
    with open(spatial_config_file_path, "r") as fin:
        config = json.load(fin)

    return config


def load_presets():
    with open(presets_file_path, "r") as fin:
        return json.load(fin)


effect_config = read_effect_config()
spatial_config = read_spatial_config()
presets = load_presets()


def save_config():
    with open(effect_config_file_path, "w") as fout:
        json.dump(effect_config, fout)
    with open(spatial_config_file_path, "w") as fout:
        json.dump(spatial_config, fout)


def containerise_elements(elements):
    remaining_element_indexes = [element for element in elements]
    complete_containers = []
    for container_index in setup_config["containers"]:
        if all([element_index in remaining_element_indexes for element_index in setup_config["container_elements"][container_index]]):
            complete_containers.append(container_index)
            for element_index in setup_config["container_elements"][container_index]:
                remaining_element_indexes.remove(element_index)

    return complete_containers, remaining_element_indexes


def containerise_elements_with_names(elements):
    remaining_element_indexes = [element[0] for element in elements]
    complete_containers = []
    for container_index in setup_config["containers"]:
        if all([element_index in remaining_element_indexes for element_index in setup_config["container_elements"][container_index]]):
            complete_containers.append((container_index, setup_config["container_names"][container_index]))
            for element_index in setup_config["container_elements"][container_index]:
                remaining_element_indexes.remove(element_index)

    remaining_elements = [(element_index, setup_config["element_names"][element_index]) for element_index in remaining_element_indexes]

    return complete_containers, remaining_elements


def get_elements_with_same_effect_config(element_index):
    indexes = []
    for i in setup_config["elements"]:
        if effect_config["elements"][i]["effect"] == effect_config["elements"][element_index]["effect"]:
            indexes.append(i)

    return indexes


def get_elements_with_same_rainbow_config(element_index):
    indexes = []
    for i in setup_config["elements"]:
        if effect_config["elements"][i]["rainbow"] == effect_config["elements"][element_index]["rainbow"]:
            indexes.append(i)

    return indexes


def get_elements_with_same_audio_config(element_index):
    indexes = []
    for i in setup_config["elements"]:
        if effect_config["elements"][i]["audio"] == effect_config["elements"][element_index]["audio"]:
            indexes.append(i)

    return indexes


def get_elements_with_same_spectrum_bars_config(element_index):
    indexes = []
    for i in setup_config["elements"]:
        if effect_config["elements"][i]["spectrum_bars"] == effect_config["elements"][element_index]["spectrum_bars"]:
            indexes.append(i)

    return indexes


def get_elements_with_same_audio_bins_config(element_index):
    indexes = []
    for i in setup_config["elements"]:
        if effect_config["elements"][i]["audio_bins"] == effect_config["elements"][element_index]["audio_bins"]:
            indexes.append(i)

    return indexes


def apply_effect(effect_form: forms.EffectForm):
    for element_index in get_all_target_elements(effect_form.targets):
        effect_config["elements"][element_index]["effect"]["enabled"] = effect_form.enabled.data
        effect_config["elements"][element_index]["effect"]["effect_name"] = effect_form.effect_name.data

    save_config()


def read_effect_to_form(effect_form, element_index):
    effect_form.enabled.data = effect_config["elements"][element_index]["effect"]["enabled"]
    effect_form.effect_name.data = effect_config["elements"][element_index]["effect"]["effect_name"]

    containers, elements = containerise_elements(get_elements_with_same_effect_config(element_index))
    if len(elements) != 0:
        effect_form.targets.apply_to_elements.data = True
        effect_form.targets.element_indexes.data = elements
    if len(containers) != 0:
        effect_form.targets.apply_to_containers.data = True
        effect_form.targets.container_indexes.data = containers


def apply_audio(audio_form: forms.AudioForm):
    for element_index in get_all_target_elements(audio_form.targets):
        effect_config["elements"][element_index]["audio"]["base_effect"] = audio_form.base_effect.data
        effect_config["elements"][element_index]["audio"]["show_peaks"] = audio_form.show_peaks.data
        effect_config["elements"][element_index]["audio"]["max_fallback_divider"] = audio_form.max_fallback_divider.data
        effect_config["elements"][element_index]["audio"]["peak_fallback_rate"] = audio_form.peak_fallback_rate.data

    save_config()


def apply_spectrum_bars(spectrum_bars_form: forms.SpectrumBarsForm):
    for element_index in get_all_target_elements(spectrum_bars_form.targets):
        effect_config["elements"][element_index]["spectrum_bars"]["hue_offset_low"] = spectrum_bars_form.hue_offset_low.data
        effect_config["elements"][element_index]["spectrum_bars"]["hue_offset_high"] = spectrum_bars_form.hue_offset_high.data
        effect_config["elements"][element_index]["spectrum_bars"]["hue_offset_peak"] = spectrum_bars_form.hue_offset_peak.data
        effect_config["elements"][element_index]["spectrum_bars"]["hue_start"] = spectrum_bars_form.hue_start.data
        effect_config["elements"][element_index]["spectrum_bars"]["hue_end"] = spectrum_bars_form.hue_end.data
        effect_config["elements"][element_index]["spectrum_bars"]["period"] = spectrum_bars_form.period.data
        effect_config["elements"][element_index]["spectrum_bars"]["value"] = spectrum_bars_form.value.data
        effect_config["elements"][element_index]["spectrum_bars"]["saturation"] = spectrum_bars_form.saturation.data
        effect_config["elements"][element_index]["spectrum_bars"]["absolute_range"] = spectrum_bars_form.absolute_range.data
        effect_config["elements"][element_index]["spectrum_bars"]["range_to_max"] = spectrum_bars_form.range_to_max.data

    save_config()


def apply_audio_bins(audio_bins_form: forms.AudioBinsForm):
    for element_index in get_all_target_elements(audio_bins_form.targets):
        effect_config["elements"][element_index]["audio_bins"]["reverse"] = audio_bins_form.reverse.data
        effect_config["elements"][element_index]["audio_bins"]["dual_bars"] = audio_bins_form.dual_bars.data
        effect_config["elements"][element_index]["audio_bins"]["middle_out"] = audio_bins_form.middle_out.data
        effect_config["elements"][element_index]["audio_bins"]["bar_1_bin_start"] = audio_bins_form.bar_1_bin_start.data
        effect_config["elements"][element_index]["audio_bins"]["bar_1_bin_end"] = audio_bins_form.bar_1_bin_end.data
        effect_config["elements"][element_index]["audio_bins"]["bar_2_bin_start"] = audio_bins_form.bar_2_bin_start.data
        effect_config["elements"][element_index]["audio_bins"]["bar_2_bin_end"] = audio_bins_form.bar_2_bin_end.data

    save_config()


def read_audio_to_form(audio_form, element_index):
    audio_form.base_effect.data = effect_config["elements"][element_index]["audio"]["base_effect"]
    audio_form.show_peaks.data = effect_config["elements"][element_index]["audio"]["show_peaks"]
    audio_form.max_fallback_divider.data = effect_config["elements"][element_index]["audio"]["max_fallback_divider"]
    audio_form.peak_fallback_rate.data = effect_config["elements"][element_index]["audio"]["peak_fallback_rate"]

    containers, elements = containerise_elements(get_elements_with_same_audio_config(element_index))
    if len(elements) != 0:
        audio_form.targets.apply_to_elements.data = True
        audio_form.targets.element_indexes.data = elements
    if len(containers) != 0:
        audio_form.targets.apply_to_containers.data = True
        audio_form.targets.container_indexes.data = containers


def read_spectrum_bars_to_form(spectrum_bars_form, element_index):
    spectrum_bars_form.hue_offset_low.data = effect_config["elements"][element_index]["spectrum_bars"]["hue_offset_low"]
    spectrum_bars_form.hue_offset_high.data = effect_config["elements"][element_index]["spectrum_bars"]["hue_offset_high"]
    spectrum_bars_form.hue_offset_peak.data = effect_config["elements"][element_index]["spectrum_bars"]["hue_offset_peak"]
    spectrum_bars_form.hue_start.data = effect_config["elements"][element_index]["spectrum_bars"]["hue_start"]
    spectrum_bars_form.hue_end.data = effect_config["elements"][element_index]["spectrum_bars"]["hue_end"]
    spectrum_bars_form.period.data = effect_config["elements"][element_index]["spectrum_bars"]["period"]
    spectrum_bars_form.value.data = effect_config["elements"][element_index]["spectrum_bars"]["value"]
    spectrum_bars_form.saturation.data = effect_config["elements"][element_index]["spectrum_bars"]["saturation"]
    spectrum_bars_form.absolute_range.data = effect_config["elements"][element_index]["spectrum_bars"]["absolute_range"]
    spectrum_bars_form.range_to_max.data = effect_config["elements"][element_index]["spectrum_bars"]["range_to_max"]

    containers, elements = containerise_elements(get_elements_with_same_spectrum_bars_config(element_index))
    if len(elements) != 0:
        spectrum_bars_form.targets.apply_to_elements.data = True
        spectrum_bars_form.targets.element_indexes.data = elements
    if len(containers) != 0:
        spectrum_bars_form.targets.apply_to_containers.data = True
        spectrum_bars_form.targets.container_indexes.data = containers


def read_audio_bins_to_form(audio_bins_form, element_index):

    audio_bins_form.reverse.data = effect_config["elements"][element_index]["audio_bins"]["reverse"]
    audio_bins_form.dual_bars.data = effect_config["elements"][element_index]["audio_bins"]["dual_bars"]
    audio_bins_form.middle_out.data = effect_config["elements"][element_index]["audio_bins"]["middle_out"]
    audio_bins_form.bar_1_bin_start.data = effect_config["elements"][element_index]["audio_bins"]["bar_1_bin_start"]
    audio_bins_form.bar_1_bin_end.data = effect_config["elements"][element_index]["audio_bins"]["bar_1_bin_end"]
    audio_bins_form.bar_2_bin_start.data = effect_config["elements"][element_index]["audio_bins"]["bar_2_bin_start"]
    audio_bins_form.bar_2_bin_end.data = effect_config["elements"][element_index]["audio_bins"]["bar_2_bin_end"]

    containers, elements = containerise_elements(get_elements_with_same_audio_bins_config(element_index))
    if len(elements) != 0:
        audio_bins_form.targets.apply_to_elements.data = True
        audio_bins_form.targets.element_indexes.data = elements
    if len(containers) != 0:
        audio_bins_form.targets.apply_to_containers.data = True
        audio_bins_form.targets.container_indexes.data = containers


def apply_rainbow(rainbow_form: forms.RainbowForm):
    for element_index in get_all_target_elements(rainbow_form.targets):
        effect_config["elements"][element_index]["rainbow"]["period"] = rainbow_form.period.data
        effect_config["elements"][element_index]["rainbow"]["hue_start"] = rainbow_form.hue_start.data
        effect_config["elements"][element_index]["rainbow"]["hue_end"] = rainbow_form.hue_end.data
        effect_config["elements"][element_index]["rainbow"]["direction"] = rainbow_form.direction.data
        effect_config["elements"][element_index]["rainbow"]["compress"] = rainbow_form.compress.data
        effect_config["elements"][element_index]["rainbow"]["value"] = rainbow_form.value.data
        effect_config["elements"][element_index]["rainbow"]["saturation"] = rainbow_form.saturation.data

    save_config()


def read_rainbow_to_form(rainbow_form, element_index):
    rainbow_form.period.data = effect_config["elements"][element_index]["rainbow"]["period"]
    rainbow_form.hue_start.data = effect_config["elements"][element_index]["rainbow"]["hue_start"]
    rainbow_form.hue_end.data = effect_config["elements"][element_index]["rainbow"]["hue_end"]
    rainbow_form.direction.data = effect_config["elements"][element_index]["rainbow"]["direction"]
    rainbow_form.compress.data = effect_config["elements"][element_index]["rainbow"]["compress"]
    rainbow_form.value.data = effect_config["elements"][element_index]["rainbow"]["value"]
    rainbow_form.saturation.data = effect_config["elements"][element_index]["rainbow"]["saturation"]

    containers, elements = containerise_elements(get_elements_with_same_rainbow_config(element_index))
    if len(elements) != 0:
        rainbow_form.targets.apply_to_elements.data = True
        rainbow_form.targets.element_indexes.data = elements
    if len(containers) != 0:
        rainbow_form.targets.apply_to_containers.data = True
        rainbow_form.targets.container_indexes.data = containers


def apply_spatial(spatial_form: forms.SpatialForm):
    for container_index in spatial_form.container_targets.container_indexes.data:
        spatial_config["containers"][container_index]["offsets"]["x"] = spatial_form.offset_x.data
        spatial_config["containers"][container_index]["offsets"]["y"] = spatial_form.offset_y.data
        spatial_config["containers"][container_index]["offsets"]["z"] = spatial_form.offset_z.data

        spatial_config["containers"][container_index]["viewpoint"]["x"] = spatial_form.viewer_x.data
        spatial_config["containers"][container_index]["viewpoint"]["y"] = spatial_form.viewer_y.data
        spatial_config["containers"][container_index]["viewpoint"]["z"] = spatial_form.viewer_z.data

    save_config()


def read_spatial_to_form(spatial_form, container_index):
    spatial_form.offset_x.data = spatial_config["containers"][container_index]["offsets"]["x"]
    spatial_form.offset_y.data = spatial_config["containers"][container_index]["offsets"]["y"]
    spatial_form.offset_z.data = spatial_config["containers"][container_index]["offsets"]["z"]

    spatial_form.viewer_x.data = spatial_config["containers"][container_index]["viewpoint"]["x"]
    spatial_form.viewer_y.data = spatial_config["containers"][container_index]["viewpoint"]["y"]
    spatial_form.viewer_z.data = spatial_config["containers"][container_index]["viewpoint"]["z"]

    spatial_form.container_targets.container_indexes.data = [container_index]


def get_effect_groups():
    effect_parameters = []
    effect_groups = []
    for element_index in setup_config["elements"]:
        if not effect_config["elements"][element_index]["effect"] in effect_parameters:
            effect_groups.append([element_index])
            effect_parameters.append(effect_config["elements"][element_index]["effect"])
        else:
            group_index = effect_parameters.index(effect_config["elements"][element_index]["effect"])
            effect_groups[group_index].append(element_index)

    return [
        [(element_index, setup_config["element_names"][element_index]) for element_index in group_indexes]
        for group_indexes in effect_groups]


def get_rainbow_groups():
    rainbow_parameters = []
    rainbow_groups = []
    for element_index in setup_config["elements"]:
        if not effect_config["elements"][element_index]["rainbow"] in rainbow_parameters:
            rainbow_groups.append([element_index])
            rainbow_parameters.append(effect_config["elements"][element_index]["rainbow"])
        else:
            group_index = rainbow_parameters.index(effect_config["elements"][element_index]["rainbow"])
            rainbow_groups[group_index].append(element_index)

    return [[(element_index, setup_config["element_names"][element_index]) for element_index in group_indexes] for group_indexes in rainbow_groups]


def get_audio_groups():
    audio_parameters = []
    audio_groups = []
    for element_index in setup_config["elements"]:
        if not effect_config["elements"][element_index]["audio"] in audio_parameters:
            audio_groups.append([element_index])
            audio_parameters.append(effect_config["elements"][element_index]["audio"])
        else:
            group_index = audio_parameters.index(effect_config["elements"][element_index]["audio"])
            audio_groups[group_index].append(element_index)

    return [[(element_index, setup_config["element_names"][element_index]) for element_index in group_indexes] for group_indexes in audio_groups]


def get_spectrum_bars_groups():
    spectrum_bars_parameters = []
    spectrum_bars_groups = []
    for element_index in setup_config["elements"]:
        if not effect_config["elements"][element_index]["spectrum_bars"] in spectrum_bars_parameters:
            spectrum_bars_groups.append([element_index])
            spectrum_bars_parameters.append(effect_config["elements"][element_index]["spectrum_bars"])
        else:
            group_index = spectrum_bars_parameters.index(effect_config["elements"][element_index]["spectrum_bars"])
            spectrum_bars_groups[group_index].append(element_index)

    return [[(element_index, setup_config["element_names"][element_index]) for element_index in group_indexes] for group_indexes in spectrum_bars_groups]


def get_audio_bins_groups():
    audio_bins_parameters = []
    audio_bins_groups = []
    for element_index in setup_config["elements"]:
        if not effect_config["elements"][element_index]["audio_bins"] in audio_bins_parameters:
            audio_bins_groups.append([element_index])
            audio_bins_parameters.append(effect_config["elements"][element_index]["audio_bins"])
        else:
            group_index = audio_bins_parameters.index(effect_config["elements"][element_index]["audio_bins"])
            audio_bins_groups[group_index].append(element_index)

    return [[(element_index, setup_config["element_names"][element_index]) for element_index in group_indexes] for group_indexes in audio_bins_groups]


def get_effect_summary(element_index):
    return effect_config["elements"][element_index]["effect"]


def get_rainbow_summary(element_index):
    return effect_config["elements"][element_index]["rainbow"]


def get_audio_summary(element_index):
    return effect_config["elements"][element_index]["audio"]


def get_spectrum_bars_summary(element_index):
    return effect_config["elements"][element_index]["spectrum_bars"]


def get_audio_bins_summary(element_index):
    return effect_config["elements"][element_index]["audio_bins"]


def get_container_spatial_summary(container_index):
    return spatial_config["containers"][container_index]


def save_effect_preset(save_effect_preset_form: forms.SavePresetForm):
    if save_effect_preset_form.preset_name.data not in presets["effects"]:
        presets["effects"][save_effect_preset_form.preset_name.data] = save_effect_preset_form.preset_description.data

        with open(os.path.join(preset_folder_path, save_effect_preset_form.preset_name.data + "-effect.json"), "w") as fout:
            json.dump(effect_config, fout)

        with open(presets_file_path, "w") as fout:
            json.dump(presets, fout)


def load_effect_preset(effect_preset_name: str):
    global effect_config
    if effect_preset_name in presets["effects"]:
        with open(os.path.join(preset_folder_path, effect_preset_name + "-effect.json"), "r") as fin:
            effect_config = json.load(fin)


def remove_effect_preset(effect_preset_name: str):
    if effect_preset_name in presets["effects"]:
        presets["effects"].pop(effect_preset_name)

        os.remove(os.path.join(preset_folder_path, effect_preset_name + "-effect.json"))

        with open(presets_file_path, "w") as fout:
            json.dump(presets, fout)


def save_spatial_preset(save_spatial_preset_form: forms.SavePresetForm):
    if save_spatial_preset_form.preset_name.data not in presets["spatial"]:
        presets["spatial"][save_spatial_preset_form.preset_name.data] = save_spatial_preset_form.preset_description.data

        with open(os.path.join(preset_folder_path, save_spatial_preset_form.preset_name.data + "-spatial.json"), "w") as fout:
            json.dump(spatial_config, fout)

        with open(presets_file_path, "w") as fout:
            json.dump(presets, fout)


def load_spatial_preset(spatial_preset_name: str):
    global spatial_config
    if spatial_preset_name in presets["spatial"]:
        with open(os.path.join(preset_folder_path, spatial_preset_name + "-spatial.json"), "r") as fin:
            spatial_config = json.load(fin)


def remove_spatial_preset(spatial_preset_name: str):
    if spatial_preset_name in presets["spatial"]:
        presets["spatial"].pop(spatial_preset_name)

        os.remove(os.path.join(preset_folder_path, spatial_preset_name + "-spatial.json"))

        with open(presets_file_path, "w") as fout:
            json.dump(presets, fout)
