import os
from uuid import uuid4

from flask import current_app


def generate_mave_csv_filepaths(session_id=None):
    """Generates MAVE CSV filepaths for MAVE schema types as follows:
    - Benchmark (key: 'benchmark') - Benchmark file to pipe into MAVE LLR R-Script
    - Score (key: 'score') - Score file to pipe into MAVE LLR R-Script
    - Output (key: 'output') - Output file for download from MAVE LLR R-Script
    - Upload (key: 'upload') - Upload file as provided by user

    Kwargs:
        session_id (str): Unique identifier to prepend to MAVE CSV filepaths

    Returns:
        (dict): Generated MAVE filepaths
    """
    # Declare upload benchmark, score, and output maveLLR-processed CSV filepaths.
    if session_id is None:
        session_id = uuid4()
    return {
        "benchmark": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-benchmark.csv"),
        "score": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv"),
        "output": os.path.join(current_app.config["DOWNLOAD_FOLDER"], f"{session_id}-maveLLR.csv"),
        # Unknown file
        "upload": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-upload.csv"),
    }


def get_mave_csv_schematype_from_exception(exception):
    """Get MAVE CSV schema type from exception string.
    E.g. get 'score' from:
    Error [400]: [...] No such file [...]: '/Users/[...]/9ff4b4d6-daea-4178-b170-7b24c77ce0c0-score.csv'

    Args:
        exception (str): Exception messaged raised due to a MAVE CSV file validation exception.
                         MAVE CSV filepath must be in the exception traceback.

    Returns:
        (str): The schematype of the MAVE CSV file or "" if schematype isn't found
    """
    try:
        return exception.lower().split(".csv")[-2].split("-")[-1]
    except IndexError:
        return ""


def rename_mave_csv_file_by_schematype(csv_filepath, csv_schematype, session_id=None):
    """Rename `csv_filepath` as '{`session_id`}-{`csv_schematype`}.csv'.

    Args:
        csv_filepath (str): CSV filepath to rename
        csv_schematype (str): MAVE CSV schema type

    Kwargs:
        session_id (str): Unique identifier for the CSV file. If not provided, a new
                          unique identifier will be generated.

    Returns:
        (None)
    """
    csv_schematype_filepath = generate_mave_csv_filepaths(session_id=session_id)[csv_schematype]
    os.rename(csv_filepath, csv_schematype_filepath)
