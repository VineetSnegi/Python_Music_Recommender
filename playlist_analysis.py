import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time


# Function to get Client Id and Client Secret
client_id = '' # <-- Enter your client_id.
client_secret = '' # <-- Enter your client secret
auth_manage = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = auth_manage) # Spotify object to access API


# Getting ID of songs in Playlist
def getPlayListIDs (user, playlist_id):
    track_ids = []
    album = sp.user_playlist(user, playlist_id)
    for item in album ['tracks']['items']:
        track = item['track']
        track_ids.append(track['id'])
    return track_ids

# Drake Playlist URI: 37i9dQZF1DX7QOv5kjbU68 
# One Direction URI: 37i9dQZF1DX6p4TJxzMRDe
# Top Hindi Hits URI: 37i9dQZF1DX0XUfTFmNBRM
track_ids = getPlayListIDs('spotify', '') # <-- Enter any playlist URI

# Extracting the Track info and features
def getPlaylistFeatures(id):
    track_info = sp.track(id)
    features_info = sp.audio_features(id)

# Track Info
    name = track_info['name']
    album = track_info['album']['name']
    artist = track_info['album']['artists'][0]['name']
    release_date = track_info['album']['release_date']
    length = track_info['duration_ms']
    popularity = track_info['popularity']

# Track Features
    acousticness = features_info[0]['acousticness']
    danceability = features_info[0]['danceability']
    energy = features_info[0]['energy']
    instrumentalness = features_info[0]['instrumentalness']
    liveness = features_info[0]['liveness']
    loudness = features_info[0]['loudness']
    speechiness = features_info[0]['speechiness']  
    tempo = features_info[0]['tempo']
    time_signature = features_info[0]['time_signature']

    track_data = [name, album, artist, release_date, length, popularity, acousticness,
                   danceability, energy, instrumentalness, liveness, loudness, speechiness, 
                   tempo, time_signature]
    return track_data


# Appending the track features for each music into a list
track_list = []
for i in range(len(track_ids)):
    time.sleep(.3)
    track_data = getPlaylistFeatures(track_ids[i])
    track_list.append(track_data)

playlist = pd.DataFrame(track_list, columns = ['Name', 'Album', 'Artist', 'Release_Date', 'Length', 
                                               'Popularity', 'Acousticness', 'Danceabililty', 
                                               'Energy', 'Instrumentness', 'Liveness',
                                               'Loudness', 'Speechness', 'Tempo',
                                               'Time_Signature'])

playlist.to_csv("playlist_features.csv")


def main():
    df = pd.read_csv("playlist_features.csv")
    result = df.head(10)
    print("First ten songs are: ")
    print(result)


if __name__ == "__main__":
    main()