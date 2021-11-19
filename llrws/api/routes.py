"""
/llrws/api/routes.py
~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes for the LLR Web Service API.
"""

from flask import Blueprint

from llrws.api.endpoints import HelloWorld

api_bp = Blueprint("api", __name__)


def initialize_routes(api):
    api.add_resource(HelloWorld, "/")
