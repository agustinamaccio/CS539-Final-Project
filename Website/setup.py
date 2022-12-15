import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.decomposition import PCA
import pickle
import matplotlib

matplotlib.use("Agg")

from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from base64 import encodebytes

import io
from PIL import Image

# import base64
from math import pi
import random
from flask import jsonify
import jinja2
from flask import Flask, request, render_template, Response

app = Flask(__name__)


@app.route("/")
def my_form():
    return render_template("index.html")


@app.route("/create_file", methods=["POST"])
def create_file():
    if request.method == "POST":
        with open(f"{request.form.get('name')}.txt", "w") as f:
            f.write("FILE CREATED AND SUCCESSFULL POST REQUEST!")
        return ("", 204)


@app.route("/test", methods=["POST"])
def my_form_post():
    name = request.form["iname"]
    url = request.form["iurl"]

    random.seed(10)

    cid = "eb85441772404a72888d8df89b2f1072"
    secret = "4042de057f244a7f932cd4d99571a6ce"

    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # input playlist link and user from website
    # temp = my_form_post()
    username = name
    playlist = url

    def call_playlist(creator, playlist_id):

        # step1

        playlist_features_list = [
            "artist",
            "album",
            "track_name",
            "track_id",
            "danceability",
            "energy",
            "key",
            "loudness",
            "mode",
            "speechiness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
            "time_signature",
        ]

        playlist_df = pd.DataFrame(columns=playlist_features_list)

        # step2
        owner = sp.user_playlist(creator, playlist_id)["owner"]["display_name"]
        playlist_name = sp.user_playlist(creator, playlist_id)["name"]
        playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
        for track in playlist:
            # Create empty dict
            playlist_features = {}
            # Get metadata
            try:
                playlist_features["artist"] = track["track"]["album"]["artists"][0][
                    "name"
                ]
                playlist_features["album"] = track["track"]["album"]["name"]
                playlist_features["track_name"] = track["track"]["name"]
                playlist_features["track_id"] = track["track"]["id"]

                # Get audio features
                audio_features = sp.audio_features(playlist_features["track_id"])[0]
                for feature in playlist_features_list[4:]:
                    playlist_features[feature] = audio_features[feature]

                # Concat the dfs
                track_df = pd.DataFrame(playlist_features, index=[0])
                playlist_df = pd.concat([playlist_df, track_df], ignore_index=True)
                playlist_df["owner"] = owner
                playlist_df["playlist_name"] = playlist_name
                playlist_df["user"] = creator

            except:
                pass
        # Step 3

        return playlist_df

    # user is an input from website
    df = call_playlist(username, playlist)

    col = [
        "playlist_name",
        "user",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
        "time_signature",
    ]

    columns = ["playlist_name", "user"]
    for n in col[2:]:
        columns.append(n + "_var")
        columns.append(n + "_mean")
        columns.append(n + "_max")
        columns.append(n + "_min")

    data = pd.DataFrame(columns=columns)

    dict = {"playlist_name": df["playlist_name"].iloc[0], "user": df["user"].iloc[0]}
    for i in col[2:]:
        Var = i + "_var"
        dict[Var] = df[i].var()
        Mean = i + "_mean"
        dict[Mean] = df[i].mean()
        Max = i + "_max"
        dict[Max] = max(df[i])
        Min = i + "_min"
        dict[Min] = min(df[i])
    data = data.append(dict, ignore_index=True)

    # import newdata from github
    dataset = pd.read_csv("newdata.csv")
    dataset = dataset.append(data, ignore_index=True)
    dataset2 = dataset.drop(columns=["playlist_name", "user", "playlist_link"])
    norm_data = normalize(dataset2)

    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(norm_data)
    pc_data = pd.DataFrame(data=principalComponents)
    new_sample = pc_data.loc[252, :]
    pc_data = pc_data.drop([252])
    new_sample = pd.DataFrame(new_sample).T

    # import model from github
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
        cluster_array = model.predict(new_sample)
        cluster = cluster_array[0]
        pc_data["cluster"] = model.labels_
        closest, _ = pairwise_distances_argmin_min(
            new_sample.to_numpy().reshape(1, -1),
            pc_data[pc_data["cluster"] == cluster].iloc[:, 0:2],
        )
        friend = dataset.loc[closest[0], :]["user"]
        f_pl = dataset.loc[closest[0], :]["playlist_name"]
        f_link = dataset.loc[closest[0], :]["playlist_link"]

        # print(friend, f_pl)
    user1_plid = playlist
    results = sp.playlist(user1_plid)
    results2 = sp.playlist(f_link)

    ###################
    # create a list of song ids
    ids = []

    for item in results["tracks"]["items"]:
        track = item["track"]["id"]
        ids.append(track)

    song_meta = {
        "id": [],
        "album": [],
        "name": [],
        "artist": [],
        "explicit": [],
        "popularity": [],
    }

    for song_id in ids:
        # get song's meta data
        meta = sp.track(song_id)

        # song id
        song_meta["id"].append(song_id)
        # album name
        album = meta["album"]["name"]
        song_meta["album"] += [album]

        # song name
        song = meta["name"]
        song_meta["name"] += [song]

        # artists name
        s = ", "
        artist = s.join([singer_name["name"] for singer_name in meta["artists"]])
        song_meta["artist"] += [artist]

        # explicit: lyrics could be considered offensive or unsuitable for children
        explicit = meta["explicit"]
        song_meta["explicit"].append(explicit)

        # song popularity
        popularity = meta["popularity"]
        song_meta["popularity"].append(popularity)

    song_meta_df = pd.DataFrame.from_dict(song_meta)

    # check the song feature
    features = sp.audio_features(song_meta["id"])
    # change dictionary to dataframe
    features_df = pd.DataFrame.from_dict(features)

    # convert milliseconds to mins
    # duration_ms: The duration of the track in milliseconds.
    # 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
    features_df["duration_ms"] = features_df["duration_ms"] / 60000

    # combine two dataframe
    final_df = song_meta_df.merge(features_df)
    ##########Music Features##########
    music_feature = features_df[
        [
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
        ]
    ]

    ###Scalar###
    min_max_scaler = MinMaxScaler()

    music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.loc[:])

    music_labels = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
    ]

    # plot size
    # fig = plt.figure(figsize=(12, 8))

    # # convert column names into a list
    categories = list(music_feature.columns)
    # # number of categories
    N = len(categories)

    # # create a list with the average of all features
    value = list(music_feature.mean())

    # # repeat first value to close the circle
    # # the plot is a circle, so we need to "complete the loop"
    # # and append the start value to the end.
    value += value[:1]
    # # print(value)
    # # calculate angle for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # # plot
    # plt.polar(angles, value)
    # plt.fill(angles, value, alpha=0.3)
    # plt.title(name, size=16, color="red", y=1.06)

    # plt.xticks(angles[:-1], categories, size=15)
    # plt.yticks(color="grey", size=15)
    # # plt.show()
    # ####
    # output = io.BytesIO()
    # FigureCanvas(fig).print_png(output)
    # # print("1111111111111111111111")
    # # plt.savefig(output, format="png")
    # # # plt.savefig(output, format="png")
    # # print("1")
    # # encoded_img = encodebytes(output.getvalue()).decode("utf8")

    # return {"message": "ok"}

    ids = []

    for item in results2["tracks"]["items"]:
        track = item["track"]["id"]
        ids.append(track)

    song_meta = {
        "id": [],
        "album": [],
        "name": [],
        "artist": [],
        "explicit": [],
        "popularity": [],
    }

    for song_id in ids:
        # get song's meta data
        meta = sp.track(song_id)

        # song id
        song_meta["id"].append(song_id)
        # album name
        album = meta["album"]["name"]
        song_meta["album"] += [album]

        # song name
        song = meta["name"]
        song_meta["name"] += [song]

        # artists name
        s = ", "
        artist = s.join([singer_name["name"] for singer_name in meta["artists"]])
        song_meta["artist"] += [artist]

        # explicit: lyrics could be considered offensive or unsuitable for children
        explicit = meta["explicit"]
        song_meta["explicit"].append(explicit)

        # song popularity
        popularity = meta["popularity"]
        song_meta["popularity"].append(popularity)

    song_meta_df = pd.DataFrame.from_dict(song_meta)

    # check the song feature
    features = sp.audio_features(song_meta["id"])
    # change dictionary to dataframe
    features_df = pd.DataFrame.from_dict(features)

    # convert milliseconds to mins
    # duration_ms: The duration of the track in milliseconds.
    # 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
    features_df["duration_ms"] = features_df["duration_ms"] / 60000

    # combine two dataframe
    final_df = song_meta_df.merge(features_df)
    ##########Music Features##########
    music_feature = features_df[
        [
            "danceability",
            "energy",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
            "duration_ms",
        ]
    ]

    ###Scalar###
    min_max_scaler = MinMaxScaler()

    music_feature.loc[:] = min_max_scaler.fit_transform(music_feature.loc[:])

    music_labels = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "duration_ms",
    ]

    # plot size
    # fig = plt.figure(figsize=(12, 8))

    # # convert column names into a list
    categories = list(music_feature.columns)
    # # number of categories
    N = len(categories)

    # # create a list with the average of all features
    value1 = list(music_feature.mean())

    # # repeat first value to close the circle
    # # the plot is a circle, so we need to "complete the loop"
    # # and append the start value to the end.
    value1 += value1[:1]
    # # print(value)
    # # calculate angle for each category
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    return jsonify(
        name=friend,
        playlist_name=f_pl,
        playlist_link=f_link,
        mean=value,
        labels=music_labels,
        mean2=value1,
    )


# @app.route("/", methods=["POST"])
# def plotfig(method="POST"):

#     cid = "91382d101a194c12b67ba7f857bede3e"
#     secret = "74179f9842234459a51e85c7f65bd180"

#     client_credentials_manager = SpotifyClientCredentials(
#         client_id=cid, client_secret=secret
#     )

#     sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#     name = request.form["iname"]
#     url = request.form["iurl"]

#     # return Response(output.getValue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
