import os
from uuid import uuid4

from flask import current_app

from llrws.tools.mave.tidydata import sort_flat_mave_csv
from llrws.tools.mave.validation import (
    validate_benchmark_schema,
    validate_score_schema,
    validate_benchmark_or_score_schema,
)


def generate_mave_csv_filepaths():
    # Declare upload benchmark, score, and output maveLLR-processed CSV filepaths.
    session_id = uuid4()
    return {
        "benchmark": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-benchmark.csv"),
        "score": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv"),
        "output": os.path.join(current_app.config["DOWNLOAD_FOLDER"], f"{session_id}-maveLLR.csv"),
        # Unknown file
        "misc": os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-misc.csv"),
    }
