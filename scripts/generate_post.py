import os
import datetime
import time
import random
import google.generativeai as genai
from google.api_core import exceptions

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- CONFIGURATION ---
# Updated path to point to docs/_posts
POSTS_DIR = "docs/_posts" 
# Using the stable model for Dec 2025
MODEL_NAME = "gemini-2.5-flash-lite" 
# ---------------------

def get_existing_topics():
    # Check the new docs/_posts directory
    if not os.path.exists(POSTS_DIR):
        return []
    return [f for f in os.listdir(POSTS_DIR) if f.endswith('.md') or f.endswith('.markdown')]

def generate_with_retry(model, prompt, max_retries=5, initial_delay=10):
    """
    Wraps the generation call with a retry loop that handles 429 Rate Limit errors.
    """
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except exceptions.ResourceExhausted:
            wait_time = (initial_delay * (2 ** attempt)) + random.uniform(0, 5)
            print(f"⚠️ Quota exceeded. Retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise e
            
    raise Exception("Failed to generate content after maximum retries due to quota limits.")

def generate_blog_post():
    model = genai.GenerativeModel(MODEL_NAME)
    
    existing_files = get_existing_topics()
    
    prompt = f"""
    You are the content strategist for 'hmpgr', a B2B website audit tool.
    Brand Voice: Clear, confident, helpful, growth-oriented. No jargon.
    Target Audience: B2B SaaS founders, marketing managers, Small busuness owners.
    Goal: Teach them how to optimize their website for conversion.
    
    Existing posts (to avoid): {existing_files[-5:]}

    Task:
    1. Generate a unique, high-impact topic about B2B website optimization.
    2. Write a full blog post in Jekyll Markdown format.
    3. Use the following Front Matter structure exactly:
    ---
    layout: post
    title: "Your Benefit-Driven Title Here"
    date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    categories: [conversion, growth]
    ---
    
    Body Requirements:
    - Use H2 (##) and H3 (###) for structure.
    - Keep sentences short.
    - Focus on "Actionable advice".
    - Include a specific "Pro Tip" section.
    - End with a call to action to use the free audit tool at hmpgr.com.
    """

    response = generate_with_retry(model, prompt)
    content = response.text
    
    # Clean up markdown code blocks
    if content.startswith("```markdown"):
        content = content.replace("```markdown", "").replace("```", "")
    elif content.startswith("```"):
        content = content.replace("```", "")
    
    return content

def save_post(content):
    # Extract title for filename
    try:
        title_line = [line for line in content.split('\n') if line.startswith('title:')][0]
        title = title_line.split('"')[1]
        slug = title.lower().replace(' ', '-').replace(':', '').replace('?', '')
        slug = "".join([c for c in slug if c.isalnum() or c == '-'])
    except:
        slug = "weekly-insight"

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{POSTS_DIR}/{date_str}-{slug}.markdown"
    
    # Ensure directory exists (docs/_posts)
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    with open(filename, "w") as f:
        f.write(content)
    
    print(f"✅ Generated post: {filename}")

if __name__ == "__main__":
    try:
        post_content = generate_blog_post()
        save_post(post_content)
    except Exception as e:
        print(f"⚠️ Skipped generation due to error: {e}")
        # Exit with 0 so workflow doesn't fail on API glitches
        exit(0)
