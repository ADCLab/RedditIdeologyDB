#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import libraries needed
import pandas as pd
import numpy as np

import tldextract

import matplotlib.pyplot as plt
import seaborn as sns

import random

import json
import glob
from natsort import natsorted

import sys

# ### prepare data for [article or not ] annotation

# In[2]:


lib_data = pd.read_json('../Lib_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded.json', orient = 'split')
print(lib_data.shape)
Conserv_data = pd.read_json('../Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded.json', orient = 'split')
print(Conserv_data.shape)


# ### Save articles in each bin (based word count)

# In[3]:


ddf = lib_data.copy()

# add word count column
ddf['totalwords'] = [len(x.split()) for x in ddf['articles'].tolist()]

# sort by word count
ddf = ddf.sort_values(by=['totalwords'], ascending=True)
print(ddf.head())
# save for later use
# ddf.to_json('../../data_clean/Lib_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount.json', orient = 'split')

spaces = np.linspace(0.05, 1.0, num=20, endpoint=True)
print(spaces, len(spaces))
lib_descrip = ddf['totalwords'].describe(spaces)
print(lib_descrip)


# In[4]:


ddf['label'] = "Negative"
ddf = ddf.rename({'articles': 'text'}, axis='columns')

ddf_text_label = ddf[['text','label']]

ddf_groups = np.array_split(ddf_text_label, 20)

    
for (idx, frame) in  enumerate(ddf_groups):
    # randomize the rows before saving
    frame = frame.sample(frac=1)
    print(idx+1, len(frame))
#     break
    fname = '../../data_clean/lib_atricles_sortedBlock_' + str(idx+1)+ "_count_" + str(len(frame)) + '.json'
#     frame.to_json(fname, orient='records', lines=False)
#     break


# In[5]:


cddf = Conserv_data.copy()

# add word count column
cddf['totalwords'] = [len(x.split()) for x in cddf['articles'].tolist()]


# sort by word count
cddf = cddf.sort_values(by=['totalwords'], ascending=True)
print(cddf.head())
# save for later use
# cddf.to_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount.json', orient = 'split')

spaces = np.linspace(0.05, 1.0, num=20, endpoint=True)
print(spaces, len(spaces))
Conserv_descrip = cddf['totalwords'].describe(spaces)
print(Conserv_descrip)


# In[6]:


cddf['label'] = "Negative"
cddf = cddf.rename({'articles': 'text'}, axis='columns')
# print(cddf.head())
print(len(cddf))

cddf_text_label = cddf[['text','label']]

cddf_groups = np.array_split(cddf_text_label, 20)
    
for (idx, frame) in  enumerate(cddf_groups):
    # randomize the rows before saving
    frame = frame.sample(frac=1)
    print(idx+1, len(frame))
#     break
    fname = '../../data_clean/Conserv_atricles_sortedBlock_' + str(idx+1)+ "_count_" + str(len(frame)) + '.json'
#     frame.to_json(fname, orient='records', lines=False)
#     break


# ### Check 100 samples from each articles block [ 20 lib an 20 conserv] using Doccano
# ### Record here which block has less than 50 original articles in both Lib and Conserv

# In[7]:


def get_percentageOFartciles(df):
    df = df.head(100)
    df['label'] = df['label'].str.get(0)
    no_articles = len(df[df.label == 'No'])
    yes_articles = len(df[df.label == 'Yes'])
    
    return yes_articles, yes_articles/len(df), no_articles, no_articles/len(df)


# In[8]:


# liberals

annot100_fnames = natsorted(glob.glob("../../data_clean/Lib_articles_batch_for_100random_check/*/all.json"))
print(len(annot100_fnames))

lib_true_articles_per_5_percent = []
for idx, annot100_fname in enumerate(annot100_fnames):
    df = pd.read_json(annot100_fname, lines=False)
    yes, yes_percent, no, no_percent = get_percentageOFartciles(df)
    lib_true_articles_per_5_percent.append(yes)
    print("{}-5% yes: {}, yes_percent: {}%, no: {}, no_percent: {}%".format(idx+1, yes, yes_percent*100, no, no_percent*100))


# In[9]:


