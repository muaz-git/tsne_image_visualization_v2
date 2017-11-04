import sys
import os

# CONSOLE STATUS PRINTING -----------------------------------------------------


# Prints a message on the console of type "act_value/total_value patches processed"
def print_status(act_value, total_value):

    out_str = '{}/{} patches processed\r'.format(act_value, total_value)
    sys.stdout.write(out_str + '\r')


def compute_histograms(patch_list, RGB=True):

    for patch in patch_list:
        cur_hist = patch.get_histogram(RGB)
        patch.tensor = cur_hist


def get_file_names(folder, file_ending):

    # get all file paths
    paths = []
    for root, dirs, files in os.walk(folder):
        for path in files:
            if path.endswith(file_ending):
                paths.append(path)

    return paths
