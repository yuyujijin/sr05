import io
import sys
import datetime


def printout(msg: str = None, file: io.TextIOWrapper = sys.stdout) -> None:
    if msg == None:
        return
    print("[{}] {}".format(datetime.datetime.now(), msg), file=file)


def printerr(msg: str = None) -> None:
    printout(msg, sys.stderr)
