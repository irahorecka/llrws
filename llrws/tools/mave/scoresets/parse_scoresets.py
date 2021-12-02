import os

from llrws.tools.mave.scoresets import read_json, SCORESETS_JSON_DIR


def query_scoresets_by_gene_name(gene_name):
    gene_name_scoresets_filepath = os.path.join(SCORESETS_JSON_DIR, "genename_scoresets.json")
    gene_name_scoresets = read_json(gene_name_scoresets_filepath)

    return gene_name_scoresets.get(gene_name.lower(), [])
