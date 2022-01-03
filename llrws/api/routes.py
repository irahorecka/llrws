"""
/llrws/api/routes.py
~~~~~~~~~~~~~~~~~~~~

Flask blueprint to handle routes for the LLR Web Service API.
"""

from flask import Blueprint

from llrws.api.llr import LLR

# Keep - externally imported
api_bp = Blueprint("api", __name__)


def initialize_routes(api):
    """Initialize API routes."""
    # LLR takes priority as base API endpoint.
    # Reference object `api_base` to route to API internally.
    api.add_resource(LLR, "/", endpoint="api_base")
