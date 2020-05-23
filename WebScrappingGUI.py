#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  23 15:29:20 2020

@author: Pedro Salamoni
"""

# import libraries
import GUI
import tkinter as tk

class WSGUI:
    
    def __init__(self, siteName):

        self.__urlPages = []
        self.__settings = {}      
        self.__gui = GUI.GUI('WebScrapping', fsize=[700,0])


        self.guiChangeStatus('Initializing')

    @property
    def urlPages(self):
        return self.__urlPages

    @urlPages.setter
    def set__urlPages(self,urlPages):
        self.__urlPages = urlPages

    @property
    def settings(self):
        return self.__settings

    @settings.setter
    def setSettings(self,settings):
        self.__settings = settings

    def createMainScreen(self):

        self.__gui.newSubframe('container')
        self.__gui.newSubframe('option', orientation=1)
        self.__gui.newSubframe('run', orientation=1)
    
        #Container main frame
        self.__gui.subframe['container'].newSubframe('URL', pack=False)
        self.__gui.subframe['container'].newSubframe('Settings', pack=False)
        self.__gui.subframe['container'].newSubframe('Status', pack=False)
    
        #Option main frame
        self.__gui.subframe['option'].newButton('URL')
        self.__gui.subframe['option'].button['URL']['command'] = lambda: self.guiChangeFrame(self.__gui.subframe['container'],self.__gui.subframe['option'],'URL')
        self.__gui.subframe['option'].newButton('Settings')
        self.__gui.subframe['option'].button['Settings']['command'] = lambda: self.guiChangeFrame(self.__gui.subframe['container'],self.__gui.subframe['option'],'Settings')    
    
        #Run main frame
        self.__gui.subframe['run'].newButton('Run')['command'] = self.GUIRun
        
        #Url container main frame
        self.__gui.subframe['container'].subframe['URL'].newSubframe('title', length=20)
        self.__gui.subframe['container'].subframe['URL'].subframe['title'].newLabel('Insert URLs')
    
        self.__gui.subframe['container'].subframe['URL'].newSubframe('content', orientation=1)
        urls = self.__gui.subframe['container'].subframe['URL'].subframe['content'].newSubframe('urls')
        handler = self.__gui.subframe['container'].subframe['URL'].subframe['content'].newSubframe('handler')
        self.guiAddURL(urls, handler)
    
        #Settings container main frame
        self.__gui.subframe['container'].subframe['Settings'].newSubframe('title', length=20)
        self.__gui.subframe['container'].subframe['Settings'].subframe['title'].newLabel('Settings')
    
        self.__gui.subframe['container'].subframe['Settings'].newSubframe('content')
        self.__gui.subframe['container'].subframe['Settings'].subframe['content'].newSubframe('row', orientation=1)
        self.__gui.subframe['container'].subframe['Settings'].subframe['content'].subframe['row'].newLabel('Output Directory: ')
        self.__gui.subframe['container'].subframe['Settings'].subframe['content'].subframe['row'].newEntry('path', width=65)
        self.__gui.subframe['container'].subframe['Settings'].subframe['content'].subframe['row'].newButton('+')['command'] = self.guiSelectFolder
        
        #Status container main frame
        self.__gui.subframe['container'].subframe['Status'].newSubframe('title', length=20)
        self.__gui.subframe['container'].subframe['Status'].subframe['title'].newLabel('STATUS')
        
        self.__gui.subframe['container'].subframe['Status'].newSubframe('content')
        self.__gui.subframe['container'].subframe['Status'].subframe['content'].newLabel('status')
        self.__gui.subframe['container'].subframe['Status'].subframe['content'].newLabel('error')['fg'] = 'red'
    
    
        #Set initial state
        self.guiChangeFrame(self.__gui.subframe['container'],self.__gui.subframe['option'],'URL')
    
        self.__gui.run()

    def guiKill(self):
        
        self.__gui.subframe['container'].subframe['Status'].subframe['content'].label['status']['text'] = 'FINISHED'
        self.__gui.run()
        #sys.exit()

    def guiChangeStatus(self, status):
        
        self.__gui.subframe['container'].subframe['Status'].subframe['content'].label['status']['text'] = status
        self.__gui.update()
        
    def guiChangeError(self, error):
        
        self.__gui.subframe['container'].subframe['Status'].subframe['content'].label['error']['text'] = error
        self.__gui.update()

    def guiSelectFolder(self):
        
        self.__settings['path'] = self.__gui.getDirectory()
        
        
        self.__gui.subframe['container'].subframe['Settings'].subframe['content'].subframe['row'].entry['path'].delete(0, tk.END)
        self.__gui.subframe['container'].subframe['Settings'].subframe['content'].subframe['row'].entry['path'].insert(0, self.__settings['path'])


    def guiChangeFrame(self, container, handler, frame):
        
        try:
            container.subframe['current'].frame.pack_forget()
        except:
            pass
        finally:
            container.subframe['current'] = container.subframe[frame]
            container.packWidget(container.subframe['current'].frame)

        try:
            handler.button['current']['state'] = tk.ACTIVE
            handler.button['current']['relief'] = tk.RAISED
        except:
            pass

        try:
            handler.button['current'] = handler.button[frame]
            handler.button['current']['state'] = tk.DISABLED
            handler.button['current']['relief'] = tk.SUNKEN
        except:
            pass

    def GUIRun(self):
                
        #Catch and verify output folder
        path = self.__gui.subframe['container'].subframe['Settings'].subframe['content'].subframe['row'].entry['path'].get()
        if path == '':
            self.__gui.raiseMessage('Warning!','You have to select the output folder')
            return
        
        #Catch typed urls
        ientries = self.__gui.subframe['container'].subframe['URL'].subframe['content'].subframe['urls'].subframe
        for i in ientries:
            entry = self.__gui.subframe['container'].subframe['URL'].subframe['content'].subframe['urls'].subframe[i].entry['url'].get()
            if entry == '':
                next
            else:
                self.__urlPages.append(entry.get())
            
        #Forget primary buttons
        self.__gui.subframe['option'].pack_forget()
        self.__gui.subframe['run'].pack_forget()

        #Change for Status frame inside container
        self.guiChangeFrame(self.__gui.subframe['container'],None,'Status')
        
        self.__gui.update()
        self.__gui.quit()
        
        return

    def guiAddURLField(self, parent,handler):
        i = 0
        
        while True:
            parent.newSubframe(i, orientation=1)
            parent.subframe[i].newLabel('Url '+str(i+1)+': ')
            parent.subframe[i].newEntry('url', width=80)
            print(i)
            
            if i == 9:
                handler.button['+'].pack_forget()

            yield i
            
            i += 1

    def guiAddURL(self, parent,handler):
        handler.newButton('+')
        g = self.guiAddURLField(parent,handler)
        handler.button['+']['command'] = lambda: next(g)
        next(g)
        
        return

#     try:
#         fset = open('settings',"r")
#         settings = eval(fset.read())
#         fset.close()
#     except:
#         pass
    
#     fset = open('settings',"w")
#     fset.write(str(settings))
#     fset.close()
    
#     return urlPages,settings


if __name__ == '__main__':
    wsGUI = WSGUI("SportStats")
    wsGUI.createMainScreen()
    
    