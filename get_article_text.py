from newspaper import Article
import requests
from bs4 import BeautifulSoup

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
        # print(count, "/", len(ids_urls_list))
        id = id_url[0]
        url = id_url[1]
        paragraphtext = get_newspaper_text(url)
        if len(paragraphtext)<32766:
            thearticles_list.append([id, url, paragraphtext])
        else:
            nn = 32000 # csv cell limit
            chunks = [paragraphtext[ii:ii+nn] for ii in range(0, len(paragraphtext), nn)]
            for chunk in chunks:
                thearticles_list.append([id, url, chunk])

        if count==100:
            break

    # print(len(thearticles_list))
    # print(thearticles_list)

    return thearticles_list


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
            thearticles_list.append([id, url, paragraphtext])
        else:
            nn = 32000 # csv cell limit
            chunks = [paragraphtext[ii:ii+nn] for ii in range(0, len(paragraphtext), nn)]
            for chunk in chunks:
                thearticles_list.append([id, url, chunk])

        if count==100:
            break

    # print(len(thearticles_list))
    # print(thearticles_list)

    return thearticles_list