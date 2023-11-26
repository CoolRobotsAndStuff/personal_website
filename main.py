from flask import Flask, render_template, render_template_string, request, redirect, url_for, abort, send_from_directory
import werkzeug
import os

import yaml


app = Flask(__name__)


supported_languages = ["en", "es"]
default_lang = "en"

def lang_abreviation_to_name(abreviation, current_lang):
    assert abreviation in supported_languages
    match abreviation, current_lang:
        case "en", "en":
            return "English"
        case "en", "es":
            return "inglés"
        case "es", "es":
            return "español"
        case "es", "en":
            return "Spanish"
        case _:
            return abreviation

def make_lang_list(abreviations: list, current_lang):
    and_words = {
        "es" : " y ",
        "en" : " and "
    }

    final_string = ""
    for i, a in enumerate(abreviations):
        if len(abreviations) == 1:
            pass
        elif i == len(abreviations) - 1:
            final_string += and_words[current_lang]
        elif i != 0:
            final_string += ", "
        final_string += lang_abreviation_to_name(a, current_lang)

    return final_string

def get_page_not_in_language_content(lang, content_dir, content_name):
    available_languages = []
    for slang in supported_languages:
        if os.path.exists(f"{content_dir}/{slang}/{content_name}"):
            available_languages.append(slang)
    
    return render_template(f"{lang}/page_not_in_language.html", lang=lang, theme=get_theme(), available_languages=make_lang_list(available_languages, lang))
    

supported_themes = ("light", "dark")
default_theme = "dark"

def get_lang():
    return werkzeug.datastructures.LanguageAccept([(al[0][0:2], al[1]) for al in request.accept_languages]).best_match(supported_languages)

def get_theme():
    theme = request.args.get("theme", default=default_theme, type=str)
    print("theme:", theme)
    return theme

def join_base_with_content(lang, content_html_name):
    if os.path.exists(f"templates/{lang}/{content_html_name}"):
        content = render_template(f"{lang}/{content_html_name}", lang=lang, theme=get_theme())
    else:
        content = get_page_not_in_language_content(lang, "templates", content_html_name)
    
    template = f'''{{% extends "{lang}/base.html" %}}\n 
                   {{% block content %}} {content} {{% endblock %}}
                   '''
    return render_template_string(template, lang=lang, theme=get_theme())

def go_to_default(page, theme=default_theme):
    lang = get_lang()
    return redirect(f"/{page}/{lang}/?theme={theme}")


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

@app.route("/cv/<lang>/")
def cv(lang):
    if lang not in supported_languages:
            return go_to_default("cv")
    
    elif lang != 'es':
        content = get_page_not_in_language_content(lang, "data", "cv_data.yaml")
    else:
        
        with open(f"./data/{lang}/cv_data.yaml", "r") as file:
            data = yaml.safe_load(file)

        content = render_template("cv.html", data=data, theme=get_theme())
        
    #print(data)
    template = f'''{{% extends "{lang}/base.html" %}}\n 
                {{% block content %}} {content} {{% endblock %}}
                   '''
    return render_template_string(template, lang=lang, theme=get_theme())

@app.route("/test/<lang>/")
def test(lang):
    #return  get_cv()
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')