import os
from uuid import uuid4

from flask import current_app
from flask_restful import Resource, reqparse
import werkzeug

from llrws.utils.rscripts import execute_maveLLR_script
from llrws.utils.web import (
    rm_files,
    send_file_for_download,
    validate_file_properties,
    validate_benchmark_or_score_csv_file,
)


class LLR(Resource):
    # Build request parser and parse post request file contents.
    # Declare reqparse.ReqestParser here to avoid instantiation overhead when POST request is made.
    parse = reqparse.RequestParser()
    parse.add_argument("benchmark_file", type=werkzeug.datastructures.FileStorage, location="files")
    parse.add_argument("score_file", type=werkzeug.datastructures.FileStorage, location="files")

    def get(self):
        return {"rothlab": "LLR Web Service"}

    def post(self):
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "benchmark_file=@table-1.csv" -F "score_file=@table-2.csv" http://localhost:5000/api/
        args = self.parse.parse_args()
        # Declare upload benchmark, score, and output maveLLR-processed CSV filepaths.
        session_id = uuid4()
        benchmark_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-benchmark.csv")
        score_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv")
        output_filepath = os.path.join(current_app.config["DOWNLOAD_FOLDER"], f"{session_id}-maveLLR.csv")

        try:
            # Collect registered filetypes after validations.
            # There should be TWO unique filetypes after file processing, i.e., {'benchmark', 'score'}
            filetypes = set()
            # Validate and save benchmark CSV file.
            benchmark_file = args["benchmark_file"]
            is_file_valid, filetype, error_msg = self._validate_and_save_benchmark_score_csv_file(
                benchmark_file, benchmark_filepath, file_descriptor="MAVE benchmark CSV"
            )
            if not is_file_valid:
                return error_msg, 400
            # Register filetype
            filetypes.add(filetype)

            # Validate and save score CSV file.
            score_file = args["score_file"]
            is_file_valid, filetype, error_msg = self._validate_and_save_benchmark_score_csv_file(
                score_file, score_filepath, file_descriptor="MAVE score CSV"
            )
            if not is_file_valid:
                return error_msg, 400
            filetypes.add(filetype)

            # Check for two unique filetypes
            if len(filetypes) != 2:
                return f"There appears to be duplicate {filetypes.pop()} CSV files.", 400

            # Execute R script ../rscripts/mave.r via Python wrapper scripts.execute_maveLLR_script.
            # error_msg is either stderr or stdout and is conditional to failure or success, respectively.
            # However, error_msg will only be returned if failure, hence it will only be used in stderr instances.
            is_script_successful, error_msg = execute_maveLLR_script(
                benchmark_filepath, score_filepath, download_filepath=output_filepath
            )
            if not is_script_successful:
                return error_msg, 400

            return send_file_for_download(output_filepath, filename="maveLLR.csv")

        finally:
            # Remove all upload and download files regardless of success / failure.
            rm_files(filepaths=[benchmark_filepath, score_filepath, output_filepath])

    @staticmethod
    def _validate_and_save_benchmark_score_csv_file(file, filepath, file_descriptor):
        # Validate input file properties and save file if valid.
        is_file_valid, error_msg = validate_file_properties(file, file_descriptor=file_descriptor)
        if not is_file_valid:
            return False, "", error_msg
        file.save(filepath)

        # At this point, we're working with a CSV file.
        # Validate CSV content and identify which file we're dealing with (i.e. score or benchmark).
        is_csv_valid, filetype, error_msg = validate_benchmark_or_score_csv_file(
            filepath, file_descriptor=file_descriptor
        )
        return is_csv_valid, filetype, error_msg
