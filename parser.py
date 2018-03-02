# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 14:52:07 2018
@author: ghaza

The code to parse the dataset for car complaints to prepare it for word2vec analysis. Entries are stripped of their title, 
lowercased, all non-alphabetical entries are omitted. All is pickle-saved into one file.  
"""

import os
import pandas as pd
import json
#import string
import pickle

labels = ['Company', 'Model', 'Year', 'Category', 'User_topic', 'Name_of_file', 'Data']
data = []
listOfWords = []
i = 0

for dirpath, dirs, files in os.walk("./carcomplaints2/"):
    if not dirs:
        paths = dirpath.split('\\')
        i=i+1
        if not i % 100:
            print (i)
        for file in files:
            fname = os.path.join(dirpath,file)
            with open(fname, encoding='utf-8') as myfile:
                text = myfile.read()
            data.append(((paths[0].split('/')[-1], *paths[1:], file, text)))
            d = text.split("\n")
            text = d[1]
            words = text.split()
            for word in words:
                currentWord = word.lower() # lowercase the word
                # remove non-char begining of word 
                while len(currentWord)>0 and (ord(currentWord[0])<97 or ord(currentWord[0])>122):
                    currentWord=currentWord[1:]    
                # remove non-char ending of word 
                while len(currentWord)>0 and (ord(currentWord[-1])<97 or ord(currentWord[-1])>122):
                    currentWord=currentWord[:-1]
                if len(currentWord)>0 and currentWord != 'updated':
                    listOfWords.append(currentWord)
                
with open('file.txt', 'w') as file:
     file.write(json.dumps(data))

df = pd.DataFrame(data, columns=labels)
df.head()
#print(listOfWords)
df.to_csv('Data.csv')

pickle.dump(listOfWords, open( "listofwords.p", "wb" )) 
