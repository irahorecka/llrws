import os
from uuid import uuid4

from flask import current_app
from flask_restful import Resource, reqparse
import werkzeug

from llrws.utils import rm_files, send_file_for_download
from llrws.rscripts import execute_maveLLR_script


class LLR(Resource):
    def get(self):
        return {"hello": "world"}

    def post(self):
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "file=@table-1.csv" http://api.localhost:5000
        # Get unique ID for session.
        session_id = uuid4()

        # Build request parser and parse post request file contents
        parse = reqparse.RequestParser()
        parse.add_argument("ref_file", type=werkzeug.datastructures.FileStorage, location="files")
        parse.add_argument("score_file", type=werkzeug.datastructures.FileStorage, location="files")
        args = parse.parse_args()

        # Save reference CSV file
        ref_file = args["ref_file"]
        ref_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-reference.csv")
        ref_file.save(ref_filepath)

        # Save score CSV file
        score_file = args["score_file"]
        score_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv")
        score_file.save(score_filepath)

        # Declare empty output_filepath, as output_filepath is otherwise declared in a try-block.
        output_filepath = ""
        try:
            # Execute R script ../rscripts/mave.r via Python wrapper scripts.execute_maveLLR_script
            output_filepath = execute_maveLLR_script(
                ref_filepath, score_filepath, current_app.config["UPLOAD_FOLDER"], unique_key=session_id
            ).strip()
            return send_file_for_download(output_filepath, "maveLLR.csv")
        finally:
            rm_files([ref_filepath, score_filepath, output_filepath])
