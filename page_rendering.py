"""
Functions to render a page taking into account language, theme and extra data in yaml format that might be necessary.
This code handles all cases where the target language is not available for the content.

"""

import os
from warnings import warn

import yaml

from flask import Flask, render_template, render_template_string, request, redirect
import werkzeug

from constants import *


def get_language():
    return werkzeug.datastructures.LanguageAccept(
        [(al[0][0:2], al[1]) for al in request.accept_languages]
    ).best_match(SUPPORTED_LANGUAGES)


def get_prefered_content_language():
    return request.args.get(
        "prefered_content_language", default=DEFAULT_LANGUAGE, type=str
    )


def get_theme():
    return request.args.get("theme", default=DEFAULT_THEME, type=str)


def load_yaml_data(language, file_name):
    path = (
        f"./data/{file_name}" if language is None else f"./data/{language}/{file_name}"
    )
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data


def join_base_with_content(ui_language, content, base_file="base.html"):
    template = f"""{{% extends "{ui_language}/{base_file}" %}}\n 
                   {{% block content %}} {content} {{% endblock %}}
                   """
    return render_template_string(template, lang=ui_language, theme=get_theme())


def get_available_languages_for_file(directory, file_name) -> list:
    available_languages = []
    for slang in SUPPORTED_LANGUAGES:
        if os.path.exists(f"{directory}/{slang}/{file_name}"):
            available_languages.append(slang)
    return available_languages


def get_yaml_data(yaml_data, content_language, find_other_language=False):
    available_languages_for_yaml = get_available_languages_for_file("data", yaml_data)
    yaml_data_exists_for_language = os.path.exists(
        f"data/{content_language}/{yaml_data}"
    )
    generic_yaml_data_exists = os.path.exists(f"data/{yaml_data}")

    if yaml_data_exists_for_language:
        return load_yaml_data(content_language, yaml_data), content_language

    elif generic_yaml_data_exists:
        return load_yaml_data(None, yaml_data), content_language

    else:
        if find_other_language and len(available_languages_for_yaml) > 0:
            prefered_language = get_prefered_content_language()
            if prefered_language in available_languages_for_yaml:
                return load_yaml_data(prefered_language, yaml_data), prefered_language
            else:
                return load_yaml_data(
                    available_languages_for_yaml[0], yaml_data
                ), available_languages_for_yaml[0]

        else:
            warn(
                f"Yaml data file '{yaml_data}' not found for language '{content_language}'."
            )
            return None, content_language


def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return "{}?{}".format(request.path, werkzeug.urls.urlencode(args))


def make_lang_list(abreviations: list, current_lang):
    final_string = ""
    for i, a in enumerate(abreviations):
        if len(abreviations) == 1:
            pass
        elif i == len(abreviations) - 1:
            final_string += LANGUAGE_TABLE[current_lang]["and"]
        elif i != 0:
            final_string += ", "
        final_string += f"<a href='{modify_query(prefered_content_language=a)}'> {LANGUAGE_TABLE[current_lang][a]}</a>"

    return final_string


def get_page_not_in_language_message(template_name, language, yaml_file_name=None):
    available_languages_for_template = get_available_languages_for_file(
        "templates", template_name
    )
    if not available_languages_for_template and yaml_file_name is not None:
        available_languages_for_template = get_available_languages_for_file(
            "data", yaml_file_name
        )

    return f"<p style='color: red'> {LANGUAGE_TABLE[language]['page_not_available']} {make_lang_list(available_languages_for_template, language)}. </p>"


def render_page(
    template_name, language, yaml_data_name=None, base_template="base.html"
):
    available_languages_for_template = get_available_languages_for_file(
        "templates", template_name
    )
    template_exists_in_language = language in available_languages_for_template
    generic_template_exists = os.path.exists(f"templates/{template_name}")

    data_language = language
    content_language = language

    if template_exists_in_language:
        template_to_render = f"{content_language}/{template_name}"
        if yaml_data_name is not None:
            data, data_language = get_yaml_data(yaml_data_name, content_language)

    elif generic_template_exists:
        template_to_render = f"{template_name}"
        if yaml_data_name is not None:
            # if the template we're rendering is generic, we can try to find different languages for the data
            data, data_language = get_yaml_data(
                yaml_data_name, content_language, find_other_language=True
            )

    elif len(available_languages_for_template) > 0:
        content_language = available_languages_for_template[0]
        template_to_render = f"{content_language}/{template_name}"
        if yaml_data_name is not None:
            data, data_language = get_yaml_data(yaml_data_name, content_language)

    else:
        raise FileNotFoundError(f"Template file '{template_name}' not found.")

    if yaml_data_name is None:
        content = render_template(template_to_render, lang=language, theme=get_theme())
    else:
        content = render_template(
            template_to_render, lang=language, theme=get_theme(), data=data
        )

    if content_language != language or data_language != language:
        content = (
            get_page_not_in_language_message(template_name, language, yaml_data_name)
            + content
        )

    return join_base_with_content(language, content, base_template)
