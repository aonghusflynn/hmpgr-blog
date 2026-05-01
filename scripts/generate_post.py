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
MODEL_NAME = "gemini-3-flash-preview" 
# ---------------------

def get_existing_topics():
    # Check the new docs/_posts directory
    if not os.path.exists(POSTS_DIR):
        return []
    return [f for f in os.listdir(POSTS_DIR) if f.endswith('.md') or f.endswith('.markdown')]

HUMANIZER_RULES = """
You are an editor that removes signs of AI-generated writing without
changing the structure, frontmatter, code blocks, or internal links of
the input post.

Apply these rules:

1. Headings: convert any Title Case heading to sentence case (the
   Jekyll frontmatter `title:` field stays Title Case — never touch it).
2. Strip AI vocabulary: testament, pivotal, vibrant, leverage, robust,
   transform, foster, garner, intricate, tapestry, landscape (figurative),
   showcase, underscore, key (adj), enduring, seamless, holistic,
   cutting-edge, world-class, best-in-class, game-changing.
3. Drop superficial -ing tail clauses (e.g. "highlighting...", "ensuring...",
   "reflecting...", "contributing to...") that pad a sentence with no
   new information.
4. Replace "It's not just X, it's Y" / "X isn't about A, it's about B"
   negative-parallelism patterns with a direct positive statement.
5. Remove inflated significance language: "marks a pivotal moment",
   "in the heart of", "stands as a testament", "shapes the future of".
6. No promotional / advertisement-like language: "boasts", "nestled",
   "breathtaking", "must-have", "revolutionary", "groundbreaking".
7. Use is/are/has — avoid copula avoidance ("serves as", "stands as",
   "represents a").
8. Trim filler: "in order to" → "to", "due to the fact that" → "because",
   "at this point in time" → "now".
9. Cut chatbot artifacts: "I hope this helps", "Let me know", "Of course!",
   "Great question!", "Here is...".
10. Cut em dashes where a comma or period reads cleaner. Don't replace
    every dash; just the ones that feel decorative.
11. Don't force three of everything. If a list of three is padding, cut
    it to two or merge into a sentence.
12. Use straight quotes, not curly quotes.
13. Vary sentence length. Short sentences are fine. Mix them with longer ones.
14. Preserve: the YAML frontmatter (everything between the first two `---`
    lines), all code blocks, all markdown links and image references,
    section structure, and the overall meaning.

Return the edited post in full, with the frontmatter unchanged. Do not
wrap the output in a code fence. Do not add any commentary before or
after.
"""


def humanize_content(model, content):
    """
    Second pass: takes a generated post and rewrites it to remove
    AI writing tells. Falls back to the original draft if the
    humanizer call fails for any reason.
    """
    prompt = f"{HUMANIZER_RULES}\n\n--- POST TO EDIT ---\n{content}"
    try:
        response = generate_with_retry(model, prompt)
        humanized = response.text

        # Strip a code fence the model may add despite the instruction.
        if humanized.startswith("```markdown"):
            humanized = humanized.replace("```markdown", "").replace("```", "")
        elif humanized.startswith("```"):
            humanized = humanized.replace("```", "")

        # Sanity check: must still have frontmatter. If the model dropped
        # it, fall back to the original.
        if not humanized.lstrip().startswith("---"):
            print("⚠️ Humanizer output missing frontmatter — using original draft.")
            return content

        print("✨ Humanizer pass complete.")
        return humanized.strip() + "\n"
    except Exception as e:
        print(f"⚠️ Humanizer pass failed ({e}) — using original draft.")
        return content


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
    Target Audience: B2B SaaS founders, marketing managers, Small business owners.
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
        model = genai.GenerativeModel(MODEL_NAME)
        post_content = generate_blog_post()
        post_content = humanize_content(model, post_content)
        save_post(post_content)
    except Exception as e:
        print(f"⚠️ Skipped generation due to error: {e}")
        # Exit with 0 so workflow doesn't fail on API glitches
        exit(0)
