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
from llrws.tools.mave import generate_mave_csv_filepaths, get_mave_csv_schematype_from_exception
from llrws.tools.mave.tidydata import get_mave_csv_sorted_by_hgvs_pro
from llrws.tools.mave.validation.score import validate_score_schema, export_score_file
from llrws.tools.mave.validation.benchmark import validate_benchmark_schema, export_benchmark_file
from llrws.tools.web import validate_file_properties

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
    """Validates uploaded score CSV file and saves CSV file if validation is successful."""
    try:
        upload_fileobj = request.files["file"]
    except KeyError:
        # Raised when user deletes file from dropzone.
        return "No file", 200

    score_filepath = generate_mave_csv_filepaths(session_id=request.cookies.get("uid"))["score"]
    try:
        validate_mave_csv_file_upload(upload_fileobj, score_filepath, validate_score_schema, "score")
    except InvalidUploadFile as e:
        return str(e), 400

    export_score_file(score_filepath)
    return "Upload successful", 200


@cross_origin(supports_credentials=True)
@main.route("/upload/benchmark", methods=["POST"])
def upload_benchmark():
    """Validates uploaded benchmark CSV file and saves CSV file if validation is successful."""
    try:
        upload_fileobj = request.files["file"]
    except KeyError:
        return "No file", 200

    benchmark_filepath = generate_mave_csv_filepaths(session_id=request.cookies.get("uid"))["benchmark"]
    try:
        validate_mave_csv_file_upload(upload_fileobj, benchmark_filepath, validate_benchmark_schema, "benchmark")
    except InvalidUploadFile as e:
        return str(e), 400

    export_benchmark_file(benchmark_filepath)
    return "Upload successful", 200


def validate_mave_csv_file_upload(upload_fileobj, upload_filepath, validation_schema, schema_type):
    """Validates uploaded file object as the appropriate MAVE CSV file.

    Args:
        upload_fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of an uploaded file
        upload_filepath (str): Filepath to save `upload_fileobj`
        validation_schema (function): Schema validation function to validate uploaded file
        schema_type (str): Descriptor for validation schema

    Raises:
        InvalidUploadFile: Uploaded file failed validation

    Returns:
        (None)
    """
    # Check if the general file properties are valid...
    try:
        validate_file_properties(upload_fileobj, file_descriptor="Uploaded file")
    except FileValidationError as e:
        raise InvalidUploadFile(e) from e

    # ... then check if the CSV schema is valid.
    upload_fileobj.save(upload_filepath)
    try:
        validation_schema(upload_filepath)
    except InvalidCsvSchema:
        raise InvalidUploadFile(f"Uploaded CSV file is not recognized as a {schema_type.title()} CSV file.")


@main.route("/get-llr")
def get_llr():
    """AJAX: Load LLR data from uploaded score and benchmark file."""
    # Get CSV filepaths using UID stored in cookie session
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
