import praw
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

def authenticate_reddit():
    return praw.Reddit(
client_id="cxPOHYcA9qxAi-uEJu06GA",         
    client_secret="iaZ-dBUpFQ4uSuYuqvVCW041qKNu9w", 
    user_agent="TrendingTopicsFinder by /u/mlvrkhn"  
    )

def get_trending_topics(reddit, subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    trending_posts = subreddit.top(time_filter="day", limit=limit)
    results = []

    for post in trending_posts:
        results.append({
            "title": post.title,
            "upvotes": post.score,
            "comments": post.num_comments,
            "url": post.url,
            "selftext": post.selftext,
            "created_utc": post.created_utc
        })

    return results 