#coding=utf-8
#Deprecated

import sys
import os
import logging
import time
import datetime
import random
import signal
from random import randint
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from stem.control import Controller
from file_helper import FileHelper
from mysql_helper import MySqlHelper
from geo_helper import GeoHelper
from rot_helper import RotHelper

FORMAT = '%(asctime)-15s:%(process)d: %(filename)s-%(lineno)d %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, filename='test_exception.log', level=logging.INFO)
logging.info('Init: %s', 'started')

class TrafficHelper:
    def __init__(self, taskFilePath, uaFilePath, rotHost, rotPort):
        self._taskFilePath = taskFilePath
        self._taskList = FileHelper.loadFileList(self._taskFilePath)
        self._taskIndex = random.randint(1, len(self._taskList))

        self._uaFilePath = uaFilePath
        self._uaList = FileHelper.loadFileList(self._uaFilePath)
        self._uaIndex = random.randint(1, len(self._uaList))
        
        self._rotHost = rotHost
        self._rotPort = rotPort
        
    def load(self, url, delay):
        try:
            dcap = dict(webdriver.DesiredCapabilities.PHANTOMJS)
            ua = self.getNextUA()
            dcap["phantomjs.page.settings.userAgent"] = ua
            dcap["phantomjs.page.settings.resourceTimeout"] = 30*1000 # in ms
            serviceArgs = ['--proxy={0}:{1}'.format(self._rotHost, self._rotPort), '--proxy-type=socks5']
            serviceArgs += ['--load-images=no'] 
            driver = webdriver.PhantomJS('/usr/bin/phantomjs', desired_capabilities=dcap, service_args=serviceArgs)
            driver.set_window_size(414, 736)
            driver.cookies_enabled = False
            pid = driver.service.process.pid
            logging.info('open driver, pid={0}'.format(pid))
            driver.get(url)
            html = driver.page_source
            FileHelper.writeContent('/data/robot/test.html', html)
            logging.info('load ok, url={0}, html.len={1}, delay={2}, ua={3}'.format(url, len(html), delay, ua))
            
            if delay > 0:
                for i in range(delay):
                    time.sleep(1)
                    logging.info('sleep at {0}'.format(i))
        except Exception as err :
            logging.info('load exception, url={0}, err={1}'.format(url, err))        
        finally:
            logging.info('close driver, pid={0}'.format(pid))
            # kill the specific phantomjs child proc
            driver.service.process.send_signal(signal.SIGTERM)
            # quit the node proc
            driver.quit()
            # another way is kill -9 and wait, to avoid defunct proceess

    def load2(self, url, delay):
        try:
            ua = self.getNextUA()
            options = Options()
            options.add_argument("--headless") # Runs Chrome in headless mode.
            options.add_argument('--no-sandbox') # # Bypass OS security model
            options.add_argument('start-maximized')
            options.add_argument('disable-infobars')
            options.add_argument("--disable-extensions")
            options.add_argument("user-agent=" + ua)
            options.add_argument("--proxy-server=socks5://{0}:{1}".format(self._rotHost, self._rotPort));
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            driver = webdriver.Chrome(chrome_options=options, executable_path='/root/chromedriver')
            driver.set_window_size(414, 736)
            pid = driver.service.process.pid
            logging.info('open driver, pid={0}'.format(pid))
            driver.get(url)
            html = driver.page_source
            FileHelper.writeContent('/data/robot/test.html', html)
            logging.info('load ok, url={0}, html.len={1}, delay={2}, ua={3}'.format(url, len(html), delay, ua))
            
            if delay > 0:
                for i in range(delay):
                    time.sleep(1)
                    logging.info('sleep at {0}'.format(i))
        except Exception as err :
            logging.info('load exception, url={0}, err={1}'.format(url, err))        
        finally:
            logging.info('close driver, pid={0}'.format(pid))
            # kill the specific child proc
            # driver.service.process.send_signal(signal.SIGTERM)
            # quit the node proc
            driver.quit()
            # another way is kill -9 and wait, to avoid defunct proceess

    def getNextTask(self):
        if True:
            if len(self._taskList) == 0:
                return None
            
            url = self._taskList[self._taskIndex]
            self._taskIndex += 1
            if self._taskIndex >= len(self._taskList):
                self._taskIndex = 0
            
            taskItem = {
                'url': url,
                'actionList': ['scroll 500', 'sleep 10'],
            }
            task = {
                'taskItemList': [taskItem]
            }
            return task
        else:
            # get task from service
            # TODO
            return None

    def getNextUA(self):
        if True:
            if len(self._uaList) == 0:
                return None
            
            ua = self._uaList[self._uaIndex]
            self._uaIndex += 1
            if self._uaIndex >= len(self._uaList):
                self._uaIndex = 0

            return ua
        else:
            # get ua from service
            # TODO
            return None

    def invoke(self):
        logging.info('invoke begin')

        task = self.getNextTask()
        if task == None or (not 'taskItemList' in task):
            logging.info('no more task, return')
            return
            
        # check all task item
        taskItemList = task['taskItemList']
        if taskItemList == None or len(taskItemList) == 0:
            logging.info('empty task item list, return')
            return
            
        # load all task item
        for taskItem in taskItemList:
            url = taskItem['url']
            #self.load(url, randint(10,20))
            self.load2(url, randint(10,20))
            logging.info('load task, url={0}'.format(url))

