# from langchain_huggingface import HuggingFaceEndpoint
# import re
#
# def keyword_fetch_(endpoint_url, secretkey, Keywords):
#     llm = HuggingFaceEndpoint(endpoint_url=endpoint_url, huggingfacehub_api_token=secretkey)
#     game= llm.invoke(f"find suitable keywords similar to and please just response in list only not any type of string : {Keywords}")
#     game = re.sub(r'<br\s*/?>', '\n', game)
#     game = game.strip()
#
#     return game

# repo_id="Qwen/Qwen2.5-Coder-32B-Instruct"
# sec_key="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"
# artical = """ article """
# print(keyword_fetch_(repo_id, sec_key, artical))


# OLD PROMPT
# suggest keywords based on this sentence
# from langchain_huggingface import HuggingFaceEndpoint
#
#
# def keyword_fetch_(endpoint_url, secretkey, Keywords):
#     llm = HuggingFaceEndpoint(endpoint_url=endpoint_url, huggingfacehub_api_token=secretkey)
#     raw_response = llm.invoke(
#         f"find suitable keywords similar to and please just response in list only not any type of string : {Keywords}")
#
#     # Filter out empty strings, None values, or whitespace-only entries
#     keywords = [kw.strip() for kw in raw_response if kw and kw.strip()]
#
#     return keywords
# from langchain_huggingface import HuggingFaceEndpoint
# import ast  # Safely convert string to list
#
#
# def keyword_fetch_(endpoint_url, secretkey, keywords):
#     """
#     Fetches suitable keywords from the HuggingFaceEndpoint based on the given input.
#
#     Args:
#         endpoint_url (str): The endpoint URL for the HuggingFace model.
#         secretkey (str): The API token for authentication.
#         keywords (str): Input keywords or sentence to base suggestions on.
#
#     Returns:
#         list: A list of clean, suitable keywords.
#     """
#     llm = HuggingFaceEndpoint(endpoint_url=endpoint_url, huggingfacehub_api_token=secretkey)
#
#     # Clear, concise prompt for strict response formatting
#     prompt = (
#         f"Provide a list of keywords similar to '{keywords}'. "
#         "Respond strictly as a Python list, with no extra text or explanation."
#     )
#
#     try:
#         # Invoke the model
#         raw_response = llm.invoke(prompt)
#         print("Raw Response:", raw_response)  # Debugging log
#
#         # Step 1: Validate if the response is already a list
#         if isinstance(raw_response, list):
#             clean_keywords = [kw.strip() for kw in raw_response if kw and kw.strip()]
#         elif isinstance(raw_response, str):
#             # Step 2: Safely convert string response into a Python list
#             try:
#                 parsed_response = ast.literal_eval(raw_response)
#                 if isinstance(parsed_response, list):
#                     clean_keywords = [kw.strip() for kw in parsed_response if kw and kw.strip()]
#                 else:
#                     raise ValueError("Response is not in a valid list format.")
#             except (SyntaxError, ValueError):
#                 raise ValueError("Failed to parse string response into a list.")
#         else:
#             raise ValueError("Unexpected response format.")
#
#         return clean_keywords
#
#     except Exception as e:
#         print(f"Error: {e}")
#         return []  # Return empty list on failure
#
#
# # Example usage
# if __name__ == "__main__":
#     endpoint_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-32B-Instruct"
#     secretkey = "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"
#     article = "Artificial Intelligence in healthcare has revolutionized diagnostics and treatment plans."
#
#     keywords = keyword_fetch_(endpoint_url, secretkey, article)
#     print("Extracted Keywords:", keywords)


import openai
import re


def keyword_fetch_(api_key,Keywords):
    openai.api_key = api_key

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Or "gpt-4-mini" if that's your specific model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Find suitable keywords similar to: {Keywords}. Please respond only with a list of keywords , no additional text."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        game = response.choices[0].message.content
        game = re.sub(r'<br\s*/?>', '\n', game)  # Handle any line breaks if present
        game = re.sub(r'\d+\.', '', game)  # Remove numbers preceding the keywords (e.g., 1. keyword)
        game = re.sub(r'\n+', '\n', game)  # Remove extra new lines
        game = game.strip()
        # Split the cleaned response into individual keywords and return them as a list
        # keywords = game.split(",\n")
        #
        #
        # # Ensure no keyword is empty
        # keywords = [keyword.strip() for keyword in keywords if keyword.strip()]
        if "," in game:
            keywords = [kw.strip() for kw in game.split(",") if kw.strip()]
        else:
            keywords = [kw.strip() for kw in game.split("\n") if kw.strip()]

            # Format keywords with a dash and newline
        formatted_keywords = "\n".join(f" {kw}" for kw in keywords)
        print(formatted_keywords)
        print(game)
        return formatted_keywords

        # return game
    except Exception as e:
        raise Exception(f"Error fetching keywords: {str(e)}")

