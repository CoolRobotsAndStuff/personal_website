import yaml
import pdfkit
from flask import render_template, render_template_string, Flask


def get_cv_string(lang):
    with open(f"./data/{lang}/cv_data.yaml", "r") as file:
        data = yaml.safe_load(file)

    with open(f"./templates/cv.html", "r") as file:
        temp = file.read()

    return render_template_string(temp, data=data, theme="light")

def cv_to_pdf(lang):
    options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    }
    content = get_cv_string(lang)
    pdfkit.from_string(content, "cv.pdf", options=options)


if __name__ == "__main__":
    app = Flask(__name__)
    with app.app_context():
        cv_to_pdf("es")

