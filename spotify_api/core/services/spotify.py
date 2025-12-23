import base64
import os
import requests
from rest_framework.exceptions import APIException

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"


def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise APIException("Spotify credentials missing")

    auth_string = f"{client_id}:{client_secret}"
    auth_base64 = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response.raise_for_status()

    return response.json()["access_token"]


def get_spotify_search(query: str, type: str):
    token = get_spotify_token()

    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,
        "type": type,
        "limit": 10,
    }

    response = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise APIException("Spotify API error")

    return response.json()
