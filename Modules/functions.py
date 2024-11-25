import os
import requests
import streamlit as st
import Modules.model as model

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

# review classifier page
def create_review_classifier_page():
    st.title("IMDb Review Classifier")
    display_dev_details()
    st.write("### Write the review to check whether it is Positive or Negative")
    review = st.text_area("Review Here","")
    length = len(review.split())
    button  = st.button("Classify")
    if (button):
        if length <= 3 and length > 0:
            prediction = model.make_prediction(review)
            st.subheader(f"The given review is : {prediction}")
        elif(length > 3):
            lstm_prediction = model.predictionsLSTM(review)
            st.subheader(f"The given review is : {lstm_prediction}")
        else:
            st.subheader("Kindly check if review is not given. ")

# movie recommender page
def create_movie_recommender_page():
    details = """
    Our movie recommender system is powered by machine learning, trained on a dataset of 5000 movies from Tmdb. 
    Using sophisticated algorithms, it analyzes user searches to recommend the next few movies tailored to their preferences.
    By understanding various movie attributes such as genre, cast, and plot, our system provides personalized suggestions for
    an enjoyable viewing experience. Whether users seek similar films or new genres to explore, our recommender leverages the 
    richness of the Tmdb dataset to offer curated selections. With its intuitive interface and accurate predictions, 
    our system enhances the movie-watching journey by delivering relevant recommendations for every user.

    After clicking on the image it will redirect you to the IMDB's official website where you can get more details of recommended movie
    """
    st.title("Movie Recommender System")
    st.write(details)
    # to display developer details
    display_dev_details()
    
    st.write("### Enter a Hollywood Movie Name:")
    movie_name = st.text_input("e.g., The Dark Knight", "")
    button = st.button("Suggest Few Movies")
    
    if button:
        if len(movie_name) == 0:
            st.warning("Please enter the name of a movie.")
        else:
            function_return = model.get_recommendations(movie_name)
            recommended_movies,closest_match = function_return[0], function_return[1]
            if recommended_movies:
                st.write("Closest match to the name you entered : ", closest_match)
                st.subheader("Recommended Movies:")
                st.write("Click on the image for more details ")
                poster_imdb_list = get_movie_poster_and_imdb_url(recommended_movies)
                
                if poster_imdb_list:
                    for movie, poster_url, imdb_url in poster_imdb_list:
                        if poster_url:
                            html = f'''
                                <div style="display: inline-block; margin: 10px;">
                                    <a href="{imdb_url}" target="_blank">
                                        <img src="{poster_url}" alt="{movie}" width="200">
                                    </a>
                                    <p style="text-align: center;">{movie}</p>
                                </div>
                            '''
                            st.markdown(html, unsafe_allow_html=True)
                else:
                    st.write("No posters found.")
            else:
                st.write("Sorry, the movie you entered is not in the dataset. Please try another one.")