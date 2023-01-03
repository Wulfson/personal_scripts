#!/usr/bin/env python3

import json
import os.path
import re

from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter
from datetime import date
from enum import Enum
from textwrap import dedent
from time import sleep
from urllib.request import urlopen, Request


class Printer(Enum):
    """
    A simple class to print colorized CLI messages without adding any external dependencies.
    Usage: Printer.{color}('Message')
    Example: Printer.red('Everything is horrible! What have you done!?')
    """

    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    magenta = "\033[1;35m"
    cyan = "\033[1;36m"
    reset = "\033[0m"

    def __call__(self, *messages):
        print(
            "{color_sequence}{message}{reset_sequence}".format(
                color_sequence=self.value,
                message="\n".join(messages),
                reset_sequence=Printer.reset.value,
            )
        )


def arg_parser():
    """ Set up CLI argument parsing """
    parser = ArgumentParser(
        description=dedent(
            """
            Downloads certain files from a certain location
            Probably won't work for any other use-case
            """
        ),
        formatter_class=RawTextHelpFormatter,
        epilog="\n\n",
    )

    parser.add_argument(
        "-d",
        "--weekday",
        type=str.lower,
        choices=["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
        default=date.today().strftime("%A").lower(),
        help=dedent(
            """
            Choose the day of the week to download files for. Defaults to current day.
            """
        ).strip(),
    )

    parser.add_argument(
        "-s",
        "--settings-file",
        dest="settings_file",
        default="./file_fetch_settings.json",
        help=dedent(
            """
            Location of the settings file
            """
        ).strip(),
    )

    args = parser.parse_args()

    args.settings = read_file(args.settings_file)

    Printer.blue("Day set to {0}".format(args.weekday))

    return args


def read_file(filepath):
    with open(filepath, "r") as f:
        return json.loads(f.read())


def write_file(data, filepath, mode="w"):
    Printer.magenta("Writing file " + filepath)
    with open(filepath, mode) as f:
        f.write(data)


def get_page(url, pause=1.2, decode=True):
    if not url:
        return None

    sleep(pause)
    Printer.green("Retrieving {0}".format(url))

    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    with urlopen(Request(url, headers={"User-Agent": agent})) as resp:
        data = resp.read()
        if decode:
            return data.decode("utf-8")
        return data


def main(args):
    settings = args.settings
    weekday = args.weekday

    if not os.path.isfile(settings["tracking_file"]):
        write_file("{}", settings["tracking_file"])

    all_tracking = read_file(settings["tracking_file"])

    for curr_url in settings["url_list"][weekday]:
        if not curr_url:
            continue

        url_parts = curr_url.split("/")
        for i in range(0, len(url_parts)):
            tmp = url_parts.pop()
            if tmp:
                Printer.cyan(tmp)
                break

        tracking = all_tracking.get(curr_url)
        if not tracking:
            Printer.blue("No tracking for {0}".format(curr_url))
            html = get_page(curr_url)
            match = re.search(r"sid=\"(\d+)\"", html)
            if match:
                all_tracking[curr_url] = {
                    "url": settings["api_base"] + match[1],
                    "downloaded": [],
                }

                tracking = all_tracking[curr_url]
                write_file(json.dumps(all_tracking, indent=4), settings["tracking_file"])

            else:
                Printer.red("Can't find sid for " + curr_url)
                continue

        data = json.loads(get_page(tracking["url"]))["episode"]
        for file, link_data in data.items():
            tracking_num = link_data["episode"]
            if tracking_num in tracking["downloaded"]:
                Printer.yellow("Already got {0}".format(tracking_num))
                continue

            file_url = next((x[settings["file_link_label"]] for x in link_data["downloads"] if x["res"] == settings["res_value"]), None)
            page_out = get_page(file_url, 0.1, False)
            write_file(page_out, "{0}/{1}.{2}".format(settings["save_to"], file, settings["file_link_label"]), "wb")

            tracking["downloaded"].append(tracking_num)
            write_file(json.dumps(all_tracking, indent=4), settings["tracking_file"])


if __name__ == "__main__":
    main(arg_parser())
