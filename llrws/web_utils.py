import os

from flask import current_app, send_file
from werkzeug.utils import secure_filename


def save_fileobj_to_filepath(fileobj, filepath, file_descriptor):
    """Validates then saves fileobj to filepath if validation is successful.
    Descriptive error is returned if validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        filepath (str): File path to save fileobj
        file_descriptor (str): Description of file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
    """
    is_valid, error_msg = validate_fileobj(fileobj, file_descriptor)
    if not is_valid:
        return False, error_msg
    # Save file if validation is successful
    fileobj.save(filepath)
    return True, ""


def validate_fileobj(fileobj, file_descriptor):
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
        error_msg = f"Missing {file_descriptor} file."
        return False, error_msg
    # Convert fileobj.filename to secure filename before evaluating filename.
    filename = secure_filename(fileobj.filename)
    if not bool(filename):
        error_msg = f"Missing {file_descriptor} file."
        return False, error_msg
    # Validate file extension
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{file_descriptor} file does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        return False, error_msg

    return True, ""


def send_file_for_download(filepath, filename, mimetype="text/csv"):
    """Sends a file for download to caller.

    Args:
        filepath (str): Path of file to send for download
        filename (str): File name to attach to download file

    Returns:
        (flask.wrappers.Response): File object for download
    """
    worklist = send_file(
        filepath,
        mimetype=mimetype,
        as_attachment=True,
        attachment_filename=filename,
        cache_timeout=-1,
    )
    worklist.headers["x-filename"] = filename
    worklist.headers["Access-Control-Expose-Headers"] = "x-filename"

    return worklist


def rm_files(filepaths):
    """Exhaustively removes files in an iterable of file paths.

    Args:
        filepaths (iter[(str)]): An iterable of file paths to be removed

    Returns:
        (None)
    """
    # Check if filepaths in an iterable container.
    if not isinstance(filepaths, (dict, list, set, tuple)):
        filepaths = [filepaths]
    for file in filepaths:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
