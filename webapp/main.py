from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap5

from forms import EffectForm, get_all_target_elements
from config_manager import *
from serial_interface import send_config, send_entire_config


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = "darkly"

send_entire_config()

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    effect_groups = get_effect_groups()
    effect_groups_formatted = []
    for effect_group in effect_groups:
        containers, elements = containerise_elements_with_names(effect_group)
        formatted_effect_group = {
            "link": url_for("effect", element=effect_group[0][0]),
            "text": ", ".join(
                [container[1] for container in containers]
                + [element[1] for element in elements]
            ),
            "summary": get_effect_summary(effect_group[0][0])
        }
        effect_groups_formatted.append(formatted_effect_group)

    rainbow_groups = get_rainbow_groups()
    rainbow_groups_formatted = []
    for rainbow_group in rainbow_groups:
        containers, elements = containerise_elements_with_names(rainbow_group)
        formatted_rainbow_group = {
            "link": url_for("rainbow", element=rainbow_group[0][0]),
            "text": ", ".join(
                [container[1] for container in containers]
                + [element[1] for element in elements]
            ),
            "summary": get_rainbow_summary(rainbow_group[0][0])
        }
        rainbow_groups_formatted.append(formatted_rainbow_group)

    audio_groups = get_audio_groups()
    audio_groups_formatted = []
    for audio_group in audio_groups:
        containers, elements = containerise_elements_with_names(audio_group)
        formatted_audio_group = {
            "link": url_for("audio", element=audio_group[0][0]),
            "text": ", ".join(
                [container[1] for container in containers]
                + [element[1] for element in elements]
            ),
            "summary": get_audio_summary(audio_group[0][0])
        }
        audio_groups_formatted.append(formatted_audio_group)

    spectrum_bars_groups = get_spectrum_bars_groups()
    spectrum_bars_groups_formatted = []
    for spectrum_bars_group in spectrum_bars_groups:
        containers, elements = containerise_elements_with_names(spectrum_bars_group)
        formatted_spectrum_bars_group = {
            "link": url_for("spectrum_bars", element=spectrum_bars_group[0][0]),
            "text": ", ".join(
                [container[1] for container in containers]
                + [element[1] for element in elements]
            ),
            "summary": get_spectrum_bars_summary(spectrum_bars_group[0][0])
        }
        spectrum_bars_groups_formatted.append(formatted_spectrum_bars_group)

    audio_bins_groups = get_audio_bins_groups()
    audio_bins_groups_formatted = []
    for audio_bins_group in audio_bins_groups:
        containers, elements = containerise_elements_with_names(audio_bins_group)
        formatted_audio_bins_group = {
            "link": url_for("bins", element=audio_bins_group[0][0]),
            "text": ", ".join(
                [container[1] for container in containers]
                + [element[1] for element in elements]
            ),
            "summary": get_audio_bins_summary(audio_bins_group[0][0])
        }
        audio_bins_groups_formatted.append(formatted_audio_bins_group)

    container_spatial_configs = read_spatial_config()
    container_spatial_configs_formatted = []
    for i, container_spatial_config in enumerate(container_spatial_configs["containers"]):
        formatted_container_spatial_config = {
            "link": url_for("spatial", container=i),
            "text": setup_config["container_names"][i],
            "summary": get_container_spatial_summary(i)
        }
        container_spatial_configs_formatted.append(formatted_container_spatial_config)

    return render_template("index.html", effect_groups_formatted=effect_groups_formatted, rainbow_groups_formatted=rainbow_groups_formatted, audio_groups_formatted=audio_groups_formatted, audio_bins_groups_formatted=audio_bins_groups_formatted, spectrum_bars_groups_formatted=spectrum_bars_groups_formatted, container_spatial_configs=container_spatial_configs_formatted)


@app.route("/effect", methods=["GET", "POST"])
def effect():
    effect_form = EffectForm()
    if effect_form.validate_on_submit():
        apply_effect(effect_form)
        send_config()
        flash("Effect applied")
        return redirect(url_for("index"))
    else:
        read_effect_to_form(effect_form, int(request.args.get("element")))

    return render_template("effect.html", effect_form=effect_form)


@app.route("/rainbow", methods=["GET", "POST"])
def rainbow():
    rainbow_form = RainbowForm()
    if rainbow_form.validate_on_submit():
        apply_rainbow(rainbow_form)
        send_config()
        flash("Rainbow applied")
        return redirect(url_for("index"))
    else:
        read_rainbow_to_form(rainbow_form, int(request.args.get("element")))

    return render_template("rainbow.html", rainbow_form=rainbow_form)


