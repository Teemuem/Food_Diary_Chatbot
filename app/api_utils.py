# api_utils.py
import requests
import urllib.parse
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to fetch nutrient data for a given food query
def fetch_nutrient_data(query):
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    encoded_query = urllib.parse.quote(query)
    headers = {'X-Api-Key': os.getenv("X_API_KEY")}  # Use the API key from .env
    response = requests.get(api_url + encoded_query, headers=headers)
    
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        st.error(f"API error: {response.status_code} - {response.text}")
        return None