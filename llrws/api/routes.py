"""
/llrws/api/routes.py
~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes for the LLR Web Service API.
"""

from flask import jsonify, render_template, Blueprint

api = Blueprint("api", __name__)


@api.route("/", subdomain="api")
def index():
    """Landing page of personal website."""
    content = {
        "title": "Home",
        "profile_img": "profile.png",
    }
    return jsonify(content)
