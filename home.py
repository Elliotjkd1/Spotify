from flask import Blueprint, render_template
from flask import request
import os
from dotenv import load_dotenv
from base64 import b64encode
import requests


def getAuth(code):
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    authOptions = {
        "url": "https://accounts.spotify.com/api/token",
        "headers": {
            "Authorization": "Basic " + b64encode((str(client_id) + ":" + str(client_secret)).encode("utf-8")).decode(
                "utf-8")
        },
        "form": {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000/home"
        },
        "json": True
    }

    authResponse = requests.post(authOptions["url"], headers=authOptions["headers"], data=authOptions["form"])
    if authResponse.status_code == 200:
        authToken = authResponse.json()["access_token"]
        return authToken
    else:
        print(authResponse.status_code)
        exit(1)


def get_user_top_tracks(auth_token):
    url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {
        "Authorization": "Bearer " + auth_token
    }
    params = {
        "time_range": "short_term"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data["items"]
    else:
        print("Failed to retrieve top tracks.")
        print("Status Code:", response.status_code)
        print("Response Content:", response.content)


home = Blueprint(__name__, "home")


# route is designed to handle a web request
@home.route("/")
def homeRoute():
    code = request.args.get('code')
    auth_token = getAuth(code)
    user_top_tracks = get_user_top_tracks(auth_token)
    return render_template("home.html", code=code, auth_token=auth_token, user_top_tracks=user_top_tracks)
