from os import write
import sys
from output import *
from message import *


class App:
    def __init__(self, parameters: dict = None, appname: str = None, mandatory_params: list = []):
        # Default params
        self.parameters = {}

        # Updating with new params
        if parameters:
            self.parameters.update(parameters)

        for e in mandatory_params:
            if e not in self.parameters:
                printerr("{} is required to launch the app".format(e))
                exit()

        # cannot have a none appname
        if appname == None:
            printerr("cannot have a null appname")
            exit()
        self.appname = appname

        self.started = False

        return

    def __appname__(self) -> str:
        return self.appname

    def __delimiter__(self) -> str:
        return "/"

    def header(self, who: str = None) -> str:
        if not who:
            printerr("[{}] cannot have a null who value".format(
                self.__appname__()))
            return None
        return "{}{}{}{}".format(self.__delimiter__(), self.__appname__(), self.__delimiter__(), who)

    def send(self, msg: Message = None, who: str = None) -> None:
        if msg == None:
            printerr("[{}] cannot send a null message".format(
                self.__appname__()))
            return
        if who == None:
            printerr("[{}] cannot send a message with a null who value".format(
                self.__appname__()))
            return

        header = self.header(who=who)
        if not header:
            return

        sys.stdout.write("{}{}{}".format(header, self.__delimiter__(),
                                         msg.format()))

    def parse(self, input: str = None) -> dict:
        L = input.split(self.__delimiter__())[1:]
        # must have 3 fields
        if len(L) != 3:
            printerr("[{}] message fields length is not equal to 3 during parsing".format(
                self.__appname__()))
        return {"src": L[0], "dest": L[1], "content": Message(_msg=L[2])}

    def receive(self, input: str = None) -> None:
        raise NotImplementedError(
            "receive method must be implemented for child classes")

    def start(self) -> None:
        if not self.started:
            self.started = True

            # read indefinitely from stdin
            for line in sys.stdin:
                self.receive(line)
