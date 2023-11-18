import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

from streamlit_lottie import st_lottie

# Getting Client Id and Client Secret
client_id = '9024429ddca6460c8b6fc35343a37b00'
client_secret = '8018a7729ac7408280c46250636fa216'
auth_manage = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = auth_manage) # Spotify object to access API

# Uploading image
def load_musicurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Taking song name as input
def get_recommendations(track_name):
    # Getring track URI
    results = sp.search(q = track_name, type = "track")
    track_uri = results["tracks"]["items"][0]["uri"]

    # Get recommended tracks
    recommendations = sp.recommendations(seed_tracks = [track_uri], limit = 10)["tracks"]
    return recommendations

def get_analysis(start_year, end_year):
    st.markdown("""## Some Analysis of the year range are:
            """)

    plt.style.use("df-style.mplstyle")
    df2 = pd.read_csv("songs.csv")

    year = df2.groupby(by='year').mean(numeric_only=True).drop(columns='peak').reset_index()

    ##============== First Row ==============##

    col1, col2 = st.columns(2)

    col1.subheader("Duration")
    fig, ax = plt.subplots()
    ax.plot(year['year'], (year['duration_ms'] / 1_000) / 60)
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0,6.5)

    # Add in title and subtitle
    ax.set_title("""Nobody got time for Music?""")
    ax.text(x=.08, y=.86, 
            s="", 
            transform=fig.transFigure, 
            ha='left', 
            fontsize=20,
            alpha=.8)
    col1.pyplot(fig)

    col2.subheader("Loudness")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['loudness'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(-15, -3)

    # Add in title and subtitle
    ax.set_title("""Hearing protection recommended""")
    ax.text(x=.08, y=.86,
            s= "", 
            transform=fig.transFigure,
            ha='left',
            fontsize=20,
            alpha=.8)
    col2.pyplot(fig)

    ##============== Second Row ==============##

    col3, col4 = st.columns(2)

    col3.subheader("Valence & Acusticness")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['valence'])
    ax.plot(year['year'], year['acousticness'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0,.85)

    # Add in title and subtitle
    ax.set_title("""I've got a negative feeling...""")
    ax.text(x=.08, y=.86, 
            s="", 
            transform=fig.transFigure, 
            ha='left', 
            fontsize=20, 
            alpha=.8)

    # Label the lines directly
    ax.text(x=.78, y=.66, s="""Valence""", 
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    ax.text(x=.73, y=.30, s="""Acousticness""", 
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    col3.pyplot(fig)

    col4.subheader("Danceability & Energy")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['danceability'])
    ax.plot(year['year'], year['energy'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0,.85)

    # Add in title and subtitle
    ax.set_title('Hmm...')
    ax.text(x=.08, y=.86, 
            s="", 
            transform=fig.transFigure, 
            ha='left', 
            fontsize=20, 
            alpha=.8)

    # Label the lines directly
    ax.text(x=.7, y=.795, s="""Energy""", 
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    ax.text(x=.685, y=.61, s="""Danceability""", 
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    col4.pyplot(fig)

    ##============== Third Row ==============##

    col5, col6 = st.columns(2)

    col5.subheader("Instrumentalness & Speechiness")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['instrumentalness'])
    ax.plot(year['year'], year['speechiness'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0,.32)

    ax.set_yticks(np.arange(0, .35, 0.05))

    # Add in title and subtitle
    ax.set_title("They don't sing like they used to..")
    ax.text(x=.08, y=.86, 
            s="", 
            transform=fig.transFigure, 
            ha='left', 
            fontsize=20, 
            alpha=.8)

    # Label the lines directly
    ax.text(x=.57, y=.17, s="""Instrumentalness""", 
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    ax.text(x=.72, y=.52, s="""Speechiness""", 
            transform=fig.transFigure, ha='left', fontsize=20, alpha=.7)
    col5.pyplot(fig)

    col6.subheader("Energy")
    fig, ax = plt.subplots()
    ax.plot(year['year'], year['energy'])
    ax.set_xlim(start_year, end_year)
    ax.set_ylim(0.03, 1)

    # Add in title and subtitle
    ax.set_title("""Is it increasing?""")
    ax.text(x=.08, y=.86, 
            s="", 
            transform=fig.transFigure, 
            ha='left', 
            fontsize=20, 
            alpha=.8)
    col6.pyplot(fig)


# Creating Streamlit App
def main():

    ##==============================
    ## Get Song Recommendation
    ##==============================
    
    lottie_music = load_musicurl("https://lottie.host/96ee915d-6c68-4989-9415-49c4396a1a4a/eH1LnsMXmA.json")
    st_lottie(lottie_music, speed=1, height=200, key="initial")

    row0_1, row0_2= st.columns((2, 1))
    row0_1.title("Music Recommendation System")

    row0_2.subheader(
        "A music recommendation web app by Vineet Singh Negi"
        )

    st.markdown(
        "The algorithm doesn't get you, we get that a lot. Maybe you want to rediscover\
        some new songs as per your music taste. Or maybe you you want top songs from school days and\
        don't want to mess with making your own playlist."
    )
    st.markdown(
        "**TO GET SONG RECOMMENDATION.** 👇"
        )

    track_name = st.text_input("Enter the song name:")

    if st.button("Get Recommendations"):
        recommendations = get_recommendations(track_name)
        
        if recommendations is not None:
            st.write("Recommended Songs Are:")
            for track in recommendations:
                st.write(track["name"])
                track_image = track["album"]["images"][0]["url"]
                st.image(track_image, width = 60)

        else:
            st.error("No such song exists")


    st.markdown("")
    st.markdown("")

    ##==============================
    ## Get Top Singles Playlist
    ##==============================
    st.markdown("**You can use this tool to find a pre-generated playlist of English songs that made\
                the Top 10 for the years you select.**")

    df = pd.read_csv("playlists.csv")
    years = list(range(1958, 2022))

    year_range = st.slider(label="Start Year", 
                        min_value=1958, 
                        max_value=2022, 
                        value=(1995, 2010))


    if st.button('Get Playlist'):
        if (int(year_range[0]) - int(year_range[1])) == 0:
            playlist_name = f"Top Singles: {year_range[0]}"
        else:
            playlist_name = f"Top Singles: {year_range[0]} - {year_range[1]}"

        if df[df['name'] == playlist_name].shape[0] > 0:
            playlist = df[df['name'] == playlist_name].to_dict(orient='records')[0]
        else:
            playlist = "Ooops, it looks like we didn't make that playlist yet. Playlists with a range of 1-20 years were created. Try again with a more narrow year range."

        if isinstance(playlist, dict):
            link = f"#### Your Spotify Playlist: [{playlist['name']}]({playlist['link']})"
            st.markdown(link, unsafe_allow_html=True)
            get_analysis(year_range[0], year_range[1])

        else:
            st.markdown(playlist)


if __name__ == "__main__":
    main()
