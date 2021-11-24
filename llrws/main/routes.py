"""
/llrws/main/routes.py
~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes.
"""

import os
import csv
from io import StringIO
from uuid import uuid4

import requests
from flask import current_app, render_template, request, session, url_for, Blueprint
from flask_cors import cross_origin

from llrws.exceptions import InvalidUploadFile
from llrws.tools.mave import generate_mave_csv_filepaths, sort_flat_mave_csv, validate_benchmark_or_score_schema
from llrws.tools.web import rm_files, validate_file_properties

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Landing page of LLRWS."""
    # Generate a unique session ID whenever user hits landing page
    session["uid"] = uuid4()

    content = {
        "title": "Home | LLRWS",
    }
    return render_template("main/index.html", content=content)


@cross_origin(supports_credentials=True)
@main.route("/upload", methods=["POST"])
def upload():
    """Demo upload validation for CSV files."""
    try:
        upload_file = request.files["file"]
    except KeyError:
        # Raised when user deletes file from dropzone.
        return "No file", 200
    upload_filepath = generate_mave_csv_filepaths()["misc"]

    try:
        # Check if the general file properties are valid...
        is_valid_file, error_msg = validate_file_properties(upload_file, file_descriptor="Uploaded file")
        if not is_valid_file:
            raise InvalidUploadFile(error_msg)

        # ... then check if the CSV content is valid.
        upload_file.save(upload_filepath)
        is_valid_csv, csv_filetype, error_msg = validate_benchmark_or_score_schema(
            upload_filepath, file_descriptor="Uploaded file"
        )
        if not is_valid_csv:
            raise InvalidUploadFile(error_msg)

        # Rename both file types with the same session UID. This will be used in /data
        if csv_filetype == "score":
            score_filepath = generate_mave_csv_filepaths(session_id=session["uid"])["score"]
            os.rename(upload_filepath, score_filepath)
        if csv_filetype == "benchmark":
            benchmark_filepath = generate_mave_csv_filepaths(session_id=session["uid"])["benchmark"]
            os.rename(upload_filepath, benchmark_filepath)

        return csv_filetype, 200
    except InvalidUploadFile as e:
        return str(e), 400
    finally:
        rm_files(upload_filepath)


@main.route("/data")
def data():
    """AJAX: Load CSV data when called."""
    # Get CSV filepaths using UID stored in session
    csv_filepaths = generate_mave_csv_filepaths(session_id=session["uid"])
    benchmark_file = os.path.join(current_app.config["UPLOAD_FOLDER"], csv_filepaths["benchmark"])
    score_file = os.path.join(current_app.config["UPLOAD_FOLDER"], csv_filepaths["score"])

    files = {
        "benchmark_file": open(benchmark_file, "rb"),
        "score_file": open(score_file, "rb"),
    }
    try:
        response = requests.post(url_for("api.api_base", _external=True), files=files)
        flat_mave_csv = sort_flat_mave_csv(iter(csv.DictReader(StringIO(response.content.decode("utf-8")))))
        return {"data": flat_mave_csv}
    finally:
        # Generate a new session UID after button click.
        session["uid"] = uuid4()
