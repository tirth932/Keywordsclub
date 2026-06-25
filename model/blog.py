import re
from datetime import datetime


# Function to clean the blog content
def clean_blog_content(blog_post):
    # Remove <br> and other line breaks
    blog_post = re.sub(r'<br\s*/?>', '\n', blog_post)
    # Remove unnecessary "---" lines
    blog_post = re.sub(r'\n\s*---\s*\n', '\n', blog_post)
    # Remove bold formatting (**)
    blog_post = re.sub(r'\*\*', '', blog_post)
    # Remove hashtags (#)
    blog_post = re.sub(r'#', '', blog_post)
    # Remove leading and trailing whitespace
    blog_post = blog_post.strip()
    # Get the current date in the desired format
    current_date = datetime.now().strftime('%B %d, %Y')
    blog_post = blog_post.replace("[Insert Date]", current_date)

    # Define a default journalist name
    journalist_name = "CricketChronicles"
    # Remove placeholder patterns like [Insert Date] and [Your Name]
    blog_post = re.sub(r'\[.*?\]', '', blog_post)

    #Replace [Insert Date] or Date: with the current date
    if not re.search(r'Date:\s*\w+', blog_post):  # If 'Date:' is not already present
        # Replace [Insert Date] or Date: with the current date
        # blog_post = re.sub(r'\[.*?\]', '', blog_post)
        blog_post = re.sub(r'Date:\s*', f"Date: {current_date}\n", blog_post, count=1)

    # Replace [Your Name] or By: with the journalist's name
    blog_post = re.sub(r'By:\s*', f"By: {journalist_name}\n", blog_post)
    # Remove extra blank lines

    blog_post = re.sub(r'\n\s*\n', '\n\n', blog_post)
    return blog_post



import openai


def create_blog_post_(api_key,keyword,num_words):
    openai.api_key = api_key

    try:
        # Generate the blog post using the model
        if num_words == "":
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # Replace with your desired OpenAI model
                messages=[
                    {"role": "system", "content": "You are a professional blog writer."},
                    {"role": "user", "content": f"Write a concise, well-structured blog post about '{keyword}'. Ensure it is engaging, informative, and formatted as a blog post."}
                ],
                temperature=0.7,
                max_tokens=2000  # Adjust the limit based on the API and content needs
            )
        else:
            num_words = int(num_words)
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional blog writer."},
                    {"role": "user", "content": f"Write a concise, well-structured blog post about '{keyword}' containing only {num_words} words. Ensure it is engaging, informative, and formatted as a blog post. End the blog with a section titled 'Conclusion.'"}
                ],
                temperature=0.7,
                max_tokens=2000
            )

        # Extract content from the response
        blog_post = response.choices[0].message.content

        # Clean the generated blog content
        cleaned_blog_post = clean_blog_content(blog_post)

        # Find the position of the last full stop in the cleaned content
        # last_full_stop_index = cleaned_blog_post.rfind('.')
        # if last_full_stop_index != -1:
        #     cleaned_blog_post = cleaned_blog_post[:last_full_stop_index + 1]
        #     conclusion_index = cleaned_blog_post.lower().find("conclusion")
        #     if conclusion_index != -1:
        #         cleaned_blog_post = cleaned_blog_post[:conclusion_index]
        last_full_stop_index = cleaned_blog_post.rfind('.')
        conclusion_index = cleaned_blog_post.lower().find("conclusion")

        if conclusion_index != -1 and last_full_stop_index > conclusion_index:
            # Find the last full stop after the "conclusion" word
            cleaned_blog_post = cleaned_blog_post[:last_full_stop_index + 1]

        # Print the cleaned blog post
        print("Cleaned Blog Post:\n", cleaned_blog_post)
        return cleaned_blog_post

    except Exception as e:
        raise Exception(f"Error generating blog post: {str(e)}")


# def clean_blog_content(content):
#     """Clean and format the blog content."""
#     # Example cleaning: remove redundant spaces, line breaks, or tags
#     content = re.sub(r'\s+', ' ', content)  # Normalize spaces
#     content = content.strip()  # Remove trailing and leading whitespace
#     return content




