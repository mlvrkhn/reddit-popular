from huggingface_hub import InferenceClient
import json
from datetime import datetime
import fpdf
import os

from config import HUGGINGFACE_TOKEN

class ContentSummarizer:
    def __init__(self, token=None):
        self.client = InferenceClient(
            model="facebook/bart-large-cnn",
            token=HUGGINGFACE_TOKEN
        )
    
    def summarize_text(self, text, max_length=500):
        if not text or len(text) < 200:  # Don't summarize short texts
            return text
            
        summary = self.client.text_generation(
            prompt=text,
            max_new_tokens=max_length,
            temperature=0.3
        )
        return summary
        
    def summarize_post(self, post):
        """Summarize both post content and comments"""
        summarized_content = self.summarize_text(post["selftext"])
        return {
            "title": post["title"],
            "selftext": summarized_content,
            "upvotes": post.get("upvotes", 0),
            "comments": post.get("comments", 0)
        }

class BusinessAnalyzer:
    def __init__(self, hf_token=None):
        self.client = InferenceClient(
            model="sshleifer/distilbart-cnn-12-6",
            token=HUGGINGFACE_TOKEN
        )
        self.summarizer = ContentSummarizer(token=HUGGINGFACE_TOKEN)
    
    def _create_analysis_prompt(self, post):
        return f"""
        Title: {post['title']}
        Content: {post['selftext'][:500]}
        
        Please evaluate on these criteria and provide a score (1-10) for each:
        1. Problem Validation: How clear and significant is the problem?
        2. Market Size: Estimate of potential market size and reach
        3. Competition: Level of existing solutions (1=saturated, 10=blue ocean)
        4. Implementation Feasibility: How feasible is it to build a solution?
        5. Monetization Potential: Clear path to revenue
        
        Provide a brief analysis for each criterion and an overall recommendation.
        Format response as JSON with the following structure:
        {{
            "problem": {{"score": number, "analysis": "text"}},
            "market": {{"score": number, "analysis": "text"}},
            "competition": {{"score": number, "analysis": "text"}},
            "feasibility": {{"score": number, "analysis": "text"}},
            "monetization": {{"score": number, "analysis": "text"}},
            "overall_recommendation": "text"
        }}
        """
    
    def _parse_response(self, response_text):
        """Clean and parse the LLM response"""
        response_text = str(response_text).strip()
        
        # Clean up JSON response
        if not response_text.startswith('{'): 
            start_idx = response_text.find('{')
            if start_idx != -1:
                response_text = response_text[start_idx:]
        if not response_text.endswith('}'):
            end_idx = response_text.rfind('}')
            if end_idx != -1:
                response_text = response_text[:end_idx+1]
        
        return json.loads(response_text)
    
    def _generate_pdf(self, post_data, analysis_results, total_score):
        """Generate PDF report"""
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        
        # Header
        pdf.cell(0, 10, "Business Idea Analysis Report", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
        
        # Post Details
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reddit Post", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, f"Title: {post_data['title']}")
        pdf.multi_cell(0, 10, f"Content: {post_data['selftext'][:500]}...")
        
        # Analysis Results
        categories = {
            "problem": "Problem Validation",
            "market": "Market Size",
            "competition": "Competition Analysis",
            "feasibility": "Implementation Feasibility",
            "monetization": "Monetization Potential"
        }
        
        for category, title in categories.items():
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"{title} - Score: {analysis_results[category]['score']}/10", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, analysis_results[category]['analysis'])
            pdf.cell(0, 5, "", ln=True)
        
        # Overall Results
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Total Score: {total_score:.1f}/10", ln=True)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Overall Recommendation:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, analysis_results['overall_recommendation'])
        
        return pdf
    
    def analyze_post(self, post_data):
        """Main analysis method"""
        try:
            # First summarize the post
            summarized_post = self.summarizer.summarize_post(post_data)
            
            # Generate and get LLM analysis
            prompt = self._create_analysis_prompt(summarized_post)
            response = self.client.text_generation(
                prompt,
                max_new_tokens=1000,
                temperature=0.7
            )
            
            # Parse response
            parsed_response = self._parse_response(response)
            
            # Calculate total score
            scores = [parsed_response[cat]["score"] for cat in ["problem", "market", "competition", "feasibility", "monetization"]]
            total_score = sum(scores) / len(scores) if scores else 0
            
            # Generate PDF
            pdf = self._generate_pdf(summarized_post, parsed_response, total_score)
            
            # Save PDF
            research_dir = "market_research"
            if not os.path.exists(research_dir):
                os.makedirs(research_dir)
            
            filename = f"business_ideas_reddit_{datetime.now().strftime('%Y%m%d')}.pdf"
            pdf_path = os.path.join(research_dir, filename)
            pdf.output(pdf_path)
            
            return {
                "post_data": summarized_post,
                "analysis": parsed_response,
                "total_score": total_score,
                "pdf_path": pdf_path
            }
            
        except Exception as e:
            print(f"Analysis failed: {str(e)}")
            return {"post_data": post_data, "analysis": None}