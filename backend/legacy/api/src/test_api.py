import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://ollama.monynha.me/generate?prompt=Tell me about Python"
headers = {"x-api-key": os.getenv("API_KEY"), "Content-Type": "application/json"}

response = requests.post(url, headers=headers)
print(response.json())
