import argparse
import os
import sys


def readlines():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path')

    args = parser.parse_args()
    path = args.input_file_path

    if not os.path.isfile(path):
        print("Input file %s doesn't exist or is a directory!" % path, file=sys.stderr)
        sys.exit(1)

    with open(args.input_file_path) as f:
        return map(lambda x: x.strip(), f.readlines())
