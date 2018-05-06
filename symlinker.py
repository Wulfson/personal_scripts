"""
Script that's useful for setting up groups of symlinks in a different directory
Example usage:
ls ~/path/to/stuff/numbered-filename-base-* | python ~/symlinker.py "Symlink Name" 01
"""

extension = 'txt'  # Extension for the resultant symlink name
exclude_list = ['720x']  # If you need to exclude a certain type of string that may match the digits check, list it here
new_name_format = "{name} g{group_num}f{file_num}.{extension}"  # Format string for the full symlink name
group_dir_format = 'Group {group_num}'  # Name of subdirectory to put symlinks in; will be created if it doesn't exist
preformat_regex = r"g\d{2,}f(\d{2,})"  # If the input filename has a pattern you can match to find the sequence number, you can put it here

###########################################################################

import os
import re
import sys

name = sys.argv[1]
group_num = sys.argv[2]
if len(sys.argv) > 3:
    dryrun = True

re_preformat_check = re.compile(preformat_regex)
re_numbers = re.compile(r"\d{2,}")

directory = group_dir_format.format(group_num=group_num) + '/'

for line in sys.stdin:
    path = line.strip()
    filename = path.split('/')[-1]

    delims = {
        '_': 0,
        '-': 0,
        '.': 0,
    }

    for key, val in delims.items():
        delims[key] = filename.count(key)

    delim = max(delims, key=delims.get)
    parts = filename.split(delim)

    chosen = None
    for part in parts:
        clean = part.strip(' _').lower()

        match = re_preformat_check.match(clean)
        if match:
            chosen = match.group(1)

        if clean.isdigit():
            chosen = clean
            break

    if chosen is None:
        for part in parts:
            clean = part.strip(' _').lower()

            if clean in exclude_list:
                continue

            match = re_numbers.match(clean)
            if match:
                chosen = match.group(0)
                break

    new_name = new_name_format.format(
        name=name,
        group_num=group_num,
        file_num=chosen,
        extension=extension,
    )

    new_file = directory + new_name
    print(new_file)

    if not dryrun:
        if not os.path.isdir(directory):
            os.mkdir(directory)

        if not os.path.islink(new_name):
            os.symlink(path, new_file)
