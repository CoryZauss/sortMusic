import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY= os.getenv("AUDD_KEY")
API_URL = "https://api.audd.io/"

if not API_KEY:
    raise ValueError("API key is missing! Check your .env file.")

def identify(file):
    with open(file, "rb") as song:
        files = {"file": song} #attatch file
        data = {"api_token": API_KEY}

        response = requests.post(API_URL, files=files, data=data)

        try:
            response.raise_for_status() #raise error for bad http resp
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR in identify(): {e}")
            return None
   
