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

import warnings
warnings.filterwarnings("ignore")

# main
if __name__ == "__main__":

    start_clock = time.time()

    ##################################### params ##################################################
    subreddit = 'Liberal' # Liberal, Conservative
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
    # firstPostTimestamp = 1306900799
    lastPostTimestamp = 1628308799 # 1628308799 #8/6/2021, 11:59:59 PM
    print("firstPostTimestamp: {}".format(firstPostTimestamp))
    print("lastPostTimestamp: {}".format(lastPostTimestamp))
    timestamp="_from"+str(firstPostTimestamp)+"to"+str(lastPostTimestamp)

    ##################################### Get ids ##################################################
    # ids_clock_st = time.time()

    # ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
    # if isdir(ids_dir) is not True:
    #     os.makedirs(ids_dir)

    # # stop 1
    # # ids_Liberal_submission_from1422733243to1425325243
    # # stop 2
    # # ids_Liberal_submission_from1446061252to1448653252
    # # stop 3
    # # ids_Liberal_submission_from1474573263to1477165263
    # # stop 4
    # # ids_Liberal_submission_from1513453278to1516045278
    # # stop 5
    # # 

    # time_delta = 30*24*60*60 # 30 day
    # start_time = 1516045278 + 1 # firstPostTimestamp 
    # end_time = start_time + time_delta
    # ids_list = []
    # day = 1
    # while start_time < lastPostTimestamp:
    #     # time.sleep(1) # 1 sec
    #     print('day',day*30, start_time, end_time)
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

    ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)

    id_files = glob.glob(ids_dir+"\*.csv")
    ids_list = []
    for id_file in id_files:
        ids_list+= list(pd.read_csv(id_file)["ids"])

    ids_list_df = pd.DataFrame(ids_list, columns = ["ids"])    
    ids_list_df.to_csv(ids_dir+ '.csv', index=False)

    ##################################### Get url ##################################################
    # ids = pd.read_csv(r'.\..\ids_'+ subreddit+ '_'+ url_type+ timestamp+ '.csv')
    # urls = get_url_list(ids=list(ids["ids"]), reddit=reddit)
    # urls_df = pd.DataFrame(urls, columns = ["urls"])
    # urls_df.to_csv(r'.\..\urls_' + subreddit+ '_'+ url_type+ timestamp+ '.csv', index=False)

    # ids_urls_df = pd.concat([ids, urls_df], axis=1)
    # ids_urls_df.to_csv(r'.\..\ids_urls_'+ subreddit+ '_'+ url_type+ timestamp+ '.csv', index=False)

    # url_time = time.time()
    # print("---url time %s seconds ---" % (url_time - ids_time))
    ################################### Get news articles ###########################################



