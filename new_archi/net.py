from collections import defaultdict
from app import *
from request import *
from horlogelogique import *


class Net(App):
    def __init__(self, parameters=None, appname="NET"):
        # forcing certain parameters
        mandatory_parameters = ["ident", "nsite"]
        # super constructor
        super().__init__(parameters=parameters, appname=appname,
                         mandatory_params=mandatory_parameters)

        # clock
        self.clk = Horloge(0)

        # help not having to (int) every time
        self.parameters["ident"] = int(self.parameters["ident"])
        self.parameters["nsite"] = int(self.parameters["nsite"])

        # ack tab
        self.tab = [(NETStatus.LIBERATION, 0)
                    for k in range(self.parameters["nsite"])]

    def receive(self, input: str = None) -> None:
        if not input:
            printerr("[{}] received empty message".format(self.__appname__()))
        # parse the input
        msg = self.parse(input)

        # TREATMENT

        # if the msg is not destined to us, ignore
        if msg["dest"] != self.__appname__():
            return

        # retrieve the content
        content = msg["content"].__values__()

        # msg is from BAS
        if msg["src"] == "BAS":
            # if one of the required field is not present, ignore the message
            required_fields = ["rqsttype"]
            for e in required_fields:
                if e not in content:
                    printerr("[{}] missing field '{}' in msg from [{}]".format(
                        self.__appname__(), e, msg["src"]))
                    return

            request = BASStatusFromStr(content["rqsttype"])

            if request == BASStatus.DEMANDESC:
                self.BASDemandeSc()
            elif request == BASStatus.FINSC:
                self.BASFinSc()
            else:
                printerr("[{}] received msg seem to have an incorrect request type from [{}]".format(
                    self.__appname__(), msg["src"]))
            pass
        # msg is from NET
        elif msg["src"] == "NET":
            # let's retreive the required field
            # if one of the required field is not present, ignore the message
            required_fields = ["rqsttype", "clk", "ident"]
            for e in required_fields:
                if e not in content:
                    printerr("[{}] missing field '{}' in msg from [{}]".format(
                        self.__appname__(), e, msg["src"]))
                    return

            # we need the foreing request type
            request = NETStatusFromStr(content["rqsttype"])
            clk = Horloge(int(content["clk"]))
            ident = int(content["ident"])

            # now lets act depending on the type of request
            if request == NETStatus.REQUETE:
                self.NETRequete(clk, ident)
            elif request == NETStatus.LIBERATION:
                self.NETLiberation(clk, ident)
            elif request == NETStatus.ACCUSE:
                # check who the message is adressed to
                if "ackto" in content:
                    ackto = int(content["ackto"])
                    # if it's for us, we treat it, else we ignore
                    if ackto == self.parameters["ident"]:
                        self.NETAccuse(clk, ident)
            else:
                printerr("[{}] received msg seem to have an incorrect request type from [{}]".format(
                    self.__appname__(), msg["src"]))
        # msg doesn't seem to be from anyone known, ignore
        else:
            pass

    def BASDemandeSc(self) -> None:
        # h_i <- h_i + 1
        self.clk.incr()
        # tab_i[i] <- (requête, h_i)
        self.tab[self.parameters["ident"]] = (
            NETStatus.REQUETE, self.clk.val())
        # envoyer([requête] h_i) à tous les autres sites
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.REQUETE})
        self.send(msg=msg, who="NET")

    def BASFinSc(self) -> None:
        # h_i <- h_i + 1
        self.clk.incr()
        # tab_i[i] <- (requête, h_i)
        self.tab[self.parameters["ident"]] = (
            NETStatus.LIBERATION, self.clk.val())
        # envoyer([requête] h_i) à tous les autres sites
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.LIBERATION})
        self.send(msg=msg, who="NET")

    def NETRequete(self, h_clock: Horloge = None, ident: int = None) -> None:
        if h_clock == None:
            printerr("[{}] None clock".format(self.__appname__()))
            return
        if ident == None:
            printerr("[{}] None ident".format(self.__appname__()))
            return
        # h_i <- max(h_i, h) + 1
        self.clk.incr(h_clock)
        # tab_i[j] <- (requête, h)
        self.tab[ident] = (NETStatus.REQUETE, h_clock.val())
        # envoyer ([accusé] h_i) à S_j
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.ACCUSE,
                               "ackto": ident})
        self.send(msg=msg, who="NET")
        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
        self.checkSC()

    def NETLiberation(self, h_clock: Horloge = None, ident: int = None) -> None:
        if h_clock == None:
            printerr("[{}] None clock".format(self.__appname__()))
            return
        if ident == None:
            printerr("[{}] None ident".format(self.__appname__()))
            return
        # h_i <- max(h_i, h) + 1
        self.clk.incr(h_clock)
        # tab_i[j] <- (libération, h)
        self.tab[ident] = (NETStatus.LIBERATION, h_clock.val())
        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
        self.checkSC()

    def NETAccuse(self, h_clock: Horloge = None, ident: int = None) -> None:
        if h_clock == None:
            printerr("[{}] None clock".format(self.__appname__()))
            return
        if ident == None:
            printerr("[{}] None ident".format(self.__appname__()))
            return
        # h_i <- max(h_i, h) + 1
        self.clk.incr(h_clock)
        # tab_i[j] <- (libération, h)
        if self.tab[ident][0] != NETStatus.REQUETE:
            self.tab[ident] = (NETStatus.ACCUSE, h_clock.val())
        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
        self.checkSC()

    def checkSC(self) -> None:
        # si tab_i[i].type == requête
        if self.tab[self.parameters["ident"]][0] == NETStatus.REQUETE:
            update = True
            # et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
            for k in range(self.parameters["nsite"]):
                if k != int(self.parameters["ident"]):

                    ei = self.tab[int(self.params["nsite"])]
                    ek = self.tab[k]

                    # not (<_2)
                    if not (ei[1] < ek[1] or (ei[1] == ek[1] and int(self.params["nsite"]) < k)):
                        update = False
                        break
            if update:
                msg = Message(_values={"rqsttype": BASStatus.DEBUTSC})
                self.send(msg=msg, who="BAS")


if __name__ == "__main__":
    # retreive the options
    d = defaultdict(list)
    for k, v in ((k.lstrip('-'), v) for k, v in (a.split('=') for a in sys.argv[1:])):
        d[k] = v

    # launch the app
    net = Net(parameters=d)
    net.start()
