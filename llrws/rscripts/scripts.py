import os
import subprocess

RSCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))


def execute_maveLLR_script(reference_path, score_path, download_path):
    """Executes mave.r and writes unique output file to {}

    Args:
        reference_path (str): Path to reference CSV file
        score_path (str): Path to score CSV file
        download_path (str): Path to maveLLR-processed CSV file

    Returns:
        (bool): Indicative of process success (True) or failure (False)
        (str): Exported CSV filepath (utf-8) from mave Rscript
    """
    mave_rscript_path = os.path.join(RSCRIPTS_DIR, "mave.r")
    rscript_call = [
        "Rscript",
        mave_rscript_path,
        f"--reference={reference_path}",
        f"--score={score_path}",
        f"--download={download_path}",
    ]
    # At this point, nearly *all* data validation should be complete for reference_path
    # and score_path.
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
