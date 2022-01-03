"""
/llrws/tools/mave/validation/__init__.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tools for interfacing with MAVE file validation tasks.
"""

import csv
import warnings

import numpy as np
import pandas as pd

warnings.simplefilter(action="ignore", category=UserWarning)


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
