import forms
from forms import *


effect_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "effect_config.json")

with open(effect_config_file_path, "r") as fin:
    effect_config = json.load(fin)


def save_config():
    with open(effect_config_file_path, "w") as fout:
        json.dump(effect_config, fout)


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
        effect_config["elements"][element_index]["audio"]["hue_offset_low"] = audio_form.hue_offset_low.data
        effect_config["elements"][element_index]["audio"]["hue_offset_high"] = audio_form.hue_offset_high.data
        effect_config["elements"][element_index]["audio"]["hue_offset_peak"] = audio_form.hue_offset_peak.data
        effect_config["elements"][element_index]["audio"]["hue_start"] = audio_form.hue_start.data
        effect_config["elements"][element_index]["audio"]["hue_end"] = audio_form.hue_end.data
        effect_config["elements"][element_index]["audio"]["period"] = audio_form.period.data
        effect_config["elements"][element_index]["audio"]["value"] = audio_form.value.data
        effect_config["elements"][element_index]["audio"]["saturation"] = audio_form.saturation.data
        effect_config["elements"][element_index]["audio"]["absolute_range"] = audio_form.absolute_range.data
        effect_config["elements"][element_index]["audio"]["range_to_max"] = audio_form.range_to_max.data
        effect_config["elements"][element_index]["audio"]["reverse"] = audio_form.reverse.data
        effect_config["elements"][element_index]["audio"]["dual_bars"] = audio_form.dual_bars.data
        effect_config["elements"][element_index]["audio"]["middle_out"] = audio_form.middle_out.data
        effect_config["elements"][element_index]["audio"]["bar_1_bin_start"] = audio_form.bar_1_bin_start.data
        effect_config["elements"][element_index]["audio"]["bar_1_bin_end"] = audio_form.bar_1_bin_end.data
        effect_config["elements"][element_index]["audio"]["bar_2_bin_start"] = audio_form.bar_2_bin_start.data
        effect_config["elements"][element_index]["audio"]["bar_2_bin_end"] = audio_form.bar_2_bin_end.data
        effect_config["elements"][element_index]["audio"]["max_fallback_divider"] = audio_form.max_fallback_divider.data
        effect_config["elements"][element_index]["audio"]["peak_fallback_rate"] = audio_form.peak_fallback_rate.data

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
    audio_form.hue_offset_low.data = effect_config["elements"][element_index]["audio"]["hue_offset_low"]
    audio_form.hue_offset_high.data = effect_config["elements"][element_index]["audio"]["hue_offset_high"]
    audio_form.hue_offset_peak.data = effect_config["elements"][element_index]["audio"]["hue_offset_peak"]
    audio_form.hue_start.data = effect_config["elements"][element_index]["audio"]["hue_start"]
    audio_form.hue_end.data = effect_config["elements"][element_index]["audio"]["hue_end"]
    audio_form.period.data = effect_config["elements"][element_index]["audio"]["period"]
    audio_form.value.data = effect_config["elements"][element_index]["audio"]["value"]
    audio_form.saturation.data = effect_config["elements"][element_index]["audio"]["saturation"]
    audio_form.absolute_range.data = effect_config["elements"][element_index]["audio"]["absolute_range"]
    audio_form.range_to_max.data = effect_config["elements"][element_index]["audio"]["range_to_max"]
    audio_form.reverse.data = effect_config["elements"][element_index]["audio"]["reverse"]
    audio_form.dual_bars.data = effect_config["elements"][element_index]["audio"]["dual_bars"]
    audio_form.middle_out.data = effect_config["elements"][element_index]["audio"]["middle_out"]
    audio_form.bar_1_bin_start.data = effect_config["elements"][element_index]["audio"]["bar_1_bin_start"]
    audio_form.bar_1_bin_end.data = effect_config["elements"][element_index]["audio"]["bar_1_bin_end"]
    audio_form.bar_2_bin_start.data = effect_config["elements"][element_index]["audio"]["bar_2_bin_start"]
    audio_form.bar_2_bin_end.data = effect_config["elements"][element_index]["audio"]["bar_2_bin_end"]
    audio_form.max_fallback_divider.data = effect_config["elements"][element_index]["audio"]["max_fallback_divider"]
    audio_form.peak_fallback_rate.data = effect_config["elements"][element_index]["audio"]["peak_fallback_rate"]

    containers, elements = containerise_elements(get_elements_with_same_audio_config(element_index))
    if len(elements) != 0:
        audio_form.targets.apply_to_elements.data = True
        audio_form.targets.element_indexes.data = elements
    if len(containers) != 0:
        audio_form.targets.apply_to_containers.data = True
        audio_form.targets.container_indexes.data = containers


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


def get_audio_bins_summary(element_index):
    return effect_config["elements"][element_index]["audio_bins"]
