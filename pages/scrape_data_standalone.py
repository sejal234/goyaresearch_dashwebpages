import dash
from dash import html, dcc

dash.register_page(__name__,
    path='/scrape_twitter_data',
    title='1: Scrape Twitter Data',
    name='1: Scrape Twitter Data',
    order = 2)

import_statements = '''
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
'''

load_authorization = '''
os.environ['TOKEN'] = <bearer token here>

def auth():
    return os.getenv('TOKEN')
'''

code_helper1 = '''
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers
'''

code_helper2 ='''
def create_url(keyword, start_date, end_date, max_results = 10):
    
    search_url = "https://api.twitter.com/2/tweets/search/all" #to access full-archive search endpoint.

    #https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
    query_params = {'query': keyword,
                    'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)
'''

code_helper3 = '''
def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
'''
code_helper4 = '''
def append_to_csv(json_response, fileName):

    #A counter variable
    counter = 0

    #Open OR create the target CSV file
    csvFile = open(fileName, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Loop through each tweet
    for tweet in json_response['data']:
        
        # We will create a variable for each since some of the keys might not exist for some tweets
        # So we will account for that

        # 1. Author ID
        author_id = tweet['author_id']

        # 2. Time created
        created_at = dateutil.parser.parse(tweet['created_at'])

        # 3. Geolocation
        if ('geo' in tweet):   
            geo = tweet['geo']['place_id']
        else:
            geo = " "

        # 4. Tweet ID
        tweet_id = tweet['id']

        # 5. Language
        lang = tweet['lang']

        # 6. Tweet metrics
        retweet_count = tweet['public_metrics']['retweet_count']
        reply_count = tweet['public_metrics']['reply_count']
        like_count = tweet['public_metrics']['like_count']
        quote_count = tweet['public_metrics']['quote_count']
        impression_count = tweet['public_metrics']['impression_count']

        # 7. Tweet text
        text = tweet['text']
        
        # Assemble all data in a list
        res = [author_id, created_at, geo, tweet_id, lang, like_count, quote_count, reply_count, retweet_count, impression_count, text]
        
        # Append the result to the CSV file
        csvWriter.writerow(res)
        counter += 1

    # When done, close the CSV file
    csvFile.close()

    # Print the number of tweets for this iteration
    print("# of Tweets added from this response: ", counter) 
'''

