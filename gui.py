from flask import Flask
from login import login
from tracks import tracks

app = Flask(__name__)
app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(tracks, url_prefix="/tracks")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
