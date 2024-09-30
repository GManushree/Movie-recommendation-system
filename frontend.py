import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Calculate popularity rank based on 'popularity' column
movies['popularity_rank'] = movies['popularity'].rank(ascending=False)

# Streamlit UI
st.title('Movie Recommendation System')

selected_movie = st.selectbox(
    "Enter the movie name",
    movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

# Data Analytics Section
st.sidebar.title('Popularity By Title')

# Displaying popularity distribution
st.sidebar.subheader('Popularity Distribution')
st.sidebar.bar_chart(movies['popularity'].head(20))  # Display popularity scores of top 20 movies

# Display top N most popular movies
top_n = 10  # Number of top popular movies to display
st.sidebar.subheader(f'Top {top_n} Most Popular Movies:')
top_movies = movies.sort_values(by='popularity', ascending=False).head(top_n)
for idx, row in top_movies.iterrows():
    st.sidebar.write(f"{row['title']} (Popularity Rank: {row['popularity_rank']})")
    st.sidebar.image(fetch_poster(row['movie_id']), use_column_width=True)
