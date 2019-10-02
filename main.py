
from pprint import pprint
import tweepy
import numpy as np
import pandas as pd
import text_classification
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import re
import pyrebase
import json
import database as db

#authenticate with twitter

def authenticate():
    #CONSUMER_KEY    =  'Z7Ww83km4ElGyxePAHVkK1ktt'
    #CONSUMER_SECRET =  'B64oPhYkqH6AR4Zzd03TYLTr0zNMeauXBtiD2JIe0miDWKEyTm'
    #ACCESS_TOKEN  =  '1015296632168931329-rjUhJK81rTjb6kouaESjAYPSzO6l4V'
    #ACCESS_SECRET = 'muryPklbv9n9XQVRUVZgMp7gstQz3MML0nHM5ye45oALR'
    CONSUMER_KEY = '189YcjF4IUzF156RGNGNucDD8'
    CONSUMER_SECRET = 'd7HY36s4pSh03HxjDg782HupUjmzdOOSDd98hd'
    ACCESS_TOKEN = '2543812-cpaIuwndjvbdjaDDp5izzndhsD7figa9gb'
    ACCESS_SECRET = '4hdyfnas7d988ddjf87sJdj3Dxn4d5CcNpwe'
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

#call authenticate
    
auth = authenticate()

#mine the tweet under hashtags

query = 'modi'
max_tweets = 1000
mined_tweets=tweepy.Cursor(auth.search, q=query).items(max_tweets)
tweets=list()
for mined_tweet in mined_tweets:
    tweets.append(mined_tweet)
#tweets = authenticate.user_timeline(screen_name="realDonaldTrump", count=200)
#get lenght of the mined tweets
print("Number of tweets extracted: {}.\n".format(len(tweets)))


####################################################################

# read the input data  from file instead of mining


with open('night.json') as f:
    tweets= json.load(f)
print("Number of tweets extracted: {}.\n".format(len(tweets))) 

####################################################################

#clean the text and put into  the data frame
def clean_tweet(tweet):
    return ' '.join(re.sub("(RT|@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",tweet).split())

twitter_data =list()
for tweet in tweets:
    clean_text=clean_tweet(tweet["text"])
    twitter_data.append(clean_text)
    

data= pd.DataFrame(data=twitter_data, columns=['Tweets'])
tweet_vector=data["Tweets"]
sentiment_vector = text_classification.getSentimentVector(tweet_vector)


#add sentiment vector in the data frame

data['Sentiment Score']  = sentiment_vector
sentiment_type = list()
for score in data["Sentiment Score"]:
    if score==1:
        sentiment_type.append("positive")
    else :
        sentiment_type.append("negative")
        
data["Sentiment Type"] =np.array(sentiment_type)

positive_tweets=[]
negative_tweets=[]

for index,tweet in enumerate(data["Tweets"]):
    if data["Sentiment Type"][index]=="positive":
        positive_tweets.append(tweet)
    else:
        negative_tweets.append(tweet)
        
        
print("Percentage of positive tweets: {}%".format(len(positive_tweets)*100/len(data['Tweets'])))
print("Percentage de negative tweets: {}%".format(len(negative_tweets)*100/len(data['Tweets'])))


print(dir(tweets[0]))





data['Date'] = np.array([tweet["created_at"] for tweet in tweets])
data['Source'] = np.array([tweet["source"] for tweet in tweets])
data['Likes']  = np.array([tweet["favorite_count"] for tweet in tweets])
data['ReeTweets count']    = np.array([tweet["retweet_count"] for tweet in tweets])

diction=data.T.to_dict()
result = db.insertData(diction)

typ =[len(positive_tweets)*100/len(data['Tweets']),(len(negative_tweets)*100/len(data['Tweets']))]
labels=["positive","negative"]
figureObject, axesObject = plt.subplots()

# Draw the pie chart
axesObject.pie(typ,
        labels=labels,
        autopct='%1.2f',
        startangle=90)
# Aspect ratio - equal means pie is a circle
axesObject.axis('equal')
plt.show()
