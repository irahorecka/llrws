import os
from uuid import uuid4

from flask import current_app

from llrws.tools.mave.tidydata import sort_mave_csv_by_hgvs_pro_from_reponse_content
from llrws.tools.mave.validation import (
    validate_benchmark_schema_from_mave_csv_file,
    validate_score_schema_from_mave_csv_file,
    validate_benchmark_or_score_schema_from_mave_csv_file,
)


def generate_mave_csv_filepaths(session_id=None):
    """Generates MAVE CSV filepaths for MAVE filetypes as follows:
    - Benchmark (key: 'benchmark')
    - Score (key: 'score')
    - Output (key: 'output')
    - Misc. (key: 'misc')

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
        "misc": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-misc.csv"),
    }


def get_mave_csv_filetype_from_exception(exception):
    """Get MAVE CSV filetype from exception string.
    E.g. get 'score' from:
    Error [400]: [...] No such file [...]: '/Users/[...]/9ff4b4d6-daea-4178-b170-7b24c77ce0c0-score.csv'

    Args:
        exception (str): Exception messaged raised due to a MAVE CSV file validation exception.
                         MAVE CSV filepath must be in the exception traceback.

    Returns:
        (str): The filetype of the MAVE CSV file or "" if filetype isn't found
    """
    try:
        return exception.lower().split(".csv")[-2].split("-")[-1]
    except IndexError:
        return ""


def rename_mave_csv_file_by_filetype(csv_filepath, csv_filetype, session_id=None):
    """Rename `csv_filepath` as '{`session_id`}-{`csv_filetype`}.csv'.

    Args:
        csv_filepath (str): CSV filepath to rename
        csv_filetype (str): MAVE CSV filetype

    Kwargs:
        session_id (str): Unique identifier for the CSV file. If not provided, a new
                          unique identifier will be generated.

    Returns:
        (None)
    """
    csv_filetype_filepath = generate_mave_csv_filepaths(session_id=session_id)[csv_filetype]
    os.rename(csv_filepath, csv_filetype_filepath)
