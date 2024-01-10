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

@app.template_global()
def change_language(new_lang: str):
    url = request.full_path.split("/", 2)
    url[1] = new_lang
    return "/".join(url)

def go_to_default(page, theme=DEFAULT_THEME):
    lang = get_language()
    if page != "":
        return redirect(f"/{lang}/{page}/?theme={theme}")
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
    
    

@app.route("/<lang>/about/")
def about(lang):
    if lang not in SUPPORTED_LANGUAGES:
        go_to_default('about')
    return render_page("about.html", lang)


    
@app.route("/<lang>/translation/")
def linguistics(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default("translation")
    return render_page("translation.html", lang)


@app.route("/<lang>/tech/projects/<project_name>/")
def project(lang, project_name):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default(f"tech/projects/{project_name}")
    return render_page(f"projects/{project_name}.html", lang)

@app.route("/<lang>/tech/")
def tech(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default("tech")
    return render_page("tech.html", lang)


'''
@app.route("/<lang>/blog/")
def blog(lang):
    if lang not in SUPPORTED_LANGUAGES:
        return go_to_default("blog")
    return render_page("blog.html", lang)
'''

@app.route("/<lang>/cv/")
def cv(lang):
    if lang not in SUPPORTED_LANGUAGES:
            return go_to_default("cv")
    
    return render_page("cv.html", lang, "cv_data.yaml")

'''
@app.route("/<lang>/gallery/")
def gallery(lang):
    if lang not in SUPPORTED_LANGUAGES:
        go_to_default('gallery')
    return render_page("gallery.html", lang)

@app.route("/<lang>/test/")
def test(lang):
    if lang not in SUPPORTED_LANGUAGES:
            return go_to_default("test")
    return render_page(r"projects/mini_me.html", lang)
'''

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="192.168.100.145")