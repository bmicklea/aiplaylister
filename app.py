from flask import Flask, redirect, request
import requests
import os
from urllib.parse import urlencode

app = Flask(__name__)

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://your-render-app-name.onrender.com/callback")

SCOPES = "playlist-modify-public playlist-modify-private"

@app.route("/")
def index():
    query = urlencode({
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES
    })
    auth_url = f"https://accounts.spotify.com/authorize?{query}"
    return f"<a href='{auth_url}'>Login with Spotify</a>"

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=payload, headers=headers)
    data = response.json()

    refresh_token = data.get("refresh_token")
    access_token = data.get("access_token")

    return f"""
    <h1>Success!</h1>
    <p><strong>Refresh Token:</strong></p>
    <code>{refresh_token}</code>
    <p><strong>Access Token (expires in 1hr):</strong></p>
    <code>{access_token}</code>
    <p>Copy your refresh token and send it to ChatGPT.</p>
    """