import os
import datetime
import time
import random
import google.generativeai as genai
from google.api_core import exceptions

# Configure Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def get_existing_topics():
    # Listing existing files to avoid duplicates
    posts_dir = "_posts"
    if not os.path.exists(posts_dir):
        return []
    return [f for f in os.listdir(posts_dir) if f.endswith('.md') or f.endswith('.markdown')]

def generate_with_retry(model, prompt, max_retries=5, initial_delay=10):
    """
    Wraps the generation call with a retry loop that handles 429 Rate Limit errors.
    Waits longer after each failure (Exponential Backoff).
    """
    for attempt in range(max_retries):
        try:
            return model.generate_content(prompt)
        except exceptions.ResourceExhausted:
            # Calculate wait time: 10s, 20s, 40s... + random jitter to avoid synchronized retries
            wait_time = (initial_delay * (2 ** attempt)) + random.uniform(0, 5)
            print(f"⚠️ Quota exceeded. Retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{max_retries})")
            time.sleep(wait_time)
        except Exception as e:
            # If it's another error (like Auth), fail immediately
            print(f"❌ Unexpected error: {e}")
            raise e
            
    raise Exception("Failed to generate content after maximum retries due to quota limits.")

def generate_blog_post():
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    existing_files = get_existing_topics()
    
    # 1. Ideation & Writing Prompt
    prompt = f"""
    You are the content strategist for 'hmpgr', a B2B website audit tool.
    Brand Voice: Clear, confident, helpful, growth-oriented. No jargon.
    Target Audience: B2B SaaS founders and marketing managers.
    Goal: Teach them how to optimize their homepage for conversion.
    
    Existing posts: {existing_files[-5:]} (Do not repeat these exact topics)

    Task:
    1. Generate a unique, high-impact topic about B2B homepage optimization.
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

    # Use the new retry function here
    response = generate_with_retry(model, prompt)
    content = response.text
    
    # Clean up markdown code blocks if the AI added them
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
        # Basic slug cleaning
        slug = "".join([c for c in slug if c.isalnum() or c == '-'])
    except:
        slug = "weekly-insight"

    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"_posts/{date_str}-{slug}.markdown"
    
    # Ensure directory exists
    os.makedirs("_posts", exist_ok=True)
    
    with open(filename, "w") as f:
        f.write(content)
    
    print(f"✅ Generated post: {filename}")

if __name__ == "__main__":
    post_content = generate_blog_post()
    save_post(post_content)