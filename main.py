from flask import Flask, render_template, render_template_string, request, redirect, url_for, abort, send_from_directory
import werkzeug
import os



app = Flask(__name__)


supported_languages = ["en", "es"]
default_lang = "en"

supported_themes = ("light", "dark")
default_theme = "dark"

def get_lang():
    return werkzeug.datastructures.LanguageAccept([(al[0][0:2], al[1]) for al in request.accept_languages]).best_match(supported_languages)

def get_theme():
    theme = request.args.get("theme", default=default_theme, type=str)
    print("theme:", theme)
    return theme

def join_base_with_content(lang, content_html_name):
    content = render_template(f"{lang}/{content_html_name}", lang=lang, theme=get_theme())
    
    template = f'''{{% extends "{lang}/base.html" %}}\n 
                   {{% block content %}} {content} {{% endblock %}}
                   '''
    return render_template_string(template, lang=lang, theme=get_theme())

def go_to_default(page, theme=default_theme):
    lang = get_lang()
    return redirect(url_for(page, lang=lang, theme=theme))


@app.route("/")
def root():
    return go_to_default("home")

@app.route("/<lang_or_page>/")
def root_lang(lang_or_page):
    

    if lang_or_page in supported_languages:
        return redirect(url_for("home", lang=lang_or_page, theme=get_theme()))
    else:
        try:
            return go_to_default(lang_or_page, theme=get_theme())
        except werkzeug.routing.exceptions.BuildError:
            abort(404)

@app.route("/about/<lang>/")
def about(lang):
    if lang not in supported_languages:
        lang = default_lang
    return join_base_with_content(lang, "about.html")

@app.route("/home/<lang>/")
def home(lang):
    if lang not in supported_languages:
        return go_to_default("home")
    return join_base_with_content(lang, "index.html")
    
@app.route("/translation/<lang>/")
def linguistics(lang):
    if lang not in supported_languages:
        return go_to_default("translation")
    return join_base_with_content(lang, "translation.html")


@app.route("/tech/<lang>/")
def tech(lang):
    if lang not in supported_languages:
        return go_to_default("tech")
    return join_base_with_content(lang, "tech.html")

@app.route("/blog/<lang>/")
def blog(lang):
    if lang not in supported_languages:
        return go_to_default("blog")
    return join_base_with_content(lang, "blog.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')