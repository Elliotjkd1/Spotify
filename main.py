import os
from base64 import b64encode
import requests
from dotenv import load_dotenv


def getAuth():
    # Load environment variables from .env file
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
            "grant_type": "client_credentials"
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


def getArtistData(token):
    # url endpoint
    # https://developer.spotify.com/documentation/web-api/reference/get-an-artist
    artistUrl = "https://api.spotify.com/v1/artists/699OTQXzgjhIYAHMy9RyPD"
    # token auth
    headers = {
        "Authorization": "Bearer " + token
    }

    response = requests.get(artistUrl, headers=headers)
    if response.status_code == 200:
        artist_data = response.json()
        # Access and print artist information
        print("Artist Name:", artist_data["name"])
        print("Followers:", artist_data["followers"]["total"])
        print("Popularity:", artist_data["popularity"])
    else:
        print("Failed to retrieve artist data.")


def main():
    getArtistData(token)


token = getAuth()
if __name__ == "__main__":
    main()
