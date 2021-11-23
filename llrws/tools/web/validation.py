import os

from flask import current_app
from werkzeug.utils import secure_filename


def validate_file_properties(fileobj, file_descriptor):
    """Validates fileobj. Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    # Validate fileobj instance
    if fileobj is None:
        error_msg = f"Missing {file_descriptor}."
        return False, error_msg
    # Convert fileobj.filename to secure filename before evaluating filename.
    filename = secure_filename(fileobj.filename)
    if not bool(filename):
        error_msg = f"Missing {file_descriptor}."
        return False, error_msg
    # Validate file extension
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{file_descriptor} does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        return False, error_msg

    return True, ""
