"""
/llrws/main/routes.py
~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes.
"""

from uuid import uuid4

import requests
from flask import render_template, make_response, request, url_for, Blueprint
from flask_cors import cross_origin

from llrws.exceptions import FileValidationError, InvalidCsvSchema, InvalidUploadFile
from llrws.tools.mave import (
    generate_mave_csv_filepaths,
    get_mave_csv_schematype_from_exception,
    rename_mave_csv_file_by_schematype,
)
from llrws.tools.mave.tidydata import get_mave_csv_sorted_by_hgvs_pro
from llrws.tools.mave.validation import validate_benchmark_schema, validate_score_schema
from llrws.tools.web import rm_files, validate_file_properties

main = Blueprint("main", __name__)


@main.route("/")
def index():
    """Landing page of LLRWS."""
    content = {
        "title": "Home | LLRWS",
    }
    response = make_response(render_template("main/index.html", content=content))
    # Generate a unique cookie ID whenever user hits landing page
    response.set_cookie("uid", str(uuid4()))
    return response


@cross_origin(supports_credentials=True)
@main.route("/upload/score", methods=["POST"])
def upload_score():
    """Demo upload validation for CSV files."""
    try:
        upload_file = request.files["file"]
    except KeyError:
        # Raised when user deletes file from dropzone.
        return "No file", 200

    return validate_and_save_mave_csv_file_upload(upload_file, validate_score_schema, "score")


@cross_origin(supports_credentials=True)
@main.route("/upload/benchmark", methods=["POST"])
def upload_benchmark():
    """Demo upload validation for CSV files."""
    try:
        upload_file = request.files["file"]
    except KeyError:
        # Raised when user deletes file from dropzone.
        return "No file", 200

    return validate_and_save_mave_csv_file_upload(upload_file, validate_benchmark_schema, "benchmark")


def validate_and_save_mave_csv_file_upload(upload_file, validation_schema, schema_type):
    upload_csv_filepath = generate_mave_csv_filepaths()["upload"]
    try:
        # Check if the general file properties are valid...
        try:
            validate_file_properties(upload_file, file_descriptor="Uploaded file")
        except FileValidationError as e:
            raise InvalidUploadFile(e) from e

        # ... then check if the CSV content is valid.
        upload_file.save(upload_csv_filepath)
        try:
            validation_schema(upload_csv_filepath)
        except InvalidCsvSchema:
            raise InvalidUploadFile(f"Uploaded CSV file is not recognized as a {schema_type.title()} CSV file.")

        rename_mave_csv_file_by_schematype(upload_csv_filepath, schema_type, session_id=request.cookies.get("uid"))
        return "Upload successful", 200

    except InvalidUploadFile as e:
        return str(e), 400

    finally:
        rm_files((upload_csv_filepath,))


@main.route("/data")
def data():
    """AJAX: Load CSV data when called."""
    # Get CSV filepaths using UID stored in session
    mave_csv_filepaths = generate_mave_csv_filepaths(session_id=request.cookies.get("uid"))
    mave_benchmark_file = mave_csv_filepaths["benchmark"]
    mave_score_file = mave_csv_filepaths["score"]
    try:
        csv_files = {
            "benchmark_file": open(mave_benchmark_file, "rb"),
            "score_file": open(mave_score_file, "rb"),
        }
    except FileNotFoundError as e:
        error_msg = f"{get_mave_csv_schematype_from_exception(str(e)).title()} filetype not found"
        return error_msg, 400

    # Get output LLR CSV stream via internal API POST request.
    response = requests.post(url_for("api.api_base", _external=True), files=csv_files)
    response_content = response.content.decode("utf-8")
    if response.status_code != 200:
        return response_content, 400

    sorted_mave_csv_content = get_mave_csv_sorted_by_hgvs_pro(response_content)
    return {"data": sorted_mave_csv_content}, 200
