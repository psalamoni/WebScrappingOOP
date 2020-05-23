#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  23 15:29:20 2020

@author: Pedro Salamoni
"""
# import libraries
from selenium import webdriver
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
import time
import sys
import abc

class Driver():

    def __init__(self,urlPages):

        self._driver = None
        
        lenurls = len(urlPages)

        if lenurls>0:
            self._driver = webdriver.Chrome()

        return
        
    @property
    def driver(self):
        return self._driver
    
    def endDriver(self):
        if self._driver != None:
            self._driver.quit()

    

class WSAPP():

    __metaclass__  = abc.ABCMeta

    def __init__(self):

        self._driver = None
        self._urlPages = None
        self._error = None

        return
    
    def scrappeURLList(self, urlPages):

        self._driver = Driver(urlPages)

        for urlPage in urlPages:

            iTime = int(time.time())
            while int(time.time())-iTime>30:
                try:
                    scrappeURL(urlPage)
                    break
                except:
                    pass
            else:
                self._error = "Error Code:\n" + sys.exc_info()[0]
                self._driver.endDriver()
                return self._error
        
        self._driver.endDriver()
        return self._error

    #Method to be implemented to process the URL page
    @abc.abstractmethod
    def scrappeURL(self,urlPage):
        return

    #Method to be implemented to collect exposed data
    @abc.abstractmethod
    def collectOuterData(self):
        return

    #Method to be implemented if exists any data hidden
    def collectInnerData(self):
        return NotImplementedError

    #Access and set the driver to specific url
    def collectData(self,urlpage):
        self._driver.driver.get(urlpage)
        
        return self._driver.driver

    #Collect Elements according to xpath
    def collectElement(self,xpath):
        contentHTML = self._driver.driver.find_elements_by_xpath(xpath)
        
        return contentHTML

    #Click in Element
    def clickElement(self,element):
        self._driver.driver.execute_script("arguments[0].click();", element)

    #Convert HTML tables into Pandas data
    def htmlToData(self,dataHTML):
        import pandas as pd
        
        data = pd.read_html(dataHTML)
        
        return data

    def CreateFinalFile(self,fileName,data,fileContent):
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
        
    def wait_clickability_element(self,element_name):
        ui.WebDriverWait(self._driver,10).until(EC.element_to_be_clickable((By.XPATH, element_name)))

        return