import warnings

warnings.simplefilter(action="ignore", category=UserWarning)

import pandas as pd
import pandera as pa


def validate_benchmark_or_score_schema_from_mave_csv_file(mave_csv_filepath, file_descriptor):
    """Identifies CSV file as benchmark or score and validates for data content schema.
    Validated content templated from known MAVE benchmark and score CSV files.
    Descriptive error is returned if validation fails.

    Args:
        mave_csv_filepath (str): File path to MAVE benchmark or score CSV file
        file_descriptor (str): Description of file to concatenate to error message if error thrown

    Returns:
        (bool): Validation success (True) or failure (False)
        (str): "" if success, error message if validation fails
        (str): CSV filetype (i.e. "score" or "benchmark"), or "" if filetype is not detected
    """
    is_valid_benchmark_schema, _ = validate_benchmark_schema_from_mave_csv_file(mave_csv_filepath)
    if is_valid_benchmark_schema:
        return True, "", "benchmark"

    is_valid_score_schema, _ = validate_score_schema_from_mave_csv_file(mave_csv_filepath)
    if is_valid_score_schema:
        return True, "", "score"

    return False, f"{file_descriptor} is neither a benchmark nor score file", ""


def validate_benchmark_schema_from_mave_csv_file(mave_csv_filepath, file_descriptor="MAVE benchmark file"):
    """Validates Pandas DataFrame with data content from MAVE benchmark file.

    Args:
        mave_csv_filepath (str): File path to MAVE benchmark CSV file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
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
        benchmark_df = pd.read_csv(mave_csv_filepath)
        # Attempt benchmark schema validation
        benchmark_schema(benchmark_df)
        return True, ""
    except (pd.errors.ParserError, pa.errors.SchemaError) as e:
        return False, f"{file_descriptor} validation encountered the following problem: {e}"


def validate_score_schema_from_mave_csv_file(mave_csv_filepath, file_descriptor="MAVE score file"):
    """Validates Pandas DataFrame with data content from MAVE score file.

    Args:
        mave_csv_filepath (str): File path to MAVE benchmark CSV file

    Returns:
        (bool): Indicative of validation success (True) or failure (False)
        (str): "" or error message if validation success or failure, respectively
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
        score_df = pd.read_csv(mave_csv_filepath)
        # Attempt score schema validation
        score_schema(score_df)
        return True, ""
    except (pd.errors.ParserError, pa.errors.SchemaError) as e:
        return False, f"{file_descriptor} validation encountered the following problem: {e}"
