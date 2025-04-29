from dotenv import load_dotenv
load_dotenv()

import os
from openai import OpenAI

import pandas as pd
from api import predict_earthquake

LLAMA_API_KEY = os.environ.get("LLAMA_API_KEY")

client = OpenAI(
    api_key=LLAMA_API_KEY, 
    base_url="https://api.llama.com/compat/v1/"
)


def generate_post(prediction): 
    response = client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[
            {"role": "system", "content": "You are a Twitter agent that is trying to spread helpful information regarding upcoming earthquake that might be happening in the Turkey."},
            {"role": "user", "content": f"I will provide you with my model's prediction about a possible earthquake in Turkey. Generate me a post depending on how significant the magnitude might be in the given location. Search for the human readable location name of the latitude and longitude data. Keep the post short, keep it concise. Here is the prediction: {prediction}.\n\nDon't include anything else than the post itself in response. Don't include any code blocks, don't include any explanations, just the post. If the prediction is in a dangerous place like Istanbul, make sure to emphasize the post with Emojis and bullet points."},
        ],
        stream=False
    )

    return response.choices[0].message.content


potential_X = pd.DataFrame({'latitude': [3.92003453e+01], 
                       'longitude': [2.94687749e+01], 
                       'depth': [9.61804979e+00], 
                       'timestamp': [1.74597713e+09]})

post = generate_post(predict_earthquake(potential_X))
print(post)


def publish_post(post): 
    pass
