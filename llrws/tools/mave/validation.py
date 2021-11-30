import csv
import warnings

warnings.simplefilter(action="ignore", category=UserWarning)

import numpy as np
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
    Data wrangling of the input file is expected as some files have metadata information in
    the header. ALL input files will be re-written to `csv_filepath` if schema validation after
    data wrangling is successful.
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
        benchmark_df = get_tidy_pd_dataframe_from_csv(csv_filepath)
        # Only isolate columns of interest - raises KeyError if column not found.
        benchmark_df = benchmark_df[["hgvsc", "hgvsp", "maf", "hom", "referenceSet", "source"]]
        # Attempt benchmark schema validation
        benchmark_schema(benchmark_df)
        # Re-export dataframe to `csv_filepath`
        benchmark_df.to_csv(csv_filepath, index=False)
    except (KeyError, pa.errors.SchemaError) as e:
        raise InvalidCsvSchema(f"Invalid schema: {file_descriptor} encountered the following problem: {e}") from e


def validate_score_schema(csv_filepath, file_descriptor="MAVE score file"):
    """Validates Pandas DataFrame with data content from MAVE score file.
    Data wrangling of the input file is expected as some files have metadata information in
    the header. ALL input files will be re-written to `csv_filepath` if schema validation after
    data wrangling is successful.
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
        score_df = get_tidy_pd_dataframe_from_csv(csv_filepath)
        # Only isolate columns of interest - raises KeyError if column not found.
        score_df = score_df[["hgvs_pro", "score", "sd", "se"]]
        # Attempt benchmark schema validation
        score_schema(score_df)
        # Re-export dataframe to `csv_filepath`
        score_df.to_csv(csv_filepath, index=False)
    except (KeyError, pa.errors.SchemaError) as e:
        raise InvalidCsvSchema(f"Invalid schema: {file_descriptor} encountered the following problem: {e}") from e


def get_tidy_pd_dataframe_from_csv(csv_filepath):
    """Similar to pd.read_csv, except there are tidying steps to remove
    metadata headers while preserving appropriate dtypes.

    Args:
        csv_filepath (str): File path to benchmark CSV file

    Returns:
        (pandas.core.frame.DataFrame): Tidied pandas dataframe
    """
    with open(csv_filepath, newline="") as csvfile:
        csv_reader = csv.reader(csvfile, skipinitialspace=True)
        csv_df = pd.DataFrame(remove_metadata_header_from_csv(csv_reader))
    # Convert 'NA' to NaN dtype
    csv_df = csv_df.replace("NA", np.nan)
    # Grab first row and set as the new header
    new_header = csv_df.iloc[0]
    csv_df = csv_df[1:]
    csv_df.columns = new_header
    # Convert object dtypes to floating point values
    csv_df = csv_df.apply(pd.to_numeric, errors="ignore")

    return csv_df.reset_index(drop=True)


def remove_metadata_header_from_csv(csv_reader):
    """Trims metadata header (starts with '#') from stream of CSV content.

    Args:
        csv_reader (_csv.reader): Reader object of a CSV file

    Returns:
        (generator[list]): CSV rows without metadata header
    """
    for row in csv_reader:
        # Don't pop!
        if row[0].startswith("#"):
            continue
        yield row
