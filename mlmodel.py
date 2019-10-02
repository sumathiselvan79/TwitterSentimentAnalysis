# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 02:35:58 2018

@author: vinod arjun

"""
import nltk
import pandas as pd

from sklearn.cross_validation import train_test_split

from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer

from nltk.tokenize import TweetTokenizer

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import confusion_matrix

import re

import json


def clean_tweet(tweet):
    return ' '.join(re.sub("(@RT[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",tweet).split())

with open('tweet.json') as f:
    tweets= json.load(f)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

########################################################################
twitter_data =list()
for tweet in tweets:
    text= clean_tweet(tweet["text"])
    twitter_data.append(text)
    print(text+"\n")
    
dat = pd.Series(data=twitter_data)
data = pd.read_csv('train.csv', encoding="Windows-1252")

print(data["Sentiment"])

X_train =data["SentimentText"]

y_train =data["Sentiment"]
tknzr = TweetTokenizer()

vect = TfidfVectorizer(strip_accents='unicode', tokenizer=tknzr.tokenize, ngram_range=(1, 2), max_df=0.9, min_df=3, sublinear_tf=True)
tfidf_train = vect.fit_transform(X_train)
tfidf_test = vect.transform(dat)
    
model = LogisticRegression(C=30, dual=True,max_iter=1000)
model.fit(tfidf_train, y_train)
preds = model.predict(tfidf_test)
accuracy = (preds==dat).mean()  
confusion_matrix(dat, preds, labels=None, sample_weight=None)
