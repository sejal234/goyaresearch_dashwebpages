c_load = '''
import pandas as pd

all_tweets = pd.read_csv("/Users/sejalgupta/Documents/GoyaProject/Dataframes/full_tweet_list.csv", index_col = 0)'''

c_duplicates =  '''
df = df.drop_duplicates() #drop duplicate rows ()
df['RT'] = df.apply(lambda x: 'RT @' in x.tweet, axis=1) #find which tweets are actually retweets
df = df[df['RT'] == False] #drop the retweets'''

c_hashtag = '''
def contains_txt(text, word):
    """Check if the given text contains the specified hashtag."""
    if text.lower().count(word.lower()) > 0:
        return 1
    return 0

hashtags = ['#BuycottGoya', '#BoycottGoya', '#BuyGoya', '#Goyaway']
for hashtag in hashtags:
    all_tweets[hashtag] = all_tweets['tweet'].apply(lambda x: contains_txt(x, hashtag))'''

c_actor = '''
def mentions_donald(text):
    """
    text is the entire text of the PDF
    """
    one_word_keys = ["donald", 'donaldtrump', 'realdonaldtrump', 'president trump']
    for word in text.split():
        #to avoid sensitivity to punctuation
        new_string = word.translate(str.maketrans('', '', string.punctuation))
        
        #to avoid sensitivity to case 
        new_string = new_string.lower()
       
        if new_string in one_word_keys:
            return 1
    return 0

def mentions_castro(text):
    """
    text is the entire text of the PDF
    """
    one_word_keys = ["castro", 'julián', 'julian', 'juliancastro'] #includes his twitter
    for word in text.split():
        #to avoid sensitivity to punctuation
        new_string = word.translate(str.maketrans('', '', string.punctuation))
        
        #to avoid sensitivity to case 
        new_string = new_string.lower()
        
        if new_string in one_word_keys:
            return 1
    return 0

actor_functions = [mentions_donald, mentions_castro] #include a function for each actor
for actor in key_actors:
    all_tweets[actor] = 0
#NOTE NOTE NOTE theres definitely a better way to do this with apply or something, come back to this
for row in range(len(all_tweets)):
    for idx in range(len(key_actors)):
        all_tweets[key_actors[idx]][row] = actor_functions[idx](all_tweets["tweet"][row])
'''
c_intialize = '''
import tweepy #we need tweepy to initialize our API object

#this information comes from your tweepy account
consumer_key = XXXXXXXXXXXXXXXXXXX 
consumer_secret = XXXXXXXXXXXXXXXXXXX 
access_token = XXXXXXXXXXXXXXXXXXX 
access_token_secret =  XXXXXXXXXXXXXXXXXXX 

#initialize api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#import geopy
import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent = 'example app')
'''

c_location = '''
def get_location(geo_id):
    if geo_id == " ": 
        return None
    return api.geo_id(geo_id).full_name

all_tweets['Location'] = all_tweets['geo'].apply(get_location)
'''

c_longitude = '''
all_tweets['Location'].fillna('', inplace=True) #the geocoder will read "NaN" as Nanno, Italy, this helps prevent that

#its fastest to find the longtitude/latitude values of each unique city and then merge the dataframe back with the full one
city_df = pd.DataFrame()
city_df['Location'] = all_tweets['Location'].unique()

#get the location
city_df["loc"] = city_df["Location"].apply(geolocator.geocode)

#Get .point containing latitude and longitude from the geocodes response, if its not None.
city_df["point"]= city_df["loc"].apply(lambda loc: tuple(loc.point) if loc else (None, None, None))

#Split the .point into separate columns 'lat' 'lon' and 'altitude'
city_df[['lat', 'lon', 'altitude']] = pd.DataFrame(city_df['point'].to_list())

#Merge the dataframe back together
all_tweets = all_tweets.merge(city_df[['lat', 'lon', 'Location']], on = 'Location')
'''

c_senti_import = '''
#import the neccessary NLP packages
from textblob import TextBlob
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
'''

c_sentiment = '''
def create_sentiment_df(dataframe, column_name):
    """
    Inputs:
    - dataframe, the dataframe of tweets you want to find sentiments for
    - column_name, the column in the dataframe the text is in (in this case, tweets)
    column_name is the name of the col you have the text in
    
    Output:
    - senti_df, the dataframe with the labelled sentiment and the compound score for each tweet
    """
    senti_df = dataframe.copy()
    senti_df['sentiment'] = None
    senti_df['compound_score'] = None
    
    # a count of how many articles are positive, neg, 
    positive = 0 
    negative = 0
    neutral = 0
    
    for i in range(len(senti_df)):
        text = senti_df[column_name][i]
        analysis = TextBlob(text)
        
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        comp = score['compound']

        #these metrics are from https://github.com/cjhutto/vaderSentiment
        if comp <= -.05:
            negative += 1
            senti_df["sentiment"][i] = 'negative'
        elif comp >= 0.05:
            positive += 1
            senti_df["sentiment"][i] = 'positive'
        elif comp > -0.05 and comp < 0.05:
            neutral += 1
            senti_df["sentiment"][i] = 'neutral'

        #if i want to go back and reference the compound score
        senti_df['compound_score'][i] = comp 
    
    print(positive, "2Positive Tweets")
    print(negative, "Negative Tweets")
    print(neutral, "Neutral Tweets")
    return senti_df

all_tweets = create_sentiment_df(all_tweets, 'tweet')
'''
