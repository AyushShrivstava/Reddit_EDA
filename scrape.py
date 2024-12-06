"""Answer for Q1: A script to scrape top 100 posts from subreddit `r/srilanka` and corresponding
comments. Python Reddit API Wrapper (PRAW) was used for data scrapping. The amount of metatdata
scraped was decided as per the consultation with the TA
"""

# %%
# Importing modules needed for the script
# =======================================

# rich.progress.Progress is used to display fancy progress bar.
#
# constants module is used to define some constants that will never change
# like column names in csv. Defined in one module to reduce errors and redundancy
#
import os
import praw
import datetime
import constants
import pandas as pd
from datetime import timezone
from rich.progress import Progress

def determine_post_type(post: praw.models.reddit.submission.Submission) -> str:
    """Function to determine the type of a reddit post as reddit has developed different kinds of
    post. The method was derived by doing some trial and error on the subreddit `r/test`.
    PRAW does not have dedicated method or attribute for this purpose. The attribute `post_hint`
    helps to differentiate between text, image and video post. But, this attribute is not
    available on all objects. For example, some old text type posts, poll and link type post
    does not have it.

    Parameters
    ----------
    post : praw.models.reddit.submission.Submission
        PRAW Submission object representing the post for which the type needs to be determined.

    Returns
    -------
    str
        The determined type of the post. Can be any of the following:

            * text: Text type. Post may contain embedded media
            * image: Image only post
            * video: Video only post
            * gallery: gallery only post. It is a slideshow of images
            * poll: Post containing poll only
            * link: Link only post
            * unknown: Unable to determine 
    """
    if hasattr(post, 'post_hint'):
        if 'self' in post.post_hint:
            return 'text'
        elif 'image' in post.post_hint:
            return 'image'
        elif 'video' in post.post_hint:
            return 'video'
    elif hasattr(post, 'poll_data'):
        return 'poll'
    elif hasattr(post, 'is_gallery') and post.is_gallery:
        return 'gallery'
    elif post.is_self == True:
        return 'text'
    elif post.is_self == False:
        return 'link'
    else:
        return 'unknown'

# %%
# Some predefined variable. Change as per requirement
# ===================================================
#
# Since, there is no reddit domain in permalink returned by PRAW,
# we use permalink_prefix to concat permalink to the domain name
# while scraing.
# For example:
# permalink returned by PRAW:
#   - /r/srilanka/comments/uketjy/sri_lankan_and_proud/
# Conacting to permalink_prefix will give:
#   - https://www.reddit.com/r/srilanka/comments/uketjy/sri_lankan_and_proud/
#
#
# We use `utc_timestamp` to calculate authors account age in terms of days.
permalink_prefix = "https://www.reddit.com"
sub_reddit = "srilanka"
post_limit = 100
post_dir = ""
comments_dir = "comments/"
dt = datetime.datetime.now(timezone.utc)
utc_time = dt.replace(tzinfo=timezone.utc)
utc_timestamp = utc_time.timestamp()

# While initialising the scrapper, praw.ini file was used for credentials.
# Check PRAW's docs for more info on praw.ini
scrapper = praw.Reddit(site_name="simple_scrapper")
sub_reddit = scrapper.subreddit(sub_reddit)
post_headers = [
    constants.POST_ID,
    constants.POST_TITLE,
    constants.POST_PERMALINK,
    constants.POST_URL,
    constants.POST_SCORE,
    constants.POST_NUM_COMMENTS,
    constants.POST_CREATED_TIMESTAMP,
    constants.POST_SUBREDDIT,
    constants.POST_UPVOTE_RATIO,
    constants.AUTHOR_USERNAME,
    constants.AUTHOR_KARMA,
    constants.AUTHOR_ACCOUNT_AGE,
    constants.POST_TYPE,
    constants.POST_TEXT_CONTENT
]

comment_headers = [
    constants.COMMENT_ID,
    constants.COMMENT_PARENT_ID,
    constants.COMMENT_SCORE,
    constants.COMMENT_DEPTH,
    constants.COMMENT_CREATED_TIMESTAMP,
    constants.AUTHOR_USERNAME,
    constants.COMMENT_TEXT_CONTENT
]

# %%
# Downloading posts...
# ====================
# 
# Some important points:
# 
# * If author is deleted, the author attribute would not be present. Hence, there is a check
#   for this.
# * For suspended author, PRAW does not return `created_utc`
# * `permalink_prefix + post.permalink` is to add domain name in permalink:
#       For example:
#       permalink returned by PRAW:
#       - /r/srilanka/comments/uketjy/sri_lankan_and_proud/
#       Conacting to permalink_prefix will give:
#       - https://www.reddit.com/r/srilanka/comments/uketjy/sri_lankan_and_proud/
#
print("Starting downloading posts...")
post_data = []
with Progress() as progress:
    i=0
    task1 = progress.add_task("Downloading posts....", total=post_limit)
    for post in sub_reddit.top(limit=post_limit):
        author = post.author
        post_data.append([
            post.id, post.title, permalink_prefix + post.permalink, post.url, post.score,
            post.num_comments, post.created_utc, post.subreddit.display_name, post.upvote_ratio,
            author.name if author is not None else pd.NA,
            author.total_karma if author is not None and hasattr(author, 'total_karma') else pd.NA,
            (utc_timestamp - author.created_utc)/86400 if author is not None and hasattr(author, 'created_utc') else pd.NA,
            determine_post_type(post), post.selftext
        ])
        i+=1
        progress.update(task1, advance=1, description=f'Downloaded post {i}')

post_data = pd.DataFrame(post_data, columns=post_headers)
post_data.to_csv(os.path.join(post_dir, "posts.csv"), index=False)
post_ids = post_data.iloc[:,0]
del post_data

# %%
# Downloading comments for each post...
# =====================================
# 
# Some important points:
# 
# * If author is deleted, the author attribute would not be present. Hence, there is a check
#   for this.
#
print("Starting downloading comments...")
with Progress() as progress:
    i=0
    task1 = progress.add_task("Downloading comments....", total=post_limit)
    for post_id in post_ids:
        comment_data = []
        post = scrapper.submission(post_id)
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comment_data.append([
                comment.id, comment.parent_id, comment.score,
                comment.depth, comment.created_utc,
                comment.author.name if comment.author is not None else pd.NA, comment.body
            ])
        comment_data = pd.DataFrame(comment_data, columns=comment_headers)
        comment_data.to_csv(os.path.join(comments_dir, f"{post_id}.csv"), index=False)
        del comment_data
        i+=1
        progress.update(task1, advance=1, description=f'Downloaded comments for post {i}')
