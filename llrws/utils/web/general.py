import os


def rm_files(filepaths):
    """Exhaustively removes files in an iterable of file paths.

    Args:
        filepaths (iter[(str)]): An iterable of file paths to be removed

    Returns:
        (None)
    """
    # Check if filepaths in an iterable container.
    if not isinstance(filepaths, (dict, list, set, tuple)):
        filepaths = [filepaths]
    for file in filepaths:
        try:
            os.remove(file)
        except FileNotFoundError:
            pass
