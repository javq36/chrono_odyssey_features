import praw
import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')

def fetch_all_posts(subreddit_name, limit=1000):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.new(limit=limit):
        posts.append({
            'id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'url': post.url
        })
    return posts

def filter_posts_by_topics(posts):
    topics = ['gameplay', 'combat', 'economy', 'skills', 'quests', 'modes', 'features']
    filtered = []
    for post in posts:
        text = (post.get('title', '') + ' ' + post.get('selftext', '')).lower()
        if any(topic in text for topic in topics):
            filtered.append(post)
    return filtered