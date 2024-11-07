import praw

# Step 1: Reddit API Authentication
reddit = praw.Reddit(
    client_id="cxPOHYcA9qxAi-uEJu06GA",         # Replace with your client ID
    client_secret="iaZ-dBUpFQ4uSuYuqvVCW041qKNu9w", # Replace with your client secret
    user_agent="TrendingTopicsFinder by /u/mlvrkhn"  # Replace with your Reddit username
)

# Step 2: Function to Get Trending Topics from a Subreddit
def get_trending_topics(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    trending_posts = subreddit.top(time_filter="day", limit=limit)
    results = []

    for post in trending_posts:
        results.append({
            "title": post.title,
            "upvotes": post.score,
            "comments": post.num_comments,
            "url": post.url,
            "selftext": post.selftext
        })

    return results

# Step 3: Function to Filter for Pain Points
def find_pain_points(posts):
    keywords = ["help", "issue", "problem", "struggling", "frustration", "need advice", "can't", "anyone know"]
    pain_points = []

    for post in posts:
        title_text = post["title"].lower()
        body_text = post["selftext"].lower()
        
        if any(keyword in title_text for keyword in keywords) or any(keyword in body_text for keyword in keywords):
            pain_points.append(post)

    return pain_points

# Step 4: Main Script to Collect Pain Points from Multiple Subreddits
def main():
    # List of subreddits to analyze for trending topics and potential issues
    subreddits = ["learnprogramming", "entrepreneur", "smallbusiness", "personalfinance", "marketing", "sales", "business"]
    all_trending_issues = []

    for sub in subreddits:
        print(f"Searching trending topics in r/{sub}...")
        posts = get_trending_topics(sub)
        issues = find_pain_points(posts)
        all_trending_issues.extend(issues)
    
    # Sort issues by number of upvotes in descending order
    all_trending_issues.sort(key=lambda x: x['upvotes'], reverse=True)
    
    # Display results
    print("\nTrending Pain Points Across Subreddits (Sorted by Upvotes):")
    for issue in all_trending_issues:
        print(f"Title: {issue['title']}")
        print(f"Upvotes: {issue['upvotes']}, Comments: {issue['comments']}")
        print(f"URL: {issue['url']}")
        print(f"Description: {issue['selftext'][:200]}...")  # Print a snippet of the post
        print("=" * 80)

if __name__ == "__main__":
    main()