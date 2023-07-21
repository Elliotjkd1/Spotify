from flask import Blueprint, render_template
from dotenv import load_dotenv
import os
import uuid

login = Blueprint(__name__, "login")



@login.route("/")
def loginRoute():
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    scope = 'user-follow-read user-top-read'
    redirect_uri = "http://localhost:3000/tracks"
    state = uuid.uuid4()
    spotify_auth_link = "https://accounts.spotify.com/authorize?response_type=code&client_id="+str(client_id)+"&scope="+str(scope)+"&redirect_uri="+redirect_uri+"&state="+str(state)
    return render_template("login.html", spotify_auth_link=spotify_auth_link)
