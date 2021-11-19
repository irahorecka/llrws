"""
/run.py
~~~~~~~

Starts a Flask web application instance.
"""
from llrws import create_app

application = create_app()

if __name__ == "__main__":
    # If you want to host purely locally with ability to use subdomain.
    application.config["SERVER_NAME"] = "localhost:5000"
    application.run(debug=True)
