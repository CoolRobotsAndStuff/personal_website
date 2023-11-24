import yaml

from flask import render_template

def get_cv():
    with open("./cv_data/cv_data.yaml", "r") as file:
        data = yaml.safe_load(file)

    return render_template("cv.html", data=data)


