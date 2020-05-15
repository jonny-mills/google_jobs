import time 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys #gives selenium access to keyboard
from selenium.common.exceptions import NoSuchElementException #error when selenium can't find certain element
import csv ##import exporting to csv stuff
import lxml.etree

import string 
#set working directory
import os
import numpy as np
import operator
from collections import Counter
from operator import itemgetter
path="/Users/isabel/Desktop/"
os.chdir(path)






def clean_words(job_type_list,stopwords):
    from nltk.corpus import stopwords
    stopwords = ' '.join(stopwords)
    stopwords = stopwords.translate(str.maketrans('','',string.punctuation)).lower()
    stopwords = stopwords.split(' ')
    stopwords.extend(['food','restaurant','get','place','really','menu','also','one','got','two','us','around','san','francisco','sf','','la','order','ordered','eat','good','come','first','go','even','would','hour','well','time','way','spot','like','make','worth','back','never','seven','close','back','etc','using','including','use',"you'll",'·','job','qualifications','plus','experience','work','working','scientist','science','company','skills','eg','equal','scientists','role','industry','data','engeineer','engineering'])
    special_chars = ['--','...','\n','•','®','●','\n']
    a = ' '.join(job_type_list)
    a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation and make lower case
    for char in special_chars:
        a = a.replace(char, ' ') #replace special char with a space
    resultwords = [word for word in a.split(' ') if word.lower() not in stopwords]
    return resultwords
    

def clean_words1(job_type_list):
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

def compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,word):
    ds = percentage_word(ds_all_jobs_text,word)
    de = percentage_word(de_all_jobs_text,word)
    print(word + ": " + str(ds) + "% DS, " + str(de) + "% DE \n")
    return [word,ds,de]


reader = open("texth.txt", "r")  ##
companies = reader.read().split(' ')
print(companies[1:49])
clean_words1(companies)











