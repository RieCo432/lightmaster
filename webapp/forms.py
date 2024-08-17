from flask_wtf import FlaskForm
from wtforms import SubmitField, DecimalField, IntegerField, BooleanField, RadioField, SelectField, SelectMultipleField
import json
import os

from wtforms.fields.form import FormField
from wtforms.fields.numeric import FloatField
from wtforms.fields.simple import StringField

setup_config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setup_config.json")

with open(setup_config_file_path, "r") as fin:
    setup_config = json.load(fin)


class TargetForm(FlaskForm):
    apply_to_elements = BooleanField("Apply to Elements")
    element_indexes = SelectMultipleField("Element Selection",
                                          choices=[(index, name)
                                                   for index, name in zip(
                                                  setup_config["elements"],
                                                  setup_config["element_names"]
                                              )], coerce=int)

    apply_to_containers = BooleanField("Apply to Containers")
    container_indexes = SelectMultipleField("Container Selection",
                                            choices=[(index, name)
                                                     for index, name in zip(
                                                    setup_config["containers"],
                                                    setup_config["container_names"]
                                                )], coerce=int)

    class Meta:
        csrf = False


def get_all_target_elements(target_form):
    elements = []
    elements += target_form.element_indexes.data if target_form.apply_to_elements.data else []
    if target_form.apply_to_containers.data:
        for i in target_form.container_indexes.data:
            elements += setup_config["container_elements"][i]

    return list(set(elements))


class EffectForm(FlaskForm):
    enabled = BooleanField("Enabled")
    effect_name = SelectField('Effect Name', choices=[("rainbow", "Rainbow"), ("audio", "Audio"), ("spectrum_bars", "SpectrumBars")])

    targets = FormField(TargetForm)

    submit = SubmitField("Apply")

    class Meta:
        csrf = False


class AudioForm(FlaskForm):
    base_effect = SelectField('Base Effect', choices=[("rainbow", "Rainbow"), ("spectrumBars", "Spectrum Bars")])
    show_peaks = BooleanField("Show Peaks")
    max_fallback_divider = FloatField("Maximum Fallback Divider")
    peak_fallback_rate = IntegerField("Peak Fallback Rate")

    targets = FormField(TargetForm)

    submit = SubmitField("Apply")

    class Meta:
        csrf = False


class SpectrumBarsForm(FlaskForm):
    hue_offset_low = FloatField("Hue Offset Low")
    hue_offset_high = FloatField("Hue Offset High")
    hue_offset_peak = FloatField("Hue Offset Peak")
    hue_start = FloatField("Hue Start")
    hue_end = FloatField("Hue End")
    period = FloatField("Period")
    value = FloatField("Value")
    saturation = FloatField("Saturation")
    absolute_range = BooleanField("Absolute Range")
    range_to_max = FloatField("Range to Max")

    targets = FormField(TargetForm)

    submit = SubmitField("Apply")

    class Meta:
        csrf = False


class AudioBinsForm(FlaskForm):
    reverse = BooleanField("Reverse")
    dual_bars = BooleanField("Dual Bars")
    middle_out = BooleanField("Middle Out")
    bar_1_bin_start = IntegerField("Bar 1 Bin Start")
    bar_1_bin_end = IntegerField("Bar 1 Bin End")
    bar_2_bin_start = IntegerField("Bar 2 Bin Start")
    bar_2_bin_end = IntegerField("Bar 2 Bin End")

    targets = FormField(TargetForm)

    submit = SubmitField("Apply")

    class Meta:
        csrf = False


class RainbowForm(FlaskForm):
    period = FloatField("Period")
    hue_start = FloatField("Hue Start")
    hue_end = FloatField("Hue End")
    direction = SelectField("Direction", choices=[(0, "Horizontal"), (1, "Vertical")])
    compress = IntegerField("Compress")
    value = FloatField("Value")
    saturation = FloatField("Saturation")

    targets = FormField(TargetForm)

    submit = SubmitField("Apply")

    class Meta:
        csrf = False

