"""
/llrws/tools/rscripts/__init__.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tools for interfacing with Rscripts in directory.
"""

import os
import subprocess

from llrws.exceptions import RscriptException

RSCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def execute_maveLLR_rscript(benchmark_filepath, score_filepath, download_filepath):
    """Executes ./mave.r and writes output CSV file to `download_filepath`.
    Raises RscriptException if R-Script raises an exception.

    Args:
        benchmark_filepath (str): Path to benchmark CSV file
        score_filepath (str): Path to score CSV file
        download_filepath (str): Path to maveLLR-processed CSV file

    Returns:
        (None)
    """
    mave_rscript_filepath = os.path.join(RSCRIPTS_DIR, "mave.r")
    # At this point, nearly *all* data validation should be complete for benchmark_filepath
    # and score_filepath.
    rscript_call = [
        "Rscript",
        mave_rscript_filepath,
        f"--benchmark={benchmark_filepath}",
        f"--score={score_filepath}",
        f"--download={download_filepath}",
    ]
    # Output CSV file is written to disk as `download_filepath` in mave.r if execution is successful.
    result, return_code = execute_subprocess(rscript_call)
    # Non-zero exit code - raise exception with stderr.
    if return_code != 0:
        raise RscriptException(result.stderr.read().decode("utf-8"))


def execute_subprocess(script_call):
    """Executes script call via subprocess.Popen and returns subprocess output and return code to caller.

    Args:
        script_call (list): Formatted script call for *NIX bash execution

    Returns:
        (subprocess.Popen): Subprocess output
        (int): Subprocess return code
    """
    result = subprocess.Popen(script_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for subprocess to complete prior to fetching return code.
    result.wait()
    result.terminate()
    return result, result.returncode
