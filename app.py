import os
from datetime import timedelta

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import requests
from requests.exceptions import RequestException

from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):           # Define the User class
    def __init__(self, token):
        self.id = token


@login_manager.user_loader       # callback used to reload the user object from the user ID stored in the session
def load_user(user_id):
    return User(user_id)


class SimilarShortEntity():
    title: str
    album: str
    artist: str
    path: str


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("list_artists"))
    return render_template("home.html")


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("list_artists"))
    return render_template("signin.html")


@app.route("/sign_user_in", methods=["POST"])
def sign_user_in():
    # Get the bearer token from the FastAPI then log in the user
    username = request.form.get("username")
    password = request.form.get("password")
    url = f"{BASE_URL}/auth/token"
    response = requests.post(url, data={"username": username, "password": password})
    token = response.json().get("access_token")
    user = User(token)
    login_user(user, remember=False, duration=timedelta(minutes=30))
    return redirect(url_for("list_artists"))


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for("home"))
    logout_user()
    return redirect(url_for("home"))


@app.route("/artists")
def list_artists():
    if not current_user.is_authenticated:
        return redirect(url_for("home"))
    url = f"{BASE_URL}/music_library/artists"
    headers = {"Authorization": f"Bearer {current_user.id}"}
    try:
        response = requests.get(url, headers=headers)
        list_of_artists = response.json()
    except RequestException as e:
        return redirect(url_for("home"))
    return render_template("artists.html", artists=list_of_artists)


@app.route("/artist/<string:artist_folder>/albums")
@login_required
def list_artist_albums(artist_folder):
    url = f"{BASE_URL}/music_library/albums"
    headers = {"Authorization": f"Bearer {current_user.id}"}
    data = {"artist_folder": f"{artist_folder}"}
    try:
        response = requests.post(url, headers=headers, json=data)
        albums = response.json()
    except RequestException as e:
        return redirect(url_for("list_artists"))
    return render_template("albums.html", albums=albums, artist_name=artist_folder)


@app.route("/artist/<string:artist_name>/album/<string:album_name>")
@login_required
def album_tracklist(artist_name, album_name):
    url = f"{BASE_URL}/music_library/songs/by_artist_and_album"
    headers = {"Authorization": f"Bearer {current_user.id}"}
    data = {"artist": f"{artist_name}", "album": f"{album_name}"}   
    try:
        response = requests.post(url, headers=headers, json=data)
        tracklist = response.json()
        tracklist.sort(key=lambda x: x['tracknumber'])  # Sort by tracknumber
    except RequestException as e:
        return redirect(url_for("list_artists"))
    return render_template("tracklist.html", tracklist=tracklist, artist_name=artist_name, album_name=album_name)


@app.route("/similar_songs/<path:full_path>")
@login_required
def similar_songs(full_path):
    url = f"{BASE_URL}/milvus/similar_short_entity"
    headers = {"Authorization": f"Bearer {current_user.id}"}
    data = {"path": [f"{full_path}"]}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        songs = response.json().get("entities", [])
    except RequestException as e:
        return redirect(url_for("list_artists"))
    band_name = full_path.split("/")[1]
    file_name = full_path.split("/")[-1].split(".")[0]
    return render_template("songs.html", songs=songs, band_name=band_name, file_name=file_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)