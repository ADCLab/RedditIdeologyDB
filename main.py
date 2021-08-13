from genericpath import isdir
import praw
from get_timestamp import get_timestamp
from psaw import PushshiftAPI
from get_ids import get_ids
from get_url_list import get_url_list
import pandas as pd
import time
import os
import glob
from get_article_text import *

import warnings
warnings.filterwarnings("ignore")

# main
if __name__ == "__main__":

    # start_clock = time.time()

    ##################################### params ##################################################
    subreddit = 'Conservative' # Liberal, Conservative
    url_type = 'submission' # submission, comment

    reddit = praw.Reddit(client_id='AuThlzMeoA8isW1Xn7cYqA', \
                        client_secret='0H4tScA1Zz6eR9qk74GSkUT_Nnhxwg', \
                        user_agent='news urls scrape', \
                        username='gradwolf', \
                        password='uT9J*8CjRDvmZBf')

    api = PushshiftAPI(reddit)

    ################################## Get timestamp ###############################################
    firstPostTimestamp = get_timestamp(subreddit=subreddit, post="first")
    # lastPostTimestamp = get_timestamp(subreddit=subreddit, post="last")
    lastPostTimestamp = 1628308799 # 1628308799 #8/6/2021, 11:59:59 PM >>> IT IS FIXED, DOM'T CHANGE
    print("firstPostTimestamp: {}".format(firstPostTimestamp))
    print("lastPostTimestamp: {}".format(lastPostTimestamp))
    timestamp="_from"+str(firstPostTimestamp)+"to"+str(lastPostTimestamp)

    ##################################### Get ids ##################################################
    # ids_clock_st = time.time()

    # ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    # if isdir(ids_dir) is not True:
    #     os.makedirs(ids_dir)

    # # stop 1
    # # ids_Conservative_submission_from1251402661to1253994661
    # # stop 2
    # # ids_Conservative_submission_from1290282676to1292874676
    # # stop 3
    # # ids_Conservative_submission_from1303242681to1305834681
    # # stop 4
    # # ids_Conservative_submission_from1318794687to1321386687
    # # stop 5
    # # ids_Conservative_submission_from1321386688to1323978688
    # # stop 6
    # # ids_Conservative_submission_from1331754692to1334346692
    # # stop 7
    # # ids_Conservative_submission_from1336938694to1339530694
    # # stop 8
    # # ids_Conservative_submission_from1342122696to1344714696
    # # stop 9
    # # ids_Conservative_submission_from1347306698to1349898698
    # # stop 10
    # # ids_Conservative_submission_from1386186713to1388778713
    # # stop 11
    # # ids_Conservative_submission_from1388778714to1391370714
    # # stop 12
    # # ids_Conservative_submission_from1392234716to1393098716
    # # stop 13
    # # 

    # time_delta = 10*24*60*60 # 10 day
    # start_time = 1627242987 + 1 # firstPostTimestamp or the timestamp where it stooped/frozen.
    # end_time = start_time + time_delta
    # ids_list = []
    # day = 1
    # while start_time < lastPostTimestamp:
    #     # time.sleep(1) # 1 sec
    #     print('day',day*10, start_time, end_time)
    #     day+=1
    #     id_lst = get_ids(api=api, subreddit=subreddit, url_type=url_type, start_epoch=start_time, end_epoch=end_time)
        
    #     print(len(id_lst))
    #     ids_list+=id_lst

    #     id_lst_df = pd.DataFrame(id_lst, columns = ["ids"])
    #     timeINTERVALstamp_="_from"+str(start_time)+"to"+str(end_time)
    #     id_lst_df.to_csv(ids_dir+ '\ids_'+ subreddit+ '_'+ url_type+ timeINTERVALstamp_+ '.csv', index=False)

    #     start_time = end_time + 1
    #     end_time = start_time + time_delta
    #     if end_time > lastPostTimestamp:
    #         end_time = lastPostTimestamp
        
    # ids_clock_en = time.time()
    # print("---ids time %s seconds ---" % (ids_clock_en - ids_clock_st))

    ############################### aggregate the ids ############################################

    # ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)

    # id_files = glob.glob(ids_dir+"\*.csv")
    # ids_list = []
    # for id_file in id_files:
    #     ids_list+= list(pd.read_csv(id_file)["ids"])

    # ids_list_df = pd.DataFrame(ids_list, columns = ["ids"])    
    # ids_list_df.to_csv(ids_dir+ '.csv', index=False)

    ##################################### Get url ##################################################
    # url_clock_st = time.time()

    # ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)

    # ids = pd.read_csv(ids_dir+ '.csv')
    # urls = get_url_list(ids=list(ids["ids"]), reddit=reddit)
    # urls_df = pd.DataFrame(urls, columns = ["url", "created_utc", "author", "num_upvotes", "num_comments", "flair"])

    # ids_urls_df = pd.concat([ids, urls_df], axis=1)
    # ids_urls_dir = ".\..\ids_urls_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    # ids_urls_df.to_csv(ids_urls_dir+ '.csv', index=False)

    # url_clock_en = time.time()
    # print("---url time %s seconds ---" % (url_clock_en - url_clock_st))

    # ################################### reddit.info(ids2) or get_url_list has a limit of 577283 (0--to-577282). 
    # ################################### so remaining 105 are collected below and then added to the above list

    # # url_clock_st = time.time()

    # # ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)

    # # ids = pd.read_csv(ids_dir+ '.csv')
    # # urls = get_url_list(ids=list(ids["ids"])[577283:], reddit=reddit)
    # # urls_df = pd.DataFrame(urls, columns = ["url", "created_utc", "author", "num_upvotes", "num_comments", "flair"])

    # # ids_urls_df = pd.concat([ids.iloc[577282:], urls_df], axis=1)
    # # ids_urls_dir = ".\..\ids_urls__remain_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    # # ids_urls_df.to_csv(ids_urls_dir+ '.csv', index=False)

    # # url_clock_en = time.time()
    # # print("---url time %s seconds ---" % (url_clock_en - url_clock_st))

    ################################### Get news articles ###########################################

    article_clock_st = time.time()

    ids_urls_dir = ".\..\ids_urls_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    ids_urls_dir_df = pd.read_csv(ids_urls_dir+ '.csv')

    # # url ="http://www.usatoday.com/news/politics/election2008/2008-09-20-Poll-Obama_N.htm?loc=interstitialskip"
    # # url_text =  get_newspaper_text(url=url)
    # # print(url_text)
    # # url_BSoup_text =  get_BSoup_text(url=url)
    # # print(url_BSoup_text)

    print("==== bsoup scrapes more articles than newspaper ====")
    
    # ids_urls_texts = get_newspaper_texts(ids_urls_list=ids_urls_dir_df.values.tolist())
    ids_urls_texts = get_BSoup_texts(ids_urls_list=ids_urls_dir_df.values.tolist())
    print(len(ids_urls_texts))
    
    ids_urls_text_df = pd.DataFrame(ids_urls_texts, columns = ["ids", "urls", "articles", "created_utc", "author", "num_upvotes", "num_comments", "flair"])
    ids_urls_text_dir = ".\..\ids_urls_articles_newsp_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    # ids_urls_text_dir = ".\..\ids_urls_articles_bsoup_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    ids_urls_text_df.to_csv(ids_urls_text_dir+ '.csv', index=False)

    article_clock_en = time.time()
    print("---article time %s seconds ---" % (article_clock_en - article_clock_st))

    ################################### END ###########################################