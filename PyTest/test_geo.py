#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    THIS is USED FOR GENERATE BINGACCOUNT DIMENSSION
'''
import maxminddb
from file_helper import FileHelper

reader = maxminddb.open_database('GeoLite2-Country.mmdb')
geo = reader.get('47.88.18.160')
reader.close()
print (geo)
country = geo['country']
countryCode = country['iso_code']
print (countryCode)

ipList = FileHelper.loadFileList('d:/tmp/stem/ip_uniq.txt')
countryList = []
reader = maxminddb.open_database('GeoLite2-Country.mmdb')
for ip in ipList:
    geo = reader.get(ip)
    if geo != None and 'country' in geo:
        country = geo['country']
        countryName = geo['country']['names']['en']
        countryCode = country['iso_code']
    else:
        countryCode = 'na'
    countryList.append(countryName)
reader.close()
FileHelper.saveFileList('d:/tmp/stem/country.txt', countryList, 'w')
