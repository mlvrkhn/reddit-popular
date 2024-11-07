# Reddit Trending Topics & Pain Points Analyzer

A Python script that analyzes multiple subreddits to identify trending topics and pain points based on user discussions.

## Features

- Fetches trending posts from multiple business and technology-related subreddits
- Identifies potential pain points using keyword analysis
- Sorts results by engagement (upvotes)
- Displays detailed information including post titles, upvotes, comments, and descriptions

## Prerequisites

- Python 3.6+
- PRAW (Python Reddit API Wrapper)

## Installation

1. Clone this repository: 
bash
git clone [your-repository-url]
```

2. Install the required Python packages:
```bash
pip install praw
```

3. Set up Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Create a new application (script)
   - Note your client_id and client_secret

## Configuration

Update the following values in `Program.py`:

```python
reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="YOUR_USER_AGENT"
)
```

## Usage

The script will output the trending topics and pain points across the specified subreddits, sorted by engagement.

## Monitored Subreddits

- r/learnprogramming
- r/entrepreneur
- r/smallbusiness
- r/personalfinance
- r/marketing
- r/sales
- r/business

## Output Format

For each identified pain point, the script displays:
- Post title
- Number of upvotes and comments
- Post URL
- Beginning of post content

## Customization

You can modify:
- The list of subreddits in the `main()` function
- Keywords for pain point detection in `find_pain_points()`
- Number of posts to analyze by changing the `limit` parameter in `get_trending_topics()`

## Security Note

Never commit your Reddit API credentials to version control. Consider using environment variables or a configuration file for sensitive data.

## License

MIT License

Copyright (c) 2024
