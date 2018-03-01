# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:52:07 2018

@author: ghaza
"""

import os
import pandas as pd
import json
#import string
import pickle

labels = ['Company', 'Model', 'Year', 'Category', 'User_topic', 'Name_of_file', 'Data']
data = []
listOfWords = []

for dirpath, dirs, files in os.walk("./carcomplaints/"):
    if not dirs:
        paths = dirpath.split('\\')
        #print(paths[0].split('/')[-1]) #company
        #print(paths[1]) #Model
        #print(paths[2]) #year
        #print(paths[3]) # Category
        #print(paths[4]) #user_topic
        for file in files:
            #print(file[:-4])
            fname = os.path.join(dirpath,file)
            with open(fname, encoding='utf-8') as myfile:
                text = myfile.read()
            data.append(((paths[0].split('/')[-1], *paths[1:], file, text)))
            #print((paths[0].split('/')[-1], *paths[1:], file, text))
            # Here we split the text, lowercase it, strip from punctuaiton 
            d = text.split("\n")
            words = text.split()
            for word in words:
                currentWord = word.lower()
                while len(currentWord)>0 and (ord(currentWord[-1])<97 or ord(currentWord[-1])>122):
                    currentWord=currentWord[:-1]
                if len(currentWord)>0:
                    listOfWords.append(currentWord)
                
with open('file.txt', 'w') as file:
     file.write(json.dumps(data))

df = pd.DataFrame(data, columns=labels)
df.head()
print(listOfWords)

df.to_csv('Data.csv')

pickle.dump(listOfWords, open( "listofwords.p", "wb" ))  
