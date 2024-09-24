import os
import requests
import uuid
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN_URL = 'https://auth.vectara.io/oauth2/token'  # Replace with your token URL

# Set up OpenAI API key
API_KEY = os.getenv('VECTARA_API_KEY')
CORPUS_ID = 'degenradar'
UPLOAD_URL = f'https://api.vectara.io/v2/corpora/{CORPUS_ID}/upload_file'
QUERY_URL = f'https://api.vectara.io/v2/corpora/{CORPUS_ID}/query'

boundary = str(uuid.uuid4())

def get_access_token():
    # Prepare the data for the token request
    data = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }

    # Make the POST request to get the token
    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        return response_data['access_token']
    else:
        raise Exception("Failed to retrieve access token. Response: {}".format(response_data))
