#coding=utf-8
#Deprecated

import sys
import os
import logging
import time
import datetime
import random
import signal
import requests
from random import randint
from stem.control import Controller

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
        logging.info('get circuits ok, len={0}'.format(len(circuits)))
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
        
    def getIPAddress(self) :
        proxies = {
            #'http': 'socks5://' + self._host + ':' + str(self._socksPort),
            'https': 'socks5://' + self._host + ':' + str(self._socksPort)
        }
        resp = requests.get('https://www.infosoap.com/ip.php', proxies=proxies)
        if resp.status_code == 200:
            html = resp.content.decode('utf-8')
            return html
        else:
            return "UNKNOWN"
        
if __name__=="__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ])

    logging.info("start")
    helper = RotHelper('127.0.0.1', 9351, 9350);

    helper.dump()

    html = helper.getIPAddress()
    logging.info("ip address={0}".format(html))
    helper.reload()

    html = helper.getIPAddress()
    logging.info("ip address={0}".format(html))
    helper.reload()

    nodePairList = helper.getPathInfo()
    logging.info("len of node={0}".format(len(nodePairList)))

    logging.info("exit")
