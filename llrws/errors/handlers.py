"""
/llrws/errors/handlers.py
~~~~~~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle errors.
"""

from flask import Blueprint

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(400)
def error_400(error):
    """Bad Request"""


@errors.app_errorhandler(403)
def error_403(error):
    """Forbidden"""


@errors.app_errorhandler(404)
def error_404(error):
    """Page Not Found"""


@errors.app_errorhandler(413)
def error_413(error):
    """Payload Too Large"""
    return "Uploaded file is too large", 413


@errors.app_errorhandler(429)
def error_429(error):
    """Too Many Requests"""


@errors.app_errorhandler(500)
def error_500(error):
    """Internal Server Error"""
