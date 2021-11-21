"""
/llrws/main/routes.py
~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes.
"""

import os
import csv

from flask import render_template, Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Landing page of LLRWS."""
    content = {
        "title": "Home | LLRWS",
    }
    return render_template("main/index.html", content=content)


@main.route("/data")
def data():
    """AJAX: Load CSV data when called."""
    var_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test.csv")
    with open(var_file) as f:
        var_csv = [i for i in csv.DictReader(f)]
    return {"data": var_csv}


@main.route("/settings")
def settings():
    """Settings page of LLRWS."""
    content = {
        "title": "Settings | LLRWS",
    }
    return render_template("main/settings.html", content=content)
