import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


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


##==================
## Streamlit Code
##==================
st.markdown("""# What songs were popular when I was in high school?
The algorithm doesn't get you, we get that a lot. Maybe you want to rediscover the top songs from your high school days. Or maybe you just don't want to mess with making your own playlist. 

You can use this tool to find a pre-generated playlist of every song that made the Top 10 in the US for the years you select. 
""")

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
        playlist = "Ooops, it looks like we didn't make that playlist yet. Playlists with a **range of 1-20 years** were created. Try again with a more narrow year range."

    if isinstance(playlist, dict):
        link = f"#### Your Spotify Playlist: [{playlist['name']}]({playlist['link']})"
        st.markdown(link, unsafe_allow_html=True)
        get_analysis(year_range[0], year_range[1])

    else:
        st.markdown(playlist)