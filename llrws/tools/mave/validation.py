import warnings

warnings.simplefilter(action="ignore", category=UserWarning)

import pandas as pd
import pandera as pa

from llrws.exceptions import InvalidCsvSchema, InvalidCsvSchemaType


def get_schema_type(csv_filepath):
    """Gets schema type from CSV filepath.
    Raises InvalidCsvSchemaType if schema type cannot be identified.

    Args:
        csv_filepath (str): File path to CSV file

    Returns:
        (str): Schema type of `csv_filepath`
    """
    schemas = {
        validate_benchmark_schema: "benchmark",
        validate_score_schema: "score",
    }
    for schema, schema_type in schemas.items():
        try:
            schema(csv_filepath)
            return schema_type
        except InvalidCsvSchema:
            pass
    raise InvalidCsvSchemaType("CSV schema type unknown.")


def validate_benchmark_schema(csv_filepath, file_descriptor="MAVE benchmark file"):
    """Validates Pandas DataFrame with data content from MAVE benchmark file.
    Raises InvalidCsvSchema if validation fails.

    Args:
        csv_filepath (str): File path to benchmark CSV file

    Returns:
        (None)
    """
    benchmark_schema = pa.DataFrameSchema(
        {
            # E.g. CALM1:c.293A>G, c.211T>Y
            "hgvsc": pa.Column(str, pa.Check.str_contains(r"c\.(.*)$")),
            # E.g. p.Asn98Ser
            "hgvsp": pa.Column(str, pa.Check.str_contains(r"p\.(.*)$")),
            "maf": pa.Column(float, nullable=True),
            "hom": pa.Column(float, nullable=True),
            "referenceSet": pa.Column(str),
            "source": pa.Column(str),
        },
        strict=True,
        coerce=True,
    )
    try:
        benchmark_df = pd.read_csv(csv_filepath)
        # Attempt benchmark schema validation
        benchmark_schema(benchmark_df)
    except (pd.errors.ParserError, pa.errors.SchemaError) as e:
        raise InvalidCsvSchema(f"Invalid schema: {file_descriptor} encountered the following problem: {e}") from e


def validate_score_schema(csv_filepath, file_descriptor="MAVE score file"):
    """Validates Pandas DataFrame with data content from MAVE score file.
    Raises InvalidCsvSchema if validation fails.

    Args:
        csv_filepath (str): File path to benchmark CSV file

    Returns:
        (None)
    """
    score_schema = pa.DataFrameSchema(
        {
            # E.g. p.Asn98Ser
            "hgvs_pro": pa.Column(str, pa.Check.str_contains(r"p\.(.*)$")),
            "score": pa.Column(float, nullable=True),
            "sd": pa.Column(float, nullable=True),
            "se": pa.Column(float, nullable=True),
        },
        strict=True,
        coerce=True,
    )
    try:
        score_df = pd.read_csv(csv_filepath)
        # Attempt score schema validation
        score_schema(score_df)
    except (pd.errors.ParserError, pa.errors.SchemaError) as e:
        raise InvalidCsvSchema(f"Invalid schema: {file_descriptor} encountered the following problem: {e}") from e
