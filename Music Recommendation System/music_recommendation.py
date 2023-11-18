import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE

import warnings
warnings.filterwarnings('ignore')


# Reading the file that was extrated by 'playlist_analysis.py'
tracks = pd.read_csv("playlist_features.csv")


# Using CountVectorizer to build a model
song_vectorizer = CountVectorizer()
song_vectorizer.fit(tracks["Name"])


# Creating similarity function using Cosine Similarity
def get_similarities(song_name, data):

    text_array1 = song_vectorizer.transform(data[data["Name"] == song_name]["Artist"]).toarray()
    num_array1 = data[data["Name"] == song_name].select_dtypes(include = np.number).to_numpy()

    sim = []
    for idx, row in data.iterrows():
        name = row["Name"]

        text_array2 = song_vectorizer.transform(data[data["Name"] == name]["Artist"]).toarray()
        num_array2 = data[data["Name"] == name].select_dtypes(include = np.number).to_numpy()

        text_sim = cosine_similarity(text_array1, text_array2)[0][0]
        num_sim = cosine_similarity(num_array1,num_array2)[0][0]
        sim.append(text_sim + num_sim)
    
    return sim

def recommend_songs(song_name, data = tracks):

    if tracks[tracks["Name"] == song_name].shape[0] == 0:
        print ("This song is either not so poplular have entered an invalid name not contained in this playlist")
        
        for song in data.sample(n=7)["Name"].values:
            print(song)
            
        return
    
    data["similarity_factor"] = get_similarities(song_name, data)
    data.sort_values(by = ["similarity_factor", "Popularity"],
                     ascending = [False,False], inplace = True)
    
    return(data[["Name", "Artist"]][1:7])


def main():
    song_name = input("Enter the Song name: ")
    print("The recommended songs are: ")
    print(recommend_songs(song_name))


if __name__ == "__main__":
    main()