# Conservative

annot100_fnames = natsorted(glob.glob("../../data_clean/Conserv_articles_batch_for_100random_check/*/all.json"))
print(len(annot100_fnames))

conserv_true_articles_per_5_percent = []
for idx, annot100_fname in enumerate(annot100_fnames):
    df = pd.read_json(annot100_fname, lines=False)
    yes, yes_percent, no, no_percent = get_percentageOFartciles(df)
    conserv_true_articles_per_5_percent.append(yes)
    print("{}-5% yes: {}, yes_percent: {}%, no: {}, no_percent: {}%".format(idx+1, yes, yes_percent*100, no, no_percent*100))


# In[75]:

# Plot Bar
xaxis = np.arange(1,21) * 5
fig = plt.figure(figsize=(2.5,1.5))
# fig.set_size_inches(4, 1.5)
# Width of a bar 
width = 1 
plt.bar(xaxis,lib_true_articles_per_5_percent, width, color='blue', label="r/Liberal")
plt.bar(xaxis+width,conserv_true_articles_per_5_percent, width, color='red', label="r/Conservative")
plt.grid()
plt.xlabel("Word-count length of article (percentile)", fontsize=8)
plt.ylabel("Verified Articles(%)", fontsize=8)
plt.axhline(y=95, color="green", label='Threshold of True Articles')
# plt.legend(["r/Liberal", "r/Conservative", 'Threshold of True Articles'], loc=4)
plt.legend(loc=4, fontsize=7)
fig.savefig('../../data_clean/Percentage_of_Articles_with_increasing_word_count_VS_Percentage_of_True_Articles_BARchart_scale1.png', bbox_inches='tight')
# plt.savefig('../../data_clean/Percentage_of_Articles_with_increasing_word_count_VS_Percentage_of_True_Articles_BARchart.svg', format='svg', dpi=1200, bbox_inches='tight')


sys.exit(101)

# ## Based on the above analysis
# We remove bottom 10% r/Liberal articles as they have less than 95% true articles.
# 
# We remove bottom 20% r/Conservative articles as they have less than 95% true articles.

# In[11]:


# Articles with above 95% true articles
lib_data_wc = pd.read_json('../../data_clean/Lib_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount.json', orient = 'split')
lib_data_wc_above95 = lib_data_wc.iloc[1254+1253:]
print(lib_data_wc_above95.shape)
Conserv_data_wc = pd.read_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount.json', orient = 'split')
Conserv_data_wc_above95 = Conserv_data_wc.iloc[12716*4:]
print(Conserv_data_wc_above95.shape)

# order tham nat time w.r.t. utc
lib_data_wc_above95_natTime = lib_data_wc_above95.sort_values(by=['created_utc'], ascending=True)
Conserv_data_wc_above95_natTime = Conserv_data_wc_above95.sort_values(by=['created_utc'], ascending=True)

# and save them
lib_data_wc_above95_natTime.to_json('../../data_clean/Lib_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime.json', orient = 'split')
Conserv_data_wc_above95_natTime.to_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime.json', orient = 'split')


# ## Now Let's select 22,554 articles from r/Lib and r/Con in the same utc

# In[12]:


print(lib_data_wc_above95_natTime.head(1)["created_utc"])
print(lib_data_wc_above95_natTime.tail(1)["created_utc"])

print(Conserv_data_wc_above95_natTime.head(1)["created_utc"])
print(Conserv_data_wc_above95_natTime.tail(1)["created_utc"])


# From the above cell, we can use select 22,554 articles from utc 1241294002 and to utc 1628267640 in the r/Con with same distribution as r/Lib

# Before that, let's plot the true distribution of the num of articles per day over time

# In[13]:


# Plot No. of articles per day over the beginning to 8/10/2021, 3:38:38 AM
from datetime import date

def get_date_freq(utc_df):
    date_df = pd.to_datetime(utc_df, unit='s')
    year = pd.DataFrame(date_df.dt.year).astype(str)
    month = pd.DataFrame(date_df.dt.month).astype(str)
    day = pd.DataFrame(date_df.dt.day).astype(str)
    df = year + "-" + month + "-" + day
    df['Frequency'] = df.groupby('created_utc')['created_utc'].transform('count')
    
    return df 