@app.route("/audio", methods=["GET", "POST"])
def audio():
    audio_form = AudioForm()
    if audio_form.validate_on_submit():
        apply_audio(audio_form)
        send_config()
        flash("Audio applied")
        return redirect(url_for("index"))
    else:
        read_audio_to_form(audio_form, int(request.args.get("element")))

    return render_template("audio.html", audio_form=audio_form)


@app.route("/spectrum-bars", methods=["GET", "POST"])
def spectrum_bars():
    spectrum_bars_form = SpectrumBarsForm()
    if spectrum_bars_form.validate_on_submit():
        apply_spectrum_bars(spectrum_bars_form)
        send_config()
        flash("Spectrum bars applied")
        return redirect(url_for("index"))
    else:
        read_spectrum_bars_to_form(spectrum_bars_form, int(request.args.get("element")))

    return render_template("spectrum-bars.html", spectrum_bars_form=spectrum_bars_form)


@app.route("/bins", methods=["GET", "POST"])
def bins():
    audio_bins_form = AudioBinsForm()
    if audio_bins_form.validate_on_submit():
        apply_audio_bins(audio_bins_form)
        send_config()
        flash("Audio Bins applied")
        return redirect(url_for("index"))
    else:
        read_audio_bins_to_form(audio_bins_form, int(request.args.get("element")))

    return render_template("bins.html", audio_bins_form=audio_bins_form)


@app.route("/spatial", methods=["GET", "POST"])
def spatial():
    spatial_form = SpatialForm()
    if spatial_form.validate_on_submit():
        apply_spatial(spatial_form)
        send_config()
        flash("Spatial applied")
        return redirect(url_for("index"))
    else:
        read_spatial_to_form(spatial_form, int(request.args.get("container")))

    return render_template("spatial.html", spatial_form=spatial_form)


@app.route("/effect-presets", methods=["GET", "POST"])
def effect_presets():
    save_effect_preset_form = SavePresetForm()

    if save_effect_preset_form.validate_on_submit():
        save_effect_preset(save_effect_preset_form)
        save_effect_preset_form.preset_name.data = None
        save_effect_preset_form.preset_description.data = None

        return redirect(url_for("effect_presets"))

    effect_presets_dict = load_presets()["effects"]
    all_effect_presets = [{"name": key, "description": effect_presets_dict[key], "apply-link": url_for("apply_effect_preset") + "?name=" + key, "delete-link": url_for("delete_effect_preset") + "?name=" + key} for key in effect_presets_dict]

    return render_template("effect-presets.html", effect_presets=all_effect_presets, save_effect_preset_form=save_effect_preset_form)


@app.route("/apply-effect-preset", methods=["GET"])
def apply_effect_preset():
    preset_name = request.args.get("name")
    load_effect_preset(preset_name)
    save_config()
    send_config()
    flash("Effect Preset applied")
    return redirect(url_for("index"))


@app.route("/delete-effect-preset", methods=["GET"])
def delete_effect_preset():
    preset_name = request.args.get("name")
    remove_effect_preset(preset_name)
    flash("Effect Preset deleted")
    return redirect(url_for("effect_presets"))



@app.route("/spatial-presets", methods=["GET", "POST"])
def spatial_presets():
    save_spatial_preset_form = SavePresetForm()

    if save_spatial_preset_form.validate_on_submit():
        save_spatial_preset(save_spatial_preset_form)
        save_spatial_preset_form.preset_name.data = None
        save_spatial_preset_form.preset_description.data = None

        return redirect(url_for("spatial_presets"))

    spatial_presets_dict = load_presets()["spatial"]
    all_spatial_presets = [{"name": key, "description": spatial_presets_dict[key], "apply-link": url_for("apply_spatial_preset") + "?name=" + key, "delete-link": url_for("delete_spatial_preset") + "?name=" + key} for key in spatial_presets_dict]

    return render_template("spatial-presets.html", spatial_presets=all_spatial_presets, save_spatial_preset_form=save_spatial_preset_form)


@app.route("/apply-spatial-preset", methods=["GET"])
def apply_spatial_preset():
    preset_name = request.args.get("name")
    load_spatial_preset(preset_name)
    save_config()
    send_config()
    flash("Spatial Preset applied")
    return redirect(url_for("index"))


@app.route("/delete-spatial-preset", methods=["GET"])
def delete_spatial_preset():
    preset_name = request.args.get("name")
    remove_spatial_preset(preset_name)
    flash("Spatial Preset deleted")
    return redirect(url_for("spatial_presets"))


@app.route("/sync-config")
def sync_config():
    send_entire_config()

    flash("Config Synced")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
