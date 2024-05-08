import os
import requests
from dotenv import load_dotenv

load_dotenv()
def get_movie_poster_url(movie_title):

    # Loading the api key 
    api_key = os.getenv("OMDB_API_KEY")
    if api_key == None:
        raise ValueError("OMDB_API_KEY environment variable is not set")
    response = requests.get("http://www.omdbapi.com/", 
                            params={"apikey": api_key, "t": movie_title})
    
    """Check if request was successful then fetch the poster and return it """
    if response.status_code == 200:
        data = response.json()
        if data.get('Poster') != 'N/A':
            return data.get('Poster')
    
    return None