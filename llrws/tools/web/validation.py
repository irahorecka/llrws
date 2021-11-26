import os

from flask import current_app
from werkzeug.utils import secure_filename


def validate_file_properties(fileobj, file_descriptor):
    """Validates `fileobj` properties through a series of checks.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    # Any procedure in `validation_procedures` will always take a file object and
    # a file descriptor as its arguments.
    validation_procedures = (validate_fileobject, validate_filename, validate_fileext)
    for procedure in validation_procedures:
        is_valid_file, error_msg = procedure(fileobj, file_descriptor)
        if not is_valid_file:
            return False, error_msg
    return True, ""


def validate_fileobject(fileobj, file_descriptor):
    """Validates `fileobj` is not null.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    if fileobj is None:
        error_msg = f"Missing {file_descriptor}."
        return False, error_msg
    return True, ""


def validate_filename(fileobj, file_descriptor):
    """Validates the file name of `fileobj`.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    # Convert fileobj.filename to secure filename before evaluating filename.
    filename = secure_filename(fileobj.filename)
    if not bool(filename):
        error_msg = f"Missing {file_descriptor}."
        return False, error_msg
    return True, ""


def validate_fileext(fileobj, file_descriptor):
    """Validates the file extension of `fileobj`.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    filename = secure_filename(fileobj.filename)
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{file_descriptor} does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        return False, error_msg
    return True, ""
