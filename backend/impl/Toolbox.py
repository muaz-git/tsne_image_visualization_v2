import sys
import os


def get_file_names(folder, file_ending):

    # get all file paths
    paths = []
    for root, dirs, files in os.walk(folder):
        for path in files:
            if path.endswith(file_ending):
                paths.append(path)

    return paths
