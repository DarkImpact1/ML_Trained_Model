import streamlit as st 
import model

def create_page():
    st.title("IMDb Review Classifier")
    st.write("### Write the review to check whether it is Positive or Negative")
    review = st.text_area("Review Here","")
    button  = st.button("Classify")
    if (button):
        if(len(review) == 0):
            st.warning("Kindly, provide some review to classify")
        else:
            prediction = model.make_prediction(review)
            st.write(f"The given review is : {prediction}")
    
create_page()