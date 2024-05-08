import streamlit as st 
import model, functions

choice = st.sidebar.selectbox("Model", ("Movie Recommender","Classify Review"))


def display_dev_details():
    st.sidebar.header("About Developer")
    st.sidebar.markdown("""
    **Name:** Mohit Dwivedi  
    **LinkedIn:** [Lets Connect](https://www.linkedin.com/in/mohit-dwivedi13/)
    """)
    
    st.sidebar.header("Contact Developer")
    st.sidebar.markdown("""
    **Email:** mohit.dev.new@gmail.com  
    """)

def create_review_classifier_page():
    st.title("IMDb Review Classifier")
    st.markdown("[Click here to visit developer](https://www.linkedin.com/in/mohit-dwivedi13/)")
    display_dev_details()
    st.write("### Write the review to check whether it is Positive or Negative")
    review = st.text_area("Review Here","")
    button  = st.button("Classify")
    if (button):
        if(len(review) == 0):
            st.warning("Kindly, provide some review to classify")
        else:
            prediction = model.make_prediction(review)
            st.subheader(f"The given review is : {prediction}")
    


def create_movie_recommender_page():
    details = """
    Our movie recommender system is powered by machine learning, trained on a dataset of 5000 movies from Tmdb. 
    Using sophisticated algorithms, it analyzes user searches to recommend the next few movies tailored to their preferences.
    By understanding various movie attributes such as genre, cast, and plot, our system provides personalized suggestions for
    an enjoyable viewing experience. Whether users seek similar films or new genres to explore, our recommender leverages the 
    richness of the Tmdb dataset to offer curated selections. With its intuitive interface and accurate predictions, 
    our system enhances the movie-watching journey by delivering relevant recommendations for every user.
    """
    st.title("Movie Recommender System")
    st.write(details)

    display_dev_details()
    
    st.write("### Enter a Hollywood Movie Name:")
    movie_name = st.text_input("e.g., The Dark Knight", "")
    button = st.button("Suggest Few Movies")
    
    if button:
        if len(movie_name) == 0:
            st.warning("Please enter the name of a movie.")
        else:
            recommended_movies = model.get_recommendations(movie_name)
            if recommended_movies:
                st.subheader("Recommended Movies:")
                poster_list = functions.get_movie_poster_url(recommended_movies)
                captions = []
                image_url = []
                for pair in poster_list:
                    movie,poster_url = pair
                    if poster_url:
                        captions.append(movie)
                        image_url.append(poster_url)
                st.image(image_url, caption=captions, width=200)
            else:
                st.write("Sorry, the movie you entered is not in the dataset. Please try another one.")



if choice == "Movie Recommender":
    create_movie_recommender_page()
elif choice == "Classify Review":
    create_review_classifier_page()
