import csv
import re
from io import StringIO


def sort_mave_csv_by_hgvs_pro_from_reponse_content(mave_response_content):
    """Gets and sorts MAVE CSV from request response content.
    Sorts MAVE content by column 'hgvs_pro' by order of AA position and substituted AA, respectively.

    Args:
        mave_response_content (str): UTF-8 MAVE content from a request response

    Returns:
        (list[dict]): Flattened and sorted post-processed MAVE CSV list
    """
    flat_mave_csv = flatten_csv_from_response_content(mave_response_content)
    return sort_mave_csv_by_column_hgvs_pro(flat_mave_csv)


def sort_mave_csv_by_column_hgvs_pro(flat_mave_csv):
    """Extract digits and terminal AA (i.e. AA position and substituted AA) from 'hgvs_pro' column
    from a flat MAVE CSV content. Sorts in ascending order.

    Args:
        flat_mave_csv (iterable[dict]): UTF-8 content from a request response

    Returns:
        (list[dict]): Flattened and sorted post-processed MAVE CSV list
    """

    re_extract_AA_pos = re.compile(r"\d+")
    re_extract_substituted_AA = re.compile(r"[^\d+]*$")
    return sorted(
        flat_mave_csv,
        key=lambda x: (
            int(re_extract_AA_pos.search(x["hgvs_pro"]).group()),
            re_extract_substituted_AA.search(x["hgvs_pro"]).group(),
        ),
    )


def flatten_csv_from_response_content(csv_content):
    """Flatten CSV content from request response content.

    Args:
        csv_content (str): UTF-8 content from a request response

    Returns:
        (iterable[dict]): Flattened CSV list
    """
    return iter(csv.DictReader(StringIO(csv_content)))
