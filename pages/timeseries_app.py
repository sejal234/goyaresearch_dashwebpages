    
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

# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_csv('full_tweet_list.csv')
date = df.copy()
date[['date', 'time']] = df['created_at'].str.split(" ",expand=True)
date = date.groupby('date').agg(lambda x: (x != 0).sum()).reset_index() 
date['date'] = pd.to_datetime(date['date'])

#the callback - what choices should the viewer be able to use to pick the tweet?
date = date.rename(columns={"id": "total"}) #because id represents the total amount of tweets
opt = ['total', 'aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo',
       '#BuycottGoya', '#BoycottGoya','#BuyGoya', '#Goyaway']

layout = html.Div([
    html.Div(children='''
       Put an explanation of the tool here.
    '''),

    html.H2('Tweets Over Time'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select Variable:"),
    dcc.Dropdown(
        id="ticker",
        options=opt,
        value="total",
        multi = True,
        clearable=False,
    ),

     html.Div([
            html.H2(children='How can I recreate this code?'),

            html.Br(),

            html.P(children='''
                To replicate this webpage, use the following code. Referencing https://plotly.com/python/line-and-scatter/ and 
                https://dash.plotly.com/basic-callbacks may be helpful. Begin with import statements:
                '''),
                   
            dcc.Markdown(f'```python\n{c_import}\n```'),

            html.Br(),
            
            ])

])

@callback(
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

c_import = '''
'''