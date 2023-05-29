import os
from base64 import b64encode
import requests
from dotenv import load_dotenv


# --MAIN FUNCTION--
def main():
    getArtistData(artistID, token)


def getAuth():
    # Load environment variables from .env file
    # Retrieve authorization token using client ID and secret from environment variables
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


def getArtistData(artistID, token):
    # Retrieve and print artist data using the provided artist ID and token
    # URL endpoint
    # https://developer.spotify.com/documentation/web-api/reference/get-an-artist
    artistUrl = "https://api.spotify.com/v1/artists/" + artistID
    # Token auth
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


def searchArtist(artist, token):
    # Search for an artist using the provided artist name and token
    # Connect to spotify search api
    searchUrl = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": "Bearer " + token
    }
    params = {
        "q": artist,
        "type": "artist",
        "limit": 1
    }

    response = requests.get(searchUrl, headers=headers, params=params)
    responseData = response.json()

    if "artists" in responseData and "items" in responseData["artists"]:
        artists = responseData["artists"]["items"]
        if artists:
            return artists[0]["id"]  # Return the ID of the first matching artist
        else:
            print("No artist found with the given name:" + artist)
    else:
        print("Failed to retrieve artist data.")
    return None


def getUserArtistSelection():
    # get user artist input and return it
    userSelection = input("ENTER IN ARTIST HERE: ")
    return userSelection


# --MAIN CODE--
token = getAuth()
artist = getUserArtistSelection()
artistID = searchArtist(artist, token)

if __name__ == "__main__":
    main()
