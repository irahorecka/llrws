"""
/llrws/tools/mave/validation/score.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tools for validating MAVE scoreset CSV file.
"""

import pandera as pa

from llrws.exceptions import InvalidCsvSchema
from llrws.tools.mave.validation import get_tidy_pd_dataframe_from_csv

SCHEMA = {
    # E.g. p.Asn98Ser
    "hgvs_pro": pa.Column(str, pa.Check.str_contains(r"p\.(.*)$")),
    "score": pa.Column(float, nullable=True),
    "sd": pa.Column(float, nullable=True),
    "se": pa.Column(float, nullable=True),
}


def validate_score_schema(csv_filepath, file_descriptor="MAVE score file"):
    """Validates Pandas DataFrame with data content from MAVE score file.
    Data wrangling of the input file is expected as some files have metadata information in
    the header. ALL input files will be re-written to `csv_filepath` if schema validation after
    data wrangling is successful.
    Raises InvalidCsvSchema if validation fails.

    Args:
        csv_filepath (str): File path to score CSV file

    Returns:
        (None)
    """
    score_schema = pa.DataFrameSchema(
        SCHEMA,
        strict=True,
        coerce=True,
    )
    try:
        score_df = get_tidy_pd_dataframe_from_csv(csv_filepath)
        # Only isolate columns of interest - raises KeyError if column not found.
        score_df = score_df[list(SCHEMA)]
        # Attempt score schema validation
        score_schema(score_df)
    except (KeyError, pa.errors.SchemaError) as e:
        raise InvalidCsvSchema(f"Invalid schema: {file_descriptor} encountered the following problem: {e}") from e


def export_score_file(score_filepath):
    """Exports score CSV file to specified filepath.

    Args:
        score_filepath (str): File path to score CSV file for export

    Returns:
        (None)
    """
    score_df = get_tidy_pd_dataframe_from_csv(score_filepath)
    score_df = score_df[list(SCHEMA)]
    score_df.to_csv(score_filepath, index=False)
