# coding=utf-8
import time
from log_helper import LogHelper
from str_helper import StrHelper
from selenium import webdriver

class TranHelper:
    
    def __init__(self):
        LogHelper.log("created")
        self.url = 'https://translate.google.cn/?hl=en#zh-CN/en/'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        time.sleep(1)
    
    def cn2en(self, txt):
        
        maxLen = 600
        segLen = 100
        
        if len(txt) > maxLen:
            return None
        
        inputStrList = StrHelper.split(txt, segLen, '。')
        
        translatedText = ''
        for inputStr in inputStrList:
            # check captcha
            #html = self.driver.execute_script("return document.documentElement.outerHTML")
            #if html.lower().find('captcha') > 0:
            #    raise Exception('captcha')
            
            # set
            textArea = self.driver.find_element_by_xpath("//TEXTAREA[@id='source']")
            if textArea != None:
                textArea.send_keys(inputStr)
            else:
                raise Exception('text area not found')
            
            # get
            time.sleep(10)    
            div = self.driver.find_element_by_xpath("//DIV[@id='gt-res-content']")
            if div != None:
                transSeg = div.get_attribute('innerText')
                translatedText += transSeg
            else:
                raise Exception('div not found')
                
            # clear
            textArea.clear()
            
        return translatedText
    
    def close(self):
        self.driver.close()
        