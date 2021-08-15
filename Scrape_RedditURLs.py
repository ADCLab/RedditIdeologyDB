import requests
from bs4 import BeautifulSoup

def get_BSoup_text(url):
    url = url.strip()
    # store the text for each article
    paragraphtext = []    
    try: 
        # get page text
        page = requests.get(url)
        # parse with BFS
        soup = BeautifulSoup(page.text, 'html.parser')    
        # get text
        articletext = soup.find_all('p') # soup.find_all('p')[8:]
        # print text
        for num, paragraph in enumerate(articletext):
            # print(num, "/", len(articletext[:-1]))
            # get the text only
            text = paragraph.get_text()  
            text = text.replace('\n', ' ').replace('\r', '')
            text = " ".join(text.split())
            # print((text))
            paragraphtext.append(text)  
    except:
        # print('***FAILED TO DOWNLOAD***', url)
        paragraphtext.append("")
    # print(paragraphtext)

    paragraphtext = ' '.join(paragraphtext)
    paragraphtext = paragraphtext.replace('\n', ' ').replace('\r', '').replace("\\", "") 
    paragraphtext = " ".join(paragraphtext.split())

    return paragraphtext

def get_BSoup_texts(ids_urls_attributes_list):
    try:
        URL_text = get_BSoup_text(ids_urls_attributes_list[1])
        return {
            'SubmissionID': ids_urls_attributes_list[0],
            'SubmissionURL': ids_urls_attributes_list[1],
            'SubmissionURLText': URL_text,
            'SubmissionUTC': ids_urls_attributes_list[2],
            'SubmissionAuthor': ids_urls_attributes_list[3],
            'SubmissionUpvotesCount': ids_urls_attributes_list[4],
            'SubmissionCommentsCount': ids_urls_attributes_list[5],
            'SubmissionAuthorFlair': ids_urls_attributes_list[6]
        }
    except Exception as e: print(e)
