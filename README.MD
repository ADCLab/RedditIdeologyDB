scrape_reddit: Reddit submission URL articles scraping
========================================

To scrape the news and external articles posted in the submissions of a subreddit. 

We scrape
--------

- submission id
- submission timestamp
- URL in the submission
- number of upvotes for the submission
- user id of the submission
- user flair of the submission
- article of the URL in the submission

Getting Started
---------

Parameters:
---------

Select the subreddit you want to scrape and what to scrape. Follow [PRAW Reddit API](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html) and fill the required parameters. 

```
subreddit = 'Conservative' # Liberal, Conservative
url_type = 'submission' # submission, comment

reddit = praw.Reddit(client_id='client_id', \
                client_secret='client_secret', \
                user_agent='user_agent', \
                username='username', \
                password='uT9J*password')

api = PushshiftAPI(reddit)
```

Get timestamp:
---------

Run this block to get the timestamps of the first and last submission on a subreddit. You can fix the last timestamp so that it won't change each time.

```
firstPostTimestamp = get_timestamp(subreddit=subreddit, post="first")
# lastPostTimestamp = get_timestamp(subreddit=subreddit, post="last")
lastPostTimestamp = 1628308799 # 1628308799 #8/6/2021, 11:59:59 PM >>> IT IS FIXED, DOM'T CHANGE
print("firstPostTimestamp: {}".format(firstPostTimestamp))
print("lastPostTimestamp: {}".format(lastPostTimestamp))
timestamp="_from"+str(firstPostTimestamp)+"to"+str(lastPostTimestamp)
```

Get submission ids:
---------

Run this block to get the submission ids on a subreddit between the first and last timestamp.  Getting all the ids over large duration will be heavy on your computer and might freeze. So we paginate overtime. Thus, change the 'time_delta' as required. when it stops/freezes, abort the program and change the 'start_time' to last 'end_time'. In the beginning, 'start_time' is set to 'firstPostTimestamp'.

```
ids_clock_st = time.time()

ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
if isdir(ids_dir) is not True:
    os.makedirs(ids_dir)

# stop 1
# ids_Conservative_submission_from1251402661to1253994661
# stop 2
# ids_Conservative_submission_from1290282676to1292874676
# stop 3
# ids_Conservative_submission_from1303242681to1305834681
# stop 4

time_delta = 10*24*60*60 # 10 day
start_time = 1627242987 + 1 # firstPostTimestamp or the timestamp where it stooped/frozen.
end_time = start_time + time_delta
ids_list = []
day = 1
while start_time < lastPostTimestamp:
    # time.sleep(1) # 1 sec
    print('day',day*10, start_time, end_time)
    day+=1
    id_lst = get_ids(api=api, subreddit=subreddit, url_type=url_type, start_epoch=start_time, end_epoch=end_time)
    
    print(len(id_lst))
    ids_list+=id_lst

    id_lst_df = pd.DataFrame(id_lst, columns = ["ids"])
    timeINTERVALstamp_="_from"+str(start_time)+"to"+str(end_time)
    id_lst_df.to_csv(ids_dir+ '\ids_'+ subreddit+ '_'+ url_type+ timeINTERVALstamp_+ '.csv', index=False)

    start_time = end_time + 1
    end_time = start_time + time_delta
    if end_time > lastPostTimestamp:
        end_time = lastPostTimestamp
    
ids_clock_en = time.time()
print("---ids time %s seconds ---" % (ids_clock_en - ids_clock_st))
```

Aggregate submission ids:
---------

In the previous step, we collected the ids at every 'time_delta'. Now combine all those ids in a single file.

```
ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)

id_files = glob.glob(ids_dir+"\*.csv")
ids_list = []
for id_file in id_files:
    ids_list+= list(pd.read_csv(id_file)["ids"])

ids_list_df = pd.DataFrame(ids_list, columns = ["ids"])    
ids_list_df.to_csv(ids_dir+ '.csv', index=False)
```

Get URLs:
---------

Here we collect the URLs posted with each submission using the submission ids we gathered in the previous tep.

```
url_clock_st = time.time()

ids_dir = ".\..\ids_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)

ids = pd.read_csv(ids_dir+ '.csv')
urls = get_url_list(ids=list(ids["ids"]), reddit=reddit)
urls_df = pd.DataFrame(urls, columns = ["urls"])

ids_urls_df = pd.concat([ids, urls_df], axis=1)
ids_urls_dir = ".\..\ids_urls_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
ids_urls_df.to_csv(ids_urls_dir+ '.csv', index=False)

url_clock_en = time.time()
print("---url time %s seconds ---" % (url_clock_en - url_clock_st))
```

Get articles:
---------

Finally, we scrape the articles from the URLs. We use BeautifulSoup4 as it scrapes more articles than newspaper.

```
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

ids_urls_text_df = pd.DataFrame(ids_urls_texts, columns = ["ids", "urls", "articles"])
ids_urls_text_dir = ".\..\ids_urls_articles_bsoup_"+ url_type+ "_"+ subreddit+ "_from_"+ str(firstPostTimestamp)+ "_to_"+ str(lastPostTimestamp)
ids_urls_text_df.to_csv(ids_urls_text_dir+ '.csv', index=False)

article_clock_en = time.time()
print("---article time %s seconds ---" % (article_clock_en - article_clock_st))
```

Citation
------

If you use significant portions of our code in your research, please cite our work:
```
@misc{ravi2021scrape_reddit,
  author={Ravi, Kamalakkannan and Vela, Adan},
  title = {Scrape Reddit},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/kamalravi/scrape_reddit}},
}
```
or
```
Ravi, Kamalakkannan, and Adan, Vela. "Scrape Reddit." https://github.com/kamalravi/scrape_reddit. (2021).
```

Questions or Comments
------

Please direct any questions or comments to me; I am happy to help in any way I can. You can either comment on the [project page](https://github.com/kamalravi/scrape_reddit), or email me directly at rk@knights.ucf.edu.