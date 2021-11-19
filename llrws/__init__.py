"""
/llrws/__init__.py

Concerns all things LLR Web Suite.
"""

from flask import Flask

from llrws.config import Config

application = Flask(__name__)


def create_app(config_class=Config):
    """Creates Flask application instance."""
    application.config.from_object(config_class)

    from llrws.api.routes import api

    application.register_blueprint(api)

    return application
