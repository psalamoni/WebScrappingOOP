#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:17:07 2020

@author: setup
"""

"""
Created on Thu Mar  5 15:29:20 2020

@author: Pedro Salamoni
"""

# import libraries
from RacePredictApplication import Search

selectedRace = ''
settings = {'Path':''}

window = None

frame = {}

button = {}

label = {}

entry = {}

radiobutton = {}


def GUIKill():
    import sys
    
    global window,frame
    
    label['labelContentStatus']['text'] = 'FINISHED'
    window.mainloop()
    sys.exit()

def GUIChangeStatus(status):
    global window,label
    
    label['labelContentStatus']['text'] = status
    window.update_idletasks()
    window.update()
    
def GUIChangeError(error):
    global window,label
    
    label['errorContentStatus']['text'] = error
    window.update_idletasks()
    window.update()

def GUISelectFolder():
    import tkinter as tk
    from tkinter import filedialog
    
    global window,entry
    
    window.directory = filedialog.askdirectory()
    window.directory = window.directory + '/'
    
    entry['entryContentSetting'].delete(0, tk.END)
    entry['entryContentSetting'].insert(0,window.directory)
    
    settings['Path'] = entry['path'].get()


def GUIKey():
    import tkinter as tk
    
    global frame,button
    
    frame['current'].pack_forget()
    frame['current'] = frame['key']
    frame['current'].pack()
    
    button['currentOption']['state'] = tk.ACTIVE
    button['currentOption']['relief'] = tk.RAISED
    button['currentOption'] = button['keyOption']
    button['currentOption']['state'] = tk.DISABLED
    button['currentOption']['relief'] = tk.SUNKEN
    
    button['searchRun'].pack()
    button['runRun'].pack_forget()
    
def GUIResults():
    import tkinter as tk
    
    global frame,button
    
    frame['current'].pack_forget()
    frame['current'] = frame['races']
    frame['current'].pack()
    
    button['currentOption']['state'] = tk.ACTIVE
    button['currentOption']['relief'] = tk.RAISED
    button['currentOption'] = button['resultsOption']
    button['currentOption']['state'] = tk.DISABLED
    button['currentOption']['relief'] = tk.SUNKEN
    
    button['searchRun'].pack_forget()
    button['runRun'].pack()

def GUISettings():
    import tkinter as tk
    
    global frame,button
    
    frame['current'].pack_forget()
    frame['current'] = frame['setting']
    frame['current'].pack()
    
    button['currentOption']['state'] = tk.ACTIVE
    button['currentOption']['relief'] = tk.RAISED
    button['currentOption'] = button['settingOption']
    button['currentOption']['state'] = tk.DISABLED
    button['currentOption']['relief'] = tk.SUNKEN

def GUISearch(results):
    import tkinter as tk
    
    global windows,frame,radiobutton,selectedRace
    
    frame['contentRaces'].pack_forget()
    frame['contentRaces'] = tk.Frame(frame['races'], bd=20)
    frame['contentRaces'].pack()
    selectedRace = tk.StringVar(frame['contentRaces'])
    
    for i,(shortRaceName,raceName,raceCity,region,date) in enumerate(results):
        textrb = raceName+'\n'+date.strftime("%x")+' | '+raceCity+' - '+region
        radiobutton[i] = tk.Radiobutton(frame['contentRaces'], text=textrb, variable=selectedRace, value=shortRaceName)
        radiobutton[i].pack( anchor = tk.W )
    
    GUIResults()
    
    window.update_idletasks()
    window.update()
    
    return

def GUIRun():
    from tkinter import messagebox
    
    global frame,entry,window,selectedRace
    
    settings['Path'] = entry['entryContentSetting'].get()
    
    if settings['Path'] == '':
        messagebox.showwarning(title='Warning!', message='You have to select the output folder')
        return
    
    selectedRace = selectedRace.get()
        
    frame['option'].pack_forget()
    frame['run'].pack_forget()
    frame['current'].pack_forget()
    frame['current'] = frame['status']
    frame['current'].pack()
    
    window.update_idletasks()
    window.update()    
    window.quit()
    
    return
    

def GUI():
    import tkinter as tk
    
    global window,frame,button,label,entry,settings,raceNameInput
    
    try:
        fset = open('settings',"r")
        settings = eval(fset.read())
        fset.close()
    except:
        pass
    
    window = tk.Tk()
    window.title("Genius Race Predictor")
    
    #Main Frames
    frame['selected'] = tk.Frame(window, width=70, bd=4)
    frame['selected'].pack()
    
    frame['option'] = tk.Frame(window, bd=4)
    frame['option'].pack()
    
    frame['run'] = tk.Frame(window, bd=4)
    frame['run'].pack()
    
    
    
    
    #Selected Frame
    frame['key'] = tk.Frame(frame['selected'], bd=4)
    frame['key'].pack()
    
    frame['current'] = frame['key']
    
    frame['setting'] = tk.Frame(frame['selected'], bd=4)
    
    frame['races'] = tk.Frame(frame['selected'], bd=5)
    
    frame['status'] = tk.Frame(frame['selected'], bd=5)
    
    #Option Frame
    button['keyOption'] = tk.Button(frame['option'], text="Key", relief=tk.SUNKEN, state=tk.DISABLED, command=GUIKey)
    button['keyOption'].pack(side=tk.LEFT)
    
    label['spaceOption'] = tk.Label(frame['option'], text="", width=1)
    label['spaceOption'].pack(side=tk.LEFT)
    
    button['resultsOption'] = tk.Button(frame['option'], text="Results", command=GUIResults)    
    button['resultsOption'].pack(side=tk.LEFT)
    
    label['spaceOption2'] = tk.Label(frame['option'], text="", width=1)
    label['spaceOption2'].pack(side=tk.LEFT)
    
    button['settingOption'] = tk.Button(frame['option'], text="Settings", command=GUISettings)    
    button['settingOption'].pack(side=tk.LEFT)
    
    button['currentOption'] = button['keyOption']
    
    #Run Frame
    button['searchRun'] = tk.Button(frame['run'], text="Search", command=lambda: GUISearch(Search(entry['entryContentKey'].get())))
    button['searchRun'].pack(side=tk.LEFT)
    
    button['runRun'] = tk.Button(frame['run'], text="Run!", command=GUIRun)
    
    
    
    
    #Key Frames
    frame['titleKey'] = tk.Frame(frame['key'], bd=4)
    frame['titleKey'].pack()
    
    frame['contentKey'] = tk.Frame(frame['key'], bd=2)
    frame['contentKey'].pack()
    
    #Settings Frame
    frame['titleSetting'] = tk.Frame(frame['setting'], bd=4)
    frame['titleSetting'].pack()
    
    frame['contentSetting'] = tk.Frame(frame['setting'], bd=2)
    frame['contentSetting'].pack()
    
    #Races Frame
    frame['titleRaces'] = tk.Frame(frame['races'], bd=4)
    frame['titleRaces'].pack()
    
    frame['contentRaces'] = tk.Frame(frame['races'], bd=20)
    frame['contentRaces'].pack()
    
    #Status Frame
    frame['titleStatus'] = tk.Frame(frame['status'], bd=4)
    frame['titleStatus'].pack()
    
    frame['contentStatus'] = tk.Frame(frame['status'], bd=20)
    frame['contentStatus'].pack()
    
    
    
    
    #Title Key Frame
    label['labelTitleKey'] = tk.Label(frame['titleKey'], text=("Type text search in Race's Name"), width="75")
    label['labelTitleKey'].pack()    
    
    #Content Key Frame
    entry['entryContentKey'] = tk.Entry(frame['contentKey'], width=80, bd=2)
    entry['entryContentKey'].pack()
    
    
    
    
    #title Setting Frame
    label['labelTitleSetting'] = tk.Label(frame['titleSetting'], text=("Settings"), width="75")
    label['labelTitleSetting'].pack()
    
    #Content Setting Frame
    label['labelContentSetting'] = tk.Label(frame['contentSetting'], text="Output Directory: ")
    label['labelContentSetting'].pack(side=tk.LEFT)
    
    entry['entryContentSetting'] = tk.Entry(frame['contentSetting'], width=65, bd=2)
    entry['entryContentSetting'].pack(side=tk.LEFT)
    entry['entryContentSetting'].insert(0,settings['Path'])
    
    label['spaceContentSetting'] = tk.Label(frame['contentSetting'], text="", width=1)
    label['spaceContentSetting'].pack(side=tk.LEFT)

    button ['buttonContentSetting'] = tk.Button(frame['contentSetting'], text="+", command=GUISelectFolder)
    button ['buttonContentSetting'].pack(side=tk.LEFT)
    
    
    
    
    #title Races Frame
    label['labeltitleRaces'] = tk.Label(frame['titleRaces'], text=("Select the race:"), width="65")
    label['labeltitleRaces'].pack()
    
    
    
    
    #title Status Frame
    label['labelTitleStatus'] = tk.Label(frame['titleStatus'], text=("STATUS"), width="65")
    label['labelTitleStatus'].pack()
    
    #status Status Frame
    label['labelContentStatus'] = tk.Label(frame['contentStatus'], text="Initializing...")
    label['labelContentStatus'].pack()
    
    #error Status Frame
    label['errorContentStatus'] = tk.Label(frame['contentStatus'], text="", fg="red")
    label['errorContentStatus'].pack()
    
    
    window.mainloop()
    
    fset = open('settings',"w")
    fset.write(str(settings))
    fset.close()
    
    return selectedRace,settings

def CreateFinalFile(fileName,data,fileContent):
    import pandas as pd
    from tabulate import tabulate
    
    if data[1] is not None:
        data = pd.concat([data[0].reset_index().drop(columns=['index']),data[1].reset_index().drop(columns=['index'])], axis=1, sort=False)
    else:
        data = data[0]
    
    fileContent += tabulate(data, headers='keys', tablefmt='rst', showindex=False)
    fileContent = fileContent[:fileContent.rfind('\n')]
    
    fileContent = fileContent.replace('nan','   ')
    
    file = open(fileName,"w")
    file.write(fileContent)