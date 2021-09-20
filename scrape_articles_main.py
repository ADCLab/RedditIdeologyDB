from genericpath import isdir
import pandas as pd
import time
import os
import glob
from get_article_text import *
from natsort import natsorted

import warnings
warnings.filterwarnings("ignore")

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

# main
if __name__ == "__main__":

    # ################################### Get news articles ###########################################

    # article_clock_st = time.time()

    # # filename = "ids_urls_submission_Liberal_from_1241293173_to_1628308799_domainFreqAddedFiltered"
    # filename = "ids_urls_submission_Conservative_from_1202154642_to_1628308799_domainFreqAddedFiltered"

    # ids_urls_dir = "./../" + filename
    # ids_urls_dir_df = pd.read_csv(ids_urls_dir+ '.csv')
    
    # # ids_dir = "./../Lib_articles"
    # ids_dir = "./../Conserv_articles"
    # if isdir(ids_dir) is not True:
    #     os.makedirs(ids_dir)

    # # count = 238
    # count = 2859 #1012

    # for ids_urls_list_100 in batch(ids_urls_dir_df.values.tolist()[(count-1)*100:], 100):
        
    #     article_clock_st100 = time.time()

    #     ids_urls_texts = get_BSoup_texts_extended(ids_urls_list=ids_urls_list_100)
    #     ids_urls_text_df = pd.DataFrame(ids_urls_texts, columns = ["ids", "urls", "articles", "created_utc", "author", "num_upvotes", "num_comments", "flair", "url_domain", "Frequency"])
        
    #     # csv_filename = ids_dir + "/" + "Lib_Articles_" + str(count*100)+ '.csv'
    #     csv_filename = ids_dir + "/" + "Conserv_Articles_" + str(count*100)+ '.csv'

    #     try:
    #         ids_urls_text_df.to_csv(csv_filename, index=False)
    #     except UnicodeEncodeError:
    #         # process data and save it without surrogates...
    #         new_ids_urls_text_df = ids_urls_text_df.applymap(lambda x: str(x).encode("utf-8", errors="ignore").decode("utf-8", errors="ignore"))
    #         new_ids_urls_text_df.to_csv(csv_filename, index=False)

    #     print("---100 article time %s seconds ---" % (time.time() - article_clock_st))
    #     count+=1

    # article_clock_en = time.time()
    # print("---article time %s seconds ---" % (article_clock_en - article_clock_st))
    # ################################### END ###########################################

    ################################### Aggregate news articles into a single csv ###########################################

    article_clock_st = time.time()

    # ids_dir = "./../Lib_articles"
    ids_dir = "./../Conserv_articles"

    files = natsorted(glob.glob(ids_dir+"/*.csv"))

    files_df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

    # files_df.to_csv("./../" + "Lib_Articles_ALL" + '.csv', index=False)
    files_df.to_csv("./../" + "Conserv_Articles_ALL" + '.csv', index=False)

    article_clock_en = time.time()
    print("---article Aggregate time %s seconds ---" % (article_clock_en - article_clock_st))
    ################################### END ###########################################
