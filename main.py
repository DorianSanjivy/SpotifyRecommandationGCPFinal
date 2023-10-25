from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.spatial import distance
import pandas as pd
import os


app = Flask(__name__)

current_dir = os.path.dirname(os.path.realpath(__file__))

df_theme = pd.read_json(os.path.join(current_dir, "content/FINAL_THEME.jsonl"), lines=True)
df_sentiment = pd.read_json(os.path.join(current_dir, "content/FINAL_SENTIMENT.jsonl"), lines=True)
df_lyrics = pd.read_json(os.path.join(current_dir, "content/FINAL_LYRICS.jsonl"), lines=True)

def theme_nearest_songs(df, artist_name, track_name):
    """
    Recommend songs based on the theme and the distance to a chosen song.
    """

    chosen_song = df[(df['artist_name'] == artist_name) & (df['track_name'] == track_name)]

    if chosen_song.empty:
        print("The specified song is not in the dataset.")
        return pd.DataFrame()  # Return an empty DataFrame

    chosen_song = chosen_song.iloc[0]
    theme = chosen_song['theme']
    chosen_coordinates = np.array(chosen_song['coordinates'])

    # Step 1: Filter songs by the chosen song's theme
    filtered_df = df[df['theme'] == theme]

    # Step 2: Compute the distances between the chosen song and all other songs with the same theme
    filtered_df['distance'] = filtered_df['coordinates'].apply(lambda x: distance.euclidean(np.array(x), chosen_coordinates))

    # Step 3: Return top 5 nearest songs excluding the chosen one
    nearest_songs = filtered_df.nsmallest(6, 'distance')

    # Removing the chosen song from the list of nearest songs (assuming unique tracks in df)
    nearest_songs = nearest_songs[nearest_songs['track_name'] != chosen_song['track_name']]

    return nearest_songs[['artist_name', 'track_name', 'distance', 'theme']]



def emotion_nearest_songs(df, artist_name, track_name):
    """
    Recommend songs based on emotional scores proximity.
    """

    chosen_song = df[(df['artist_name'] == artist_name) & (df['track_name'] == track_name)]

    if chosen_song.empty:
        print("The specified song is not in the dataset.")
        return pd.DataFrame()  # Return an empty DataFrame

    chosen_song = chosen_song.iloc[0]
    emotion_scores = [
        'rejoicing_score', 'soothing_satisfied_score', 'sadness_disappointment_score', 'anger_discontent_score'
    ]
    chosen_emotion_vector = chosen_song[emotion_scores].values
    df_copy = df.copy()

    # Step 1: Compute the distances between the chosen song and all other songs based on emotion scores
    df_copy['distance'] = df_copy.apply(lambda row: distance.euclidean(row[emotion_scores].values, chosen_emotion_vector), axis=1)

    # Step 2: Return top 5 nearest songs excluding the chosen one
    nearest_songs = df_copy.nsmallest(6, 'distance')

    # Removing the chosen song from the list of nearest songs (assuming unique tracks in df)
    nearest_songs = nearest_songs[nearest_songs['track_name'] != chosen_song['track_name']]

    return nearest_songs[['artist_name', 'track_name', 'distance']]



def lyrics_nearest_songs(df, artist_name, track_name):
    """
    Recommend songs based on lyrical vector similarity.
    """

    chosen_song = df[(df['artist_name'] == artist_name) & (df['track_name'] == track_name)]

    if chosen_song.empty:
        print("The specified song is not in the dataset.")
        return pd.DataFrame()  # Return an empty DataFrame

    chosen_song = chosen_song.iloc[0]
    lyric_vectors = [str(i) for i in range(17)]  # columns from '0' to '16'
    chosen_lyric_vector = chosen_song[lyric_vectors].values

    # Compute the distances between the chosen song and all other songs based on lyric vectors
    df['distance'] = df.apply(lambda row: distance.euclidean(row[lyric_vectors].values, chosen_lyric_vector), axis=1)

    # Return top 5 nearest songs excluding the chosen one
    nearest_songs = df.nsmallest(6, 'distance')

    # Removing the chosen song from the list of nearest songs (assuming unique tracks in df)
    nearest_songs = nearest_songs[nearest_songs['track_name'] != chosen_song['track_name']]

    return nearest_songs[['artist_name', 'track_name', 'distance']]



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    artist_name = request.form.get('artist_name')
    track_name = request.form.get('track_name')

    theme_results = theme_nearest_songs(df_theme, artist_name, track_name).to_dict('records')
    emotion_results = emotion_nearest_songs(df_sentiment, artist_name, track_name).to_dict('records')
    lyrics_results = lyrics_nearest_songs(df_lyrics, artist_name, track_name).to_dict('records')

    return jsonify({
        'theme': theme_results,
        'emotion': emotion_results,
        'lyrics': lyrics_results
    })


if __name__ == '__main__':
    app.run(debug=True)
