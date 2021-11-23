"""
/llrws/main/routes.py
~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes.
"""

import os
import csv
from io import StringIO

import requests
from flask import render_template, request, url_for, Blueprint

from llrws.utils.web import validate_file_properties

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Landing page of LLRWS."""
    content = {
        "title": "Home | LLRWS",
    }
    return render_template("main/index.html", content=content)


@main.route("/upload", methods=["POST"])
def upload():
    """Demo upload validation for CSV files."""
    try:
        uploaded_file = request.files["file"]
    except KeyError:
        # Usually raised when user deletes file from dropzone.
        return "No file", 200
    is_file_valid, error_msg = validate_file_properties(uploaded_file, file_descriptor="Uploaded")
    if not is_file_valid:
        return error_msg, 400
    return "Success", 200


@main.route("/data")
def data():
    """AJAX: Load CSV data when called."""
    file_dir = os.path.dirname(os.path.abspath(__file__))

    # In the future these will be user input files
    benchmark_file = os.path.join(file_dir, "CALM123_jointReference.csv")
    score_file = os.path.join(file_dir, "CALM1_full_imputation_refined_mavedb.csv")
    files = {
        "benchmark_file": open(benchmark_file, "rb"),
        "score_file": open(score_file, "rb"),
    }
    response = requests.post(url_for("api.api_base", _external=True), files=files)
    var_csv = [i for i in csv.DictReader(StringIO(response.content.decode("utf-8")))]

    # Just load written input file to avoid post calls every time a page refresh is invoked.
    # var_csv = [i for i in csv.DictReader(open(os.path.join(file_dir, "test.csv")))]

    return {"data": var_csv}
