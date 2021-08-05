import streamlit as st
import pickle
#for api
import requests



new_df = pickle.load(open('movies.pkl', 'rb'))
movies_list = new_df['title'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))
#create title
st.title("movie recommender system")

#fetch poster function
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=504a5e93a2e9e316e7062a97cafe7a86&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
#create selectbox
selected_movies_name = st.selectbox(
'How would you like to be contacted?',movies_list)

#recommed movie
def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    recommended = []
    recommended_movie_poster = []
    for i in movie_list:
        movie_id = new_df.iloc[i[0]].movie_id
        
        recommended.append(new_df.iloc[i[0]].title)
        #fetch poster from api
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended, recommended_movie_poster
#create button
if st.button('Recommend'):
    names, posters = recommend(selected_movies_name)    
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
      st.text(names[0])
      st.image(posters[0])
    with col2:
      st.text(names[1])
      st.image(posters[1])
    with col3:
      st.text(names[2])
      st.image(posters[2])
    with col4:
      st.text(names[3])
      st.image(posters[3])
    with col5:
      st.text(names[4])
      st.image(posters[4])
      

      
