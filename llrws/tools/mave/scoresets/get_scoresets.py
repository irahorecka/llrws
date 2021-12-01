import json
import os
from collections import defaultdict

from llrws.tools.mave.api import scoresets
from llrws.tools.mave.scoresets import SCORESETS_PATH


def generate_scoresets_json_files_from_mavedb():
    scoresets = get_all_scoresets_as_json_from_mavedb()
    scoresets_json_filepath = os.path.join(SCORESETS_PATH, "scoresets.json")
    write_to_json(scoresets, scoresets_json_filepath)

    genename_scoresets = get_scoresets_linked_by_genenames(scoresets)
    genename_scoresets_json_filepath = os.path.join(SCORESETS_PATH, "genename_scoresets.json")
    write_to_json(genename_scoresets, genename_scoresets_json_filepath)


def get_all_scoresets_as_json_from_mavedb():
    return scoresets().get().json()


def write_to_json(json_content, json_filepath):
    with open(json_filepath, "w") as file:
        json.dump(json_content, file)


def get_scoresets_linked_by_genenames(scoresets):
    # Link gene name to scoresets
    gene_name_scoresets = defaultdict(list)
    # Dicts are usually treated as references - make copy.
    for scoreset in scoresets.copy():
        gene = scoreset["target"]["name"].lower()
        gene_name_scoresets[gene].append(scoreset)

    return gene_name_scoresets
