"""
/llrws/config.py

Module to store Flask configurations.
"""

import os


class Config:
    """Flask app configuration class."""

    DEBUG = True
    TESTING = False
    SERVER_NAME = "localhost:5000"
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
