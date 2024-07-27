from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_bootstrap import Bootstrap5

from forms import EffectForm, get_all_target_elements
from config_manager import *


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'you-will-never-guess'


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
            )
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
            )
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
            )
        }
        audio_groups_formatted.append(formatted_audio_group)

    return render_template("index.html", effect_groups_formatted=effect_groups_formatted, rainbow_groups_formatted=rainbow_groups_formatted, audio_groups_formatted=audio_groups_formatted)



@app.route("/effect", methods=["GET", "POST"])
def effect():
    effect_form = EffectForm()
    if effect_form.validate_on_submit():
        apply_effect(effect_form)
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
        flash("Audio applied")
        return redirect(url_for("index"))
    else:
        read_audio_to_form(audio_form, int(request.args.get("element")))

    return render_template("audio.html", audio_form=audio_form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)