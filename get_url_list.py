

# Getting the List of every submission

from re import sub


def get_url_list(ids,  reddit):

    ids2 = [i if i.startswith('t3_') else f't3_{i}' for i in ids]
    url_list = []
    
    for count, submission in enumerate(reddit.info(ids2)):
        print(count, "/", len(ids2))
        # refer: https://praw.readthedocs.io/en/stable/code_overview/models/submission.html?highlight=submission
        author_name = None if submission.author is None else submission.author.name
        id_attributes = [submission.url, submission.created_utc, author_name, submission.score, submission.num_comments, submission.link_flair_text]
        # print(id_attributes)
        url_list.append(id_attributes)

        # if count==10:
        #     break

    return url_list
