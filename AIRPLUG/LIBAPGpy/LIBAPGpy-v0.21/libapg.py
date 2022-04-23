import asyncio
import sys
from time import sleep
import uvloop
from datetime import datetime
import os
import libapg_com as com
import libapg_svg as svg
import libapg_int as gui
import libapg_msg as msg
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())




def boolFromStr(text):
    """
    returns bool corresponding to text if text is "true" or "false" (case insensitive) or text if it isn’t
    """
    text=str(text)
    if text.lower() == "false":
        return False
    elif text.lower() == "true":
        return True
    else:
        return text
    

class Application:
    def __init__(self, default_options={}):
        ### Default options for all applications
        self.params={"appname":sys.argv[0][2:5],"verbose":"0", "notk":False, "debug":False, "mode":"term", "remote":False, "saving":False, "auto":"2", "ident":os.uname().nodename, "safemode": False, "what":True}
        ### Setting app-specific default options
        self.params.update(default_options)
        self.parse_options()
        self.update_apg_variables() 
        self.started = False
        self.mandatory_parameters = []
        self.loop = asyncio.get_event_loop()
        self.com=com.ComManager(self, self.variables['com_delim'])
        self.svg = svg.SvgManager(self)
        self.gui = gui.WindowManager(self)
        self.vrb("self : '{}'".format(self),5)
        self.debug("params : '{}'".format(self.params), 2)
        self.default_msg="Default APG message"
        self.vrb("starting gui",5)
        ## Airplug zone (top bar)
        self.gui.tk_instr("""
self.airplug_zone = tk.Frame(self.root)
self.start_button = tk.Button(self.airplug_zone, text="Start", command=self.app().start, activebackground="red", foreground="red", width=10)
self.start_button.pack(side="right")
""")
        self.gui.tk_instr('self.airplug_zone.pack(fill="both", expand="yes", side="top", pady=5)')
        ## Receive zone
        self.gui.tk_instr("""
self.receive_zone = tk.LabelFrame(self.root, text="Message reçu")
self.in_msg = tk.Label(self.receive_zone, text="")
self.in_msg.pack(side="left", expand="yes", fill="y", pady=2)
self.in_app = tk.Label(self.receive_zone, text="", width=4)
self.in_app.pack(side="left", expand="no", fill="y", pady=2)
self.in_zon = tk.Label(self.receive_zone, text="", width=4)
self.in_zon.pack(side="left", expand="no", fill="y", pady=2)
self.send_zone = tk.LabelFrame(self.root, text="Envoi")
self.var_msg_send = tk.StringVar()
self.var_msg_send.set("{}")
self.msg_send = tk.Entry(self.send_zone, width=32, textvariable = self.var_msg_send)
self.var_who_send = tk.StringVar()
self.var_who_send.set("{}")
self.who_send = tk.Entry(self.send_zone, width=4, textvariable = self.var_who_send)
self.var_where_send = tk.StringVar()
self.var_where_send.set("{}")
self.where_send = tk.Entry(self.send_zone, width=4, textvariable = self.var_where_send)
self.sending_button = tk.Button(self.send_zone, text="Send", command=partial(self.app().send_button,self.var_msg_send, self.var_who_send, self.var_where_send))
self.msg_send.pack(side="left")
self.who_send.pack(side="left")
self.where_send.pack(side="left")
self.sending_button.pack(side="left")
self.subscribe_zone = tk.LabelFrame(self.root, text="Message reçu")
self.var_sub_app = tk.StringVar()
self.var_sub_app.set("{}")
self.sub_app = tk.Entry(self.subscribe_zone, width=4, textvariable = self.var_sub_app)
self.var_sub_zon = tk.StringVar()
self.var_sub_zon.set("{}")
self.sub_zon = tk.Entry(self.subscribe_zone, width=4, textvariable = self.var_sub_zon)
self.subscribe_button=tk.Button(self.subscribe_zone, text="Subscribe", command=partial(self.app().com.subscribe_button,self.var_sub_app, self.var_sub_zon))
self.unsubscribe_button=tk.Button(self.subscribe_zone, text="Unsubscribe", command=partial(self.app().com.unsubscribe_button,self.var_sub_app, self.var_sub_zon))
self.sub_app.pack(side="left")
self.sub_zon.pack(side="left")
self.unsubscribe_button.pack(side="left")
self.subscribe_button.pack(side="left")

""".format(self.default_msg, self.APP(), self.com.hst_air(), self.APP(),self.com.hst_air()))
        return
    def end_initialisation(self):
        self.vrb("APP.end_initialisation()", 6)
        self.gui.tk_instr("""self.receive_zone.pack(fill="both", expand="yes", side="top", pady=5)
self.send_zone.pack(side="left")
self.subscribe_zone.pack(side="left")""")
        if self.params["auto"]:
            self.vrb("auto option detected, starting app in {} sec".format(self.params["auto"]),6)
            sleep(float(self.params["auto"]))
            self.start()
        self.gui.start()
    def update_apg_variables(self):
        csv_read=False # if global csv file used
        self.variables={}
        if csv_read:
            f=open('../apg_variables.csv')
            for line in f.read().split("\n"):
                if line.find(' ') >0:
                    self.variables[line.split(' ',1)[0]]=line.split(' ',1)[1]
        else:
            self.variables={'com_hst_lch': 'LCH', 'com_delim': '\x07', 'com_hst_air': 'AIR', 'msg_eq': '~', 'com_hst_all': 'ALL', 'msg_delim': '^'}
        self.vrb("apg variables : {}".format(self.variables),6)
    def check_mandatory_parameters(self):
        for param in self.mandatory_parameters:
            if not param in self.params:
                self.vrb_disperror("mandatory parameter '{}' missing, aborting".format(param))
                return False        
        return True
    def app(self):
        return self.params["appname"].lower()
    def APP(self):
        return self.params["appname"].upper()
    def add_default_arg_value(self, arg_name, value):
        if not arg_name in self.params:
            self.params[arg_name] = value
    def window(self):
        """
        returns the window root of tkinter (result of the tkinter.Tk())
        """
        return self.gui.root
    def parse_option(self, text):
        """
        prend en argument txt une option de la forme "--option-name=option-value" et retourne alors la liste ["option-name", "option-value"]
        Les options ne comportement pas de valeur seront évaluées à true
        """
        #Vérifier que l’option commence par "--"
        if text[0:2] != "--":
            return None
        #Supprimer le "--" du début
        text=text[2:]
        l=text.split("=", 1)
        if len(l)==1:
            l.append(True)
        else :
            l[1] = boolFromStr(l[1])
        return l
    def parse_options(self):
        """
        reçoit la chaîne de caractères de lancement du programme splittée argv et renvoie un dictionnaire des options d’appel
        le paramètre optionnel default est un dictionnaires des valeurs par défaut des options de l’application
        """
        self.vrb("APP.parse_options()", 6)
        argv=sys.argv.copy()
        self.vrb("argv='{}'".format(argv), 6)
        del argv[0]
        for arg in argv:
            l=self.parse_option(arg)
            if not l is None:
                self.params[l[0]] = l[1]
        if ("whatwhowhere" in self.params and self.params["whatwhowhere"]) or ("www" in self.params and self.params["www"]):
            self.header_mode="whatwhowhere"
            self.debug("option whatwhowhere found, using whatwhowhere mode", 5)
        elif ("whatwho" in self.params and self.params["whatwho"]) or ("ww" in self.params and self.params["ww"]):
            self.header_mode="whatwho"
            self.debug("option whatwho found, using whatwho mode", 5)
        elif "what" in self.params and self.params["what"]or ("w" in self.params and self.params["w"]):
            self.header_mode="what"
            self.debug("option what found, using what mode", 5)
        else:
            self.debug("No option what whatwho or whatwhowhere found, using what mode")
            self.header_mode="what"
    def start(self):
        if self.started:
            self.vrb_dispwarning("Application {} already activated".format(self.APP()))
        else:
            self.vrb("APP.start()", 6)
            self.vrb("Starting {} app".format(self.APP()), 6)
            self.started = True
    def stop(self):
        self.vrb("APP.stop()", 6)
        self.started = False
    def ready(self):
        return "stdout" in self.com.protocols
    ### Communications management
    #def rcv(self, txt, what, who , where):
        #self.vrb("APP.rcv(txt={}, what={}, who={}, where={})".format(txt, what, who, where), 6)
        #self.svg.save_line("stdin > {}  : {}".format(self.APP(),txt))
        #self.gui.tk_instr("self.in_msg.config(text = '{}')".format(txt))
        #if self.header_mode == "whatwho" or self.header_mode == "whatwhowhere":
            #self.gui.tk_instr("self.in_app.config(text = '{}')".format(what))
        #if self.header_mode == "whatwhowhere":
            #self.gui.tk_instr("self.in_zon.config(text = '{}')".format(where))
        #self.vrb("received message : '{}' from app {} on zone {}".format(txt, what, where), 3)
    def receive(self,pld,src,dst,where):
        self.vrb("APP.receive(pld={}, src={}, dst={}, where={})".format(pld, src, dst, where), 6)
        self.svg.save_line("stdin > {}  : {}".format(self.APP(),pld))
        self.gui.tk_instr("self.in_msg.config(text = '{}')".format(pld))
        if self.header_mode == "whatwho" or self.header_mode == "whatwhowhere":
            self.gui.tk_instr("self.in_app.config(text = '{}')".format(src))
        if self.header_mode == "whatwhowhere":
            self.gui.tk_instr("self.in_zon.config(text = '{}')".format(where))
    def snd(self, txt, saving = True, who=None, where=None, what=None):
        if what == None:
            what = self.APP()
        self.vrb("APP.snd({}, saving={}, what={}, who={}, where={})".format(txt, saving,what, who, where), 6)
        if self.com :
            self.com.send(txt, save = saving, what=what, who=who, where=where)
        else:
            self.vrb_disperror("No communication manager set")
    def send_button(self, gui_msg, gui_who, gui_where):
        """Only called if the gui send button is pushed"""
        if self.gui.notk():
            self.vrb_disperror("send_button function called without GUI, cancelling")
            return
        self.vrb("APP.send_button(gui_msg={}, gui_who={}, gui_where={})".format(gui_msg, gui_who, gui_where),6)
        self.snd(gui_msg.get(), who=gui_who.get(), where=gui_where.get())
    ### Verbose management
    def vrb(self, text, lvl):
        """
        Affiche text sur stderr si lvl est inférieur au niveau de verbosité global de l’application
        """
        if int(self.params["verbose"]) >= int(lvl):
            print("*** {} - {} {} - vrb{} *** ".format(datetime.now(), self.APP(), self.params["ident"], lvl)+str(text), file=sys.stderr)
    def vrb_disperror(self, text):
        """
        Affiche une erreur
        """
        self.vrb("error : " + text, 0)
    def vrb_dispwarning(self, text):
        """
        Affiche un warning
        """
        self.vrb("warn : "+text, 1)
    def debug(self,text, lvl=0):
        if bool(self.params["debug"]):
            self.vrb("debug : " + text, lvl)
    
        



