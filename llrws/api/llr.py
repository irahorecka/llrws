import os
from uuid import uuid4

from flask import current_app
from flask_restful import Resource, reqparse
import werkzeug

from llrws.web_utils import rm_files, save_CSV_fileobj_to_filepath, send_file_for_download
from llrws.rscripts import execute_maveLLR_script


class LLR(Resource):
    # Build request parser and parse post request file contents.
    parse = reqparse.RequestParser()
    parse.add_argument("ref_file", type=werkzeug.datastructures.FileStorage, location="files")
    parse.add_argument("score_file", type=werkzeug.datastructures.FileStorage, location="files")

    def get(self):
        return {"hello": "world"}

    def post(self):
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "ref_file=@table-1.csv" -F "score_file=@table-2.csv" http://api.localhost:5000
        # Get unique ID for session.
        session_id = uuid4()
        # Get parse_args instantiated obj.
        args = self.parse.parse_args()
        # Declare reference CSV filepath.
        ref_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-reference.csv")
        # Declare score CSV filepath.
        score_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv")
        # Declare output filepath for maveLLR-processed CSV file.
        output_filepath = os.path.join(current_app.config["DOWNLOAD_FOLDER"], f"{session_id}-maveLLR.csv")

        # Try/finally block to remove all uploaded files regardless of success or error.
        try:
            # Validate and save reference CSV file.
            ref_file = args["ref_file"]
            bool_file_saved, error_msg = save_CSV_fileobj_to_filepath(ref_file, ref_filepath)
            if bool_file_saved is False:
                return error_msg, 400

            # Validate and save score CSV file.
            score_file = args["score_file"]
            bool_file_saved, error_msg = save_CSV_fileobj_to_filepath(score_file, score_filepath)
            if bool_file_saved is False:
                return error_msg, 400

            # Execute R script ../rscripts/mave.r via Python wrapper scripts.execute_maveLLR_script
            # stderr_out indicates either a stderr or stdout.
            bool_success, stderr_out = execute_maveLLR_script(ref_filepath, score_filepath, output_filepath)
            if not bool_success:
                return stderr_out, 400
            return send_file_for_download(output_filepath, "maveLLR.csv")

        finally:
            # rm_files([ref_filepath, score_filepath, output_filepath])
            pass
