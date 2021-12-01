import json
import os

from llrws.tools.mave.scoresets import SCORESETS_PATH


def query_scoresets_by_gene_name(gene_name):
    genename_scoresets_filepath = os.path.join(SCORESETS_PATH, "genename_scoresets.json")
    genename_scoresets = read_json(genename_scoresets_filepath)

    return genename_scoresets.get(gene_name.lower(), [])


def read_json(json_filepath):
    with open(json_filepath) as f:
        scoresets = json.load(f)
    return scoresets
