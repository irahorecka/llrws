from flask import send_file


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
