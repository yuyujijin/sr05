#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg

#Global variables
srcapp="appnet"

class NETMessage(apg.msg.Message):
    """Application-specific message treatment"""
    def __init__(self, text, app):
        super().__init__(text, app)
        self.fields += [srcapp]
        self.parse_text(text)
    def is_local(self):
        return not srcapp in self.content
    
    
        
    
            
 
class NETApp(apg.Application):
    def __init__(self):
        #default_options_values={"appname":"NET"}
        default_options_values={'whatwho':True,"appname":"NET"}
        super().__init__(default_options_values)
        self.mandatory_parameters += [] # No mandatory parameter for this app
        #self.destination_app=self.APP()
        #self.destination_zone=self.com.hst_air()
        self.received_message=""
        self.sent_message=""
        if self.check_mandatory_parameters():
            self.config_gui()
            self.end_initialisation()
    def receive(self, pld, src, dst, where):
        """When a message is received """
        if self.started  and self.check_mandatory_parameters():
            self.vrb("{}.rcv(pld={}, src={}, dst={}, where={})".format(self.APP(),pld, src, dst, where), 6)
            super().receive(pld, src=src, dst=dst, where=where) # Useful for logs management, mostly
            self.received_message=NETMessage(pld,self)
            if self.received_message.is_local() and src != self.APP():
                self.gui.tk_instr("""self.received_msg.config(text="Received from {} : {}")""".format(src,self.received_message))
                self.received_message.content[srcapp] = src 
                self.snd("{}".format(self.received_message), who=self.APP(), where=self.com.hst_air())
                self.gui.tk_instr('self.transmitted_msg.config(text="Message transmitted to {} : {}")'.format(self.APP(),self.received_message))
            elif not self.received_message.is_local() and src == self.APP():
                self.gui.tk_instr("""self.received_msg.config(text="Received from {} : {}")""".format(self.APP(),self.received_message))
                destination_app = self.received_message.content.pop(srcapp, None)
                if destination_app != None:
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

