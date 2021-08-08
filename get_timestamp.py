import urllib
import os

def get_timestamp(subreddit, post):

    redChar = [' ','{','}','\'','\\n','"created_utc"','"data"',':','[',']']

    #Getting the timestamp of first/last post on the subreddit
    sort="asc" if post=="first" else "desc"

    api_url = "https://api.pushshift.io/reddit/submission/search/?subreddit="+ subreddit+ "&sort="+ sort+ "&filter=created_utc&size=1"
    # print(api_url)
    ps = urllib.request.urlopen(api_url)
    htmltext = ps.read()
    htmltext = str(htmltext)
    htmltext = htmltext[1:]
    for c in redChar:
        htmltext = htmltext.replace(c,'')
    PostTimestamp = int(htmltext)
    # print("PostTimestamp: {}".format(PostTimestamp))
    
    return PostTimestamp