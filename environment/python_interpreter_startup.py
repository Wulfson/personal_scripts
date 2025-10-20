# Script for use with PYTHONSTARTUP env variable

import importlib
import json
import readline
import sys

from base64 import b64decode
from contextlib import contextmanager
from enum import Enum
from zlib import decompress


#########################
# General settings

# Set interpreter prompts
# The \001 and \002 fix history scrollback; see https://stackoverflow.com/questions/9468435/how-to-fix-column-calculation-in-python-readline-if-using-color-prompt
sys.ps1 = "\001\033[0;32m\002>> \001\033[0m\002"
sys.ps2 = "\001\033[0;34m\002.. \001\033[0m\002"

# Make it easier to copy & paste JSON blobs
null = None
true = True
false = False


#########################
# Output tools

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

    def __str__(self):
        return self.value

    def __call__(self, *messages):
        print(
            "{color_sequence}{message}{reset_sequence}".format(
                color_sequence=self.value,
                message="\n".join(map(str, messages)),
                reset_sequence=Printer.reset.value,
            ),
            file=sys.stderr,
        )

    @classmethod
    def custom(cls, *messages):
        for msg in messages:
            cls.default(msg.format(**Printer._member_map_))


def jdump(obj, print_out=True):
    out = json.dumps(obj, indent=4, default=str, sort_keys=True)
    if print_out:
        Printer.blue(out)
    else:
        return out


#########################
# Common tools

def history(max_lines=80):
    history_length = readline.get_current_history_length()

    start_line = 1
    if max_lines > 0 and history_length > max_lines:
        start_line = history_length - max_lines

    Printer.blue(*[str(readline.get_history_item(i + start_line)) for i in range(history_length - start_line)])


def reload_module(name):
    importlib.reload(sys.modules[name])
    Printer.magenta("Reloaded " + name)


#########################
# postgres tools

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor


    db_creds = {"host": "localhost", "dbname": "devops", "user": "devops", "password": None, "port": 5432}


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
except Exception:
    Printer.yellow("psycopg2 is not available")


try:
    import boto3
except Exception:
    Printer.yellow("boto3 is not available")


#########################
# Application tools

def unraw(inp):
    try:
        ret = json.loads(decompress(b64decode(inp)))
        Printer.blue("JSON loaded")
    except Exception:
        ret = decompress(b64decode(inp))
        Printer.yellow("Not a JSON object")

    return ret

try:
    import django
    django.setup()

    from django.db import connections
    from django.conf import settings
    from django import db

    import django.db.backends.base.base
    import django.db.backends.mysql.base
    from django.db.utils import OperationalError


    # Monkey-patch the Django methods to handle reconnects on certain OperationalErrors (timeout, db has gone away)
    _original_cursor = django.db.backends.base.base.BaseDatabaseWrapper.cursor
    _original_execute = django.db.backends.mysql.base.CursorWrapper.execute

    # 2006: "MySQL server has gone away"
    # 2013: "Lost connection to MySQL server during query"
    # 4031: "The client was disconnected by the server because of inactivity"
    _db_error_list = (2006, 2013, 4031)


    def _cursor_with_reconnect(self, *args, **kwargs):
        try:
            return _original_cursor(self, *args, **kwargs)
        except OperationalError as ex:
            code = getattr(ex, "args", [None])[0]
            if code in _db_error_list:
                Printer.yellow("Attempting to reconnect to the database due to OperationalError: {}".format(ex))
                self.close()
                return _original_cursor(self, *args, **kwargs)
            raise


    def _execute_with_reconnect(self, sql, params=None):
        try:
            return _original_execute(self, sql, params)
        except OperationalError as ex:
            code = getattr(ex, "args", [None])[0]
            if code in _db_error_list:
                self.db.close()
                with self.db.cursor() as new_cursor:
                    return new_cursor.execute(sql, params)
            raise


    django_loaded = True
    django.db.backends.base.base.BaseDatabaseWrapper.cursor = _cursor_with_reconnect
    django.db.backends.mysql.base.CursorWrapper.execute = _execute_with_reconnect


    def kick_db():
        """
        Conditionally close all database connections.
        Useful when you know the database is down or has been restarted.
        """
        Printer.yellow("Testing all database connections...")
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()

except Exception:
    django_loaded = False
    Printer.yellow("django is not available")

if django_loaded:
    try:
        from personal_tools import ws
    except Exception:
        Printer.yellow("personal_tools.ws is not available")

    try:
        from tests_functional import setup_package
        setup_package()
    except Exception:
        Printer.yellow("functional test harness is not available")

Printer.cyan("Interpreter tools configured")
