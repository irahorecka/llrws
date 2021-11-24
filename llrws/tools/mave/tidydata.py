import re


def sort_flat_mave_csv(flat_mave_csv):
    """Sorts a flat post-processed MAVE CSV iterable by order of AA position and substituted AA, respectively.

    Args:
        flat_mave_csv (iterable[dict]): Flat post-processed MAVE CSV iterable

    Returns:
        (list[dict]): Sorted flat post-processed MAVE CSV list
    """
    # Extract digits and terminal AA (i.e. AA position and substituted AA) from 'hgvs_pro' column
    # and sort in ascending order.
    re_extract_AA_pos = re.compile(r"\d+")
    re_extract_substituted_AA = re.compile(r"[^\d+]*$")
    return sorted(
        flat_mave_csv,
        key=lambda x: (
            int(re_extract_AA_pos.search(x["hgvs_pro"]).group()),
            re_extract_substituted_AA.search(x["hgvs_pro"]).group(),
        ),
    )