def get_no_of_artcles_per_day(all_dates_ArtcileCount, lib_date_freq, Conserv_date_freq):
    
    for (index, row_series) in all_dates_ArtcileCount.iterrows():  
                
        if sum(lib_date_freq['created_utc'] == row_series['date'])>0: #lib_date_freq['created_utc'].str.contains(row_series['date']).any():      
            all_dates_ArtcileCount.at[index,'lib_article_count'] = lib_date_freq.loc[lib_date_freq['created_utc'] == row_series['date'], 'Frequency'].iloc[0]   
            
        if sum(Conserv_date_freq['created_utc'] == row_series['date'])>0: #Conserv_date_freq['created_utc'].str.contains(row_series['date']).any(): 
            all_dates_ArtcileCount.at[index,'Conserv_article_count'] = Conserv_date_freq.loc[Conserv_date_freq['created_utc'] == row_series['date'], 'Frequency'].iloc[0]

    return all_dates_ArtcileCount


# In[14]:


lib_date_freq = get_date_freq(lib_data_wc_above95_natTime["created_utc"])
Conserv_date_freq = get_date_freq(Conserv_data_wc_above95_natTime["created_utc"])

sdate = date(2008,2,4)  # 1202154685 # y/m/d # start dateor date of the first post on r/conserv
edate = date(2021,8,10)  # 1628581118  # end date 8/10/2021, 3:38:38 AM
all_dates_ArtcileCount = pd.date_range(sdate,edate,freq='d')
all_dates_ArtcileCount = pd.DataFrame(all_dates_ArtcileCount.strftime('%Y-%-m-%-d'), columns=["date"])
all_dates_ArtcileCount["lib_article_count"] = 0
all_dates_ArtcileCount["Conserv_article_count"] = 0
print(all_dates_ArtcileCount)

print(lib_date_freq)
print(Conserv_date_freq)

no_of_artcles_per_day = get_no_of_artcles_per_day(all_dates_ArtcileCount, lib_date_freq, Conserv_date_freq)
print(no_of_artcles_per_day)
# save it
no_of_artcles_per_day.to_csv("../../data_clean/no_of_artcles_per_day.csv", index=False)


# In[15]:


no_of_artcles_per_day.plot(x="date", y=["lib_article_count", "Conserv_article_count"], figsize=(18,5), grid=True,
                          alpha=0.5, color=["blue", 'red'])
# Customize the major grid
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')


# In[16]:


no_of_artcles_per_day.plot(x="date", y=["lib_article_count", "Conserv_article_count"], figsize=(6,3), grid=True,
                          alpha=0.5, color=["blue", 'red'])
