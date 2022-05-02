from output import *


class Message:
    def __init__(self, _msg: str = None, _values: dict() = None):
        self.values = {}
        # Construct with a str
        if _msg:
            for e in _msg.split(self.__delimiter__())[1:]:
                k, v = e.split(self.__equal__())
                self.values[k] = v
        # Construct with a dict
        else:
            if not _values:
                printerr("cannot create a message with not value fields")
                return None
            self.values.update(_values)

    def __delimiter__(self):
        return "^"

    def __equal__(self):
        return "~"

    def __values__(self):
        return self.values

    # Returns the message with the given format
    def format(self) -> str:
        L = ["{}{}{}{}".format(self.__delimiter__(), k, self.__equal__(), v)
             for k, v in self.values.items()]
        return ''.join(L)
