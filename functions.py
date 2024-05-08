import os
import requests

def get_movie_poster_url(movies):
    poster_list = []
    for movie_title in movies:
        response = requests.get("http://www.omdbapi.com/", 
                                params={"apikey": "457a2c32", "t": movie_title})
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            if data.get('Poster') != 'N/A':
                pair = (movie_title, data.get('Poster'))
                poster_list.append(pair)
    if(len(poster_list)>0):
        return poster_list
    return None
