import re
import string 
#set working directory!!
import os
import numpy as np
path="/Users/isabel/Desktop/Python Spyder/Google_jobs"
os.chdir(path)
import Google_jobs_project_functions
import frequency_analysis_functions

with open("test.txt", "rb") as fp:   # Unpickling
    data_engineer_list = pickle.load(fp)

with open("test.txt", "rb") as fp:   # Unpickling
    data_science_list = pickle.load(fp)
    
##############################
###### Analysis ##############
##############################
clean_words(data_engineer_list)
top_words_counter(data_engineer_list)

clean_words(data_science_list)
top_words_counter(data_science_list)

compare_percentage_ds_de(ds_all_jobs_text,de_all_jobs_text,word)

for i in top_words_DE:
    compare_percentage
    
    