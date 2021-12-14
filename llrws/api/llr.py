from flask_restful import Resource, reqparse
import werkzeug


from llrws.exceptions import InvalidCsvSchema, RscriptException
from llrws.tools.mave import generate_mave_csv_filepaths
from llrws.tools.mave.validation.benchmark import validate_benchmark_schema
from llrws.tools.mave.validation.score import validate_score_schema
from llrws.tools.rscripts import execute_maveLLR_rscript
from llrws.tools.web import rm_files, send_file_for_download, validate_file_properties


class LLR(Resource):
    # Build request parser and parse post request file contents.
    # Declare reqparse.ReqestParser here to avoid instantiation overhead when POST request is made.
    parse = reqparse.RequestParser()
    parse.add_argument("benchmark_file", type=werkzeug.datastructures.FileStorage, location="files")
    parse.add_argument("score_file", type=werkzeug.datastructures.FileStorage, location="files")

    def get(self):
        """Simple GET request routed to `LLR`."""
        return {"rothlab": "LLR Web Service"}

    def post(self):
        """Handles POST request routed to `LLR`. Caller must upload two files (benchmark and score).
        If validation of two files successful, an LLR will be generated and streamed as CSV to the
        caller."""
        # Example cURL call: curl -v POST -H "Content-Type: multipart/form-data" -F "benchmark_file=@table-1.csv" -F "score_file=@table-2.csv" http://localhost:5000/api/
        args = self.parse.parse_args()
        mave_csv_filepaths = generate_mave_csv_filepaths()
        benchmark_csv_filepath = mave_csv_filepaths["benchmark"]
        score_csv_filepath = mave_csv_filepaths["score"]
        output_csv_filepath = mave_csv_filepaths["output"]

        try:
            benchmark_file = args["benchmark_file"]
            # Files from args are wildcards - may or may not be CSV files.
            validate_file_properties(benchmark_file, file_descriptor="MAVE benchmark CSV")
            # We are confident our benchmark file is a CSV - save and validate schema.
            benchmark_file.save(benchmark_csv_filepath)
            validate_benchmark_schema(benchmark_csv_filepath, file_descriptor="MAVE benchmark CSV")

            score_file = args["score_file"]
            validate_file_properties(score_file, file_descriptor="MAVE score CSV")
            score_file.save(score_csv_filepath)
            validate_score_schema(score_csv_filepath, file_descriptor="MAVE score CSV")

            # Execute R script ../rscripts/mave.r via Python wrapper scripts.execute_maveLLR_rscript and save
            # output to `output_csv_filepath`.
            execute_maveLLR_rscript(benchmark_csv_filepath, score_csv_filepath, download_filepath=output_csv_filepath)
            return send_file_for_download(output_csv_filepath, filename="maveLLR.csv")

        except (InvalidCsvSchema, RscriptException) as e:
            return str(e), 400

        finally:
            # Remove all upload and download files regardless of success / failure.
            rm_files(
                filepaths=(
                    benchmark_csv_filepath,
                    score_csv_filepath,
                    output_csv_filepath,
                )
            )
