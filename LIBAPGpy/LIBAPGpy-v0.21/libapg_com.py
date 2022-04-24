import asyncio
import sys
class ComProtocol(asyncio.Protocol):
    def __init__(self, manager, names):
        self.manager = manager
        self.names=names
        for name in names:
            self.manager.protocols[name] = self 
        self.app().debug("protocol {} initialized, waiting for connection".format(names), 3)
    def app(self):
        return self.manager.app()
    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.app().debug('{} connecting to {} port {}'.format(self.names, self.address, self.address), 1)
    def eof_received(self):
        """
        Méthode appelée lorsque la communication est coupée par le partenaire de communication
        """
        self.app().vrb_disperror('received EOF')
        self.transport.close()
    def connection_lost(self, exc):
        """
        Méthode appelée lorsque la communication est perdue (utilisant un mécanisme de timeout)
        """
        self.app().vrb_disperror('server closed connection')
        self.transport.close()
    def send(self, text=None):
        """
        envoie le texte en paramètre au partenaire de communication
        """
        if text:
            self.app().debug("sending {}".format(text), 1)
            data=(str(text)+"\n").encode()            
            self.transport.write(data)
        else:
            self.app().dispwarning("No text to send")
    def data_received(self, data):
        text = data.decode().strip()
        for line in text.split("\n"):
            self.app().debug("Message received : '{}' on protocol {}".format(line, self.names), 1)
            self.manager.msg_received(self, text = line)
