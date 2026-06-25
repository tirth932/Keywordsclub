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

