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
from collections import Counter
from operator import itemgetter
path="/Users/isabel/Desktop/Python Spyder/Google_jobs"
os.chdir(path)


##########################
######Global Vars###########
##########################

driver = webdriver.Chrome(executable_path = '/Users/isabel/.wdm/chromedriver/2.46/mac64/chromedriver' )
 

with open('data_science_search_urls.txt') as f:
    data_science_url_list = f.read().splitlines()

with open('data_engineer_search_urls.txt') as f:
    data_engineer_url_list = f.read().splitlines()



global_ds_jobs_descriptions = np.load('data_science_job_listings.npy').item() #load dictionary of restaurants
global_de_jobs_descriptions =np.load('data_engineer_job_listings.npy').item() #load dictionary of restaurants
##############################
######Launch Website #####
##############################
#from webdriver_manager.chrome import ChromeDriverManager

##############################
######Play #####
##############################
driver.get(zz)
body = driver.find_element_by_xpath('//div[starts-with(@jsname, "rymPhb")]')
#body = driver.find_element_by_xpath('//div[starts-with(@class, "UbEfxe gws-horizon-textlists__tl-lvc")]')


def url_into_dictionary_item(url,file_name):
    '''
   Input: URL
   Output: A dictionary key/value. Key is URL. Value is DF with 2 columns (job title and text)
    '''
    driver.get(url) #set up. Random company initially searched for because Glassdoor always opens a new tab when the first company is searched for, which we won't want
    time.sleep(1)
    body = driver.find_element_by_xpath('//div[starts-with(@jsname, "rymPhb")]')
    #body = driver.find_element_by_xpath('//div[starts-with(@class, "UbEfxe gws-horizon-textlists__tl-lvc")]')
    
    for i in range(350):
        body.send_keys(Keys.PAGE_DOWN)
        
    root = lxml.html.fromstring(driver.page_source)
    job_title = [i.text_content() for i in root.xpath('//div[starts-with(@class, "BjJfJf gsrt cPd5d")]')]#[0] #rest rating
    job_text = [i.text_content() for i in root.xpath('//span[starts-with(@class, "Cyt8W HBvzbc")]')]#[0] #rest rating
    df = pd.DataFrame()
    df['job_title'] = job_title
    df['job_text']= job_text
    my_dict = {}
    my_dict[url] = df
    return(my_dict[url])

def big_dict_into_big_df(big_dict):
    '''Input: A dictionary with all the keys/values
    Output: A massive dataframe'''
    big_df = pd.concat(bid_dict.values(), ignore_index=True)
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
    df.drop(df.index[[1,3]], inplace=True)
    
    big_df = big_df.drop_duplicates(subset=['job_text']) #drop any duplicate job descriptions
    searchfor = ['data','the']
    df = df[df.CC.str.contains('|'.join(searchfor),case=False) & df['CC'].str.len() >= 1] #-has the word "data" and "the" and -review is over 1000 characters.
    
    searchfor = ['engineer']
    df = df[df.CC.str.contains('|'.join(searchfor),case=False) & df['CC'].str.len() >= 1] #-has the word "data" and "the" and -review is over 1000 characters.
    return df
   

def scrape_job_text(url):
    
    
#a = scrape_job_text('https://www.google.com/search?q=data+scientist&ibp=htl;jobs#fpstate=tldetail&htichips=job_family_1:data%20scientist,job_family_1:data%20science,city:O13QqUW2j4Ciw3zdJvuNdg%3D%3D&htidocid=gPQbEIqS6gcFH9aTAAAAAA%3D%3D&htilrad=24.1401&htischips=job_family_1;data%20scientist;data%20science,city;O13QqUW2j4Ciw3zdJvuNdg%3D%3D:Sunnyvale&htivrt=jobs')
#[item for sublist in a for item in sublist]


for url in url_list:
        try:
            master_dict[url] = global_jobs_descriptions[url]
        except:
            master_dict[url] = scrape_job_text(url)
            global_jobs_descriptions[url] = master_dict[url]
    np.save(file_name, global_jobs_descriptions)



























