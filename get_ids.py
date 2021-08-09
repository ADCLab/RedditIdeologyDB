import pandas as pd

def get_ids(api, subreddit, url_type, start_epoch, end_epoch):
    if url_type=='submission': # submission, comment
        results = list(api.search_submissions(after=start_epoch,
                                                        before=end_epoch,
                                                        subreddit=subreddit,
                                                        filter=['id']))
    else:
        results = list(api.search_comments(after=start_epoch,
                                                        before=end_epoch,
                                                        subreddit=subreddit,
                                                        filter=['id']))

    # print(results)
    # results_df = pd.DataFrame(results, columns = ["ids"])
    # print(results_df)
    
    return results