import pandera as pa

from llrws.exceptions import InvalidCsvSchema
from llrws.tools.mave.validation import get_tidy_pd_dataframe_from_csv

SCHEMA = {
    # E.g. CALM1:c.293A>G, c.211T>Y
    "hgvsc": pa.Column(str, pa.Check.str_contains(r"c\.(.*)$")),
    # E.g. p.Asn98Ser
    "hgvsp": pa.Column(str, pa.Check.str_contains(r"p\.(.*)$")),
    "maf": pa.Column(float, nullable=True),
    "hom": pa.Column(float, nullable=True),
    "referenceSet": pa.Column(str),
    "source": pa.Column(str),
}


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
        SCHEMA,
        strict=True,
        coerce=True,
    )
    try:
        benchmark_df = get_tidy_pd_dataframe_from_csv(csv_filepath)
        # Only isolate columns of interest - raises KeyError if column not found.
        benchmark_df = benchmark_df[list(SCHEMA)]
        # Attempt benchmark schema validation
        benchmark_schema(benchmark_df)
    except (KeyError, pa.errors.SchemaError) as e:
        raise InvalidCsvSchema(f"Invalid schema: {file_descriptor} encountered the following problem: {e}") from e


def export_benchmark_file(benchmark_filepath):
    """Exports benchmark CSV file to specified filepath.

    Args:
        benchmark_filepath (str): File path to benchmark CSV file for export

    Returns:
        (None)
    """
    benchmark_df = get_tidy_pd_dataframe_from_csv(benchmark_filepath)
    benchmark_df = benchmark_df[list(SCHEMA)]
    benchmark_df.to_csv(benchmark_filepath, index=False)
