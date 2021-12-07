import os

from llrws.tools.mave.scoresets import read_json, SCORESETS_JSON_DIR


def query_available_urns_by_gene_name(gene_name):
    scoresets = query_scoresets_by_gene_name(gene_name)
    if not scoresets:
        return []
    return [{gene.title(): entry["urn"]} for gene, entries in scoresets.items() for entry in entries]


def query_scoresets_by_gene_name(gene_name):
    gene_name_scoresets_filepath = os.path.join(SCORESETS_JSON_DIR, "genename_scoresets.json")
    gene_name_scoresets = read_json(gene_name_scoresets_filepath)
    # This is the startswith logic... get anything that starts with something
    gene_name_scoresets = {
        gene: data for gene, data in gene_name_scoresets.items() if gene.startswith(gene_name.lower())
    }

    return gene_name_scoresets
