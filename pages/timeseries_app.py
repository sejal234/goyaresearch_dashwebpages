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

dash.register_page(__name__)

from timeseries_instructions import *

df = pd.read_csv('full_tweet_list.csv')
df[['date', 'time']] = df['created_at'].str.split(" ", expand=True)
date = df.copy()
columns_to_convert = ['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo', '#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']
date[columns_to_convert] = date[columns_to_convert].applymap(lambda x: 1 if x > 0 else 0)
date['total'] = 1

#now aggregate by date
columns_to_sum = columns_to_convert + ['total']
date = date.groupby('date')[columns_to_sum].sum().reset_index()

#and then aggregate by date (summing up the columns to convert),  
#and then go back in and add each tweet and retweet_count value at max_retweet_idx ?
max_retweet_idx = df.groupby('date')['retweet_count'].idxmax()
max_tweets = df[['date', 'id', 'retweet_count', 'tweet']].iloc[max_retweet_idx]

df_full = pd.merge(max_tweets, date,  how='left', left_on=['date'], right_on = ['date'])

#the callback - what choices should the viewer be able to use to pick the tweet?
opt = ['total', 'aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo',
       '#BuycottGoya', '#BoycottGoya','#BuyGoya', '#Goyaway']

layout = html.Div([
    html.H1(children='Tweets Over Time', style={'textAlign':'center'}),
    html.P(children='''
        A timeseries helps us understand how the conversation surrounding the Goya Boycott changed over time. An initial high spike and the following steady, low conversation indicate
        the conversation was eventful, but short-lived. We can look at how often different political actors were tweeted about to understand how they fit into the conversation. Hovering over 
        a specific date reveals that the most retweeted tweet of that date (related to the the Goya Boycott). 
        '''),
    
    html.Br(),
    dcc.Graph(id="time-series-chart"),
    html.P("Select Variable:"),
    dcc.Dropdown(
        id="ticker",
        options=opt,
        value="total",
        multi = True,
        clearable=False,
    ),
    html.Br(),

    html.Div([
            html.H2(children='How can I recreate this code?'),

            html.Br(),

            # html.P(children='''
            # This tutorial shows you how to make a Dash Webpage, but to replicate the graph itself, use the plotly.express "line" tool, like so:
            #     '''),
            # dcc.Markdown(f'```python\n{c_graph_itself}\n```'),

            html.P(children='''
            This tutorial shows you how to make a Dash Webpage, but to replicate the graph itself, use the plotly.express "line" tool.
            To replicate this webpage, use the following tutorial. Referencing https://plotly.com/python/line-and-scatter/ and 
                https://dash.plotly.com/basic-callbacks may be helpful. Begin with import statements:
                '''),
                   
            dcc.Markdown(f'```python\n{c_import}\n```'),

            html.Br(),

            html.P(children='''
                Then, declare your "app" variable NOTE TO SELF: PROBABLY EXPLAIN HOW THE WEBPAGE WORKS IN THE HOME PAGE? 
                '''),

            dcc.Markdown(f'```python\n{c_app}\n```'),

            html.Br(),

            html.P(children='''
                Clean your data. Your actor and hashtag columns must be represented as a binary variable (a 1 if the actor/hashtag is mentioned in the test, a 0 if not). 
                If you have not yet created actor columns (or found sentiment), reference the data cleaning page to learn more about what these columns are and get the steps to create them.
                Since the timeseries shows the number of tweets per date, we need to extract the date from the "created_at" column and group.
                '''),

            dcc.Markdown(f'```python\n{c_clean}\n```'),

            html.Br(),

            html.P(children='''
                We then go back through and find the index of the most retweeted tweet per day (we later include this in our timeseries hover template).
                '''),

            dcc.Markdown(f'```python\n{c_clean2}\n```'),

            html.Br(),

            html.P(children='''
                Create the callback, which sets the input/output elements, of the app. The "opt" list is the list of columns that the user will be able to display
                as lines in the timeseries.
                '''),

            dcc.Markdown(f'```python\n{c_callback}\n```'),

            html.Br(),
            
            html.P(children='''
                Create the layout (the elements on the webpage), which uses "opt" to create the dropdown menu. 
                '''),

            dcc.Markdown(f'```python\n{c_layout}\n```'),

            html.Br(),

            html.P(children='''
                Create a function to display your graph. This function sets the hover template, a default time range that the user will first see when loading the graph, and customizable
                time range options. The time ranges in the code are 1 month, 3 months, 6 months, and 1 year. 
                '''),

            dcc.Markdown(f'```python\n{c_display}\n```'),

            html.Br(),

            html.P(children='''
            Launch the web server and start the application. When running this script in your terminal, the terminal will return a link for you to view the page on
            your web browser.
                '''),

            dcc.Markdown(f'```python\n{c_run}\n```'),

            html.Br(),
            ]),
])

@callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))

def display_time_series(ticker):
    fig = px.line(df_full, x='date', y=ticker)

    # the hover template is what displays when 
    hover_template = """<b>Most Retweeted Tweet of %{x} (Of All Tweets):</b></br></br>"%{text}"</br>. There were %{y} original tweets tweeted on %{x}."""
    fig.update_traces(hovertemplate=hover_template, text=df_full['tweet'])

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

# # see https://plotly.com/python/px-arguments/ for more options

# df = pd.read_csv('full_tweet_list.csv')
# date = df.copy()
# date[['date', 'time']] = df['created_at'].str.split(" ",expand=True)
# date = date.groupby('date').agg(lambda x: (x != 0).sum()).reset_index() 
# date['date'] = pd.to_datetime(date['date'])

# #the callback - what choices should the viewer be able to use to pick the tweet?
# date = date.rename(columns={"id": "total"}) #because id represents the total amount of tweets
# opt = ['total', 'aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo',
#        '#BuycottGoya', '#BoycottGoya','#BuyGoya', '#Goyaway']

# layout = html.Div([
#     html.Div(children='''
#        Put an explanation of the tool here.
#     '''),

#     html.H2('Tweets Over Time'),
#     dcc.Graph(id="time-series-chart"),
#     html.P("Select Variable:"),
#     dcc.Dropdown(
#         id="ticker",
#         options=opt,
#         value="total",
#         multi = True,
#         clearable=False,
#     ),

#      html.Div([
#             html.H2(children='How can I recreate this code?'),

#             html.Br(),

#             html.P(children='''
#                 To replicate this webpage, use the following code. Referencing https://plotly.com/python/line-and-scatter/ and 
#                 https://dash.plotly.com/basic-callbacks may be helpful. Begin with import statements:
#                 '''),
                   
#             dcc.Markdown(f'```python\n{c_import}\n```'),

#             html.Br(),
            
#             ])

# ])

# @callback(
#     Output("time-series-chart", "figure"), 
#     Input("ticker", "value"))
# def display_time_series(ticker):
#     fig = px.line(date, x='date', y=ticker)
#     fig.update_xaxes(
#         rangeslider_visible=True,
#         range=['2020-07-11', '2021-02-01'],
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=1, label="1m", step="month", stepmode="backward"),
#                 dict(count=3, label="3m", step="month", stepmode="backward"),
#                 dict(count=6, label="6m", step="month", stepmode="backward"),
#                 dict(count=1, label="1y", step="year", stepmode="backward"),
#                 dict(step="all")
#             ])
#         )
#     )
#     return fig