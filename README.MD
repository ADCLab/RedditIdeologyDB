scrape_reddit: Reddit submission URL articles scraping
========================================

To scrape the news and external articles posted in the submissions of a subreddit. 

We scrape
--------

- submission id (id)
- submission timestamp (created_utc)
- URL in the submission (url)
- number of upvotes for the submission (num_upvotes)
- number of comments on the submission (num_comments)
- user id of the submission (author)
- user flair of the submission (flair)
- article of the URL in the submission (article)

Getting Started
---------

In the ```main.py```

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

In the ```scrape_articles_main.py```

Finally, we scrape the articles from the URLs. We use BeautifulSoup4 as it scrapes more articles than newspaper. When we send continuous URL requests, our requests may get blocked and also appending/storing all the scrapped articles will lead to execution freeze. So we send each URL request with 1 second delay and we saved every 100 articles in a csv file. If program freezes at any point, abort and run it from the last known URL count (can be found from the last saved csv file).  

```
article_clock_st = time.time()

# filename = "ids_urls_submission_Liberal_from_1241293173_to_1628308799_domainFreqAddedFiltered"
filename = "ids_urls_submission_Conservative_from_1202154642_to_1628308799_domainFreqAddedFiltered"

ids_urls_dir = "./../" + filename
ids_urls_dir_df = pd.read_csv(ids_urls_dir+ '.csv')

# ids_dir = "./../Lib_articles"
ids_dir = "./../Conserv_articles"
if isdir(ids_dir) is not True:
    os.makedirs(ids_dir)

# count = 238 # Init count is 1
count = 2859 #1012 # Init count is 1

for ids_urls_list_100 in batch(ids_urls_dir_df.values.tolist()[(count-1)*100:], 100):
    
    article_clock_st100 = time.time()

    ids_urls_texts = get_BSoup_texts_extended(ids_urls_list=ids_urls_list_100)
    ids_urls_text_df = pd.DataFrame(ids_urls_texts, columns = ["ids", "urls", "articles", "created_utc", "author", "num_upvotes", "num_comments", "flair", "url_domain", "Frequency"])
    
    # csv_filename = ids_dir + "/" + "Lib_Articles_" + str(count*100)+ '.csv'
    csv_filename = ids_dir + "/" + "Conserv_Articles_" + str(count*100)+ '.csv'

    try:
        ids_urls_text_df.to_csv(csv_filename, index=False)
    except UnicodeEncodeError:
        # process data and save it without surrogates...
        new_ids_urls_text_df = ids_urls_text_df.applymap(lambda x: str(x).encode("utf-8", errors="ignore").decode("utf-8", errors="ignore"))
        new_ids_urls_text_df.to_csv(csv_filename, index=False)

    print("---100 article time %s seconds ---" % (time.time() - article_clock_st))
    count+=1

article_clock_en = time.time()
print("---article time %s seconds ---" % (article_clock_en - article_clock_st))
```

Once we have all the articles in csv files of 100 URL-batch, we aggregate news articles into a single csv.

```
    article_clock_st = time.time()

    # ids_dir = "./../Lib_articles"
    ids_dir = "./../Conserv_articles"

    files = natsorted(glob.glob(ids_dir+"/*.csv"))

    files_df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)

    # files_df.to_csv("./../" + "Lib_Articles_ALL" + '.csv', index=False)
    files_df.to_csv("./../" + "Conserv_Articles_ALL" + '.csv', index=False)

    article_clock_en = time.time()
    print("---article Aggregate time %s seconds ---" % (article_clock_en - article_clock_st))
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

Acknowledgement
------

Inspired by [PRAW Reddit API](https://praw.readthedocs.io/) and [Pushshift Reddit API](https://reddit-api.readthedocs.io/).


Questions or Comments
------

Please direct any questions or comments to me; I am happy to help in any way I can. You can either comment on the [project page](https://github.com/kamalravi/scrape_reddit), or email me directly at rk@knights.ucf.edu.