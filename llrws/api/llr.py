import os
from uuid import uuid4

from flask import current_app
from flask_restful import Resource, reqparse
import werkzeug

from llrws.utils import send_file_for_download
from llrws.rscripts import execute_maveLLR_script


class LLR(Resource):
    def get(self):
        return {"hello": "world"}

    def post(self):
        session_id = uuid4()
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "file=@table-1.csv" http://api.localhost:5000
        parse = reqparse.RequestParser()
        parse.add_argument("reffile", type=werkzeug.datastructures.FileStorage, location="files")
        parse.add_argument("scorefile", type=werkzeug.datastructures.FileStorage, location="files")
        args = parse.parse_args()

        ref_file = args["reffile"]
        score_file = args["scorefile"]
        ref_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-reference.csv")
        score_filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{session_id}-score.csv")

        ref_file.save(ref_filepath)
        score_file.save(score_filepath)

        output_filepath = execute_maveLLR_script(
            ref_filepath, score_filepath, current_app.config["UPLOAD_FOLDER"], session_id
        ).strip()

        return send_file_for_download(output_filepath, "maveLLR.csv")
