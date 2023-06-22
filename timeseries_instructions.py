c_import = '''
import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np
import json
import re
import flask
'''

c_app = '''
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)
'''

c_clean = '''
# load in your dataframe and extract the date of each tweet 
df = pd.read_csv('full_tweet_list.csv')
df[['date', 'time']] = df['created_at'].str.split(" ", expand=True)
date = df.copy() #creating a copy to avoid messing up the original dataframe

#now aggregate by date (we create a total column to sum the number of tweets per day)
date['total'] = 1
columns_to_sum = ['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo', '#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway', 'total']
date = date.groupby('date')[columns_to_sum].sum().reset_index()
'''

c_clean2 = '''
# find the tweet with the most retweets at each date (can sub retweet_count with any numeric variable)
max_retweet_idx = df.groupby('date')['retweet_count'].idxmax()

# create a dateframe, max_tweets_ with just the most tweeted tweets
max_tweets = df[['date', 'id', 'retweet_count', 'tweet']].iloc[max_retweet_idx]

# merge the dateframes together
df_full = pd.merge(max_tweets, date,  how='left', left_on=['date'], right_on = ['date'])
'''

c_callback = '''
opt = ['total', 'aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo',
       '#BuycottGoya', '#BoycottGoya','#BuyGoya', '#Goyaway']

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
'''

c_layout = '''
app.layout = html.Div([
    html.H1(children='Tweets Over Time', style={'textAlign':'center'}),
    html.P(children=<description here>),
    dcc.Graph(id="time-series-chart"),
    html.P("Select Variable:"),
    dcc.Dropdown(
        id="ticker",
        options=opt,
        value="total",
        multi = True,
        clearable=False,
    ),
])
'''

c_display = '''
def display_time_series(ticker):
    fig = px.line(df_full, x='date', y=ticker)

    # the hover template is what displays when you hover over a date, this is currently set to display the most retweeted tweet
    # x is the data and text is the tweet from "update_traces" 
    # remove the "<>" between opening brackets and variables, those were put in due to Python formatting
    hover_template = """<b>Most Retweeted Tweet of %{<>x} (Of All Tweets):</b></br></br>"%{<>text}"</br>. There were %{<>y} original tweets tweeted on %{<>x}."""
    fig.update_traces(hovertemplate=hover_template, text=df_full['tweet'])
    
    #setting the range for the x-axis
    fig.update_xaxes(
        rangeslider_visible=True,
        range=['2020-07-11', '2021-02-01'], #the default range
        rangeselector=dict(
            #customize buttons to time ranges of your choice
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return fig
'''

c_run = '''
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)
'''

c_graph_itself  = '''
#i don't have anything yet
'''