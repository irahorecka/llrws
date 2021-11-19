from uuid import uuid4

from flask_restful import Resource, reqparse
import werkzeug


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}

    def post(self):
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "file=@table-1.csv" http://api.localhost:5000
        parse = reqparse.RequestParser()
        parse.add_argument("file", type=werkzeug.datastructures.FileStorage, location="files")
        args = parse.parse_args()
        image_file = args["file"]
        filename = f"{uuid4()}.csv"
        image_file.save(filename)
        print(filename)
