#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 14:04:55 2018

@author: default
"""
import time 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys #gives selenium access to keyboard
from selenium.common.exceptions import NoSuchElementException #error when selenium can't find certain element
import csv ##import exporting to csv stuff
import lxml.etree
import lxml.html
import requests
import re
import string 
#set working directory
import os
import numpy as np
import operator
import pandas as pd

#driver = webdriver.Chrome(executable_path = '/Users/isabel/.wdm/chromedriver/2.46/mac64/chromedriver' )


def url_into_dictionary_item(url,driver):
    '''
   Input: URL
   Output: A dictionary key/value. Key is URL. Value is DF with 2 columns (job title and text)
    '''
    driver.get(url)
    time.sleep(1)
    body = driver.find_element_by_xpath('//div[starts-with(@jsname, "rymPhb")]')
    #body = driver.find_element_by_xpath('//div[starts-with(@class, "UbEfxe gws-horizon-textlists__tl-lvc")]')
    
    for i in range(350):
        body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    root = lxml.html.fromstring(driver.page_source)
    dd = [i.text_content() for i in root.xpath('//div[starts-with(@id, "gws-horizon-textlists__job_details_page")]')]#[0] #rest rating
    job_title,job_text = [],[]
    for z in dd[1:-1]:
        zAfterReplace = z.replace(z[z.find("SaveSign in to save jobsSave"):z.find(";})();")+6], "**strip_here** ") 
        job_title.append(zAfterReplace.split("**strip_here**")[0])
        job_text.append(zAfterReplace.split("**strip_here**")[1])

    df = pd.DataFrame()
    df['job_title'] = job_title
    df['job_text']= job_text
    my_dict = {}
    my_dict[url] = df
    return(my_dict[url])

def big_dict_into_big_df(big_dict):
    '''Input: A dictionary with all the keys/values
    Output: A massive dataframe'''
    big_df = pd.concat(big_dict.values(), ignore_index=True)
    return(big_df)

def prune_df(big_df):
    '''
    Input: raw df
    Output: A dataframe that
        -that removes all duplicates
        -has the word "data" and "the"
        -review is over 1000 characters.
        -only has relavent job titles
    '''
    #big_df.drop(big_df.index[[1,3]], inplace=True)
    print(len(big_df))
    big_df = big_df.drop_duplicates(subset=['job_text']) #drop any duplicate job descriptions
    print(len(big_df))
    searchfor = ['data','the']
    big_df = big_df[ (big_df.job_text.str.contains('|'.join(searchfor),case=False)) & (big_df['job_text'].str.len() >= 1000) ] #-has the word "data" and "the" and -review is over 1000 characters.
    print(len(big_df))
    
    #searchfor = ['engineer']
    #df = df[df.CC.str.contains('|'.join(searchfor),case=False) & df['CC'].str.len() >= 1] #-has the word "data" and "the" and -review is over 1000 characters.
    return big_df

def trimmed_df_to_list(trimmed_df):
    '''input: trimmed dataframe.
    Output. A list. Each index in list contains the job description.'''
    job_text_list = trimmed_df['job_text'].values()
    return job_text_list








import string
import re

#re.sub("[SaveSign].*[();]", , string)
#z.find('save')

dd = [i.text_content() for i in root.xpath('//div[starts-with(@id, "gws-horizon-textlists__job_details_page")]')]#[0] #rest rating
job_title,job_text = [],[]
for z in dd[1:]:
    zAfterReplace = z.replace(z[z.find("SaveSign in to save jobsSave"):z.find(";})();")+6], "**strip_here** ") 
    job_title.append(zAfterReplace.split("**strip_here**")[0])
    job_text.append(zAfterReplace.split("**strip_here**")[1])












          
