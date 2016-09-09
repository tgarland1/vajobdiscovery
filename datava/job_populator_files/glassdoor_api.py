# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 20:40:27 2016

@author: alsherman
"""

import requests
import pandas as pd
import urllib2
import json


data = pd.read_table(r'INSERT YOUR FILE PATH TO DATA', sep='\t')

job_dict = {}
pay_low_list = []
pay_med_list = []
pay_high_list = []

for ind, row in data.iterrows():
    job_title = row['normalizedTitle_onetTitle']

    if job_title == '':
        pay_low_list.append(0)  
        continue    
    
    already_collect_job_info = job_dict.get(job_title, '') != ''
    if already_collect_job_info:
        pay_low = job_dict[job_title]['pay_low']        
        pay_low_list.append(pay_low)
        continue 
    
    url = """http://api.glassdoor.com/api/api.htm?jobTitle={0}&t.p={1}&t.k={2}&userip={3}&useragent={4}&format=json&v=1&action=jobs-prog&countryId=1""".format(
                job_title.replace(' ','%20'),
                '', # REPLACE WITH YOUR t.p
                '', # REPLACE WITH YOUR t.k
                '', # REPLACE WITH YOUR userip
                ''  # REPLACE WITH YOUR useragent
                ).replace('\n','')
    
    # These are required to get the api data from glassdoor.com
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=hdr)   
    api_results = json.load(urllib2.urlopen(req))
    api_results = api_results.get('response','')
    
    if api_results:            
        pay_low = api_results.get('payLow',0)
        pay_med = api_results.get('payMedian',0)
        pay_high = api_results.get('payHigh',0)
    else: 
        pay_low = 0
        pay_med = 0
        pay_high = 0

    # insert results into a dict
    # used to prevent multiple api requests for the same job title
    job_dict[job_title] = {'pay_low':pay_low,'pay_med':pay_med,'pay_high':pay_high}    

    pay_low_list.append(pay_low)


data['pay_low'] = pay_low_list

















import requests
import urllib



url = """http://api.glassdoor.com/api/api.htm?jobTitle=Mechanical%20Designer&t.p=87504&t.k=iU662hJ4IuM&userip=167.219.88.140&useragent=Mozilla/5.0%20(Windows%20NT%206.3;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/52.0.2743.116%20Safari/537.36&format=json&v=1&action=jobs-prog&countryId=1"""




for i in response:
    print i