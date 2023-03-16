# import libraries needed
import pandas as pd
import glob
from natsort import natsorted
import json
import tldextract
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import random
import re
from tqdm import tqdm

## Remove url_domains and urls from text

datadir = "/home/ravi/DATA_Paper/step 6 - Selected articles/"
filename = "Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime.json"
Newfilename = "Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime_CopyRightRemoved.json"

dataDF = pd.read_json(datadir+filename, orient="split")
dataDF = dataDF.to_dict('records')

# print(dataDF)

df =[]
for row in tqdm(dataDF):

    # print(row)
    # print(row['url_domain'])
    # print(type(row))
    
    textArticle = row['articles']
    # print(type(textArticle))
    
    # Remove URLs
    textArticle = re.sub(r"\S*https?:\S*", "", textArticle)
    
    # Remove url_domains present in the text
    compiled = re.compile(re.escape(row['url_domain']), re.IGNORECASE)
    textArticle = compiled.sub("", textArticle)
    
    # Remove Copyright templates 
    row['articles'] = textArticle.split("Copyright", 1)[0]
    
    # print(row)
    # print(type(row))
    
    df.append(row)
    # break
df = pd.DataFrame(df)
df.to_json(datadir+Newfilename, orient="records")    
print(df.head(1))
