import os
import re
import pickle
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from fuzzywuzzy import process
porter = PorterStemmer()
stop_words = set(stopwords.words('english'))


def preprocess_text(review):
    text = re.sub(r'<br />', ' ', review.lower())
    stemmed_text = [porter.stem(word) for word in re.findall(r'\b[a-zA-Z]+\b', text) if word not in stop_words]
    processed_review = " ".join(stemmed_text)
    return processed_review

path = "DumpedFile"

# For Movie Review Sentiment Analysis
sentiment_vectorizer_file_path = os.path.join(path,"vectorizer.pkl")
sentiment_model_file_path = os.path.join(path,"trained_model.pkl")
loaded_sentiment_vectorizer = pickle.load(open(sentiment_vectorizer_file_path,'rb'))
loaded_sentiment_model = pickle.load(open(sentiment_model_file_path,'rb'))



def make_prediction(review):
    processed_review = preprocess_text(review)
    vector = loaded_sentiment_vectorizer.transform([processed_review])
    pred  = loaded_sentiment_model.predict(vector)
    return "Positive" if (pred == 1) else "Negative"
    
# For Movie Recommender System
rec_vec_file_path = os.path.join(path,"movie_rec_vec.pkl")
rec_model_file_path = os.path.join(path,"movie_recommender_model.pkl")
rec_df_path = os.path.join(path, "movie_dataframe.pkl")

loaded_df = pickle.load(open(rec_df_path ,'rb'))
loaded_rec_vec = pickle.load(open(rec_vec_file_path,'rb'))
loaded_rec_model = pickle.load(open(rec_model_file_path,'rb'))



# Function to get recommendations for a given movie name (with fuzzy matching)
def get_recommendations(movie_name_query):
    # Find the closest matching movie name using fuzzy matching
    closest_match = process.extractOne(movie_name_query, loaded_df['title'])

    # Check if a match is found
    if closest_match is not None:
        closest_movie_name, similarity_score = closest_match[0],closest_match[1]

        # Check if the similarity score is above the threshold
        if similarity_score >= 80:
            # Find the index of the closest matching movie in the DataFrame
            movie_index = loaded_df.index[loaded_df['title'] == closest_movie_name].tolist()[0]

            # Transform the movie tags into TF-IDF vectors using the loaded vectorizer
            movie_vector = loaded_rec_vec.transform([loaded_df.iloc[movie_index]['tags1']]).toarray()

            # Find the k nearest neighbors of the movie
            distances, indices = loaded_rec_model.kneighbors(movie_vector, n_neighbors=7)

            # Exclude the first neighbor, which is the movie itself
            neighbor_indices = indices.flatten()[1:]

            # Get the titles of the nearest neighbor movies
            neighbor_movie_titles = [loaded_df.iloc[i]['title'] for i in neighbor_indices]

            return set(neighbor_movie_titles)
        else:
            return "No similar movie found. Please enter a valid movie name."
    else:
        return "No match found for the entered movie name."

