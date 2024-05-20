import streamlit as st 
import model
import functions

choice = st.sidebar.selectbox("Model", ("Movie Recommender","Classify Review"))

if choice == "Movie Recommender":
    functions.create_movie_recommender_page()
elif choice == "Classify Review":
    functions.create_review_classifier_page()
