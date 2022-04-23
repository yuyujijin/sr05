import asyncio
import tkinter as tk
from functools import partial
import sys


class WindowManager:
    def __init__(self, app):
        self.application = app
        if self.notk():
            self.app().vrb("There will be no GUI",2)
            return
        self.app().vrb("There will be a GUI",2)
        #self.app().vrb_disperror("argv : '{}'".format(sys.argv))
        self.root = self.root = tk.Tk()
        self.root.title("{} on node {}".format(self.app().APP(), self.app().params["ident"]))
        self.root.protocol('WM_DELETE_WINDOW', self._onDeleteWindow)
    def app(self):
        return self.application
    def notk(self):
        self.app().vrb("WindowManager.notk() returning {}".format(self.app().params["notk"]),6)
        return self.app().params["notk"]
    def _onDeleteWindow(self):
        if self.notk():
            return
        self.root = None
        return
    async def tk_loop(self):
        if self.notk():
            self.app().vrb("No tk_loop as notk", 6)
            return 
        while self.root :
            self.root.update()
            await asyncio.sleep(0.05)
    def start(self):
        if self.notk():
            self.app().loop.run_forever()
        
        self.app().loop.run_until_complete(self.tk_loop())
    
    
    #### GUI features
    
    def tk_instr(self, instruction):
        self.app().vrb("GuiManager.tk_instr({})".format(instruction),6)
        if self.notk():
            return
        self.app().vrb("evaluating expr '{}'".format(instruction),4)
        exec(instruction)
        
    
    #def add_zone(self, area_name):
        #self.app().vrb("WindowManager.add_zone({})".format(area_name), 6)
        #self.zones[area_name] = tk.Frame(self.root)
    #def add_button(self, area_name, button_name, command, text = None, bg_color="red", fg_color="red", width=10, side="right"):
        #self.app().vrb("WindowManager.add_zone(area_name={}, button_name={}, command={}, text={}, bg_color={}, fg_color={}, width={}, side={})".format(area_name, button_name, command, text, bg_color, fg_color, width, side), 6)
        #if text == None:
            #text = button_name
        #self.buttons[button_name] = tk.Button(self.zones[area_name], text=text, command=command, activebackground=bg_color, foreground=fg_color, width=width)
        #self.buttons[button_name].pack(side=side)
