#!/usr/bin/python3
import os
import sys

from requests import request
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
from request import *
import horlogelogique as hlg

#Global variables
srcapp="appnet"

class NETMessage(apg.msg.Message):
    """Application-specific message treatment"""
    def __init__(self, text, app):
        super().__init__(text, app)
        self.fields += [srcapp, "nsite"]
        self.parse_text(text)

    def is_local(self):
        return not srcapp in self.content
    

class NETApp(apg.Application):
    def __init__(self):
        #default_options_values={"appname":"NET"}
        default_options_values={'whatwho':True,"appname":"NET"}
        super().__init__(default_options_values)

        # nmax est nécessaire pour la file : on doit connaître le nombre de site (numéro de 0 à nmax - 1)
        self.mandatory_parameters += ["nmax"]
        # nsite est nécessaire pour l'estempillage : on doit avoir un numéro de site
        self.mandatory_parameters += ["nsite"]

        #self.destination_app=self.APP()
        #self.destination_zone=self.com.hst_air()
        self.received_message=""
        self.sent_message=""

        # Ajout de l'horloge
        # h_i <- 0
        self.clk = hlg.Horloge()

        if self.check_mandatory_parameters():
            # Ajout du tableau des états
            # Tab_i[k] <- (libération, 0) pour tout k € {1,...N}
            self.tab = [(NETStatus.LIBERATION, 0) for k in range(int(self.params["nmax"]))]

            self.config_gui()
            self.end_initialisation()


    # Reception d'un message
    # Utilise l'algo de file, cf. ce dernier
    def receive(self, pld, src, dst, where):
        """When a message is received """
        if self.started  and self.check_mandatory_parameters():
            self.vrb("{}.rcv(pld={}, src={}, dst={}, where={})".format(self.APP(),pld, src, dst, where), 6)
            super().receive(pld, src=src, dst=dst, where=where) # Useful for logs management, mostly

            self.received_message=NETMessage(pld,self)

            # Renvoyer les messages sur le réseau NET
            if self.received_message.is_local() and src != self.APP():
                self.gui.tk_instr("""self.received_msg.config(text="Received from {} : {}")""".format(src,self.received_message))

                self.received_message.content[srcapp] = src 
                self.received_message.content["nsite"] = self.params["nsite"]

                # Ajout de l'horloge aux messages sur le réseau
                self.received_message.fields += ["clk"]
                self.received_message.content["clk"] = str(self.clk)

                requeststatus = BASStatusFromStr(self.received_message.content["rqsttype"])

                # h_i <- h_i + 1
                self.clk.incr()

                # Selon la requête de BAS, on adapte
                # - Reception d'une demande de section critique de l'app. de base
                if requeststatus == BASStatus.DEMANDESC:
                    # tab_i[i] <- (requête, h_i)
                    self.tab[int(self.params["nsite"])] = (NETStatus.REQUETE, self.clk)
                    # envoyer([requête] h_i) à tous les autres sites
                    self.received_message.content["rqsttype"] = NETStatus.REQUETE

                # - Reception fin de section critique de l'app. de base
                elif requeststatus == BASStatus.FINSC:
                    # tab_i[i] <- (requête, h_i)
                    self.tab[int(self.params["nsite"])] = (NETStatus.LIBERATION, self.clk)
                    # envoyer([libération] h_i) à tous les autres sites
                    self.received_message.content["rqsttype"] = NETStatus.LIBERATION

                self.snd("{}".format(self.received_message), who=self.APP(), where=self.com.hst_air())
                self.gui.tk_instr('self.transmitted_msg.config(text="Message transmitted to {} : {}")'.format(self.APP(),self.received_message))

            # Renvoyer les messages a BAS
            elif not self.received_message.is_local() and src == self.APP():
                self.gui.tk_instr("""self.received_msg.config(text="Received from {} : {}")""".format(self.APP(),self.received_message))
                destination_app = self.received_message.content.pop(srcapp, None)

                if destination_app != None:

                    requeststatus = NETStatusFromStr(self.received_message.content["rqsttype"])

                    h_clk = hlg.Horloge(int(self.received_message.content["clk"]))
                    j = int(self.received_message.content["nsite"])
                    
                    # Selon la requête de NET, on adapte
                    # - Reception d'un message de type requête
                    if requeststatus == NETStatus.REQUETE:
                        # h_i <- max(h_i, h) + 1
                        self.clk.incr(h_clk)
                        # tab_i[j] <- (requête, h)
                        self.tab[j] = (NETStatus.REQUETE, self.clk.val())
                        # envoyer([accusé] h_i) à Sj
                        # TODO
                        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
                            # envoyer([débutSC]) à l'application de base
                            # TODO

                    # - Reception d'un message de type libération
                    elif requeststatus == NETStatus.LIBERATION:
                        # h_i <- max(h_i, h) + 1
                        self.clk.incr(h_clk)
                        # tab_i[j] <- (requête, h)
                        self.tab[j] = (NETStatus.LIBERATION, self.clk.val())
                        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
                            # envoyer([débutSC]) à l'application de base
                            # TODO

                    # - Reception d'un message de type accusé
                    elif requeststatus == NETStatus.ACCUSE:
                        # h_i <- max(h_i, h) + 1
                        self.clk.incr(h_clk)
                        # si tab_i[j].type != requête
                        if self.tab[j][0] != NETStatus.REQUETE:
                            # on n'écrase pas la dâte d'une requête par celle d'un accusé
                            # tab_i[j] <- (accusé, h)
                            self.tab[j] = (NETStatus.ACCUSE, self.clk.val())
                        # si tab_i[i].type == requête et (tab_i[i].date, i) <_2 (tab_i[k].date, k) pour tout k != i
                            # envoyer([débutSC]) à l'application de base
                            # TODO

                    self.snd("{}".format(self.received_message), who=destination_app, where=self.com.hst_lch())
                    self.gui.tk_instr('self.transmitted_msg.config(text="Message transmitted to {} : {}")'.format(destination_app, self.received_message))
                else:
                    self.vrb_dispwarning("No destination app")
            else:
                self.vrb_dispwarning("Unused message '{}' (probably syntax error) from {} {}".format(pld, src, where))
        else:
            self.vrb_dispwarning("Application {} not started".format(self.APP()))
    def config_gui(self):
        ## Interface
        self.gui.tk_instr("""
self.app_zone = tk.LabelFrame(self.root, text="{}")
self.received_msg = tk.Label(self.app_zone,text="{}")
self.transmitted_msg = tk.Label(self.app_zone,text="{}")
self.received_msg.pack(side="top")
self.transmitted_msg.pack(side="top")
self.app_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format(self.APP(),self.received_message, self.sent_message)) # Graphic interface (interpreted if no option notk)

app = NETApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")

