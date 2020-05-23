#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:18:24 2020

@author: Pedro Salamoni
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Frame:
    
    def __init__(self, parent_frame, orientation, fsize):
        
        #Attibutes
        self._frame = tk.Frame(parent_frame, bd=2, width=fsize[0], height=fsize[1])
        self._fsize = fsize
        self._orientation = orientation
        
        self._subframe = {}

    # frame attribute
    @property
    def frame(self):  
        return self._frame
  
    @frame.deleter
    def del_frame(self): 
        del self._frame

    # subframe attribute
    @property
    def subframe(self):  
        return self._subframe

    def newSubframe(self, name, pack=True, orientation=0, length=None):
        #Resize if length is changed
        if length != None:
            if self._orientation == 0:
                fsize = [self._fsize[0],length]
            elif self._orientation == 1:
                fsize = [length,self._fsize[1]]
        else:
            fsize = self._fsize

        self._subframe[name] = Util_frame(self.frame, orientation, fsize)

        #Deactivate propagate when length is changed
        if length != None:
            self._subframe[name].frame.pack_propagate(0)

        if pack == True:
            self.packWidget(self._subframe[name].frame)

        return self._subframe[name]
            
    @subframe.deleter
    def del_subframe(self): 
        del self.subframe

    
    def packWidget(self, widget):
        #Pack according to orientation
        if self._orientation == 0:
            widget.pack()
        elif self._orientation == 1:
            widget.pack(side=tk.LEFT)

class Util_frame(Frame):

    def __init__(self, parent_frame, orientation, fsize):
        super().__init__(parent_frame, orientation, fsize)
        self.__button = {}
        self.__label = {}
        self.__entry = {}

    # button attribute
    @property
    def button(self):  
        return self.__button
  
    def newButton(self, name, pack=True): 
        self.__button[name] = tk.Button(self.frame, text=name, command=None, bd=2)
        if pack == True:
            self.packWidget(self.__button[name])

        return self.__button[name]
    
    @button.deleter
    def del_button(self): 
        del self.__button

    # label attribute
    @property
    def label(self):  
        return self.__label
  
    def newLabel(self, name, pack=True): 
        self.__label[name] = tk.Label(self.frame, text=name, bd=2)
        if pack == True:
            self.packWidget(self.__label[name])

        return self.__label[name]

    
    @label.deleter
    def del_label(self): 
        del self.__label

    # entry attribute
    @property
    def entry(self):  
        return self.__entry
  
    def newEntry(self, name, width=50, pack=True): 
        self.__entry[name] = tk.Entry(self.frame, width=width, bd=2)
        if pack == True:
            self.packWidget(self.__entry[name])

        return self.__entry[name]

    
    @entry.deleter
    def del_entry(self): 
        del self.__entry


class GUI(Frame):
    
    #Instance
    def __init__(self,name,fsize=[500,100]):
        
        #Class Attribute
        self.__window = tk.Tk()
        self.__window.title(name)
        self.__window.minsize(fsize[0],fsize[1])

        super().__init__(self.__window, orientation=0, fsize=fsize)

        self._frame.pack(fill=None, expand=False)



    def run(self):
        self.__window.mainloop()

    def update(self):
        self.__window.update_idletasks()
        self.__window.update()

    def getDirectory(self):
        self.__window.directory = filedialog.askdirectory() + '/'

        return self.__window.directory

    def raiseMessage(self, title, message):
        messagebox.showwarning(title=title, message=message)

    def quit(self):
        self.__window.quit()

