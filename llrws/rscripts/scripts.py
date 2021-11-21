import os
import subprocess

RSCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def execute_maveLLR_script(benchmark_filepath, score_filepath, download_filepath):
    """Executes mave.r and writes unique output file to {}

    Args:
        benchmark_filepath (str): Path to benchmark CSV file
        score_filepath (str): Path to score CSV file
        download_filepath (str): Path to maveLLR-processed CSV file

    Returns:
        (bool): Indicative of process success (True) or failure (False)
        (str): Exported CSV filepath (utf-8) from mave Rscript
    """
    mave_rscript_filepath = os.path.join(RSCRIPTS_DIR, "mave.r")
    rscript_call = [
        "Rscript",
        mave_rscript_filepath,
        f"--benchmark={benchmark_filepath}",
        f"--score={score_filepath}",
        f"--download={download_filepath}",
    ]
    # At this point, nearly *all* data validation should be complete for benchmark_filepath
    # and score_filepath.
    return execute_subprocess(rscript_call)


def execute_subprocess(script_call):
    """Executes script call via subprocess.Popen. Returns True, stdout if execution
    was successful. Returns False, stderr if execution failed.

    Args:
        script_call (str): Formatted script call for *NIX bash execution.

    Returns:
        (bool, str): Indicator of process success, stdout (if success) or stderror (if failure)
    """
    result = subprocess.Popen(script_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for subprocess to complete prior to fetching return code.
    result.wait()
    return_code = result.returncode

    # Non-zero exit code - indicate error and return stderr to caller.
    if return_code != 0:
        return False, result.stderr.read().decode("utf-8")
    # Return success flag + stdout from Rscript execution.
    return True, result.stdout.read().decode("utf-8")
