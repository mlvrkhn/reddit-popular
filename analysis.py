from openai import OpenAI, RateLimitError
import json
from config import OPENAI_API_KEY

def analyze_post_with_llm(post_data):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""
    Analyze this Reddit post for business potential:
    Title: {post_data['title']}
    Content: {post_data['selftext'][:1000]}
    
    Please evaluate on these criteria and provide a score (1-10) for each:
    1. Problem Validation: How clear and significant is the problem?
    2. Market Size: Estimate of potential market size and reach
    3. Competition: Level of existing solutions (1=saturated, 10=blue ocean)
    4. Implementation Feasibility: How feasible is it to build a solution?
    5. Monetization Potential: Clear path to revenue
    
    Provide a brief analysis for each criterion and an overall recommendation.
    Format response as JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return json.loads(response.choices[0].message.content)
    except OpenAI.RateLimitError:
        print("Rate limit exceeded. Please check your OpenAI quota and billing status.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None