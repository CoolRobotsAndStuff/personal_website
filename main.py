from flask import Flask, render_template, render_template_string, request, redirect, url_for, abort
import werkzeug


app = Flask(__name__)

supported_languages = ["en", "es"]
default_lang = "en"

def get_lang():
    return werkzeug.datastructures.LanguageAccept([(al[0][0:2], al[1]) for al in request.accept_languages]).best_match(supported_languages)

def join_base_with_content(lang, content_html_name):
    content = render_template(f"{lang}/{content_html_name}", lang=lang)
    
    template = f'''{{% extends "{lang}/base.html" %}}\n 
                   {{% block content %}} {content} {{% endblock %}}
                   '''
    return render_template_string(template, lang=lang)

def go_to_default(page):
    lang = get_lang()
    return redirect(url_for(page, lang=lang))

@app.route("/")
def root():
    return go_to_default("home")

@app.route("/<lang_or_page>/")
def root_lang(lang_or_page):
    if lang_or_page in supported_languages:
        return redirect(url_for("home", lang=lang_or_page))
    else:
        try:
            return go_to_default(lang_or_page)
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
    
@app.route("/linguistics/<lang>/")
def linguistics(lang):
    if lang not in supported_languages:
        return go_to_default("linguistics")
    return join_base_with_content(lang, "linguistics.html")


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
    app.run(debug=True)