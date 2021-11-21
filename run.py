"""
/run.py
~~~~~~~

Starts a Flask web application instance.
"""

from llrws import create_app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
