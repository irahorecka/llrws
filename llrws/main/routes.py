"""
/llrws/main/routes.py
~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes.
"""

from uuid import uuid4

import requests
from flask import render_template, request, session, url_for, Blueprint
from flask_cors import cross_origin

from llrws.exceptions import FileValidationError, InvalidCsvSchema, InvalidCsvSchemaType, InvalidUploadFile
from llrws.tools.mave import (
    generate_mave_csv_filepaths,
    get_mave_csv_schematype_from_exception,
    rename_mave_csv_file_by_schematype,
)
from llrws.tools.mave.tidydata import get_mave_csv_sorted_by_hgvs_pro
from llrws.tools.mave.validation import get_schema_type, validate_schema
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
        try:
            validate_file_properties(upload_file, file_descriptor="Uploaded file")
        except FileValidationError as e:
            raise InvalidUploadFile(e) from e

        # ... then check if the CSV content is valid.
        upload_file.save(upload_csv_filepath)
        try:
            schema_type = get_schema_type(upload_csv_filepath)
        except InvalidCsvSchemaType:
            raise InvalidUploadFile("Uploaded CSV file is not recognized.")

        validate_schema(upload_csv_filepath, schema_type)
        # Validation was successful - rename uploaded file to sync with detected schema type.
        rename_mave_csv_file_by_schematype(upload_csv_filepath, schema_type, session_id=session["uid"])
        return "Upload successful", 200

    except (InvalidCsvSchema, InvalidUploadFile) as e:
        return str(e), 400

    finally:
        rm_files((upload_csv_filepath,))


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
        error_msg = f"{get_mave_csv_schematype_from_exception(str(e)).title()} filetype not found"
        return error_msg, 400
    try:
        # Get output LLR CSV stream via internal API POST request.
        response = requests.post(url_for("api.api_base", _external=True), files=csv_files)
        response_content = response.content.decode("utf-8")
        if response.status_code != 200:
            return response_content, 400
        sorted_mave_csv_content = get_mave_csv_sorted_by_hgvs_pro(response_content)
        return {"data": sorted_mave_csv_content}, 200
    finally:
        # Generate a new session UID after button click.
        session["uid"] = uuid4()