def turn_dict_into_list(global_jobs_descriptions):
    master_list = list(global_jobs_descriptions.values())
    flat_list = [item for sublist in master_list for item in sublist if 'data' in item and 'the' in item and len(item)>1000]
    print(len(flat_list))
    master_job_text = list(set(flat_list))
    print(len(master_job_text))
    return master_job_text







a = turn_dict_into_list(global_de_jobs_descriptions)
len(a)
####################################
#### Stopwords #######
####################################


import nltk
from nltk.corpus import stopwords

stopwords = nltk.corpus.stopwords.words('english')
stopwords = ' '.join(stopwords)
stopwords = stopwords.translate(str.maketrans('','',string.punctuation)).lower()
stopwords = stopwords.split(' ')
stopwords.extend(['food','restaurant','get','place','really','menu','also','one','got','two','us','around','san','francisco','sf','','la','order','ordered','eat','good','come','first','go','even','would','hour','well','time','way','spot','like','make','worth','back','never','seven','close','back','etc','using','including','use',"you'll",'·','job','qualifications','plus','experience','work','working','scientist','science','company','skills','eg','equal','scientists','role','industry','data','engeineer','engineering'])

####################################
#### Top Single words #######
####################################



def clean_words(job_type_list):
    special_chars = ['--','...','\n','•','®','●','\n']
    a = ' '.join(job_type_list)
    a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
    for char in special_chars:
        a = a.replace(char, ' ') #replace special char with a space
    resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
    return resultwords
    

def top_words_counter(resultwords,num_reviews):
    counts = Counter(resultwords)
    my_dict = dict(counts)
    sorted_x = sorted(my_dict.items(), key=operator.itemgetter(1),reverse=True)
    try:
        return (sorted_x[0:num_reviews])
    except:
        return("Not enough words")
        


def percentage_word(job_type_list,word):
    num_appear = sum([1 for i in job_type_list if word.lower() in i.lower()])
    total = len(job_type_list)
    return round((num_appear/total)*100,2)

percentage_word(a,'scala')
def compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,word):
    ds = percentage_word(ds_all_jobs_text,word)
    de = percentage_word(de_all_jobs_text,word)
    print(word + ": " + str(ds) + "% DS, " + str(de) + "% DE \n")
    return [word,ds,de]

#####################################################
####Define variables that contain raw job text#######
#####################################################
#ds_all_jobs_text = create_raw_job_text(data_science_url_list)



ds_all_jobs_text = create_raw_job_dict(global_ds_jobs_descriptions,data_science_url_list,'data_science_job_listings.npy')
de_all_jobs_text = create_raw_job_dict(global_de_jobs_descriptions,data_engineer_url_list,'data_engineer_job_listings.npy')






#####################################################
####Clean words #####################################
#####################################################
ds_all_jobs_text_c = clean_words(ds_all_jobs_text)
#print(ds_all_jobs_text)
de_all_jobs_text_c = clean_words(de_all_jobs_text)

#####################################################
####Define DS variables that contain raw job text#######
#####################################################
ds_top_100 = top_words_counter(ds_all_jobs_text_c,100)
print(ds_top_100)

de_top_100 = top_words_counter(de_all_jobs_text_c,100)
print(de_top_100)

#####################################################
####Define DE variables that contain raw job text#######
#####################################################
de_top_100 = top_words_counter(ds_all_jobs_text,100)

compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'machine learning')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'statistic')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'analysis')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'artificial intelligence')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'predictive modeling')

compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'pipeline')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'big data')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'infrastructure')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'aws')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'ETL')











compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'kafka')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'scala')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'spark')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'hive')

compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'SQL')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'noSQL')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'hadoop')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'airflow')

compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'aws')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'redshift')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'EC2')




















compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'')



compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'airflow')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'scikit')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'')


compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'tensorflow')
compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'')


compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'cloud')

compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,'o')







