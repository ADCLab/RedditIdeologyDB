from newspaper import Article

def get_text(url):
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

def get_texts(urls_list):
    texts_list = []
    for count, url in enumerate(urls_list):
        print(count, "/", len(urls_list))
        texts_list.append(get_text(url))
        if count==100:
            break

    return texts_list
    