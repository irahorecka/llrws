import re


def sort_flat_mave_csv(flat_mave_csv):
    # Extract digits and terminal AA (i.e. AA position and substituted AA) from 'hgvs_pro' column
    # and sort in ascending order.
    re_extract_AA_pos = re.compile(r"\d+")
    re_extract_substituted_AA = re.compile(r"[^\d+]*$")
    flat_mave_csv.sort(
        key=lambda x: (
            int(re_extract_AA_pos.search(x["hgvs_pro"]).group()),
            re_extract_substituted_AA.search(x["hgvs_pro"]).group(),
        )
    )

    return flat_mave_csv
