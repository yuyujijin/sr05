from sortedcontainers import SortedDict
class Message():
    def __init__(self, text, app):
        self.init_text=text
        self.application = app
        self.content = SortedDict()
        self.fields = []
    def delim(self):
        """Hard-set delim"""
        return "^"
    #def delim(self):
        #"""Délimiteur issu du fichier csv"""
        #return self.app().variables['msg_delim']
    #def delim(self):
        #return self.init_text[0]
    def eq(self):
        """Hard-set eq symbol"""
        return "~"
    #def eq(self):
        #"""Délimiteur issu du fichier csv"""
        #return self.app().variables['msg_eq']
    #def eq(self):
        #return self.init_text[1]
    def parse_text(self,txt):
        self.app().vrb("apg.msg.parse_text(text={})".format(txt),6)
        msg = txt.split(self.delim())
        if txt[0] == self.delim():
            del(msg[0])
        if txt[-1] == self.delim():
            del(msg[len(msg)-1])
        for elt in msg:
            l=str(elt).split(self.eq(), 1)
            if len(elt)>0:
                self.content[l[0]] = l[1]
    def parse_text_with_known_fields(self, txt):
        """Parses the text considering every character as part of one of the fields (in self.fields list), allowing delimiters in the values"""
        self.app().vrb("apg.msg.parse_text_with_known_fields(text={})".format(txt),6)
        msg = txt.split(self.delim())
        if txt[0] == self.delim():
            del(msg[0])
        if txt[-1] == self.delim():
            del(msg[len(msg)-1])
        i=0
        while i < len(msg):
            if self.is_field(msg[i]):
                i += 1
            elif i != 0:
                msg[i-1] += self.delim() + msg[i]
                del(msg[i])
            else:
                i +=1
        for elt in msg:
            l=str(elt).split(self.eq(), 1)
            if len(elt)>0:
                self.content[l[0]] = l[1]
        self.app().vrb("apg.msg.Message.content={}".format(self.content),5)
    def is_field(self, text):
        """ Checks if text is part of the list self.fields"""
        self.app().vrb("apg.msg.is_field(text={})".format(text),5)
        text = str(text)
        for field in self.fields:
            if text.find(field, 0, len(field)-1) and len(text) > len(field) :
                if text[len(field)] == self.eq():
                    self.app().vrb("{} is a field of the message {}".format(text, self.init_text), 6)
                    return True
        self.app().vrb("{} is a not a field of the message {}".format(text, self.init_text), 6)
        return False
                
        
    def __str__(self):
        """Formats the message to send it, as a string"""
        r=self.delim()
        for key in self.content:
            value = str(self.content[key])
            r+="{}{}{}{}".format(key, self.eq(), value, self.delim())
        return r 
    def app(self):
        """Useful to get app vrb features, mostly"""
        return self.application