code_function = '''
def search_tweets(keyword, filename):
    """
    keyword & filename should both be strings, filename should end in .csv
    """
    keyword = keyword
    FILENAME = filename

    #remains same
    bearer_token = auth()
    headers = create_headers(bearer_token)

    #this is just lists i created, since theres a lot of tweets at the beginning i decided
        #to split the beginning up a bit
    start_list2 = [    '2020-07-09T00:00:00.000Z',
    '2020-07-09T12:00:00.000Z',
    '2020-07-10T00:00:00.000Z',
    '2020-07-10T12:00:00.000Z',
    '2020-07-11T00:00:00.000Z',
    '2020-07-11T12:00:00.000Z',
    '2020-07-12T00:00:00.000Z',
    '2020-07-12T12:00:00.000Z',
    '2020-07-13T00:00:00.000Z',
    '2020-07-13T12:00:00.000Z',
    '2020-07-14T00:00:00.000Z',
    '2020-07-14T12:00:00.000Z',
    '2020-07-15T00:00:00.000Z',
    '2020-07-15T12:00:00.000Z',
    '2020-07-16T00:00:00.000Z',
    '2020-07-16T12:00:00.000Z',
    '2020-07-17T00:00:00.000Z',
    '2020-07-17T12:00:00.000Z',
    '2020-07-18T00:00:00.000Z',
    '2020-07-18T12:00:00.000Z',
    '2020-07-19T00:00:00.000Z',
    '2020-07-19T12:00:00.000Z',
    '2020-07-20T00:00:00.000Z',
    '2020-07-20T12:00:00.000Z',
    '2020-07-21T00:00:00.000Z',
             '2020-07-23T00:00:00.000Z', 
         '2020-08-06T00:00:00.000Z',  
         '2020-08-20T00:00:00.000Z',  
             '2020-09-03T00:00:00.000Z', 
         '2020-09-17T00:00:00.000Z', 
         '2020-10-01T00:00:00.000Z', 
             '2020-10-15T00:00:00.000Z', 
         '2020-10-29T00:00:00.000Z', 
         '2020-11-12T00:00:00.000Z', 
             '2020-11-26T00:00:00.000Z', 
         '2020-12-10T00:00:00.000Z', 
         '2020-12-24T00:00:00.000Z', 
             '2021-01-07T00:00:00.000Z', 
         '2021-01-28T00:00:00.000Z']

    end_list2 = ['2020-07-09T12:00:00.000Z',
    '2020-07-10T00:00:00.000Z',
    '2020-07-10T12:00:00.000Z',
    '2020-07-11T00:00:00.000Z',
    '2020-07-11T12:00:00.000Z',
    '2020-07-12T00:00:00.000Z',
    '2020-07-12T12:00:00.000Z',
    '2020-07-13T00:00:00.000Z',
    '2020-07-13T12:00:00.000Z',
    '2020-07-14T00:00:00.000Z',
    '2020-07-14T12:00:00.000Z',
    '2020-07-15T00:00:00.000Z',
    '2020-07-15T12:00:00.000Z',
    '2020-07-16T00:00:00.000Z',
    '2020-07-16T12:00:00.000Z',
    '2020-07-17T00:00:00.000Z',
    '2020-07-17T12:00:00.000Z',
    '2020-07-18T00:00:00.000Z',
    '2020-07-18T12:00:00.000Z',
    '2020-07-19T00:00:00.000Z',
    '2020-07-19T12:00:00.000Z',
    '2020-07-20T00:00:00.000Z',
    '2020-07-20T12:00:00.000Z',
    '2020-07-21T00:00:00.000Z',
                 '2020-07-23T00:00:00.000Z', 
         '2020-08-06T00:00:00.000Z', 
         '2020-08-20T00:00:00.000Z', 
            '2020-09-03T00:00:00.000Z', 
         '2020-09-17T00:00:00.000Z', 
         '2020-10-01T00:00:00.000Z', 
             '2020-10-15T00:00:00.000Z', 
         '2020-10-29T00:00:00.000Z', 
         '2020-11-12T00:00:00.000Z', 
             '2020-11-26T00:00:00.000Z', 
         '2020-12-10T00:00:00.000Z', 
         '2020-12-24T00:00:00.000Z', 
             '2021-01-07T00:00:00.000Z', 
         '2021-01-28T00:00:00.000Z', 
             '2021-02-02T00:00:00.000Z']
    max_results = 500


    #Total number of tweets we collected from the loop
    total_tweets = 0

    # Create file
    csvFile = open(FILENAME, "a", newline="", encoding='utf-8')
    csvWriter = csv.writer(csvFile)

    #Create headers for the data you want to save, in this example, we only want save these columns in our dataset
    csvWriter.writerow(['author id', 'created_at', 'geo', 'id','lang', 'like_count', 'quote_count', 'reply_count','retweet_count','impression_count','tweet'])
    csvFile.close()

    for i in range(0,len(start_list2)):

        # Inputs
        count = 0 # Counting tweets per time period
        max_count = 100 # Max tweets per time period
        flag = True
        next_token = None

        # Check if flag is true
        while flag:
            # Check if max_count reached
            if count >= max_count:
                break
            print("-------------------")
            print("Token: ", next_token)
            url = create_url(keyword, start_list2[i],end_list2[i], max_results)
            json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
            result_count = json_response['meta']['result_count']

            if 'next_token' in json_response['meta']:
                # Save the token to use for next call
                next_token = json_response['meta']['next_token']
                print("Next Token: ", next_token)
                if result_count is not None and result_count > 0 and next_token is not None:
                    print("Start Date: ", start_list2[i])
                    append_to_csv(json_response, FILENAME)
                    count += result_count
                    total_tweets += result_count
                    print("Total # of Tweets added: ", total_tweets)
                    print("-------------------")
                    time.sleep(5)                
            # If no next token exists
            else:
                if result_count is not None and result_count > 0:
                    print("-------------------")
                    print("Start Date: ", start_list2[i])
                    append_to_csv(json_response, FILENAME)
                    count += result_count
                    total_tweets += result_count
                    print("Total # of Tweets added: ", total_tweets)
                    print("-------------------")
                    time.sleep(5)

                #Since this is the final request, turn flag to false to move to the next time period.
                flag = False
                next_token = None
            time.sleep(5)
    print("Total number of results: ", total_tweets)
    
    return "All done!"

#An example of how to run the code
search_tweets('#BuyGoya', "Dataframes/BuyGoya.csv")
'''

