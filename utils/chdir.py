import os
from contextlib import contextmanager


@contextmanager
def chdir(new_dir):
    # save the original directory
    original_dir = os.getcwd()

    try:
        # change to the new directory
        os.chdir(new_dir)
        yield
    finally:
        # change back to the original directory
        os.chdir(original_dir)
