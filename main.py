import praw
from get_timestamp import get_timestamp
from psaw import PushshiftAPI
from get_ids import get_ids
from get_url_list import get_url_list
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

# main
if __name__ == "__main__":

    ##################################### params ##################################################
    subreddit = 'Conservative' # Liberal, Conservative
    url_type = 'submission' # submission, comment

    reddit = praw.Reddit(client_id='AuThlzMeoA8isW1Xn7cYqA', \
                        client_secret='0H4tScA1Zz6eR9qk74GSkUT_Nnhxwg', \
                        user_agent='news urls scrape', \
                        username='gradwolf', \
                        password='uT9J*8CjRDvmZBf')

    api = PushshiftAPI(reddit)

    firstPostTimestamp = get_timestamp(subreddit=subreddit, post="first")
    lastPostTimestamp = get_timestamp(subreddit=subreddit, post="last")
    print("firstPostTimestamp: {}".format(firstPostTimestamp))
    print("lastPostTimestamp: {}".format(lastPostTimestamp))

    ##################################### Get ids ##################################################
    ids_df = get_ids(api=api, subreddit=subreddit, url_type=url_type, start_epoch=1628040381, end_epoch=lastPostTimestamp)
    # print(ids_df)
    ids_df.to_csv(r'.\..\ids_'+ subreddit+ '_'+ url_type+ '.csv', index=False)

    ##################################### Get url ##################################################
    ids = pd.read_csv(r'.\..\ids_'+ subreddit+ '_'+ url_type+  '.csv')
    urls = get_url_list(ids=list(ids["ids"]), reddit=reddit)
    urls_df = pd.DataFrame(urls, columns = ["urls"])
    urls_df.to_csv(r'.\..\urls_' + subreddit+ '_'+ url_type+ '.csv', index=False)

    ids_urls_df = pd.concat([ids, urls_df], axis=1)
    ids_urls_df.to_csv(r'.\..\ids_urls_'+ subreddit+ '_'+ url_type+  '.csv', index=False)

    ################################### Get news articles ###########################################



