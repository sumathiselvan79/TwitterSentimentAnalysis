
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from nltk.tokenize import TweetTokenizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import re
from scipy.sparse import csr_matrix
import json
data = pd.read_csv('train.csv', encoding="Windows-1252")
def clean_tweet(tweet):
    return ' '.join(re.sub("(@RT[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",tweet).split())

def getSentimentVector(twitter_frame):
    X_train =data["SentimentText"]
    X_train = [clean_tweet(text) for text in X_train ]
    X_train =pd.Series(data=X_train)
    y_train =data["Sentiment"]
    tknzr = TweetTokenizer()    
    vect = CountVectorizer( tokenizer=tknzr.itokenize)
    tf_train = vect.fit_transform(X_train)
    tf_test = vect.transform(twitter_frame)
       #vect = TfidfVectorizer(strip_accents='unicode', tokenizer=tknzr.tokenize, ngram_range=(1, 2), max_df=0.9, min_df=3, sublinear_tf=True)
    #tfidf_train = vect.fit_transform(X_train)
    #tfidf_test = vect.transform(data_frame)
    model = LogisticRegression(C=30, dual=True,max_iter=1000)
    model.fit(tf_train, y_train)
    pred = model.predict(tf_test)
    return pred

text = input("enter the text")
text_vector=[[]]
text_vetor.append([text])

output_vector=getSentimetnVector(text_vector)
print(output_vector)
