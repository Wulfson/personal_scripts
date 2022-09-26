"""
Common helpers for CLI tasks
"""

import json

from argparse import ArgumentTypeError
from enum import Enum
from os import path
from sys import stderr


class Printer(Enum):
    """
    A simple class to print colorized CLI messages without adding any external dependencies.
    Prints to stderr; just use print() if you want to send to stdout for piping purposes
    Usage: Printer.{color}('Message')
    Example: Printer.red('Everything is horrible! What have you done!?')
    """

    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    magenta = "\033[1;35m"
    cyan = "\033[1;36m"
    default = "\033[0m"
    reset = "\033[0m"

    def __call__(self, *messages):
        print(
            "{color_sequence}{message}{reset_sequence}".format(
                color_sequence=self.value,
                message="\n".join(map(str, messages)),
                reset_sequence=Printer.reset.value,
            ),
            file=stderr,
        )


def csv_list(val):
    """Sanitize & dedupe a comma separated list passed from the CLI"""
    tmp = map(str.strip, val.split(","))
    return list(dict.fromkeys(filter(None, tmp)))


def valid_path(val):
    """Sanitize & validate a path"""
    val = path.abspath(path.expanduser(val))
    if val and not path.exists(val):
        raise ArgumentTypeError("{0}Path does not exist: {1}{2}".format(
            Printer.red.value,
            val,
            Printer.reset.value,
        ))

    return val


def dir_path(val):
    """Validate that a path points to a directory"""
    val = valid_path(val)
    if not path.isdir(val):
        raise ArgumentTypeError("{0}Path does not refer to a directory: {1}{2}".format(
            Printer.red.value,
            val,
            Printer.reset.value,
        ))

    return val


def file_path(val):
    """Validate that a path points to a file"""
    val = valid_path(val)
    if not path.isfile(val):
        raise ArgumentTypeError("{0}Path does not refer to a file: {1}{2}".format(
            Printer.red.value,
            val,
            Printer.reset.value,
        ))

    return val


def debug(show, val):
    """Print val in debug color if show is True"""
    if not show:
        return

    if isinstance(val, (str, int)):
        output = val
    else:
        try:
            output = json.dumps(val, indent=4, sort_keys=True)
        except TypeError:
            output = json.dumps(vars(val), indent=4, sort_keys=True)

    Printer.blue(output)
