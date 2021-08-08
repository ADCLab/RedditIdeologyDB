import pandas as pd

def get_ids(api, subreddit, start_epoch, end_epoch):
    submission_results = list(api.search_submissions(after=start_epoch,
                                                    before=end_epoch,
                                                    subreddit=subreddit,
                                                    filter=['id']))

    submission_results_df = pd.DataFrame(submission_results, columns = ["ids"])
    # print(submission_results_df)
    
    return submission_results_df