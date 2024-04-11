import os
import re
import pickle
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
porter = PorterStemmer()
stop_words = set(stopwords.words('english'))


def preprocess_text(review):
    text = re.sub(r'<br />', ' ', review.lower())
    stemmed_text = [porter.stem(word) for word in re.findall(r'\b[a-zA-Z]+\b', text) if word not in stop_words]
    processed_review = " ".join(stemmed_text)
    return processed_review

path = "DumpedFile"
vectorizer_file_path = os.path.join(path,"vectorizer.pkl")
model_file_path = os.path.join(path,"trained_model.pkl")

loaded_vectorizer = pickle.load(open(vectorizer_file_path,'rb'))
loaded_model = pickle.load(open(model_file_path,'rb'))

def make_prediction(review):
    processed_review = preprocess_text(review)
    vector = loaded_vectorizer.transform([processed_review])
    pred  = loaded_model.predict(vector)
    return "Positive" if (pred == 1) else "Negative"
    

