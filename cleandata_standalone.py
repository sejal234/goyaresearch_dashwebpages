#HOW TO CLEAN DATA

import dash
from dash import html, dcc
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)


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

app.layout = html.Div(children=[

    #introducation block
    html.H2(children='Cleaning Scraped Data'),
    
    html.P('''After using the Tweepy API to scrape tweets, we need to clean our dataset. Check out the (link) page to learn more! For reference, this dataset is represented as a pandas dataframe, 
    and has the columns (as I named them during the scraping process) author id, created_at, geo id, lang, like_count, quote_count, reply_count, retweet_count, impression_count, and tweet, 
    which correlate with the [something abt the tweet object link it here or something idk]. Each row is an individual tweet. This cleaning process drops duplicate tweets, 
    filters for hashtags/actors (customizable for research purposes), uses the geo tweet object (confirm if this is right) to find tweet locations, and
    applies NTLK's VADER Tool to perform sentiment analysis.'''),

    html.Br(),

    #it'd be cool if i could somehow put snapshot in here of what the df looks like ? so u can see what the code is doing ? idk

    html.P('First, import the required API and load your dataframe in. We use the variable name "all_tweets" throughout the cleaning process. '),
    
    dcc.Markdown(f'```python\n{c_load}\n```'),

    html.Br(),

    html.P('Follow the following steps to clean your data.'),

    html.Br(),

    #duplicate/retweet tweet block

    html.H5(children='Step 1: Drop Duplicate Tweets and Retweets'),

    html.P('''If you use keywords to scrape tweets, multiple keywords could flag the tweet, making it appear multiple times in your dataset. 
    When scraping tweets, each retweet of a tweet appears as a seperate tweet in the dataset. 
    IE if a tweet was retweeted four times, the original tweet + the four retweets (signalled by a 'RT @[username]') will each appear in the dataset. 
    We drop all retweets to only look at original tweets.'''),

    dcc.Markdown(f'```python\n{c_duplicates}\n```'),

    html.Br(),

    #hashtag block
    
    html.H5(children='Step 2: Create Hashtag Columns'),

    html.P('''This is a function that uses the "tweet" column (a string with the text of the tweet) to search if a tweet contains a specified hashtag.
           Alter the list "hashtags" for your research purposes. Each hashtag is represented as a column in the dataset. For each row, the value is 1 if the 
              hashtag is mentioned in the row tweet, and 0 if not. '''),

    dcc.Markdown(f'```python\n{c_hashtag}\n```'),

    html.Br(),

    #actor block

    html.H5(children='Step 3: Create Actor Columns'),

    html.P('''This is similar to the hashtag columns. Make a "mentions_actor" function for each actor of choice (the examples below are functions that search
    for instances of Donald Trump and Julián Castro) and compile each function in the "actor_functions" list. Keys to search for an actor include their username
    (without the '@' symbol), common nicknames, and variations of their names. Each actor is represented as a column in the dataset. For each row, the value is 1 if the 
    actor is mentioned in the row tweet, and 0 if not. '''),

    dcc.Markdown(f'```python\n{c_actor}\n```'),

    html.Br(),

    #location block
    
    html.H5(children='Step 4: Find Locations of Tweets'),

    html.P('''Some tweets come with a "geo id", which we saved in the column "geo" when scraping tweets. 
           We can use our API to convert these geo ids to actual location names (ex: '011add077f4d2da3' becomes 'Brooklyn, NY').
           First, intialize the API. '''),

    dcc.Markdown(f'```python\n{c_intialize}\n```'),

    html.Br(),

    html.P('''Then, use this API to convert geo ids to location names.'''),

    dcc.Markdown(f'```python\n{c_location}\n```'),

    html.Br(),

    html.P('''Use these location names to pull longitude/latitude coordinates for mapping purposes. 
    These will not be the actual longitude/latitude of where the tweet came from, but rather a general reference of what city the tweet was tweeted from.'''), 

    dcc.Markdown(f'```python\n{c_longitude}\n```'),

    html.Br(),

    #sentiment block

    html.H5(children='Step 5: Sentiment Analysis'),

    html.P('''text'''),

    dcc.Markdown(f'```python\n{c_sentiment}\n```'),

    html.Br(),

    ])

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)