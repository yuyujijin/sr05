#!/usr/bin/env python3

from cgitb import text
import random
from app import *
from request import *
from tkinter import *
from tkinter import ttk
import message as mg
from threading import Thread


class Bas(App):
    def __init__(self, parameters=None, appname="BAS"):
        # forcing certain parameters
        mandatory_parameters = []
        # super constructor
        super().__init__(parameters=parameters, appname=appname,
                         mandatory_params=mandatory_parameters)

        self.accounts = {i: 0 for i in range(100)}

        self.sc = False
        self.window = None
        self.lastrequest = None

    def __accounts__(self):
        return self.accounts

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
        elif request == BASStatus.UPDATE:
            # check if every fields is here
            required_fields = ["account1", "account2", "amount"]
            for e in required_fields:
                if e not in content:
                    printerr("[{}] missing field '{}' in msg from [{}] for {}".format(
                        self.__appname__(), e, msg["src"], request))
                    return
            self.BASUpdateSC(int(content["account1"]), int(
                content["account2"]), int(content["amount"]))
        else:
            printerr("[{}] received msg seem to have an incorrect request type from [{}]".format(
                self.__appname__(), msg["src"]))

    def BASDemandeSC(self, account1: int, account2: int, amount: int):
        if self.sc:
            return
        # do whatever it needs
        if account1 == account2:
            printerr("[{}] account ids must be different".format(
                self.__appname__()))
            return

        self.lastrequest = {"account1": int(account1),
                            "account2": int(account2), "amount": int(amount)}

        msg = mg.Message(_values={"rqsttype": BASStatus.DEMANDESC})
        self.send(msg=msg, who="NET")
    
    def BASUpdateSC(self, account1: int, account2: int, amount: int ):
        self.lastrequest = {"account1": int(account1),
                            "account2": int(account2), "amount": int(amount)}

        # update values
        self.updateValues()

    def BASDebutSC(self):
        self.sc = True
        printerr("[{}] now have access to SC".format(self.__appname__()))

        # update values
        self.updateValues()
        
        # then send end of SC
        self.BASFinSC()

    def BASFinSC(self):
        msg = mg.Message(_values={"rqsttype": BASStatus.FINSC, 
         "account1" : self.lastrequest["account1"],
         "account2" : self.lastrequest["account2"],
         "amount" : self.lastrequest["amount"]})
        self.send(msg=msg, who="NET")
        self.sc = False
        printerr("[{}] released acces to SC".format(self.__appname__()))

    def updateValues(self):
        # retrieve amounts
        self.accounts[self.lastrequest["account1"]
                      ] += self.lastrequest["amount"]
        self.accounts[self.lastrequest["account2"]
                      ] -= self.lastrequest["amount"]

        # then update the window
        if self.window:
            self.window.updateListe(
                self.lastrequest["account1"], self.accounts[self.lastrequest["account1"]])
            self.window.updateListe(
                self.lastrequest["account2"], self.accounts[self.lastrequest["account2"]])

class BasWindow:
    def __init__(self):
        # create root
        root = Tk()

        # create app
        self.app = Bas()
        # set the app
        self.app.window = self
        self.startBas()

        # create main window
        frm = ttk.Frame(root, padding=30)

        # labels
        Label(frm, text="Bank accounts").pack()

        # list the accounts
        self.liste = Listbox(frm)
        for k, v in self.app.__accounts__().items():
            self.liste.insert(k, "#{} : {}".format(k, v))
        self.liste.pack()

        iptframe = ttk.Frame(frm, padding=20, borderwidth=2, relief=GROOVE)

        # buttons
        # spinbox for user 1
        Label(iptframe, text="Account 1 : ").pack()
        self.spb1 = Spinbox(iptframe, values=list(
            self.app.__accounts__().keys()))
        self.spb1.pack()
        # spinbox for user 2
        Label(iptframe, text="Account 2 : ").pack()
        self.spb2 = Spinbox(iptframe, values=list(
            self.app.__accounts__().keys()))
        self.spb2.pack()
        # spinbox for ammount
        Label(iptframe, text="Amount : ").pack()
        var = StringVar(root)
        var.set("0")
        self.amount = Spinbox(iptframe, from_=-10000,
                              to=10000, textvariable=var)
        self.amount.pack()
        # button for sending
        Button(iptframe, text="Send", command=self.requestBas).pack()

        iptframe.pack()

        frm.pack()

        root.mainloop()

    def startBas(self) -> None:
        Thread(target=self.app.start).start()

    def requestBas(self) -> None:
        def work(): return self.app.BASDemandeSC(
            self.spb1.get(), self.spb2.get(), self.amount.get())
        Thread(target=work).start()

    def updateListe(self, account: int, amount: int) -> None:
        self.liste.delete(account)
        self.liste.insert(account, "#{} : {}".format(account, amount))


if __name__ == "__main__":
    Thread(target=BasWindow).start()
