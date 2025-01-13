from openai import OpenAI
import dotenv
import os

dotenv.load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


def generate_response(input):
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"{input}"
            }
        ]
    )

    return completion.choices[0].message

