import os
import warnings

warnings.simplefilter(action="ignore", category=UserWarning)

from flask import current_app
from werkzeug.utils import secure_filename
import pandas as pd
import pandera as pa


def validate_file_properties(fileobj, file_descriptor):
    """Validates fileobj. Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    # Validate fileobj instance
    if fileobj is None:
        error_msg = f"Missing {file_descriptor}."
        return False, error_msg
    # Convert fileobj.filename to secure filename before evaluating filename.
    filename = secure_filename(fileobj.filename)
    if not bool(filename):
        error_msg = f"Missing {file_descriptor}."
        return False, error_msg
    # Validate file extension
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{file_descriptor} does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        return False, error_msg

    return True, ""


def validate_benchmark_or_score_csv_file(csv_filepath, file_descriptor):
    """Validates CSV for data content pertaining to MAVE benchmark or score files.
    Descriptive error is returned if validation fails.

    Args:
        csv_filepath (str): File path to CSV file
        file_descriptor (str): Description of file to concatenate to error message if error thrown

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): CSV filetype (i.e. "score" or "benchmark") or "" if filetype detected or not, respectively
        (str): "" or error message if validation success or failure, respectively
    """
    mave_df = pd.read_csv(csv_filepath)
    try:
        validate_benchmark_schema(mave_df)
        return True, "benchmark", ""

    except pa.errors.SchemaError:
        try:
            validate_score_schema(mave_df)
            return True, "score", ""

        except pa.errors.SchemaError as e:
            return False, "", f"{file_descriptor} encountered the following problem: {e}"


def validate_benchmark_schema(mave_df):
    """Validates benchmark Pandas DataFrame for data content pertaining to MAVE benchmark files.

    Args:
        mave_df (pandas.core.frame.DataFrame): A MAVE DataFrame object

    Returns:
        (None)
    """
    benchmark_schema = pa.DataFrameSchema(
        {
            # E.g. CALM1:c.293A>G, c.211T>Y
            "hgvsc": pa.Column(str, pa.Check.str_contains(r"c\.(.*)$")),
            # E.g. p.Asn98Ser
            "hgvsp": pa.Column(str, pa.Check.str_contains(r"p\.(.*)$")),
            "maf": pa.Column(float, nullable=True),
            "hom": pa.Column(float, nullable=True),
            "referenceSet": pa.Column(str),
            "source": pa.Column(str),
        },
        strict=True,
        coerce=True,
    )
    # Attempt benchmark schema validation - raise pa.errors.SchemaError if validation fails.
    benchmark_schema(mave_df)


def validate_score_schema(mave_df):
    """Validates score Pandas DataFrame for data content pertaining to MAVE score files.

    Args:
        mave_df (pandas.core.frame.DataFrame): A MAVE DataFrame object

    Returns:
        (None)
    """
    score_schema = pa.DataFrameSchema(
        {
            # E.g. p.Asn98Ser
            "hgvs_pro": pa.Column(str, pa.Check.str_contains(r"p\.(.*)$")),
            "score": pa.Column(float, nullable=True),
            "sd": pa.Column(float, nullable=True),
            "se": pa.Column(float, nullable=True),
        },
        strict=True,
        coerce=True,
    )
    # Attempt score schema validation - raise pa.errors.SchemaError if validation fails.
    score_schema(mave_df)