# Customize the major grid
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
plt.xlabel("Date")
plt.ylabel("Articles count")
plt.savefig('../../data_clean/no_of_artcles_per_day_ALL_Lib_n_Con.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# Now from the above cell, we can use select 22,554 articles from utc 1241294002 and to utc 1628267640 in the r/Con with same distribution as r/Lib

# In[16]:


lib_date_freq = get_date_freq(lib_data_wc_above95_natTime["created_utc"])
Conserv_date_freq = get_date_freq(Conserv_data_wc_above95_natTime["created_utc"])

sdate = date(2009,5,2)  # 1202154685 # y/m/d # start dateor date of the first post on r/conserv
edate = date(2021,8,6)  # 1628581118  # end date 8/10/2021, 3:38:38 AM
all_dates_ArtcileCount = pd.date_range(sdate,edate,freq='d')
all_dates_ArtcileCount = pd.DataFrame(all_dates_ArtcileCount.strftime('%Y-%-m-%-d'), columns=["date"])
all_dates_ArtcileCount["lib_article_count"] = 0
all_dates_ArtcileCount["Conserv_article_count"] = 0
print(all_dates_ArtcileCount)

print(lib_date_freq)
print(Conserv_date_freq)

no_of_artcles_per_day_22554 = get_no_of_artcles_per_day(all_dates_ArtcileCount, lib_date_freq, Conserv_date_freq)
print(no_of_artcles_per_day_22554)
# save it
no_of_artcles_per_day_22554.to_csv("../../data_clean/no_of_artcles_per_day_22554.csv", index=False)


# In[17]:


no_of_artcles_per_day_22554.plot(x="date", y=["lib_article_count", "Conserv_article_count"], figsize=(18,5), grid=True,
                          alpha=0.5, color=["blue", 'red'])
# Customize the major grid
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')


# In[18]:


def select_Conserv_article_per_day(df):
    conditions = [
        (df['lib_article_count']==df['Conserv_article_count']),
        (df['lib_article_count']<df['Conserv_article_count']),
        (df['lib_article_count']>df['Conserv_article_count'])]
    choices = [
        df['lib_article_count'], 
        df['lib_article_count'],
        df['Conserv_article_count']]
    df["Conserv_article_count_selected"] = np.select(conditions, choices)
         
    conditions = [
        (df['lib_article_count']>df['Conserv_article_count'])]
    choices = [
        df['Conserv_article_count']-df['lib_article_count']]
    df["deficit"] = np.select(conditions, choices)
         
    conditions = [
        (df['lib_article_count']<df['Conserv_article_count'])]
    choices = [
        df['Conserv_article_count']-df['lib_article_count']]
    df["surplus"] = np.select(conditions, choices)
    
    return df

no_of_artcles_per_day_22554 = pd.read_csv("../../data_clean/no_of_artcles_per_day_22554.csv")
no_of_artcles_per_day_22554_availability = select_Conserv_article_per_day(no_of_artcles_per_day_22554.copy())
print(no_of_artcles_per_day_22554_availability.head(1))
print(no_of_artcles_per_day_22554_availability.shape)
no_of_artcles_per_day_22554_availability.to_csv("../../data_clean/no_of_artcles_per_day_22554_availability.csv", index=False)


# In[19]:


# lib_data_wc_above95_natTime = pd.read_json('../../data_clean/Lib_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime.json', orient = 'split')
# print(lib_data_wc_above95_natTime.head(1))
Conserv_data_wc_above95_natTime_date = pd.read_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime.json', orient = 'split')

Conserv_data_wc_above95_natTime_date["date"] = pd.to_datetime(Conserv_data_wc_above95_natTime_date["created_utc"], unit='s')
Conserv_data_wc_above95_natTime_date["date"] = Conserv_data_wc_above95_natTime_date["date"].dt.strftime('%Y-%-m-%-d')
print(Conserv_data_wc_above95_natTime_date.shape)
print(Conserv_data_wc_above95_natTime_date.head(1))

Conserv_data_wc_above95_natTime_date = Conserv_data_wc_above95_natTime_date[
    Conserv_data_wc_above95_natTime_date.date.isin(no_of_artcles_per_day_22554_availability["date"])]

Conserv_data_wc_above95_natTime_date.to_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime_2009to2021.json', orient = 'split')

print(Conserv_data_wc_above95_natTime_date.shape)
print(Conserv_data_wc_above95_natTime_date.head(1))


# In[20]:


def get_articles_wo_replacement(date_count_df, df):
    
    print(date_count_df.shape)
    print(df.shape)
    
    # first: select row["Conserv_article_count_selected"] article per date
    selected_con_df = pd.DataFrame(columns = ['ids', 'urls', 'articles', 'created_utc', 'author',
                                                  'num_upvotes', 'num_comments', 'flair', 'url_domain',
                                                  'Frequency', 'totalwords', 'date'])
    unselected_con_df = selected_con_df.copy()
    
    for idx, row in date_count_df.iterrows():
#         print(idx)
        selected_rows = df.loc[df['date'] == row["date"]]
        if len(selected_rows)==0:
            pass
        else:
            chosen = selected_rows.sample(row["Conserv_article_count_selected"],random_state=42)
            selected_con_df = selected_con_df.append(chosen)
            remaining = selected_rows.drop(chosen.index)
            unselected_con_df = unselected_con_df.append(remaining)
#         break

    print(selected_con_df.shape)
    print(unselected_con_df.shape)
    
    # 2nd: select row["deficit"] article randomly from the unselected_con_df and append to selected_con_df
    deficit_count = -1 * date_count_df["deficit"].sum()
    print(deficit_count)
    deficit_chosen = unselected_con_df.sample(n=deficit_count,random_state=42)
    selected_con_df = selected_con_df.append(deficit_chosen)
    
    unselected_con_df = unselected_con_df.drop(deficit_chosen.index)
    
    selected_con_df = selected_con_df.sort_values(by=['created_utc'], ascending=True)
    unselected_con_df = unselected_con_df.sort_values(by=['created_utc'], ascending=True)
    
    print(selected_con_df.shape)
    print(unselected_con_df.shape)
    
    return selected_con_df, unselected_con_df

selected_con_df, unselected_con_df = get_articles_wo_replacement(no_of_artcles_per_day_22554_availability, Conserv_data_wc_above95_natTime_date.copy())
selected_con_df.to_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime_2009to2021_Selected22554.json', orient = 'split')
unselected_con_df.to_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime_2009to2021_UnSelected180308.json', orient = 'split')
print(selected_con_df.shape)
print(selected_con_df.head(1))
print(unselected_con_df.shape)
print(unselected_con_df.head(1))


# In[21]:


lib_date_freq = get_date_freq(lib_data_wc_above95_natTime["created_utc"])
Conserv_date_freq = get_date_freq(selected_con_df["created_utc"])

sdate = date(2009,5,2)  # 1202154685 # y/m/d # start dateor date of the first post on r/conserv
edate = date(2021,8,6)  # 1628581118  # end date 8/10/2021, 3:38:38 AM
all_dates_ArtcileCount = pd.date_range(sdate,edate,freq='d')
all_dates_ArtcileCount = pd.DataFrame(all_dates_ArtcileCount.strftime('%Y-%-m-%-d'), columns=["date"])
all_dates_ArtcileCount["lib_article_count"] = 0
all_dates_ArtcileCount["Conserv_article_count"] = 0
print(all_dates_ArtcileCount)

print(lib_date_freq)
print(Conserv_date_freq)

no_of_artcles_per_day_22554_Lib_n_SelectedCon = get_no_of_artcles_per_day(all_dates_ArtcileCount, lib_date_freq, Conserv_date_freq)
print(no_of_artcles_per_day_22554_Lib_n_SelectedCon)
# save it
no_of_artcles_per_day_22554_Lib_n_SelectedCon.to_csv("../../data_clean/no_of_artcles_per_day_22554_Lib_n_SelectedCon.csv", index=False)


no_of_artcles_per_day_22554_Lib_n_SelectedCon.plot(x="date", y=["lib_article_count", "Conserv_article_count"], figsize=(18,5), grid=True,
                          alpha=0.5, color=["blue", 'red'])
# Customize the major grid
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')


# ## Analysis and Final Plots

# ### Plot 1: CDF ========> url_domain.value_counts() make sure to check it

# In[2]:


# Distribution of domains of the collected URLs

lib_data = pd.read_json('../../data_clean/Lib_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime.json', orient = 'split')
Conserv_data = pd.read_json('../../data_clean/Conserv_ALL_ArticlesNoSplit_NaNremoved_natTime_OriginalData_dropDup_DUPnbadArticle_MissAdded_WordCount_above95_natTime_2009to2021_Selected22554.json', orient = 'split')

URL_dist = plt.figure(figsize=(6, 12))
plt.subplot(1,2,1)
ax=plt.gca()
# plot lib_df_domainFreq_filtered url_domain distribution
lib_data.url_domain.value_counts()[:80].plot(kind='barh', color="blue")
ax.set_frame_on(False)
plt.ylabel("URL domains")
plt.xlabel("Number of URLs")

plt.subplot(1,2,2)
ax=plt.gca()
# plot con_df_domainFreq_filtered url_domain distribution
Conserv_data.url_domain.value_counts()[:80].plot(kind='barh', color="red")
ax.set_frame_on(False)
plt.xlabel("Number of URLs")

plt.show()
URL_dist.savefig('../../data_clean/Articles_URL_dist.svg', format='svg', dpi=1200, bbox_inches='tight')


# In[3]:


# Distribution of domains of the collected URLs

URL_dist = plt.figure(figsize=(3, 12))
ax=plt.gca()
# plot lib_df_domainFreq_filtered url_domain distribution
lib_data.url_domain.value_counts()[:80].plot(kind='barh', alpha=0.3, color="blue")
ax.set_frame_on(False)
plt.ylabel("URL domains")
plt.xlabel("Number of URLs")


plt.show()
URL_dist.savefig('../../data_clean/Lib_Articles_URL_dist.svg', format='svg', dpi=1200, bbox_inches='tight')


# In[4]:


# Distribution of domains of the collected URLs

URL_dist = plt.figure(figsize=(3, 12))

ax=plt.gca()
# plot con_df_domainFreq_filtered url_domain distribution
Conserv_data.url_domain.value_counts()[:80].plot(kind='barh', alpha=0.3, color="red")
ax.set_frame_on(False)
plt.ylabel("URL domains")
plt.xlabel("Number of URLs")

plt.show()
URL_dist.savefig('../../data_clean/Conserv_Articles_URL_dist.svg', format='svg', dpi=1200, bbox_inches='tight')


# In[6]:


# CDF of domains of the collected URLs

# plot CDF of url_domain counts
URL_pdf_cdf = plt.figure(figsize=(6, 3))
plt.subplot(1,2,1)
ax=plt.gca()
count, bins_count = np.histogram(lib_data.url_domain.value_counts(), bins=len(lib_data.url_domain.value_counts()))
# finding the PDF of the histogram using count values
pdf = count / sum(count)
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf = np.cumsum(pdf)
# plotting CDF
plt.plot(bins_count[1:], cdf, color="blue", label="CDF")
# plt.legend()
ax.set_frame_on(False)
ax.set_xscale('log')
plt.xlabel("Unique domains")
plt.ylabel("Density")

# plot CDF of url_domain counts
plt.subplot(1,2,2)
ax=plt.gca()
count, bins_count = np.histogram(Conserv_data.url_domain.value_counts(), bins=len(Conserv_data.url_domain.value_counts()))
# finding the PDF of the histogram using count values
pdf = count / sum(count)
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf = np.cumsum(pdf)
# plotting CDF
plt.plot(bins_count[1:], cdf, color="red", label="CDF")
# plt.legend()
ax.set_frame_on(False)
ax.set_xscale('log')
plt.xlabel("Unique domains")

URL_pdf_cdf.savefig('../../data_clean/Articles_URL_cdf.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[15]:


# CDF of domains of the collected URLs

# plot CDF of url_domain counts
URL_pdf_cdf = plt.figure(figsize=(6, 3))
ax=plt.gca()
count, bins_count = np.histogram(lib_data.url_domain.value_counts(), bins=len(lib_data.url_domain.value_counts()))
# finding the PDF of the histogram using count values
pdf = count / sum(count)
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf = np.cumsum(pdf)
# plotting CDF
plt.plot(bins_count[1:], cdf, color="blue", label="CDF")
# plt.legend()
ax.set_frame_on(False)
ax.set_xscale('log')
plt.xlabel("Unique domains")
plt.ylabel("Density")

# plot CDF of url_domain counts
count, bins_count = np.histogram(Conserv_data.url_domain.value_counts(), bins=len(Conserv_data.url_domain.value_counts()))
# finding the PDF of the histogram using count values
pdf = count / sum(count)
# using numpy np.cumsum to calculate the CDF
# We can also find using the PDF values by looping and adding
cdf = np.cumsum(pdf)
# plotting CDF
plt.plot(bins_count[1:], cdf, color="red", label="CDF")
# plt.legend()
ax.set_frame_on(False)
ax.set_xscale('log')
plt.xlabel("Unique domains")

plt.legend(["Liberal", "Conservative"], loc='lower right' )
plt.grid(which='major', linestyle='-', linewidth='0.1', color='black')

URL_pdf_cdf.savefig('../../data_clean/Articles_URL_cdf_combined.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# ### Plot 2: No of Articles per Day

# In[26]:


lib_date_freq = get_date_freq(lib_data["created_utc"])
Conserv_date_freq = get_date_freq(Conserv_data["created_utc"])

sdate = date(2008,2,4)   # start dateor date of the first post on r/conserv
edate = date(2021,8,10)   # end date 8/10/2021, 3:38:38 AM
all_dates_ArtcileCount = pd.date_range(sdate,edate,freq='d')
all_dates_ArtcileCount = pd.DataFrame(all_dates_ArtcileCount.strftime('%Y-%-m-%-d'), columns=["date"])
all_dates_ArtcileCount["lib_article_count"] = 0
all_dates_ArtcileCount["Conserv_article_count"] = 0
print(all_dates_ArtcileCount)

print(lib_date_freq)
print(Conserv_date_freq)

no_of_artcles_per_day = get_no_of_artcles_per_day(all_dates_ArtcileCount, lib_date_freq, Conserv_date_freq)
print(no_of_artcles_per_day)


# In[27]:


no_of_artcles_per_day.plot(x="date", y=["lib_article_count", "Conserv_article_count"], figsize=(6,3), grid=True,
                          alpha=0.5, color=["blue", 'red'])
# Customize the major grid
plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
plt.xlabel("Date")
plt.ylabel("Articles count")
plt.savefig('../../data_clean/no_of_artcles_per_day_22554_Lib_n_SelectedCon.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# ### Plot 3: Word statistics

# In[28]:


# plot no of articles in each word limit (bin)
plt.figsize=(6,3)
bins = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
plt.hist(lib_data["totalwords"].to_numpy(), bins=bins, alpha=1, color='blue')
plt.hist(Conserv_data["totalwords"].to_numpy(), bins=bins, alpha=.5, color='red')
plt.legend()
plt.yscale('log')
plt.xscale('log')
plt.legend(["r/Liberal", "r/Conservative"])
plt.xlabel("Number of words")
plt.ylabel("Number of Articles")
plt.savefig('../../data_clean/no_of_artcles_VS_no_of_artcles_22554_Lib_n_SelectedCon.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[29]:


# get stats on sentences and words
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

lib_data['totalsentences'] = lib_data['articles'].apply(sent_tokenize).tolist()
lib_data['totalsentences'] = lib_data['totalsentences'].apply(len)
print(lib_data['totalsentences'].describe())

Conserv_data['totalsentences'] = Conserv_data['articles'].apply(sent_tokenize).tolist()
Conserv_data['totalsentences'] = Conserv_data['totalsentences'].apply(len)
print(Conserv_data['totalsentences'].describe())


# In[30]:


# get stats on words
print(lib_data['totalwords'].describe())
print(Conserv_data['totalwords'].describe())


# In[31]:


# word cloud

# importing all necessary modules
from wordcloud import WordCloud #, STOPWORDS
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk_stopwords = set(stopwords.words("english"))
nltk_stopwords.update(["u"])
# nltk_stopwords.update(["said", "now", "like", "also", "would", "year", "new", "one"])

def get_wordcloud(df):
    comment_words = ''
#     stopwords = set(STOPWORDS)
    stopwords = set(nltk_stopwords)

    # iterate through the csv file
    for val in df.articles:

        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()

        comment_words += " ".join(tokens)+" "

    wordcloud = WordCloud(background_color ='white',
                    stopwords = stopwords,
                    collocations=False,
                    min_font_size = 10).generate(comment_words)
    
    return wordcloud


# In[32]:


# plot the WordCloud image         
lib_wordcloud = get_wordcloud(lib_data)

plt.figure(figsize = (6, 3), facecolor = None)
plt.imshow(lib_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('../../data_clean/lib_wordcloud.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[33]:


# plot the WordCloud image         
conserv_wordcloud = get_wordcloud(Conserv_data)

plt.figure(figsize = (6, 3), facecolor = None)
plt.imshow(conserv_wordcloud, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('../../data_clean/conserv_wordcloud.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[34]:


# plot the WordCloud image         
lib_data_thehill = lib_data[lib_data["url_domain"]=="thehill"]
lib_wordcloud_thehill = get_wordcloud(lib_data_thehill)

plt.figure(figsize = (6, 3), facecolor = None)
plt.imshow(lib_wordcloud_thehill, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('../../data_clean/lib_wordcloud_thehill.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[35]:


# plot the WordCloud image         
Conserv_data_thehill = Conserv_data[Conserv_data["url_domain"]=="thehill"]
conserv_wordcloud_thehill = get_wordcloud(Conserv_data_thehill)

plt.figure(figsize = (6, 3), facecolor = None)
plt.imshow(conserv_wordcloud_thehill, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('../../data_clean/conserv_wordcloud_thehill.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[36]:


# plot the WordCloud image         
lib_data_nytimes = lib_data[lib_data["url_domain"]=="nytimes"]
lib_wordcloud_nytimes = get_wordcloud(lib_data_nytimes)

plt.figure(figsize = (6, 3), facecolor = None)
plt.imshow(lib_wordcloud_nytimes, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('../../data_clean/lib_wordcloud_nytimes.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[37]:


# plot the WordCloud image         
Conserv_data_breitbart = Conserv_data[Conserv_data["url_domain"]=="breitbart"]
conserv_wordcloud_breitbart = get_wordcloud(Conserv_data_breitbart)

plt.figure(figsize = (6, 3), facecolor = None)
plt.imshow(conserv_wordcloud_breitbart, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad = 0)

plt.savefig('../../data_clean/conserv_wordcloud_breitbart.svg', format='svg', dpi=1200, bbox_inches='tight')
plt.show()


# In[38]:


# # combine all 6 in subplot
# resolution was bad => just combine above 6 figs

# plt.figure(figsize = (6, 3), facecolor = None)
# plt.subplot(2,3,1)
# plt.imshow(lib_wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.subplot(2,3,4)
# plt.imshow(conserv_wordcloud, interpolation='bilinear')
# plt.axis("off")
# plt.subplot(2,3,2)
# plt.imshow(lib_wordcloud_thehill, interpolation='bilinear')
# plt.axis("off")
# plt.subplot(2,3,5)
# plt.imshow(conserv_wordcloud_thehill, interpolation='bilinear')
# plt.axis("off")
# plt.subplot(2,3,3)
# plt.imshow(lib_wordcloud_nytimes, interpolation='bilinear')
# plt.axis("off")
# plt.subplot(2,3,6)
# plt.imshow(conserv_wordcloud_breitbart, interpolation='bilinear')
# plt.axis("off")
# plt.tight_layout(pad = 0)
# plt.savefig('../../data_clean/lib_n_conserv_wordcloud.svg', format='svg', dpi=1200, bbox_inches='tight')
# plt.show()


# ## Randomize and Save articles alone

# In[55]:


# # lib
# lib_22554articles_shuffled = lib_data.copy()
# lib_22554articles_shuffled["label"] = 0
# lib_22554articles_shuffled = lib_22554articles_shuffled[["articles","label"]].copy()
# # shuffle the DataFrame rows
# lib_22554articles_shuffled = lib_22554articles_shuffled.sample(frac = 1, random_state=42).reset_index(drop=True)
# lib_22554articles_shuffled.to_json('../../data_clean/lib_22554articles_shuffled.json', orient = 'records')

# # conserv
# con_22554articles_shuffled = Conserv_data.copy()
# con_22554articles_shuffled["label"] = 1
# con_22554articles_shuffled = con_22554articles_shuffled[["articles","label"]].copy()
# # shuffle the DataFrame rows
# con_22554articles_shuffled = con_22554articles_shuffled.sample(frac = 1, random_state=42).reset_index(drop=True)
# con_22554articles_shuffled.to_json('../../data_clean/con_22554articles_shuffled.json', orient = 'records')


# In[56]:


# # join
# lib_con_22554articles_n_label = pd.concat([lib_22554articles_shuffled, con_22554articles_shuffled], ignore_index=True)
# # shuffle the DataFrame rows
# lib_con_22554articles_n_label_shuffled = lib_con_22554articles_n_label.sample(frac = 1, random_state=42).reset_index(drop=True)
# lib_con_22554articles_n_label_shuffled.to_json('../../data_clean/lib_con_22554articles_n_label_shuffled.json', orient = 'records')


# In[57]:


lib_con_22554articles_n_label_shuffled.head()


# In[ ]:




