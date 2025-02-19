import streamlit as st
import pickle
import pandas as pd
import requests

with open('movies_dict.pkl','rb') as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

select_movie_name = st.selectbox(
    "Type movie that you like as recommend?",
    movies['title'].values,
)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=90ef6ab01ca91782f39d64b5c9e7ff43&&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]
    
    
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movies_poster

if st.button("Recommend"):
    name,poster = recommend(select_movie_name)
    
    col1,col2,col3,col4,col5 = st.columns(5)
    
    with col1:
        st.text(name[0])
        st.image(poster[0])
        
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])
        
