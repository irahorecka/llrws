"""
/llrws/exceptions.py
~~~~~~~~~~~~~~~~~~~~

Module to store custom exceptions.
"""


class FileValidationError(Exception):
    """File validation failed."""


class InvalidUploadFile(Exception):
    """Invalid file was uploaded by user."""


class InvalidCsvSchema(Exception):
    """Invalid CSV schema."""


class InvalidCsvSchemaType(Exception):
    """Invalid CSV schema type."""


class RscriptException(Exception):
    """Invoked R-Script raised an exception."""
