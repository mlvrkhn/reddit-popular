from reddit_api import authenticate_reddit, get_trending_topics
from analysis import analyze_post_with_llm
from config import KEYWORDS
import json
from datetime import datetime

def find_pain_points(posts):
    pain_points = []
    for post in posts:
        title_text = post["title"].lower()
        body_text = post["selftext"].lower()
        
        if any(keyword in title_text for keyword in KEYWORDS) or any(keyword in body_text for keyword in KEYWORDS):
            pain_points.append(post)

    return pain_points

def generate_market_research_report(analyzed_posts):
    report = []
    for post in analyzed_posts:
        analysis = analyze_post_with_llm(post)
        report.append({
            "post_data": post,
            "analysis": analysis,
            "total_score": sum(analysis.values()) / 5 if isinstance(analysis, dict) else 0
        })
    return report

def save_report(report, filename=None):
    if filename is None:
        filename = f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)
    return filename

def main():
    reddit = authenticate_reddit()
    subreddits = ["startups", "entrepreneur", "smallbusiness", "SaaS", "business"]
    all_trending_posts = []

    for sub in subreddits:
        print(f"Analyzing r/{sub}...")
        posts = get_trending_topics(reddit, sub, limit=5)
        all_trending_posts.extend(posts)
    
    # Filter for pain points first
    pain_points = find_pain_points(all_trending_posts)
    print(f"\nFound {len(pain_points)} posts containing pain points...")
    
    # Only analyze the pain points
    print("\nGenerating market research report...")
    analyzed_posts = generate_market_research_report(pain_points)
    analyzed_posts.sort(key=lambda x: x['total_score'], reverse=True)
    filename = save_report(analyzed_posts)
    
    print("\nMarket Research Report Summary:")
    for post in analyzed_posts:
        print(f"\nTitle: {post['post_data']['title']}")
        print(f"Total Score: {post['total_score']:.2f}/10")
        print(f"Analysis Highlights:")
        for criterion, score in post['analysis'].items():
            print(f"- {criterion}: {score}")
        print("=" * 80)
    
    print(f"\nFull report saved to: {filename}")

if __name__ == "__main__":
    main() 