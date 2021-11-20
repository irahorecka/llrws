import os
from uuid import uuid4

from flask import current_app
from flask_restful import Resource, reqparse
import werkzeug

from llrws.utils import send_file_for_download


class LLR(Resource):
    def get(self):
        return {"hello": "world"}

    def post(self):
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "file=@table-1.csv" http://api.localhost:5000
        parse = reqparse.RequestParser()
        parse.add_argument("file", type=werkzeug.datastructures.FileStorage, location="files")
        args = parse.parse_args()
        image_file = args["file"]
        filename = f"{uuid4()}.csv"
        image_file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        return send_file_for_download("table-1.csv", "test.csv")
