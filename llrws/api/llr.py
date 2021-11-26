from flask_restful import Resource, reqparse
import werkzeug

from llrws.tools.mave import (
    generate_mave_csv_filepaths,
    validate_benchmark_schema_from_mave_csv_file,
    validate_score_schema_from_mave_csv_file,
)
from llrws.tools.rscripts import execute_maveLLR_rscript
from llrws.tools.web import rm_files, send_file_for_download, validate_file_properties


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
        mave_csv_filepaths = generate_mave_csv_filepaths()
        benchmark_csv_filepath = mave_csv_filepaths["benchmark"]
        score_csv_filepath = mave_csv_filepaths["score"]
        output_csv_filepath = mave_csv_filepaths["output"]

        try:
            # Files from args are wildcards - may or may not be CSV files.
            benchmark_file = args["benchmark_file"]
            is_valid_benchmark_file, error_msg = self._validate_and_save_csv_file(
                benchmark_file,
                benchmark_csv_filepath,
                file_descriptor="MAVE benchmark CSV",
                schema_validator=validate_benchmark_schema_from_mave_csv_file,
            )
            if not is_valid_benchmark_file:
                error_msg = f"{error_msg}. Please verify your MAVE benchmark CSV file and try again."
                return error_msg, 400

            score_file = args["score_file"]
            is_valid_score_file, error_msg = self._validate_and_save_csv_file(
                score_file,
                score_csv_filepath,
                file_descriptor="MAVE score CSV",
                schema_validator=validate_score_schema_from_mave_csv_file,
            )
            if not is_valid_score_file:
                error_msg = f"{error_msg}. Please verify your MAVE score CSV file and try again."
                return error_msg, 400

            # Execute R script ../rscripts/mave.r via Python wrapper scripts.execute_maveLLR_rscript.
            # error_msg is either stderr or stdout and is conditional to failure or success, respectively.
            # However, error_msg will only be returned if failure, hence it will only be used in stderr instances.
            is_script_successful, error_msg = execute_maveLLR_rscript(
                benchmark_csv_filepath, score_csv_filepath, download_filepath=output_csv_filepath
            )
            if not is_script_successful:
                return error_msg, 400

            return send_file_for_download(output_csv_filepath, filename="maveLLR.csv")

        finally:
            # Remove all upload and download files regardless of success / failure.
            rm_files(filepaths=[benchmark_csv_filepath, score_csv_filepath, output_csv_filepath])

    @staticmethod
    def _validate_and_save_csv_file(file, filepath, file_descriptor, schema_validator):
        """Validates file properties, saves CSV file, and validates appropriate CSV schema of file.
        Descriptive error is returned if validation fails.

        Args:
            file (werkzeug.datastructures.FileStorage): FileStorage instance of MAVE benchmark or score CSV file
            filepath (str): File path to MAVE benchmark or score CSV file
            file_descriptor (str): Description of CSV file
            schema_validator (llrws.utils.web.validate_benchmark_schema_from_mave_csv_file or *.*.*.validate_score_schema_from_mave_csv_file):
                A function that validates the MAVE benchmark or score CSV file schema.

        Returns:
            (bool): Indicative of validation success (True) or failure (False)
            (str): "" or error message if validation success or failure, respectively
        """
        # Validate input file properties and save file if valid.
        is_valid_file, error_msg = validate_file_properties(file, file_descriptor=file_descriptor)
        if not is_valid_file:
            return False, "", error_msg

        file.save(filepath)
        # At this point, we're working with a CSV file - validate CSV schema.
        is_valid_csv, error_msg = schema_validator(filepath, file_descriptor=file_descriptor)
        return is_valid_csv, error_msg
