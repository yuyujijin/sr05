import sys
import os
import datetime

class SvgManager:
    def __init__(self, app):
        self.application = app 
        self.start_date = datetime.datetime.now()
    def dir_path(self):
        return "{}/output/{}".format(os.environ["APG_PATH"], self.app().app())
    def file_path(self,name = ""):
        self.app().vrb("SvgManager.file_path(name='{}')".format(name),6)
        if name:
            return "{}/{}".format(self.dir_path(), name)
        return "{}/svg-{}-{}.{}".format(self.dir_path(), self.app().params["ident"],str(self.start_date).replace(':', '-').replace(' ', '-'), self.app().app())
    def app(self):
        return self.application        
    def start_save(self, first_line = "", file_name = None):
        if self.saving():
            self.app().vrb("SvgManager.start_save(first_line='{}', file_name='{}')".format(first_line, file_name),6)
            with open(self.file_path(), "w") as file_handler:
                self.file_handler.write(str(first_line)+"\n")
            file_handler.close()
    def save_line(self, line = "", file_name = None, timestamp = True):
        if self.saving():
            self.app().vrb("SvgManager.save_line(line='{}', file_name='{}')".format(line, file_name),6)
            if timestamp:
                ts = "{}\t: {} :".format(str(datetime.datetime.now()).replace(':','-'), (datetime.datetime.now() - self.start_date).total_seconds())
            else:
                ts = ""
            with open(self.file_path(), "a") as file_handler:
                file_handler.write("{}{}\n".format(ts, line))
            file_handler.close()
    def saving(self):
        return bool(self.app().params["saving"])
    
        
