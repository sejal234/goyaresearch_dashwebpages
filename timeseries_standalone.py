    
#TIMESERIES ATTEMPT 1

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)

# df = pd.read_csv('full_tweet_list.csv')
# df[['date', 'time']] = df['created_at'].str.split(" ", expand=True)
# date = df.copy()
# columns_to_convert = ['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo', '#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']
# date[columns_to_convert] = date[columns_to_convert].applymap(lambda x: 1 if x > 0 else 0)
# date['total'] = 1

# #now aggregate by date
# columns_to_sum = columns_to_convert + ['total']
# date = date.groupby('date')[columns_to_sum].sum().reset_index()

# #and then aggregate by date (summing up the columns to convert),  
# #and then go back in and add each tweet and retweet_count value at max_retweet_idx ?
# max_retweet_idx = date.groupby('date')['retweet_count'].idxmax()
# max_tweets = df[['date', 'id', 'retweet_count', 'tweet']].iloc[max_retweet_idx]

# df_full = pd.merge(max_tweets, date,  how='left', left_on=['date'], right_on = ['date'])




# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.read_csv('full_tweet_list.csv')
# date = df.copy()
# date[['date', 'time']] = df['created_at'].str.split(" ",expand=True)
# date = date.groupby('date').agg(lambda x: (x != 0).sum()).reset_index() 
# date['date'] = pd.to_datetime(date['date'])

#the callback - what choices should the viewer be able to use to pick the tweet?
date = date.rename(columns={"id": "total"}) #because id represents the total amount of tweets
opt = ['total', 'aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo',
       '#BuycottGoya', '#BoycottGoya','#BuyGoya', '#Goyaway']

app.layout = html.Div([
    html.H4('Tweets Over Time'),
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

@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    fig = px.line(date, x='date', y=ticker)
    fig.update_xaxes(
        rangeslider_visible=True,
        range=['2020-07-11', '2021-02-01'],
        rangeselector=dict(
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

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)

