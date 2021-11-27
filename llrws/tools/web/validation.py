import os

from flask import current_app
from werkzeug.utils import secure_filename

from llrws.exceptions import FileValidationError


def validate_file_properties(fileobj, file_descriptor):
    """Validates `fileobj` properties through a series of checks.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (None)
    """
    # Any procedure in `validation_procedures` will always take a file object and
    # a file descriptor as its arguments.
    validation_procedures = (validate_fileobject, validate_filename, validate_fileext)
    for procedure in validation_procedures:
        # Raises `FileValidationError` if validation fails
        procedure(fileobj, file_descriptor)


def validate_fileobject(fileobj, file_descriptor):
    """Validates `fileobj` is not null.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (None)
    """
    if fileobj is None:
        error_msg = f"Missing {file_descriptor}."
        raise FileValidationError(error_msg)


def validate_filename(fileobj, file_descriptor):
    """Validates the file name of `fileobj`.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (None)
    """
    # Convert fileobj.filename to secure filename before evaluating filename.
    filename = secure_filename(fileobj.filename)
    if not bool(filename):
        error_msg = f"Missing {file_descriptor}."
        raise FileValidationError(error_msg)


def validate_fileext(fileobj, file_descriptor):
    """Validates the file extension of `fileobj`.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        file_descriptor (str): Description of file

    Returns:
        (None)
    """
    filename = secure_filename(fileobj.filename)
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{file_descriptor} does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        raise FileValidationError(error_msg)