def createOrUpdateNode(mysqlHelper, node, position, region):
    sql = 'SELECT category, title, finger FROM node WHERE category = %s AND finger = %s'
    doc = mysqlHelper.queryOne(sql, (node['category'], node['finger']))
    if doc != None:
        # update, TODO
        print()
    else:
        sql = "INSERT INTO `node`(`category`, `title`, `finger`, `historyPath`, `position`, `region`, `createTime`, `updateTime`, `state`, `errorCount`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mysqlHelper.executeOne(
            sql, 
            (
                node['category'], 
                node['title'], 
                node['finger'], 
                node['path'], 
                position, 
                region, 
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                'FETCHED',
                0)
        )

def testIPLookup(taskFilePath, torPort, count = 1, pagePerCount = 1):
    try:
        rotHelper = RotHelper('127.0.0.1', torPort + 1, torPort)
        logging.info ('rot ok')
        mysqlHelper = MySqlHelper('localhost', 3306, 'traffic', 'sunfei', 'msnP@ssw0rd01!')
        logging.info ('mysql ok')
        geoHelper = GeoHelper('GeoLite2-Country.mmdb')
        logging.info ('geo ok')
        trafficHelper = TrafficHelper(taskFilePath, './mobile_ua_list.txt', '127.0.0.1', torPort)
        logging.info ('traffic ok')
        for i in range(0, count, 1):

            rotHelper.reload()
            #rotHelper.setConf('ExitNodes', 'US,UK,FR')
            logging.info ('index={0}, reload'.format(i))
            
            try:
                ipAddress = rotHelper.getIPAddress()
                countryName, countryCode = geoHelper.getCountryInfo(ipAddress)            
                logging.info ('index={0}, ipAddress={1}, countryName={2}, countryCode={3}'.format(i, ipAddress, countryName, countryCode))
            except Exception as err2:
                logging.info('getIPAddress  exception')        
                time.sleep(5)
                continue

            rotHelper.dump()
            logging.info('dump ok')        

            nodePairList = rotHelper.getPathInfo()
            if len(nodePairList) > 0:
                logging.info('getPathInfo ok')
                for nodePair in nodePairList:
                    print (nodePair)
                    firstNode = nodePair[0]
                    lastNode = nodePair[1]
                    createOrUpdateNode(mysqlHelper, firstNode, ipAddress, countryName)
                    createOrUpdateNode(mysqlHelper, lastNode, ipAddress, countryName)
                    logging.info('createOrUpdateNode ok')
            else:
                logging.info('getPathInfo error')
                #return
                
            time.sleep(5)
            
            for j in range(0, pagePerCount):
                trafficHelper.invoke()
            
    except Exception as err :
        logging.info('testIPLookup exception, ' + str(err))        
    finally:
        mysqlHelper.close()
        geoHelper.close()
        rotHelper.close()

def testTraffic():
    try:
        rotHelper = RotHelper('127.0.0.1', 9351, 9350)
        trafficHelper = TrafficHelper('./task.txt', './mobile_ua_list.txt', '127.0.0.1', 9350)
        rotHelper.reload()
        trafficHelper.invoke()
    except Exception as err :
        logging.info('test traffic error, {0}'.format(err))
    finally:
        rotHelper.close()

if __name__=="__main__":
    print("main")
    print ('usage: python3 test_exception task_file_path tor_port run_count page_per_count')
    taskFilePath = './task.txt'
    torPort = 9350
    runCount = 10000
    pagePerCount = 1
	
    if len(sys.argv) == 5:
        taskFilePath = sys.argv[1]
        torPort = int(sys.argv[2])
        runCount = int(sys.argv[3])
        pagePerCount = int(sys.argv[4])
	
    logging.info('##################################################### start ######################################################')
    testIPLookup(taskFilePath, torPort, runCount, pagePerCount)
    #testIPLookup('./task.diabetes.txt', torPort, 2, 2)
    #testIPLookup('./task.txt', torPort, 20000)
    #testTraffic()
    print("exit")
