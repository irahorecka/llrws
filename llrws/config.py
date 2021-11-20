"""
/llrws/config.py

Module to store Flask configurations.
"""

import os


class Config:
    """Flask app configuration class."""

    # App config
    DEBUG = True
    TESTING = False
    SERVER_NAME = "localhost:5000"

    # File processing
    # 1MB max file size
    MAX_CONTENT_LENGTH = 1024 * 1024
    UPLOAD_EXTENSIONS = [".csv"]
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