code_run = '''
words = ["Latino", "Latine", "Latina", "Latinx", "heartbroken", "disrespect", "protest", "protester", "criminal", "speaking for", "economy", "leaders", "leadership", "free speech", "truly blessed", "cancel culture",
         "activists", "activism", "adobo", "adobo sauce", "beans", "seasoning", "over", "friendship", "bad marketing", 
         "disappointment", "disillusioned", "sad", "disappointed", "sofrito", "recipes", "family"]

for i in words:
    query_goya = "Goya " + i
    url_goya = ("Dataframes/Goya_" + i + '.csv')
    search_tweets_short(query_goya, url_goya)
    query_unanue = "Unanue " + i
    url_unanue = ("Dataframes/Unanue_" + i + '.csv')
    search_tweets_short(query_unanue, query_unanue)
'''

layout = html.Div([
    html.H2(children='Scraping Twitter Data!'),

     html.P(children=[
        """We used Tweepy to scrape our dataset. We searched for a collection of keywords related to the Goya Boycott within a specified
        timeframe. We followed the """,
        html.A("hyperlinked tutorial", 
               href="https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a",
                target="_blank"),
        " to scrape our Twitter Data."]),

    html.Br(),

    html.P(children=[
        "First, load the neccessary import statements and create an authorization function with your bearer token. You will need a Tweepy Developer account with access to the Academic Research track. Find more information ",
         html.A("here.", 
               href="https://towardsdatascience.com/an-extensive-guide-to-collecting-tweets-from-twitter-api-v2-for-academic-research-using-python-3-518fcb71df2a",
                target="_blank")]),

    dcc.Markdown(f'```python\n{import_statements}\n```'),

    dcc.Markdown(f'```python\n{load_authorization}\n```'),

    html.Br(),

    html.P('''Code in neccesary helper functions: headers, URL, and connecting to the endpoint.'''),
           
    dcc.Markdown(f'```python\n{code_helper1}\n```'),
    dcc.Markdown(f'```python\n{code_helper2}\n```'),
    dcc.Markdown(f'```python\n{code_helper3}\n```'),
    dcc.Markdown(f'```python\n{code_helper4}\n```'),

    html.Br(),

    html.P('''
        Write a function to loop through set time periods and collect tweets. We found that the API collects the first 450-500 tweets 
        that meet the query in one request, meaning that if simply set the time period to July 2020 - February 2021, we would only get 
        the first 500 tweets tweeted in July. Since the conversation was much more active in July, we scraped tweets from every 12 hour period
        for the first twelve days, then scraped tweets from every two week period. Modify the code to the time period neccesary for your research purposes. 
    '''),

    dcc.Markdown(f'```python\n{code_function}\n```'),

    html.P('''
        To pull tweets related to the Goya Boycott, we used a set of around 30 keywords. We looped through a list of the keywords and 
        searched tweets containing each word paired with the term "Goya" and tweets containing each word paired with the term "Unanue". We saved each
        result as a seperate dataframe in the "Dateframes" folder in our working directory. Modify the function and keyword list to fit your research purposes.
    '''),

    html.Br(),

    dcc.Markdown(f'```python\n{code_run}\n```'),

    html.P('''
        To clean the data, we combined all the resulting dataframes into one large dataset, where we subsequentially removed duplicate tweets 
        that arise when multiple keywords are mentioned in the same tweet. To clean the data, view the the cleaning tutorial. You can read in each file
        individually, put all file names into a list, and use pd.concat to concatenate the dataframes.
    ''') ])

#i saved them as all seperate dataframes and then combined them into one
# dataframe at the end (which is why i had to remove duplicates)