print(percentage_word(ds_all_jobs_text,"data"))

print(top_words_counter(ds_all_jobs_text_c,100))

z = top_words_counter(de_all_jobs_text_c,100)
top_100_list = [i[0] for i in z]
print(top_100_list)

top_100_comparison = [compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,word) for word in top_100_list]
print(top_100_comparison)


#####################################################
####Both top lists job text#######
#####################################################
common_words = list(set(ds_top_100)&set(de_top_100))
print(len(common_words))

#####################################################
####Percentage word appears analysis ################
#####################################################
print(percentage_word(ds_all_jobs_text,"data"))
print(percentage_word(de_all_jobs_text,"data"))

print(percentage_word(ds_all_jobs_text,"python"))
print(percentage_word(de_all_jobs_text,"python"))

print(percentage_word(ds_all_jobs_text,"spark"))
print(percentage_word(de_all_jobs_text,"spark"))












from nltk import word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder
from nltk.collocations import QuadgramCollocationFinder 

string.punctuation += "’"

def top_words_bicounter(job_type_list):
    special_chars = ['--','...','\n','•','®','·']
    a = ' '.join(job_type_list)
    a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
    for char in special_chars:
        a = a.replace(char, ' ') #replace special char with a space
    #resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
    #text = ' '.join(resultwords)
    a
    finder = BigramCollocationFinder.from_words(word_tokenize(a))
    l = []
    for k,v in finder.ngram_fd.items():
        #count += 1
        z = (k,v)
        l.append(z)
    l = sorted(l,key=itemgetter(1),reverse=True)
    return(l[0:300])
            
top_words_bicounter(job_text)


def top_words_tricounter(job_type_list):
    special_chars = ['--','...','\n','•','®','·']
    a = ' '.join(job_type_list)
    a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
    for char in special_chars:
        a = a.replace(char, ' ') #replace special char with a space
    #resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
    #text = ' '.join(resultwords)
    a
    finder = TrigramCollocationFinder.from_words(word_tokenize(a))
    l = []
    for k,v in finder.ngram_fd.items():
        #count += 1
        z = (k,v)
        l.append(z)
    l = sorted(l,key=itemgetter(1),reverse=True)
    return(l[0:300])

top_words_tricounter(job_text)

def top_words_quadcounter(job_type_list):
    special_chars = ['--','...','\n','•','®','·']
    a = ' '.join(job_type_list)
    a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
    for char in special_chars:
        a = a.replace(char, ' ') #replace special char with a space
    #resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
    #text = ' '.join(resultwords)
    a
    finder = QuadgramCollocationFinder.from_words(word_tokenize(a))
    l = []
    for k,v in finder.ngram_fd.items():
        #count += 1
        z = (k,v)
        l.append(z)
    l = sorted(l,key=itemgetter(1),reverse=True)
    return(l[0:300])
            
top_words_quadcounter(job_text)



special_chars = ['--','...','\n','•','®']
a = ' '.join(job_text)
a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
for char in special_chars:
    a = a.replace(char, ' ') #replace special char with a space
resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
text = ' '.join(resultwords)
finder = BigramCollocationFinder.from_words(word_tokenize(text))
for k,v in finder.ngram_fd.items():
    print(k,v)


##deep copy. save a copy.




a = ' '.join(job_text)
a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
a = a.replace('\n', ' ') #replace \n with a space
a = a.replace('•', ' ')
resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
    
flat_list = [item for sublist in all_job_text for item in sublist]
flat_list.split()
a = ''.join(flat_list)
sentence = a.split() #turn into a list

from collections import Counter
counts = Counter(a)
counts.most_common(10)
sentence = a

sentence
counts = Counter(sentence)
dict(counts.most_common(30))




#str.replace(“\n”, “”)

##Google selenium locate element by xpath, two attributes
##read more 


####LOOK FOR READ MORE BUTTOM





with open("data_science_jobs_raw_text.txt","rb") as fp:
    job_text = pickle.load(fp)

