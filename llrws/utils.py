import os

from flask import send_file


def send_file_for_download(filepath, filename):
    """Sends a file for download to the web-app user."""
    worklist = send_file(
        filepath,
        as_attachment=True,
        attachment_filename=filename,
        cache_timeout=-1,
    )
    worklist.headers["x-filename"] = filename
    worklist.headers["Access-Control-Expose-Headers"] = "x-filename"

    return worklist
