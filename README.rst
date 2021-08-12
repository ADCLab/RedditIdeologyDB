scrape_reddit: Reddit submission URL articles scraping & curation
========================================

To scrape the news and external articles posted in the submissions of a subreddit. 

We scrape
--------

- submission id
- submission timestamp
- URL in the submission
- number of upvotes for the submission
- user id of the submission
- user flair of the submission
- article of the URL in the submission

Getting Started:
---------

Parameters:
---------

Select the subreddit you want to scrape and what to scrape. Follow [PRAW Reddit API](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html) and fill the required parameters. 

.. code-block:: pycon

    >>> subreddit = 'Conservative' # Liberal, Conservative
    >>> url_type = 'submission' # submission, comment

    >>> reddit = praw.Reddit(client_id='client_id', \
                        client_secret='client_secret', \
                        user_agent='user_agent', \
                        username='username', \
                        password='uT9J*password')

    >>> api = PushshiftAPI(reddit)



Citation
------

If you use significant portions of our code in your research, please cite our work:
```
@misc{ravi2021scrape_reddit,
  author=Ravi, Kamalakkannan},
  title = {Scrape Reddit},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/kamalravi/scrape_reddit}},
}
```

Questions or Comments
------

Please direct any questions or comments to me; I am happy to help in any way I can. You can either comment on the [project page](https://github.com/kamalravi/scrape_reddit), or email me directly at rk@knights.ucf.edu.