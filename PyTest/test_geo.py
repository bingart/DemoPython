#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    THIS is USED FOR GENERATE BINGACCOUNT DIMENSSION
'''
import maxminddb

reader = maxminddb.open_database('GeoLite2-Country.mmdb')
geo = reader.get('47.88.18.160')
reader.close()
print (geo)
country = geo['country']
countryCode = country['iso_code']
print (countryCode)
