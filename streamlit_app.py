import streamlit as st 
import model

choice = st.sidebar.selectbox("Model", ("Movie Recommender","Classify Review"))

def create_review_classifier_page():
    st.title("IMDb Review Classifier")
    st.markdown("[Click here to visit developer](https://www.linkedin.com/in/mohit-dwivedi13/)")
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
    st.title("Movie Recommender System")
    st.write("This model is trained on tmdb movie dataset")
    st.markdown("[Click here to visit developer](https://www.linkedin.com/in/mohit-dwivedi13/)")
    st.write("### Enter movie name ( Hollywood Movie)")
    movie_name = st.text_area("Here","")
    button  = st.button("Suggest few movies")
    if (button):
        if(len(movie_name) == 0):
            st.warning("Kindly, Enter the name of Movie ")
        else:
            recommended_movie = model.get_recommendations(movie_name)
            if recommended_movie:
                st.subheader("Recommended Movie: ")
                for movie in recommended_movie:
                    st.write(movie)

if choice == "Movie Recommender":
    create_movie_recommender_page()
elif choice == "Classify Review":
    create_review_classifier_page()
