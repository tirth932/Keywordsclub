import re
from datetime import datetime

import openai


SYSTEM_PROMPT = (
    "You are a professional blog writer. Write in plain text only: no markdown "
    "symbols (no #, *, or ---), no HTML tags, and no placeholders like [Insert Date] "
    "or [Your Name]. Start with the blog title on its own line, use short section "
    "headings on their own lines, and separate paragraphs with blank lines."
)


def clean_blog_content(blog_post):
    """Normalize model output into clean plain text."""
    # Convert stray <br> tags to newlines
    blog_post = re.sub(r'<br\s*/?>', '\n', blog_post)
    # Remove horizontal-rule lines
    blog_post = re.sub(r'\n\s*---+\s*\n', '\n', blog_post)
    # Strip markdown bold/heading markers if the model slips them in
    blog_post = re.sub(r'\*\*', '', blog_post)
    blog_post = re.sub(r'^#+\s*', '', blog_post, flags=re.MULTILINE)
    # Replace any remaining bracket placeholders; fill date-like ones first
    current_date = datetime.now().strftime('%B %d, %Y')
    blog_post = re.sub(r'\[\s*(insert\s+)?date\s*\]', current_date, blog_post, flags=re.IGNORECASE)
    blog_post = re.sub(r'\[.*?\]', '', blog_post)
    # Drop empty byline/date lines left behind
    blog_post = re.sub(r'^(By|Date):\s*$', '', blog_post, flags=re.MULTILINE)
    # Collapse extra blank lines
    blog_post = re.sub(r'\n\s*\n', '\n\n', blog_post)
    return blog_post.strip()


def create_blog_post_(api_key, keyword, num_words):
    openai.api_key = api_key

    if num_words:
        user_prompt = (
            f"Write a concise, well-structured blog post about '{keyword}' of roughly "
            f"{int(num_words)} words. Make it engaging and informative, and end with a "
            "section titled 'Conclusion'."
        )
    else:
        user_prompt = (
            f"Write a concise, well-structured blog post about '{keyword}'. Make it "
            "engaging and informative, and end with a section titled 'Conclusion'."
        )

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            max_tokens=2000,
        )

        blog_post = response.choices[0].message.content
        cleaned_blog_post = clean_blog_content(blog_post)

        # If generation was cut off mid-sentence after the conclusion, trim to the last full stop
        last_full_stop_index = cleaned_blog_post.rfind('.')
        conclusion_index = cleaned_blog_post.lower().find("conclusion")
        if conclusion_index != -1 and last_full_stop_index > conclusion_index:
            cleaned_blog_post = cleaned_blog_post[:last_full_stop_index + 1]

        return cleaned_blog_post

    except Exception as e:
        raise Exception(f"Error generating blog post: {str(e)}")
