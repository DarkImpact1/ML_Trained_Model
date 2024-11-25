import os
import re
import pickle
import gzip
import io
from fuzzywuzzy import process
import nltk
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Download required NLTK resources
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Initialize NLP utilities
porter = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Directory path
path = "DumpedFile"

### Preprocessing Utility Functions ###
def preprocess_text(review):
    """Preprocesses text by removing HTML tags, stopwords, and stemming."""
    text = re.sub(r'<br />', ' ', review.lower())
    stemmed_text = [porter.stem(word) for word in re.findall(r'\b[a-zA-Z]+\b', text) if word not in stop_words]
    return " ".join(stemmed_text)

### Sentiment Analysis Section ###
# File paths for sentiment analysis
sentiment_tokenizer_file_path = os.path.join(path, "classifierTokenizer.pkl")
sentiment_vectorizer_file_path = os.path.join(path, "vectorizer.pkl")
sentiment_model_file_path = os.path.join(path, "trained_model.pkl")
compressed_sentiment_model_file_path = os.path.join(path, "classifierModel.pkl.gz")

# Load sentiment tokenizer
loaded_sentiment_tokenizer = pickle.load(open(sentiment_tokenizer_file_path, 'rb'))

# Load compressed LSTM sentiment model
with gzip.open(compressed_sentiment_model_file_path, 'rb') as f:
    buffer = io.BytesIO(f.read())
    buffer.seek(0)  # Reset buffer position to start
    loaded_LSTM_model = pickle.load(buffer)

# LSTM-based Sentiment Prediction
def predictionsLSTM(text):
    """Predicts sentiment using the loaded LSTM model."""
    text = preprocess_text(text)
    text = loaded_sentiment_tokenizer.texts_to_sequences([text])
    text = pad_sequences(text, maxlen=200, padding='post', truncating='post')
    prediction = loaded_LSTM_model.predict(text)
    return "Positive" if prediction > 0.5 else "Negative"

# Load additional sentiment analysis resources
loaded_sentiment_vectorizer = pickle.load(open(sentiment_vectorizer_file_path, 'rb'))
loaded_sentiment_model = pickle.load(open(sentiment_model_file_path, 'rb'))

def make_prediction(review):
    """Predicts sentiment using a traditional ML model."""
    processed_review = preprocess_text(review)
    vector = loaded_sentiment_vectorizer.transform([processed_review])
    pred = loaded_sentiment_model.predict(vector)
    return "Positive" if (pred == 1) else "Negative"

### Movie Recommender System Section ###
# File paths for recommender system
rec_vec_file_path = os.path.join(path, "movie_rec_vec.pkl")
compressed_rec_model_file_path = os.path.join(path, "movie_recommender_model.pkl.gz")
rec_df_path = os.path.join(path, "movie_dataframe.pkl")

# Load movie recommender resources
loaded_df = pickle.load(open(rec_df_path, 'rb'))
loaded_rec_vec = pickle.load(open(rec_vec_file_path, 'rb'))

# Load compressed recommender model
with gzip.open(compressed_rec_model_file_path, 'rb') as f:
    buffer = io.BytesIO(f.read())
    buffer.seek(0)  # Reset buffer position to start
    loaded_compressed_rec_model = pickle.load(buffer)

def get_recommendations(movie_name_query):
    """Fetches movie recommendations for a given movie name."""
    # Find the closest matching movie name using fuzzy matching
    closest_match = process.extractOne(movie_name_query, loaded_df['title'])

    if closest_match is not None:
        closest_movie_name, similarity_score = closest_match[0], closest_match[1]

        if similarity_score >= 80:
            # Find the index of the closest matching movie
            movie_index = loaded_df.index[loaded_df['title'] == closest_movie_name].tolist()[0]

            # Transform the movie tags into TF-IDF vectors
            movie_vector = loaded_rec_vec.transform([loaded_df.iloc[movie_index]['tags1']]).toarray()

            # Find the k nearest neighbors of the movie
            distances, indices = loaded_compressed_rec_model.kneighbors(movie_vector, n_neighbors=7)

            # Exclude the first neighbor (the movie itself)
            neighbor_indices = indices.flatten()[1:]

            # Get the titles of the nearest neighbor movies
            neighbor_movie_titles = [loaded_df.iloc[i]['title'] for i in neighbor_indices]

            return {
                "Recommended Movies": set(neighbor_movie_titles),
                "Closest Match": closest_movie_name
            }
        else:
            return {"Error": "Low similarity score. No recommendations found."}
    else:
        return {"Error": "No matching movie found."}
