import argparse
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

import ProxyStubGenerator.Log as Log

NAME = "ConfigCompare"
VERBOSE = False
SHOW_WARNINGS = True
DOC_ISSUES = False

log = Log.Log(NAME, VERBOSE, SHOW_WARNINGS, DOC_ISSUES)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description='JSON Config Compare',
        formatter_class=argparse.RawTextHelpFormatter)

    argparser.add_argument("json1",
                           metavar="FilePath",
                           action="store",
                           type=str,
                           help="Full Path of Json File 1")

    argparser.add_argument("json2",
                           metavar="FilePath",
                           action="store",
                           type=str,
                           help="Full Path of Json File 2")

    argparser.add_argument("-i",
                           "--ignoreorder",
                           action="store_true",
                           help='Ignore order of items')

    args = argparser.parse_args(sys.argv[1:])

    if not os.path.exists(args.json1) or not os.path.exists(args.json2):
        log.Error("Error: Config File not found\n")
        sys.exit(2)

    with open(args.json1) as json_file_1:
        json1 = ordered(json.load(json_file_1)) if args.ignoreorder else json.load(json_file_1)

    with open(args.json2) as json_file_2:
        json2 = ordered(json.load(json_file_2)) if args.ignoreorder else json.load(json_file_2)

    if json1 != json2:
        log.Error(f"JSON Input files are not identical")
        sys.exit(1)
