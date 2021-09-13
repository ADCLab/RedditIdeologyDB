from newspaper import Article
import requests
from bs4 import BeautifulSoup
import csv
import time

def get_newspaper_text(url):
    url = url.strip()
    article = Article(url)
    #To download the article
    # Try-Except
    try:
        article.download()
        #To parse the article
        article.parse()
        #To extract text)
        article_text = article.text
    except:
        print('***FAILED TO DOWNLOAD***', article.url)
        article_text = ""

    return article_text

def get_newspaper_texts(ids_urls_list):
    # Empty lists for content
    thearticles_list = []
    for count, id_url in enumerate(ids_urls_list):  
        print(count, "/", len(ids_urls_list))
        id = id_url[0]
        url = id_url[1]
        paragraphtext = get_newspaper_text(url)
        if len(paragraphtext)<32766:
            thearticles_list.append([id, url, paragraphtext, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6]])
        else:
            nn = 32000 # csv cell limit
            chunks = [paragraphtext[ii:ii+nn] for ii in range(0, len(paragraphtext), nn)]
            for chunk in chunks:
                thearticles_list.append([id, url, chunk, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6]])

        # if count==100:
        #     break

    # print(len(thearticles_list))
    # print(thearticles_list)

    return thearticles_list


# >>>>>>>>>>>>
def get_BSoup_text(url):
    url = url.strip()
    # store the text for each article
    paragraphtext = []    
    try: 
        # get page text
        page = requests.get(url, timeout=1)
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
    except (requests.exceptions.Timeout) as e: 
        print (e)
        print('***FAILED TO DOWNLOAD***', url)
        paragraphtext.append("")
    except: 
        print ("Other Error")
        print('***FAILED TO DOWNLOAD***', url)
        paragraphtext.append("")
    # print(paragraphtext)

    paragraphtext = ' '.join(paragraphtext)
    paragraphtext = paragraphtext.replace('\n', ' ').replace('\r', '').replace("\\", "") 
    paragraphtext = " ".join(paragraphtext.split())

    return paragraphtext

def get_BSoup_texts(ids_urls_list):
    # Empty lists for content
    thearticles_list = []
    for count, id_url in enumerate(ids_urls_list):  
        print(count, "/", len(ids_urls_list))
        id = id_url[0]
        url = id_url[1]
        paragraphtext = get_BSoup_text(url)
        if len(paragraphtext)<32766:
            thearticles_list.append([id, url, paragraphtext, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6]])
        else:
            nn = 32000 # csv cell limit
            chunks = [paragraphtext[ii:ii+nn] for ii in range(0, len(paragraphtext), nn)]
            for chunk in chunks:
                thearticles_list.append([id, url, chunk, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6]])

        # if count==100:
        #     break

    # print(len(thearticles_list))
    # print(thearticles_list)

    return thearticles_list

# def get_BSoup_texts(ids_urls_dir_df, ids_urls_text_dir):
#     ids_urls_list=ids_urls_dir_df.values.tolist()
#     # Empty lists for content

#     with open(ids_urls_text_dir+ '.csv', 'a', newline='', encoding="utf-8") as fp:
#         wr = csv.writer(fp, dialect='excel')
#         for count, id_url in enumerate(ids_urls_list):  
#             print(count, "/", len(ids_urls_list))
#             id = id_url[0]
#             url = id_url[1]
#             paragraphtext = get_BSoup_text(url)
#             if len(paragraphtext)<32766:
#                 thearticles_list=[id, url, paragraphtext, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6]]
#                 wr.writerow(thearticles_list)
#             else:
#                 nn = 32000 # csv cell limit
#                 chunks = [paragraphtext[ii:ii+nn] for ii in range(0, len(paragraphtext), nn)]
#                 for chunk in chunks:
#                     thearticles_list=[id, url, chunk, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6]]
#                     wr.writerow(thearticles_list)

#             # if count==100:
#             #     break

def get_BSoup_texts_extended(ids_urls_list):
    # Empty lists for content
    thearticles_list = []
    for count, id_url in enumerate(ids_urls_list):  
        time.sleep(1) # to avoid freezing get_BSoup_text scrapping
        print(count, "/", len(ids_urls_list))
        id = id_url[0]
        url = id_url[1]
        paragraphtext = get_BSoup_text(url)
        if len(paragraphtext)<32766:
            thearticles_list.append([id, url, paragraphtext, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6], id_url[7], id_url[8]])
        else:
            nn = 32000 # csv cell limit
            chunks = [paragraphtext[ii:ii+nn] for ii in range(0, len(paragraphtext), nn)]
            for chunk in chunks:
                thearticles_list.append([id, url, chunk, id_url[2], id_url[3], id_url[4], id_url[5], id_url[6], id_url[7], id_url[8]])

        # if count==100:
        #     break

    # print(len(thearticles_list))
    # print(thearticles_list)

    return thearticles_list
