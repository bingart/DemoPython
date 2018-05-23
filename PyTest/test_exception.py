#coding=utf-8
#Deprecated

import logging
import time
import datetime
import random
import signal
from random import randint
import requests
from selenium import webdriver
from stem.control import Controller
from file_helper import FileHelper
from mysql_helper import MySqlHelper
from geo_helper import GeoHelper

FORMAT = '%(asctime)-15s:%(process)d: %(filename)s-%(lineno)d %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, filename='test_exception.log', level=logging.INFO)
logging.info('Init: %s', 'started')

class RotHelper:
    
    def __init__(self, host, controlPort, socksPort, password = None):
        self._host = host
        self._controlPort = controlPort
        self._socksPort = socksPort
        self._password = password
        self._controller = Controller.from_port(address=self._host, port=self._controlPort)
        self._controller.authenticate()
        logging.info('created, host={0}, controlPort={1}, socksPort={2}'.format(self._host, self._controlPort, self._socksPort))

    def close(self):
        self._controller.close()
            
    def getIPAddress(self) :
        proxies = {'http': 'socks5://' + self._host + ':' + str(self._socksPort)}
        resp = requests.get('http://45.79.95.201/ip.php', proxies=proxies)
        if resp.status_code == 200:
            html = resp.content.decode('utf-8')
            return html
        else:
            return "UNKNOWN"
        
    def reload(self):
        circuits = self._controller.get_circuits()
        cidList = []
        for c in circuits:
            cidList.append(c.id)    
        for cid in cidList:
            self._controller.close_circuit(cid)
        logging.info ('reload')
    
    def getPathInfo(self):
        circuits = self._controller.get_circuits()
        nodePairList = []
        for c in circuits:
            if len(c.path) > 1:
                firstNodeItem = None
                lastNodeItem = None
                firstNode = None
                lastNode = None
                path = ''
                for nodeItem in c.path:
                    if firstNodeItem == None:
                        firstNodeItem = nodeItem
                    lastNodeItem = nodeItem
                    path += lastNodeItem[0] + ';'
                
                if firstNodeItem != None:
                    firstNode = {
                        'category': 'ENTRY',
                        'finger': firstNodeItem[0],
                        'title': firstNodeItem[1],
                        'path': path,
                    }
                
                if lastNodeItem != None:
                    lastNode = {
                        'category': 'EXIT',
                        'finger': lastNodeItem[0],
                        'title': lastNodeItem[1],
                        'path': path,
                    }
                nodePairList.append([firstNode, lastNode])
        return nodePairList
    
    def dump(self):
        logging.info("running version %s" % self._controller.get_version())
        logging.info("running pid %s" % self._controller.get_pid())
        
        circuits = self._controller.get_circuits()
        logging.info('circuits=%d' % len(circuits))
        for c in circuits:
            logging.info('c: id={0}, status={1}, path={2}, purpose={3}'.format(c.id, c.status, c.path, c.purpose))
            path = '{0}'.format(c.purpose)
            for nodeItem in c.path:
                logging.info ('nodeItem={0}'.format(nodeItem))
                path += ';' + nodeItem[0] + ',' + nodeItem[1]
            logging.info('c.path={0}'.format(path))
                
        streams = self._controller.get_streams()
        logging.info('streams=%d' % len(streams))
        for s in streams:
            logging.info('s: id={0}, circ_id={1}, source_address={2}, target_address={3}'.format(s.id, s.circ_id, s.source_address, s.target_address))

    def closeCircuit(self, cid):
        self._controller.close_circuit(cid)
        logging.info ('close circuit {0}'.format(cid))
    
    def closeAllCircuit(self):
        circuits = self._controller.get_circuits()
        logging.info('circuits=')
        logging.info(circuits)
        cidList = []
        for c in circuits:
            cidList.append(c.id)
    
        for cid in cidList:
            self._controller.close_circuit(cid)
        logging.info ('close all circuit')
    
    def getConf(self, key):
        value = self._controller.get_conf(key)
        logging.info ('get_config: key={0}, value={1}', key, value)
    
    def setConf(self, key, value):
        self._controller.set_conf(key, value)
        logging.info ('setConfig: key={0}, value={1}', key, value)
        newValue = self.getConf(key)
        logging.info ('setConfig: key={0}, new value={1}', key, newValue)
        
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
            print('open driver, pid={0}'.format(pid))
            driver.get(url)
            html = driver.page_source
            logging.info('load ok, url={0}, html.len={1}, delay={2}, ua={3}'.format(url, len(html), delay, ua))
            print('load ok, url={0}, html.len={1}, delay={2}, ua={3}'.format(url, len(html), delay, ua))
            
            if delay > 0:
                for i in range(delay):
                    time.sleep(1)
                    logging.info('sleep at {0}'.format(i))
                    print('sleep at {0}'.format(i))
        except Exception as err :
            print(err)
            logging.info('load exception, url={0}, err={1}'.format(url, err))        
        finally:
            logging.info('close driver, pid={0}'.format(pid))
            print('close driver, pid={0}'.format(pid))
            # kill the specific phantomjs child proc
            driver.service.process.send_signal(signal.SIGTERM)
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
            self.load(url, randint(10,20))
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

def testIPLookup(count = 1):
    try:
        rotHelper = RotHelper('127.0.0.1', 9351, 9350)
        mysqlHelper = MySqlHelper('localhost', 3306, 'traffic', 'sunfei', 'Bingart503', )
        geoHelper = GeoHelper('GeoLite2-Country.mmdb')
        trafficHelper = TrafficHelper('./task.txt', './mobile_ua_list.txt', '127.0.0.1', 9350)
        for i in range(0, count, 1):
            rotHelper.reload()
            #rotHelper.setConf('ExitNodes', 'US,UK,FR')
            logging.info ('index={0}, reload'.format(i))
            ipAddress = rotHelper.getIPAddress()
            countryName, countryCode = geoHelper.getCountryInfo(ipAddress)            
            logging.info ('index={0}, ipAddress={1}, countryName={2}, countryCode={3}'.format(
                i, ipAddress, countryName, countryCode))
            print('index={0}, ipAddress={1}, countryName={2}, countryCode={3}'.format(
                i, ipAddress, countryName, countryCode))
            rotHelper.dump()
            
            nodePairList = rotHelper.getPathInfo()
            for nodePair in nodePairList:
                print (nodePair)
                firstNode = nodePair[0]
                lastNode = nodePair[1]
                createOrUpdateNode(mysqlHelper, firstNode, ipAddress, countryName)
                createOrUpdateNode(mysqlHelper, lastNode, ipAddress, countryName)
                
            time.sleep(5)
            
            trafficHelper.invoke()
            
    except Exception as err :
        print(err)
        logging.info('testIPLookup exception, {0}'.format(err))        
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
        print(err)
        logging.info('test traffic error, {0}'.format(err))
    finally:
        rotHelper.close()

if __name__=="__main__":
    print("main")
    testIPLookup(20000)
    #testTraffic()
    print("exit")
