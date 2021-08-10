

# Getting the List of every submission

def get_url_list(ids,  reddit):

    ids2 = [i if i.startswith('t3_') else f't3_{i}' for i in ids]
    url_list = []
    
    for count, submission in enumerate(reddit.info(ids2)):
        print(count, "/", len(ids2))
        url_list.append(submission.url)
        # print(submission.title, submission.url)
    
    return url_list
