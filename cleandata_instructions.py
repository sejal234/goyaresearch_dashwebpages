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

c_location = '''
def get_location(geo_id):
    if geo_id == " ": 
        return None
    return api.geo_id(geo_id).full_name

all_tweets['Location'] = all_tweets['geo'].apply(get_location)
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
'''

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

c_longitude = ''' #insert code here '''

c_sentiment = ''' #insert code here '''