class ComManager:
    def __init__(self, app, header_delim, default_what = None, default_who=None, default_where=None):
        self.application = app 
        self.header_mode = self.app().header_mode
        self.header_delim = header_delim
        self.subscriptions={}
        self.subscribe(self.app().APP(),self.hst_air())
        
        ## Initializing non blocking communication pipes
        self.protocols = {}
        remote_option = self.app().params["remote"]
        if remote_option :
            address, port = remote_option.split(":",1)
            asyncio.ensure_future(self.app().loop.create_connection(lambda: ComProtocol(self, ["stdin", "stdout"]), host=addr, port=port))
        else:
            asyncio.ensure_future(self.app().loop.connect_write_pipe(lambda: ComProtocol(self, ["stdout"]), sys.stdout))
            asyncio.ensure_future(self.app().loop.connect_read_pipe(lambda: ComProtocol(self, ["stdin"]), sys.stdin))
        ## Defining default header fields
        if not default_what:
            self.default_what = str(self.app().APP())
        if not default_who:
            self.default_who = self.default_what
        if not default_where:
            self.default_where = self.hst_air()
        self.app().vrb("application : {}, protocols : {}".format(self.app(), self.protocols), 6)
    def hst_lch(self):
        #return self.app().variables['hst_lch']
        return "LCH"
    def hst_air(self):
        #return self.app().variables['hst_air']
        return "AIR"
    def hst_all(self):
        #return self.app().variables['hst_all']
        return "ALL"
    ## Gestion des envois
    def send(self, text=None, save = True, what=None, who=None, where=None, protocol_name="stdout"):
        """
        envoie le texte en paramètre au partenaire de communication
        """
        if text :
            if protocol_name in self.protocols:
                self.app().debug("sending {} in mode {}".format(text, self.header_mode), 5)
                header = self.generate_header(what, who, where)
                self.protocols[protocol_name].send("{}{}".format(header,text))
                if save :
                    self.app().svg.save_line("{} > {} : {}{}".format(self.app().APP(), protocol_name, header,text))
            else:
                self.app().vrb_disperror("No protocol named '{}'".format(protocol_name))
        else:    
            self.app().debug("No text to send, aborting sending", 1)

    def generate_header(self, what, who, where):
        if not what:
            what = self.default_what
        if not who:
            who = self.default_who
        if not where:
            where = self.default_where
        if self.header_mode == "whatwhowhere":
            return "{}{}{}{}{}{}{}".format(self.header_delim, what, self.header_delim, who, self.header_delim, where, self.header_delim)
        elif self.header_mode == "whatwho":
            return "{}{}{}{}{}".format(self.header_delim, what, self.header_delim, who, self.header_delim)
        elif self.header_mode == "what":
            return ""
        else:
            return ""
    ## Reception
    def msg_received(self, protocol, text):
        if text:
            what = who = where = None
            if self.header_mode == "whatwho" or self.header_mode == "whatwhowhere":
                if not text[0].isalpha():
                    header = text.split(text[0], 4)
                else:
                    header = ['',text]
                if len(header) > 2:
                    what = header[1]
                if len(header)>3:
                    who = header[2]
                if len(header) >4:
                    where = header[3]
                text = header[len(header) - 1]
            header = self.complete_header(what, who, where)
            if "stdin" in protocol.names:
                self.app().vrb("transmitting (if safe) to application {} txt '{}', from {}, to {} from zone {}".format(self.app(), text, header["what"], header["who"], header["where"]), 6)
                safe_message = False
                if self.header_mode == "what":
                    safe_message = True
                    self.app().vrb("Every message is accepted in what mode",6)
                elif who == self.app().APP():
                    if self.is_subscribed(what,where):
                        safe_message = True
                        self.app().vrb("Message designed for this app from a subscribed app",6)
                    if where == self.hst_lch() or self.header_mode == "whatwho":
                        safe_message = True
                        self.app().vrb("Message designed for this app from a local app",6)
                elif who == self.hst_all() and self.is_subscribed(what,where):
                    safe_message = True
                    self.app().vrb("Message designed for all apps from a subscribed app",6)
                if self.header_mode == "whatwho" and (not self.valid_appname(header["what"]) or not self.valid_appname(header["who"])):
                    self.app().vrb_disperror("Invalid app or zone name what='{}', who='{}'".format(header["what"], header["who"]))
                    return
                elif self.header_mode == "whatwhowhere" and (not self.valid_appname(header["what"]) or not self.valid_appname(header["who"]) or not self.valid_zone(header["where"])):
                    self.app().vrb_disperror("Invalid app or zone name what='{}', who='{}',where='{}'".format(header["what"], header["who"], header["where"]))
                    return
                if safe_message :
                    # self.app().rcv(text, header["what"], header["who"], header["where"])
                    self.app().receive(text, header["what"], header["who"], header["where"])
                else:
                    self.app().debug("Unsafe message",2)
            else:
                self.app().vrb("protocol is {} called {}, not stdin".format(protocol, protocol.names),4)
                self.app().vrb("""
                    protocols : {}
                    protocols[stdin].names : {}
                    protocols[stdout].names: {}
                    """.format(self.protocols, self.protocols["stdin"].names, self.protocols["stdout"].names), 6)
    def complete_header(self, what, who, where):
        self.app().vrb("APP.complete_header(what={}, who={}, where={})".format(what, who, where), 6)
        r = {"what":what, "who":who, "where":where}
        if self.header_mode == "whatwhowhere" or self.header_mode == "whatwho" :
            if what == None:
                if self.app().params["safemode"]:
                    self.app().stop()
                    self.app().vrb_disperror("non-conform header syntax, safemode option enabled, stopping app")
                    return {}
                else:
                    r["what"] = self.default_what
            elif who == None:
                if self.app().params["safemode"]:
                    self.app().stop()
                    self.app().vrb_disperror("non-conform header syntax, safemode option enabled, stopping app")
                    return {}
                else:
                    r["who"] = self.default_what
        if self.header_mode == "whatwhowhere":
            if where == None:
                if self.app().params["safemode"]:
                    self.app().stop()
                    self.app().vrb_disperror("non-conform header syntax, safemode option enabled, stopping app")
                    return {}
                else:
                    r["where"] = self.default_where
        if self.header_mode == "whatwhowhere":
            return r
        elif self.header_mode =="whatwho":
            r["where"] = ""
            return r
        else:
            r["who"] = ""
            r["where"] = ""
            if what == None:
                r["what"] = self.app().APP()
            else:
                return r
        return r
    def app(self):
        return self.application
    ## Abonnements
    def valid_appname(self,text):
        self.app().vrb("APP.com.valid_appname({})".format(text),6)
        if text.isalnum() and len(text) == 3 and text[0].isalpha():
            return True
        self.app().vrb_dispwarning("Invalid zone name : '{}'".format(text))
        return False
    def valid_zone(self,text):
        self.app().vrb("APP.com.valid_zone({})".format(text),6)
        if text == self.hst_air() or text == self.hst_lch():
            return True
        self.app().vrb_dispwarning("Invalid zone name : '{}'; should be '{}' or '{}'".format(text, self.hst_air(), self.hst_lch()))
        return False
    def subscribe_lch(self,who):
        self.subscribe(who,self.hst_lch())
    def subscribe_air(self,who):
        self.subscribe(who,self.hst_air())
    def subscribe(self,who,where=None):
        self.app().vrb("APP.com.subscribe({},{})".format(who, where),6)
        if self.header_mode == "what":
            self.app().vrb_dispwarning("No subscriptions in what mode")
            return
        if where == None or self.header_mode == "whatwho":
            where = self.hst_lch()
        if self.valid_appname(who) and self.valid_zone(where):
            if not who in self.subscriptions:
                self.subscriptions.update({who:[]})
            if self.is_subscribed(who,where):
                self.app().vrb_dispwarning("App {} already subscribed on zone {}".format(who,where))
            else:
                self.subscriptions[who].append(where)
            self.app().debug("subscriptions : {}".format(self.subscriptions),5)
    def is_subscribed(self,who,where):
        if self.header_mode=="whatwho":
            self.app().vrb("Impossible to subscribe apps on zone AIR in mode whatwho. Zone is {}".format(self.hst_lch()),6)
            where = self.hst_lch()
        if who in self.subscriptions:
            return where in self.subscriptions[who]
        return False
    def unsubscribe_lch(self,who):
        self.unsubscribe(who,self.hst_lch())
    def unsubscribe_air(self,who):
        self.unsubscribe(who,self.hst_air())
    def unsubscribe(self,who,where):
        self.app().vrb("APP.com.subscribe({},{})".format(who, where),6)
        if self.header_mode == "what":
            self.app().vrb_dispwarning("No subscriptions in what mode")
            return
        if where == None or self.header_mode == "whatwho":
            where = self.hst_lch()
        if self.is_subscribed(who,where):
            del(self.subscriptions[who][self.subscriptions[who].index(where)])
        else:
            self.app().vrb_dispwarning("App {} not subscribed on zone {}".format(who,where))
        self.update_subscribed_list()
    def update_subscribed_list(self):
        self.app().vrb("APP.com.update_subscribed_list()",6)
        unsubscribed_apps = []
        for app in self.subscriptions:
            if self.subscriptions[app] == []:
                unsubscribed_apps.append(app)
        for app in unsubscribed_apps:
            del(self.subscriptions[app])
        self.app().debug("subscriptions : {}".format(self.subscriptions),5)
            
    def subscribe_button(self,gui_app,gui_zone):
        self.app().vrb("APP.com.subscribe_button({},{})".format(gui_app, gui_zone),6)
        self.subscribe(gui_app.get(), gui_zone.get())
    def unsubscribe_button(self,gui_app, gui_zone):
        self.app().vrb("APP.com.unsubsubscribe_button({},{})".format(gui_app, gui_zone),6)
        self.unsubscribe(gui_app.get(), gui_zone.get())
    
    
    ## TODO add protocols with files (named pipes, network connections, etc…)
    #def add_protocol(self, )
