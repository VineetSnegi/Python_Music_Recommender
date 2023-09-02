import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyOAuth 
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = '' # <-- Enter your client_id
client_secret = '' # <-- Enter your client secret

# Function to get Client Id and Client Secret
auth_manage = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)

sp = spotipy.Spotify(client_credentials_manager = auth_manage) # Spotify object to access API

# Getting artist URI
artist_name = input("Enter the atrist name: ")
results = sp.search(q = artist_name, type = "artist")
artist_uri = results["artists"]["items"][0]["uri"]
artist = sp.artist(artist_uri)

if len(artist_uri) > 0:
    artist = results["artists"]["items"][0]
    print(artist['name'], artist['images'][0]['url']) # <-- Prints the Name and profile pic for artist


# Atrist top tracks
print("Top", artist_name,"Recent songs are:\n")
artist_top_track = artist_uri
results = sp.artist_top_tracks(artist_top_track)

for track in results['tracks'][:10]:
    print("Song: ", track['name'])
    print("Audio: ", track["preview_url"])
    print()
