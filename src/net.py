#!/usr/bin/env python3

from collections import defaultdict
from app import *
from request import *
from horlogelogique import *
from horlogevectorielle import *


class Net(App):
    def __init__(self, parameters=None, appname="NET"):
        # forcing certain parameters
        mandatory_parameters = ["ident", "nsite"]
        # super constructor
        super().__init__(parameters=parameters, appname=appname,
                         mandatory_params=mandatory_parameters)

        # help not having to (int) every time
        self.parameters["ident"] = int(self.parameters["ident"])
        self.parameters["nsite"] = int(self.parameters["nsite"])

        # clock
        self.clk = Horloge(0)
        # construction de l'horloge vectorielle
        self.vectclk = HorlogeVect(size = self.parameters["nsite"], index = self.parameters["ident"])

        # var for snapshot
        self.init = False
        self.snap = False
        self.snapStates = []
        self.nbEtatAttendu = self.parameters["nsite"]

        # ack tab
        self.tab = [(NETStatus.LIBERATION, 0)
                    for k in range(self.parameters["nsite"])]

        self.SC = False

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
            # Action interne : incrémentatation horloge vect
            self.vectclk.incr()

            # if one of the required field is not present, ignore the message
            required_fields = ["rqsttype"]
            for e in required_fields:
                if e not in content:
                    printerr("[{}] missing field '{}' in msg from [{}]".format(
                        self.__appname__(), e, msg["src"]))
                    return

            request = BASStatusFromStr(content["rqsttype"])

            # Critical section request
            if request == BASStatus.DEMANDESC:
                self.BASDemandeSc()
            # Critical section usage ended
            elif request == BASStatus.FINSC:
                required_fields = ["account1", "account2", "amount"]
                for e in required_fields:
                    if e not in content:
                        printerr("[{}] missing field '{}' in msg from [{}]".format(
                            self.__appname__(), e, msg["src"]))
                        return
                self.BASFinSc(account1 = int(content["account1"]), account2 = int(
                    content["account2"]), amount = int(content["amount"]))
            # Snapshot request
            elif request == BASStatus.SNAPSHOT:
                required_fields = ["data"]
                for e in required_fields:
                    if e not in content:
                        printerr("[{}] missing field '{}' in msg from [{}]".format(
                            self.__appname__(), e, msg["src"]))
                        return
                self.BASSnap(content["data"])
            # Snapshot answer
            elif request == BASStatus.ETAT:
                required_fields = ["data"]
                for e in required_fields:
                    if e not in content:
                        printerr("[{}] missing field '{}' in msg from [{}]".format(
                            self.__appname__(), e, msg["src"]))
                        return
                self.BASEtat(data = content["data"])
            # Anything
            else:
                printerr("[{}] received msg seem to have an incorrect request type from [{}]".format(
                    self.__appname__(), msg["src"]))
            pass
        # msg is from NET
        elif msg["src"] == "NET":
            # let's retreive the required field
            # if one of the required field is not present, ignore the message
            required_fields = ["rqsttype", "clk", "ident", "vectclk"]
            for e in required_fields:
                if e not in content:
                    printerr("[{}] missing field '{}' in msg from [{}]".format(
                        self.__appname__(), e, msg["src"]))
                    return

            # we need the foreing request type
            request = NETStatusFromStr(content["rqsttype"])
            clk = Horloge(int(content["clk"]))
            ident = int(content["ident"])
            # construction de l'horloge à partir d'un string
            vectclk = HorlogeVect(index = self.parameters["ident"], _str = content["vectclk"])
            # incrementation de l'horloge avec la foreign
            self.vectclk.incr(vectclk)

            # now lets act depending on the type of request
            if request == NETStatus.REQUETE:
                self.NETRequete(h_clock=clk, ident=ident)
            elif request == NETStatus.LIBERATION:
                required_fields = ["account1", "account2", "amount"]
                for e in required_fields:
                    if e not in content:
                        printerr("[{}] missing field '{}' in msg from [{}] for {}".format(
                            self.__appname__(), e, msg["src"], request))
                        return
                self.NETLiberation(account1 = int(content["account1"]), account2 = int(
                    content["account2"]), amount = int(content["amount"]), h_clock=clk, ident=ident)
            elif request == NETStatus.ACCUSE:
                # check who the message is adressed to
                if "ackto" in content:
                    ackto = int(content["ackto"])
                    # if it's for us, we treat it, else we ignore
                    if ackto == self.parameters["ident"]:
                        self.NETAccuse(h_clock = clk, ident = ident)
            elif request == NETStatus.SNAPSHOT:
                if not self.snap:
                    self.NETSnap()
            elif request == NETStatus.ETAT:
                if self.init:
                    required_fields = ["data"]
                    for e in required_fields:
                        if e not in content:
                            printerr("[{}] missing field '{}' in msg from [{}] for {}".format(
                                self.__appname__(), e, msg["src"], request))
                            return
                    self.NETEtat(ident = ident, h_vectclk = vectclk, data = content["data"])
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
        # incrémentation horloge
        self.vectclk.incr()
        # envoyer([requête] h_i) à tous les autres sites
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"], "rqsttype": NETStatus.REQUETE,
                      "vectclk" : self.vectclk})
        self.send(msg=msg, who="NET")

    def BASFinSc(self, account1: int = None, account2: int = None, amount: int = None) -> None:
        if account1 == None or account2 == None or amount == None:
            printerr("[{}] BASFinSC() : one of args is None".format(self.__appname__()))
            return
        # h_i <- h_i + 1
        self.clk.incr()
        # tab_i[i] <- (requête, h_i)
        self.tab[self.parameters["ident"]] = (
            NETStatus.LIBERATION, self.clk.val())
        # incrémentation horloge
        self.vectclk.incr()
        self.SC = False
        # envoyer([requête] h_i) à tous les autres sites
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.LIBERATION, 
                               "account1": account1, 
                               "account2": account2, 
                               "amount": amount,
                               "vectclk": self.vectclk})
        self.send(msg=msg, who="NET")

    def BASSnap(self, data = None):
        if data == None:
            printerr("[{}] None data".format(self.__appname__()))
            return

        # incrémentation horloge
        self.vectclk.incr()

        # initiator
        self.init = True
        # turns red
        self.snap = True
        # waiting one less site
        self.nbEtatAttendu -= 1
        self.snapStates = [{"ident" : self.parameters["ident"], "clk" : str(self.vectclk), "data" : data}]

        # send SNAP to every neighbour
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.SNAPSHOT,
                               "vectclk": self.vectclk})

        self.send(msg = msg, who = "NET")

    def BASEtat(self, data = None):
        if data == None:
            printerr("[{}] None data".format(self.__appname__()))
            return
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.ETAT,
                               "vectclk": self.vectclk,
                               "data" : data})
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

        # incrémentation horloge
        self.vectclk.incr()

        # envoyer ([accusé] h_i) à S_j
        msg = Message(_values={"clk": self.clk.val(),
                      "ident": self.parameters["ident"],
                               "rqsttype": NETStatus.ACCUSE,
                               "ackto": ident,
                               "vectclk": self.vectclk})
        self.send(msg=msg, who="NET")
        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
        self.checkSC()

    def NETLiberation(self,account1: int = None, account2: int = None, amount: int = None,  h_clock: Horloge = None, ident: int = None) -> None:
        if h_clock == None:
            printerr("[{}] None clock".format(self.__appname__()))
            return
        if ident == None:
            printerr("[{}] None ident".format(self.__appname__()))
            return
        if account1 == None or account2 == None or amount == None:
            printerr("[{}] NETLiberation() : one of args is None".format(self.__appname__()))
        # h_i <- max(h_i, h) + 1
        self.clk.incr(h_clock)
        # tab_i[j] <- (libération, h)
        self.tab[ident] = (NETStatus.LIBERATION, h_clock.val())

        # avant de vérifier si il a accès a la SC, on met a jour le BAS avec les données de la dernière modif
        basmsg = Message(_values={"rqsttype": BASStatus.UPDATE,
                         "account1": account1, "account2": account2, "amount": amount})
        self.send(msg=basmsg, who="BAS")

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

    def NETSnap(self):
        # on passe en rouge
        self.snap = True
        # on demande une snapshot a BAS
        msg = Message(_values={"rqsttype": BASStatus.ETAT})
        self.send(msg=msg, who="BAS")

    def NETEtat(self, ident = None, data = None, h_vectclk = None):
        if data == None:
            printerr("[{}] None data".format(self.__appname__()))
            return
        if h_vectclk == None:
            printerr("[{}] None vectorial clock".format(self.__appname__()))
            return
        if ident == None:
            printerr("[{}] None ident".format(self.__appname__()))
            return

        printerr("[{}] Received data from NET for snapshot".format(self.__appname__()))
        self.nbEtatAttendu -= 1
        self.snapStates.append({"ident" : ident, "clk" : str(h_vectclk), "data ": data})

        # if we received every states
        if self.nbEtatAttendu == 0:
            printerr("[{}] Received every data for snapshot".format(self.__appname__()))
            printerr("[{}] Now sending everything to BAS".format(self.__appname__()))

            msg = Message(_values = {"rqsttype" : BASStatus.SNAPSHOT,
            "data" : self.snapStates})

            self.send(msg = msg, who = "BAS")
            

    def checkSC(self) -> None:
        # si tab_i[i].type == requête
        if self.tab[self.parameters["ident"]][0] == NETStatus.REQUETE:
            update = True
            # et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
            for k in range(self.parameters["nsite"]):
                if k != self.parameters["ident"]:

                    ei = self.tab[self.parameters["ident"]]
                    ek = self.tab[k]

                    printerr("i : {} k : {} | ei : {} ek : {}".format(self.parameters["ident"],k,ei,ek))

                    # not (<_2)
                    if not (ei[1] < ek[1] or (ei[1] == ek[1] and self.parameters["ident"] < k)):
                        update = False
                        break
            if update and not self.SC:
                printerr("VASY MON GRAND {}".format(self.parameters["ident"]))
                self.SC = True
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
