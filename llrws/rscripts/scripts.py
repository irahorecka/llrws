import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def execute_maveLLR_script(reference_path, score_path, download_path, unique_key=None):
    """Executes mave.r and writes unique output file to {}

    Args:
        reference_path (str): Path to reference CSV file
        score_path (str): Path to score CSV file
        unique_key (str): Unique identifier
    """
    mave_path = os.path.join(BASE_DIR, "mave.r")
    call = [
        "Rscript",
        mave_path,
        f"--reference={reference_path}",
        f"--score={score_path}",
        f"--downloadpath={download_path}",
        f"--key={unique_key}",
    ]
    result = subprocess.Popen(call, stdout=subprocess.PIPE)
    # Return exported filepath from R script's stdout
    return result.stdout.read().decode("utf-8")
