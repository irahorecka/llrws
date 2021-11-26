"""
/llrws/main/routes.py
~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes.
"""

import os
from uuid import uuid4

import requests
from flask import render_template, request, session, url_for, Blueprint
from flask_cors import cross_origin

from llrws.exceptions import InvalidUploadFile
from llrws.tools.mave import (
    generate_mave_csv_filepaths,
    get_mave_csv_filetype_from_exception,
    rename_mave_csv_file_by_filetype,
    sort_mave_csv_by_hgvs_pro_from_reponse_content,
    validate_benchmark_or_score_schema_from_mave_csv_file,
)
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

    upload_csv_filepath = generate_mave_csv_filepaths()["misc"]
    try:
        # Check if the general file properties are valid...
        is_valid_file, error_msg = validate_file_properties(upload_file, file_descriptor="Uploaded file")
        if not is_valid_file:
            raise InvalidUploadFile(error_msg)
        # ... then check if the CSV content is valid.
        upload_file.save(upload_csv_filepath)
        is_valid_csv, error_msg, csv_filetype = validate_benchmark_or_score_schema_from_mave_csv_file(
            upload_csv_filepath, file_descriptor="Uploaded CSV file"
        )
        if not is_valid_csv:
            raise InvalidUploadFile(error_msg)
        rename_mave_csv_file_by_filetype(upload_csv_filepath, csv_filetype, session_id=session["uid"])
        return "Upload successful", 200

    except InvalidUploadFile as e:
        return str(e), 400

    finally:
        rm_files(upload_csv_filepath)


@main.route("/data")
def data():
    """AJAX: Load CSV data when called."""
    # Get CSV filepaths using UID stored in session
    mave_csv_filepaths = generate_mave_csv_filepaths(session_id=session["uid"])
    mave_benchmark_file = mave_csv_filepaths["benchmark"]
    mave_score_file = mave_csv_filepaths["score"]
    try:
        csv_files = {
            "benchmark_file": open(mave_benchmark_file, "rb"),
            "score_file": open(mave_score_file, "rb"),
        }
    except FileNotFoundError as e:
        error_msg = f"{get_mave_csv_filetype_from_exception(str(e)).title()} filetype not found"
        return error_msg, 400
    try:
        response = requests.post(url_for("api.api_base", _external=True), files=csv_files)
        response_content = response.content.decode("utf-8")
        if response.status_code != 200:
            return response_content, 400
        sorted_mave_csv = sort_mave_csv_by_hgvs_pro_from_reponse_content(response_content)
        return {"data": sorted_mave_csv}, 200
    finally:
        # Generate a new session UID after button click.
        session["uid"] = uuid4()
