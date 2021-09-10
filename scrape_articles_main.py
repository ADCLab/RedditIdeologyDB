from genericpath import isdir
import pandas as pd
import time
import os
import glob
from get_article_text import *

import warnings
warnings.filterwarnings("ignore")

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

# main
if __name__ == "__main__":

    ################################### Get news articles ###########################################

    article_clock_st = time.time()

    filename = "ids_urls_submission_Liberal_from_1241293173_to_1628308799_domainFreqAddedFiltered"
    ids_urls_dir = ".\..\\" + filename
    ids_urls_dir_df = pd.read_csv(ids_urls_dir+ '.csv')

    # # url ="http://www.usatoday.com/news/politics/election2008/2008-09-20-Poll-Obama_N.htm?loc=interstitialskip"
    # # url_BSoup_text =  get_BSoup_text(url=url)
    # # print(url_BSoup_text)SS
    
    ids_dir = ".\..\Lib_articles"
    if isdir(ids_dir) is not True:
        os.makedirs(ids_dir)

    count = 1
    for ids_urls_list_100 in batch(ids_urls_dir_df.values.tolist()[:430], 100):
        article_clock_st100 = time.time()

        ids_urls_texts = get_BSoup_texts_extended(ids_urls_list=ids_urls_list_100)
        ids_urls_text_df = pd.DataFrame(ids_urls_texts, columns = ["ids", "urls", "articles", "created_utc", "author", "num_upvotes", "num_comments", "flair", "url_domain", "Frequency"])
        ids_urls_text_df.to_csv(ids_dir + "\\" + "Lib_Articles_" + str(count*100)+ '.csv', index=False)
        
        print("---100 article time %s seconds ---" % (time.time() - article_clock_st))
        count+=1

    article_clock_en = time.time()
    print("---article time %s seconds ---" % (article_clock_en - article_clock_st))
    ################################### END ###########################################