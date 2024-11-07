from reddit_api.reddit_api import authenticate_reddit, get_trending_topics
from analysis.summarizer import ContentSummarizer
from analysis.analyzer import BusinessAnalyzer
from config import KEYWORDS
import json
from datetime import datetime
import os

def find_pain_points(posts):
    pain_points = []
    keywords_set = set(keyword.lower() for keyword in KEYWORDS)
    
    for post in posts:
        combined_text = (post["title"] + " " + post["selftext"]).lower()
        
        if len(combined_text) < 100 or post["upvotes"] < 10:
            continue
            
        skip_phrases = {"help needed", "question", "how do i", "newbie"}
        if any(phrase in combined_text for phrase in skip_phrases):
            continue
        
        if any(keyword in combined_text for keyword in keywords_set):
            pain_points.append(post)

    return pain_points

def generate_market_research_report(pain_points):
    summarizer = ContentSummarizer()
    analyzer = BusinessAnalyzer()
    analyzed_posts = []
    
    sorted_posts = sorted(
        pain_points, 
        key=lambda x: (x["upvotes"] + x["comments"] * 2), 
        reverse=True
    )[:5]
    
    for post in sorted_posts:
        # First summarize
        summarized_post = summarizer.summarize_post(post)
        
        # Then analyze
        analysis = analyzer.analyze_post(summarized_post)
        if analysis and analysis.get("total_score", 0) >= 5:
            analyzed_posts.append(analysis)
            
    return analyzed_posts

def save_report(report, filename=None):
    # Create market_research directory if it doesn't exist
    os.makedirs('market_research', exist_ok=True)
    
    if filename is None:
        filename = f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    # Prepend the market_research directory to the filename
    filepath = os.path.join('market_research', filename)
    
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=4)
    return filepath

def main():
    reddit = authenticate_reddit()
    subreddits = ["startups", "entrepreneur", "SaaS"]
    all_trending_posts = []

    for sub in subreddits:
        print(f"Analyzing r/{sub}...")
        posts = get_trending_topics(reddit, sub, limit=3)
        all_trending_posts.extend(posts)
    
    pain_points = find_pain_points(all_trending_posts)
    print(f"\nFound {len(pain_points)} posts containing pain points...")
    
    print("\nGenerating market research report...")
    analyzed_posts = generate_market_research_report(pain_points)
    if analyzed_posts:
        analyzed_posts.sort(key=lambda x: x.get('total_score', 0), reverse=True)
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