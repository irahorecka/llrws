import os
from uuid import uuid4

from flask import current_app
from flask_restful import Resource, reqparse
import werkzeug

from llrws.rscripts import execute_maveLLR_script
from llrws.web_utils import rm_files, save_fileobj_to_filepath, send_file_for_download


class LLR(Resource):
    # Build request parser and parse post request file contents.
    parse = reqparse.RequestParser()
    parse.add_argument("benchmark_file", type=werkzeug.datastructures.FileStorage, location="files")
    parse.add_argument("score_file", type=werkzeug.datastructures.FileStorage, location="files")

    def get(self):
        return {"hello": "world"}

    def post(self):
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "benchmark_file=@table-1.csv" -F "score_file=@table-2.csv" http://api.localhost:5000
        # Get unique ID for session.
        session_id = uuid4()
        # Get parse_args instantiated obj.
        args = self.parse.parse_args()
        # Declare benchmark CSV filepath.
        benchmark_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-benchmark.csv")
        # Declare score CSV filepath.
        score_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv")
        # Declare output filepath for maveLLR-processed CSV file.
        output_filepath = os.path.join(current_app.config["DOWNLOAD_FOLDER"], f"{session_id}-maveLLR.csv")

        # Try/finally block to remove all uploaded files regardless of success or error.
        try:
            # Validate and save benchmark CSV file.
            benchmark_file = args["benchmark_file"]
            is_file_saved, error_msg = save_fileobj_to_filepath(
                benchmark_file, benchmark_filepath, file_descriptor="MAVE benchmark CSV"
            )
            if is_file_saved is False:
                return error_msg, 400

            # Validate and save score CSV file.
            score_file = args["score_file"]
            is_file_saved, error_msg = save_fileobj_to_filepath(
                score_file, score_filepath, file_descriptor="MAVE score CSV"
            )
            if is_file_saved is False:
                return error_msg, 400

            # Execute R script ../rscripts/mave.r via Python wrapper scripts.execute_maveLLR_script.
            # stderr_out is either stderr or stdout and is conditional to failure or success, respectively.
            is_successful, stderr_out = execute_maveLLR_script(
                benchmark_filepath, score_filepath, download_filepath=output_filepath
            )
            if not is_successful:
                return stderr_out, 400

            return send_file_for_download(output_filepath, filename="maveLLR.csv")
        finally:
            rm_files(filepaths=[benchmark_filepath, score_filepath, output_filepath])
