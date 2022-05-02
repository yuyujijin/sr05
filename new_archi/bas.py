from app import *
from request import *


class Bas(App):
    def __init__(self, parameters=None, appname="BAS"):
        # forcing certain parameters
        mandatory_parameters = []
        # super constructor
        super().__init__(parameters=parameters, appname=appname,
                         mandatory_params=mandatory_parameters)

    def receive(self, input: str = None) -> None:
        if not input:
            printerr("[{}] received empty message".format(self.__appname__()))
        # parse the input
        msg = self.parse(input)

        # TREATMENT

        # if the msg is not destined to us, skip
        if msg["dest"] != self.__appname__():
            return

        content = msg["content"].__values__()

        if "rqsttype" not in content:
            printerr("[{}] missing field 'rqsstype' in msg from [{}]".format(
                self.__appname__(), msg["src"]))
            return

        request = BASStatusFromStr(content["rqsttype"])

        if request == BASStatus.DEBUTSC:
            self.BASDebutSC()
            pass
        else:
            printerr("[{}] received msg seem to have an incorrect request type from [{}]".format(
                self.__appname__(), msg["src"]))

    def BASDemandeSC(self):
        pass

    def BASDebutSC(self):
        printerr("BAS now have access to SC")
        # do whatever it needs
        self.BASFinSC()

    def BASFinSC(self):
        msg = Message(_values={"rqsttype": BASStatus.FINSC})
        self.send(msg=msg, who="NET")


a = Bas(appname="BAS", parameters={"ident": "truc"})
m = Message(_values={"machin": "chouette", "truc": "muche",
            "rqsttype": "BASStatus.DEMANDESC"})

a.send(msg=m, who="NET")
