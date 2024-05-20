import os
import requests
import streamlit as st

def get_movie_poster_and_imdb_url(movies):
    poster_imdb_list = []
    for movie_title in movies:
        response = requests.get("http://www.omdbapi.com/", 
                                params={"apikey": "457a2c32", "t": movie_title})
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            if data.get('Poster') != 'N/A' and 'imdbID' in data:
                imdb_url = f"https://www.imdb.com/title/{data['imdbID']}/"
                pair = (movie_title, data.get('Poster'), imdb_url)
                poster_imdb_list.append(pair)
    if len(poster_imdb_list) > 0:
        return poster_imdb_list
    return None


def display_dev_details():
    st.sidebar.header("About Developer")
    st.sidebar.markdown("""
        **Name:** Mohit Dwivedi\n
        **LinkedIn:** [Lets Connect](https://www.linkedin.com/in/mohit-dwivedi13/)\n
        **Twitter (X):** [click here](https://twitter.com/dmohit013)\n
        **Github:** [click here](https://github.com/DarkImpact1/)\n
        **Instagram:** [click here](https://www.instagram.com/dmohit13/)\n
    """)
    
    
    st.sidebar.header("Contact Developer")
    st.sidebar.markdown("""
    **Email:** mohit.dev.new@gmail.com  
    """)
