import os

from flask import current_app, send_file
from werkzeug.utils import secure_filename


def save_fileobj_to_filepath(fileobj, filepath, file_descriptor):
    """Validates then saves fileobj to filepath. Descriptive error with file_descriptor is returned if
    validation fails.

    Args:
        fileobj (werkzeug.datastructures.FileStorage): FileStorage instance of a file
        filepath (str): File path to save fileobj
        file_descriptor (str): Description of file

    Returns:
        (bool, str): Indicator of validation success, "" (if success) or error message (if failure)
    """
    error_msg = ""

    # Validate fileobj
    if fileobj is None:
        error_msg = f"Missing {file_descriptor} file."
        return False, error_msg
    # Convert fileobj.filename to secure filename before evaluating.
    filename = secure_filename(fileobj.filename)
    if not bool(filename):
        error_msg = f"Missing {file_descriptor} file."
        return False, error_msg
    # Validate file extension
    fileext = os.path.splitext(filename)[1]
    if fileext.lower() not in current_app.config["UPLOAD_EXTENSIONS"]:
        error_msg = f"{file_descriptor} file does not have one of the allowed extensions: {' '.join(current_app.config['UPLOAD_EXTENSIONS'])}"
        return False, error_msg

    # Save file
    fileobj.save(filepath)
    return True, error_msg


def send_file_for_download(filepath, filename):
    """Sends a file for download to the web-app user.

    Args:
        filepath (str): Path to file to send for download
        filename (str): File name to attach to file for download

    Returns:
        (flask.wrappers.Response): File object for download
    """
    worklist = send_file(
        filepath,
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
