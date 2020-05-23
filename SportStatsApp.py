#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# specify urls
urlPages = []

# Specify the sleep time
sleepTime = .1 

# Specify aimed data
outerAimedData = ['BIB','NAME','CATEGORY','RANK','GENDER PLACE']
innerAimedData = ['CITY','PROVINCE','COUNTRY']

# Specify data to be renamed
oldColumnName = ['CATEGORY']
newColumnName = ['AGE']

# Specify output folder
outputFolder = ''

#===============================================================================================================================================
#
#                                                    DO NEVER CHANGE UNDER THIS SIGN, THANK YOU.
#
#================================================================================================================================================

"""
Created on Thu Mar  5 15:29:20 2020

@author: Pedro Salamoni
"""

# import libraries
#import re
import WebScrappingApp
import WebScrappingGUI
import time
import pandas as pd

class SportStatsApp(WebScrappingApp.WSAPP):

    def __init__(self):
        super().__init__()

        self.__gui = None
        self.__data = pd.DataFrame()

        return

    def startGUI(self):
        self.__gui = WebScrappingGUI.WSGUI('SportStats')
        self.__gui.createMainScreen()

    @scrappeURL
    def scrappeURL(self,urlPage):

        webScrappingApp = WebScrappingApp.WSAPP()
        webScrappingApp.collectData(urlPage)

        pageNumber=1
        
        # Loop to identify where should the script go for another page
        namesElement = self.collectElement("//tr[@role='row']//td[4]//a")
        while (len(namesElement)>0):

            #Send info to GUI about current status
            statusInfo = 'URL: ' + urlPage + ' Page: ' + str(pageNumber)            
            self.__gui.guiChangeStatus(statusInfo)
            
            #Verify if any tab is opened under rows
            viewBtnElement = self.collectElement("//tr[@role='row']//div[contains(@aria-expanded, 'true')]")
            for viewbtn in viewBtnElement:
                self.clickElement(viewbtn)
                time.sleep(1)
            
            #Collect and create data
            outerData = self.collectOuterData()
            innerData = self.collectInnerData()
            self.__data = self.__data.append(pd.concat([outerData.reset_index().drop(columns=['index']),innerData.reset_index().drop(columns=['index'])], axis=1, sort=False))


            #Change to the next page of the URL
            previousElement = self.collectElement("//div[@class='ui-datatable-tablewrapper']")[0].get_attribute('innerHTML')
            nxtbtnHTML = self.collectElement("//div[@id='mainForm:pageNav']//a[contains(@class, 'fa-angle-right')]")
            if len(nxtbtnHTML)>0:

                self.clickElement(nxtbtnHTML[0])
                pageNumber += 1
                iTime = int(time.time())

                while True:
                    try:
                        newElement = self.collectElement("//div[@class='ui-datatable-tablewrapper']")[0].get_attribute('innerHTML')
                    except:
                        continue

                    if previousElement != newElement:
                        time.sleep(1)
                        break
                    
                    if int(time.time())-iTime>10:
                        self.__gui.guiChangeError('Runtime Error - ScrappeURL function')
                        self._driver.endDriver()
                        self.__gui.guiKill()
            else:
                break
        
        return self.__data

        data = ProcessData(data)
            
        CreateFile(urlPage,data,driver)

    @collectOuterData
    def collectOuterData(self):

        DataHTML = self.collectElement("//div[@id='mainForm:result_table']")[0].get_attribute('innerHTML')

        data = self.htmlToData(DataHTML)[0]
        
        return data

    @collectInnerData
    def collectInnerData(self):

        #Attribute
        data = pd.DataFrame()

        #Get the pop-up element
        popupElement = lambda: self.collectElement("//div[@id='athlete-popup']")[0]

        previousStyle = popupElement().get_attribute('style')
        previousHtml = popupElement().get_attribute('innerHTML')

        self.wait_clickability_element("//tr[@role='row']//td[4]//a")
        namesHTML = self.collectElement("//tr[@role='row']//td[4]//a")
        
        for nameHTML in namesHTML:
            try:
                self.clickElement(nameHTML)
            except:
                data = data.append(pd.Series(), ignore_index=True)
                continue

            iTime = int(time.time())
            while True:
                try:
                    newStyle = popupElement().get_attribute('style')
                    newHtml = popupElement().get_attribute('innerHTML')
                except:
                    continue
                
                if (previousHtml != newHtml) or (previousStyle != newStyle):
                    previousStyle = newStyle
                    previousHtml = newHtml

                    innerDataRow = self.htmlToData(newHtml)[0].set_index(0).T               
                    data = data.append(innerDataRow)
                
                if int(time.time())-iTime>100:
                    self.__gui.guiChangeError('Runtime Error - collectInnerData function')
                    self._driver.endDriver()
                    self.__gui.guiKill()
                
        return data


    def processData(self,bulkData):
        
        for column in bulkData[0].columns:
            if (column.upper() not in outerAimedData) and (re.match(r"\d+:\d+:\d+(\.\d+)*", str(bulkData[0][column].iloc[1]))==None):
                bulkData[0] = bulkData[0].drop(columns=[column])
        
        for column in bulkData[1].columns:
            if column.upper() not in innerAimedData:
                try:
                    bulkData[1] = bulkData[1].drop(columns=[column])
                except:
                    continue
                
        return bulkData

def main():
    pass

if __name__ == '__main__':
    main()

def CreateFile(urlPage,data):
        
    raceTitleHTML = driver.find_elements_by_xpath("//div[@id='main']//h1[1]")
    raceTitle = raceTitleHTML[0].text
    raceDateTypeHTML = driver.find_elements_by_xpath("//div[@id='main']//p[1]")
    
    try:
        [raceDate,raceType] = re.split(r"•", raceDateTypeHTML[0].text)
        fileString = raceTitle + "_" + raceDate + "_" + raceType
    except:
        fileString = raceTitle
        GUIChangeError("Procedure Error - 127")
        
    fileString = fileString.replace('/', '-')
    fileName = outputFolder + fileString + ".txt"
    
    heading = urlPage + '\n' + raceTitle + '\n' + raceDateTypeHTML[0].text + '\n\nline 1\nline 2\nline 3\nline 4\n'
    
    CreateFinalFile(fileName,data,heading)

def main():
    
    sportStatsApp = SportStatsApp()

   
    global urlPages,outputFolder
    
    urlPages,settings = GUI('SportStats')
    
    outputFolder = settings['Path']
            
            
        
    if lenurls>0:
        driver.quit()
        
    GUIKill()
    return

if __name__ == '__main__':
    main()
