import pickle
import pandas as pd
import streamlit as st
import requests
import gdown
import os

# ---------------------- Styling ----------------------
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .movie-title {
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        margin-bottom: 8px;
        color: #ffffff;
    }
  
    h1, h4, .stSelectbox label, .stButton button {
        color: white !important;
    }
    .stSelectbox > div {
        background-color: #1e1e1e;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Functions ----------------------
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url, timeout=7)
        response.raise_for_status()
        data = response.json()
        if data.get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except Exception as e:
        print(f"Poster fetch error: {e}")
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# ---------------------- Load Data ----------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

@st.cache_data
def load_similarity():
    file_id = "1zHNpsLPeGUpZXy4JiD7zqkVmVgXfVmrh"  # <-- your real .pkl file ID here
    output_path = "similarity.pkl"

    if not os.path.exists(output_path):
        gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)

    with open(output_path, 'rb') as f:
        return pickle.load(f)

similarity = load_similarity()

# ---------------------- UI ----------------------
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>iRecommend</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: white;'>Find your next favorite movie</h4>", unsafe_allow_html=True)
st.markdown("---")

selected_movie_name = st.selectbox(
    "Which movie did you like? We'll suggest more!",
    movies['title'].values
)

if st.button('Show Suggestions'):
    with st.spinner('Finding perfect movies for you...'):
        try:
            names, posters = recommend(selected_movie_name)
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                if idx < len(names):
                    with col:
                        st.markdown(f"<div class='movie-title'>{names[idx]}</div>", unsafe_allow_html=True)
                        st.image(posters[idx])
        except Exception as e:
            st.error(f"Something went wrong: {e}")

st.markdown(""""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f0f0;
            color: #555;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            border-top: 1px solid #ddd;
        }
    </style>
    <div class="footer">
        Made with care by <strong>Jass</strong> © 2025. All rights reserved.
    </div>
""", unsafe_allow_html=True)
