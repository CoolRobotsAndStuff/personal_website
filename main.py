import random

from flask import Flask, render_template, render_template_string, request, redirect, url_for, abort, send_from_directory
import werkzeug

from constants import *
from page_rendering import render_page, get_language, get_theme

import pyfiglet

app = Flask(__name__)

@app.template_global()
def get_big_text(text: str, font = 'standard', width=50):
    return str(pyfiglet.figlet_format(text, font, width=width))

@app.template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, werkzeug.urls.urlencode(args))


def go_to_default(page, theme=DEFAULT_THEME):
    lang = get_language()
    if page != "":
        return redirect(f"/{page}/{lang}/?theme={theme}")
    else:
        return redirect(f"/{lang}/?theme={theme}")


@app.route("/")
def empty_root():
    return go_to_default("")

@app.route("/<lang_or_page>/")
def root(lang_or_page):
    if lang_or_page in SUPPORTED_LANGUAGES:
        return render_page("index.html", lang_or_page)
    else:
        try:
            return go_to_default(lang_or_page, theme=get_theme())
        except werkzeug.routing.exceptions.BuildError:
            return go_to_default("")
    
    

@app.route("/about/<lang>/")
def about(lang):
    if lang not in SUPPORTED_LANGUAGES:
        go_to_default('about')
    return render_page("about.html", lang)


    
@app.route("/translation/<lang>/")
def linguistics(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default("translation")
    return render_page("translation.html", lang)


@app.route("/tech/<lang>/")
def tech(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default("tech")
    return render_page("tech.html", lang)

@app.route("/blog/<lang>/")
def blog(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default("blog")
    return render_page("blog.html", lang)

@app.route("/cv/<lang>/")
def cv(lang):
    if lang not in SUPPORTED_LANGUAGES:
            return go_to_default("cv")
    
    return render_page("cv.html", lang, "cv_data.yaml")

@app.route("/gallery/<lang>/")
def gallery(lang):
    if lang not in SUPPORTED_LANGUAGES:
        go_to_default('gallery')
    return render_page("gallery.html", lang)

@app.route("/test/<lang>/")
def test(lang):
    #return  get_cv()
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')