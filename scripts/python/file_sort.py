#!/usr/bin/env python3

import pathlib
import re
import shutil

from argparse import ArgumentParser, RawTextHelpFormatter
from os import path, walk
from textwrap import dedent

from cli_util import debug, dir_path, Printer


def arg_parser():
    """ Set up CLI argument parsing """
    parser = ArgumentParser(
        description=dedent(
            """
            Sorts sequences of files into folders, re-orders tags if included
            Requirements:
                Python 3.8+ is required
            """
        ),
        formatter_class=RawTextHelpFormatter,
        epilog="\n\n",
    )

    parser.add_argument(
        "--commit",
        action="store_true",
        help="Actually move files; will only dry-run unless this is supplied",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print debug output",
    )

    parser.add_argument(
        "--source",
        type=dir_path,
        required=True,
        help="Directory to scan for files in",
    )

    parser.add_argument(
        "--target",
        type=dir_path,
        required=True,
        help="Directory to move files to",
    )

    parser.add_argument(
        "--skip-tagless",
        action="store_true",
        help="Don't operate on tagless files",
    )

    args = parser.parse_args()

    args.filenames = next(walk(args.source), (None, None, []))[2]

    debug(args.debug, args)

    return args


def fix_name(args, name):
    tags = re.findall(r"\[([^\]]+)\]", name)

    if tags:
        base_name, extension = re.sub(r" ?\[[^\]]+\] ?", "", name).rsplit(".", 1)

        if base_name.endswith(")"):
            format_string = "{0}[{1}].{2}"
        else:
            format_string = "{0} [{1}].{2}"

        new_name = format_string.format(base_name, "][".join(tags), extension)
    else:
        if args.skip_tagless:
            return None
        new_name = name

    return new_name


def get_base_name(name):
    matches = re.match(r"^(\[[^\]]+\] )?(.+) - \d", name)
    if matches:
        return matches[2]


def move_file(args, source_file, new_dir, target_name):
    target_dir = path.join(args.target, new_dir)
    if not path.isdir(target_dir):
        Printer.magenta("Creating " + target_dir)
        if args.commit:
            pathlib.Path(target_dir).mkdir(parents=True, exist_ok=True)

    new_path = path.join(target_dir, target_name)

    debug(args.debug, "{0}\n => {1}".format(path.join(args.source, source_file), new_path))
    if args.commit:
        shutil.move(os.path.join(args.source, source_file), new_path)


def main(args):
    for name in args.filenames:
        Printer.cyan(name)
        if not args.commit:
            Printer.yellow("---DRY RUN---")

        new_name = fix_name(args, name)
        if not new_name:
            continue

        debug(args.debug, "New Name: " + new_name)

        base_name = get_base_name(new_name)
        if not base_name:
            continue

        debug(args.debug, "Base Name: " + base_name)

        move_file(args, name, base_name, new_name)


if __name__ == "__main__":
    main(arg_parser())
