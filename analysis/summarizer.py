from huggingface_hub import InferenceClient
from config import HUGGINGFACE_TOKEN

class ContentSummarizer:
    def __init__(self, hf_token=None):
        self.client = InferenceClient(
            model="google/pegasus-xsum",
            token=HUGGINGFACE_TOKEN
        )
    
    def summarize_text(self, text, max_length=500):
        if not text or len(text) < 200:  # Don't summarize short texts
            return text
            
        response = self.client.summarization(
            text=text
        )
        return response["summary_text"]
        
    def summarize_post(self, post):
        """Summarize both post content and comments"""
        # Get post content, defaulting to empty string if 'selftext' is missing
        content = post.get("selftext", post.get("text", ""))  # try both common keys
        summarized_content = self.summarize_text(content) if content else ""
        
        return {
            "title": post.get("title", ""),
            "content": summarized_content,
            "upvotes": post.get("upvotes", 0),
            "comments_count": post.get("comments", 0)
        } 