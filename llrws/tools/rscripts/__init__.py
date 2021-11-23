import os
import subprocess

RSCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def execute_maveLLR_script(benchmark_filepath, score_filepath, download_filepath):
    """Executes ./mave.r and writes output CSV file to `download_filepath`.

    Args:
        benchmark_filepath (str): Path to benchmark CSV file
        score_filepath (str): Path to score CSV file
        download_filepath (str): Path to maveLLR-processed CSV file

    Returns:
        (bool): Indicative of process success (True) or failure (False)
        (str): StdError of StdOut if failure or success, respectively
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
    # Output CSV file is written to disk in mave.r if execution is successful.
    result, return_code = execute_subprocess(rscript_call)
    # Non-zero exit code - indicate error and return stderr to caller.
    if return_code != 0:
        return False, result.stderr.read().decode("utf-8")
    # Return success flag + stdout from Rscript execution.
    return True, result.stdout.read().decode("utf-8")


def execute_subprocess(script_call):
    """Executes script call via subprocess.Popen and returns subprocess output and return code to caller.

    Args:
        script_call (str): Formatted script call for *NIX bash execution

    Returns:
        (subprocess.Popen): Subprocess output
        (int): Subprocess return code
    """
    result = subprocess.Popen(script_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for subprocess to complete prior to fetching return code.
    result.wait()
    return result, result.returncode
