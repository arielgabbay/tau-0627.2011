import argparse
import sys

from utilities import UTILITIES


def parse_args():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(help="The utility to run (run --help with the utility for more details on each utility", dest="utility")
    for util in UTILITIES:
        p = sub.add_parser(util.name, description=util.description)
        util.add_args(p)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.utility is None:
        print("No utility chosen! Run with --help for a list of utilities.", file=sys.stderr)
        return
    util = [u for u in UTILITIES if u.name == args.utility][0]
    util.run(args)


if __name__ == "__main__":
    main()

