#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg


class WHEMessage(apg.msg.Message):
    """Application-specific message treatment"""
    def __init__(self, text, app):
        super().__init__(text, app)
    
        
    
            
 
class WHEApp(apg.Application):
    def __init__(self):
        default_options_values={"default-msg":"Hello World","appname":"WHE"}
        super().__init__(default_options_values)
        self.mandatory_parameters += [] # No mandatory parameter for this app
        self.msg = self.params["default-msg"]
        self.destination_app=self.APP()
        self.destination_zone=self.com.hst_air()
        if self.check_mandatory_parameters():
            self.config_gui()
            self.end_initialisation()
    def receive(self, pld, src, dst, where):
        if self.started  and self.check_mandatory_parameters():
            self.vrb("{}.rcv(pld={}, src={}, dst={}, where={})".format(self.APP(),pld, src, dst, where), 6)
            super().receive(pld, src=src, dst=dst, where=where)
        else:
            self.vrb_dispwarning("Application {} not started".format(self.APP()))
    def send_button(self, graphic_msg=None, graphic_who=None,graphic_where=None):
        """ When send button on app area is pushed """
        self.vrb("send_button(graphic_msg={})".format(graphic_msg),6)
        if graphic_msg != None:
            self.msg=graphic_msg.get()
        if graphic_who != None:
            self.destination_app = graphic_who.get()
        if graphic_where != None:
            self.destination_zone = graphic_where.get()
        self.snd(self.msg, who=self.destination_app, where=self.destination_zone)
    def config_gui(self):
        ## Interface
        self.gui.tk_instr("""
self.app_zone = tk.LabelFrame(self.root, text="{}")
self.var_msg_send = tk.StringVar()
self.var_msg_send.set("{}")
self.msg = tk.Entry(self.app_zone, width=32, textvariable = self.var_msg_send)
self.msg.pack(side="left")
self.var_who_send = tk.StringVar()
self.var_who_send.set("{}")
self.who = tk.Entry(self.app_zone, width=10, textvariable = self.var_who_send)
self.who.pack(side="left")
self.var_where_send = tk.StringVar()
self.var_where_send.set("{}")
self.where = tk.Entry(self.app_zone, width=10, textvariable = self.var_where_send)
self.where.pack(side="left")
self.sending_button = tk.Button(self.app_zone, text="Send", command=partial(self.app().send_button,self.var_msg_send, self.var_who_send, self.var_where_send), activebackground="red", foreground="red", width=10)
self.sending_button.pack(side="right")
self.app_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format(self.APP(),self.msg, self.destination_app, self.destination_zone)) # Graphic interface (interpreted if no option notk)

app = WHEApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")

