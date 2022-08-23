# Script for use with PYTHONSTARTUP env variable

import importlib
import json
import readline
import sys

from contextlib import contextmanager
from enum import Enum


# Set interpreter prompts
# The \001 and \002 fix history scrollback; see https://stackoverflow.com/questions/9468435/how-to-fix-column-calculation-in-python-readline-if-using-color-prompt
sys.ps1 = "\001\033[0;32m\002>> \001\033[0m\002"
sys.ps2 = "\001\033[0;34m\002.. \001\033[0m\002"


class Printer(Enum):
    """
    A simple class to print colorized CLI messages without adding any external dependencies.
    Usage: Printer.{color}("Message")
    Example: Printer.red("Everything is horrible! What have you done!?")
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
            file=sys.stderr,
        )


try:
    import boto3
except Exception:
    Printer.yellow("boto3 is not available")

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception:
    Printer.yellow("psycopg2 is not available")


# Make it easier to copy & paste JSON blobs
null = None
true = True
false = False


def jdump(obj, print_out=True):
    out = json.dumps(obj, indent=4, default=str, sort_keys=True)
    if print_out:
        Printer.blue(out)
    else:
        return out


db_creds = {"host": "localhost", "dbname": "devops", "user": "devops-schema-user", "password": None, "port": 5432}


@contextmanager
def pg_connect(db_creds):
    conn = psycopg2.connect(**db_creds)
    yield conn.cursor(cursor_factory=RealDictCursor)
    conn.close()


def query(sql, data=None):
    res = None
    with pg_connect(db_creds) as curs:
        curs.execute(sql, data)
        return curs.fetchall()


def reload_module(name):
    importlib.reload(sys.modules[name])
    Printer.magenta("Reloaded " + name)


def history(max_lines=50):
    history_length = readline.get_current_history_length()

    start_line = 1
    if max_lines > 0 and history_length > max_lines:
        start_line = history_length - max_lines

    Printer.blue(*[str(readline.get_history_item(i + start_line)) for i in range(history_length - start_line)])


Printer.cyan("Interpreter tools configured")
