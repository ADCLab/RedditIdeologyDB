

# Getting the List of every submission

def get_url_list(ids, reddit):
    ids2 = [i if i.startswith('t3_') else f't3_{i}' for i in ids]

    submission_url_list = []
    for submission in reddit.info(ids2):
        submission_url_list.append(submission.url)
        # print(submission.url)

    return submission_url_list

# totalSubmissions = len(submission_results)
# for ID in submission_results:
#     # ID = "p07ef8"
#     # print(type(ID))
#     submissionitem = reddit.submission(id=ID)
#     print(submissionitem)
#     submissionList.append(submissionitem)
#     current += 1
#     percentage = current/totalSubmissions*100
#     print(str(round(percentage,2))+'%',end='\r')

# print(len(submissionList))
