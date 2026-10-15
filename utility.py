#pip install google-genai
from google import genai

api_key="AQ.Ab8RN6I3UQF_UNmkLylTwj553RjGyN0IhVbEkrd2qqT3MmsuMQ"

# step1 : authenticate

client = genai.Client(api_key=api_key)


prompt = "what is ai agent in simple words"

response = client.models.generate_content(

    model = "gemini-3.5-flash",
    contents=prompt
)

print(response.text)