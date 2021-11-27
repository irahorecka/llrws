import csv
import re
from io import StringIO


def get_mave_csv_sorted_by_hgvs_pro(mave_response_content):
    """Gets and sorts MAVE CSV from request response content.
    Sorts MAVE content by column 'hgvs_pro' by order of AA position and substituted AA, respectively.

    Args:
        mave_response_content (str): UTF-8 MAVE content from a request response

    Returns:
        (list[dict]): Flattened and sorted post-processed MAVE CSV reader
    """
    mave_reader = csv_to_reader_from_response_content(mave_response_content)
    return sort_mave_reader_by_hgvs_pro(mave_reader)


def sort_mave_reader_by_hgvs_pro(mave_dict):
    """Extract digits and terminal AA (i.e. AA position and substituted AA) from 'hgvs_pro' column
    from a MAVE CSV content in ditionary format. Sort in ascending order.

    Args:
        mave_dict (iterable[dict]): UTF-8 content from a request response

    Returns:
        (list[dict]): Flattened and sorted post-processed MAVE CSV reader
    """

    re_extract_AA_pos = re.compile(r"\d+")
    re_extract_substituted_AA = re.compile(r"[^\d+]*$")
    return sorted(
        mave_dict,
        key=lambda x: (
            int(re_extract_AA_pos.search(x["hgvs_pro"]).group()),
            re_extract_substituted_AA.search(x["hgvs_pro"]).group(),
        ),
    )


def csv_to_reader_from_response_content(csv_content):
    """Converts a stream of CSV content to a reader object.

    Args:
        csv_content (str): Stream of UTF-8 CSV content from a request response

    Returns:
        (iterable[dict]): Flattened CSV reader
    """
    return iter(csv.DictReader(StringIO(csv_content)))
