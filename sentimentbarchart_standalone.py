#BARCHART ATTEMPT 1

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

# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('full_tweet_list.csv')
# # if your variable columns is represented as counts, convert count values to binary (0 or 1)
columns_to_convert = ['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo', '#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']
df[columns_to_convert] = df[columns_to_convert].applymap(lambda x: 1 if x > 0 else 0)

def create_percents(df):
    df["total"] = df["negative"] + df["neutral"] + df["positive"]
    df["neg_percent"] = df["negative"] / df["total"] * 100
    df["neu_percent"] = df["neutral"] / df["total"] * 100
    df["pos_percent"] = df["positive"] / df["total"] * 100
    df = df.sort_values('neg_percent', ascending=False)
    return df

toy_actor_df = df.groupby('sentiment').sum()[['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo']].T.reset_index()
toy_actor_df = create_percents(toy_actor_df)  

hasht = df.groupby('sentiment').sum()[['#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']].T.reset_index()
hasht = create_percents(hasht)  

app.layout = html.Div(children=[
    html.H1(children='Sentiment by Variable'),
    html.Div(children='''Exploring the sentiment behind reactions to the Goya Boycott. Use the dropdown to select the variable to examine.'''),
    dcc.Dropdown(
        id='input-dropdown',
        options=[
            {'label': 'Actor', 'value': 'actor'},
            {'label': 'Hashtag', 'value': 'hashtag'}
        ],
        value='actor'
    ),
    dcc.Graph(id='example-graph')
])

@app.callback(
    Output('example-graph', 'figure'),
    Input('input-dropdown', 'value')
)
def update_graph(input_value):
    #print('Input Value:', input_value)
    if input_value == 'actor':
        fig = px.bar(toy_actor_df, x="index", y=["neg_percent", "pos_percent"], 
                     color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
                     barmode='group', title="Sentiment by Actor")
        fig.update_layout(xaxis_title='Actor', yaxis_title='Percent of Tweets')

    elif input_value == 'hashtag':
        fig = px.bar(hasht, x="index", y=["neg_percent", "pos_percent"], 
                     color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
                     barmode='group', title="Sentiment by Hashtag")
        fig.update_layout(xaxis_title='Hashtag', yaxis_title='Percent of Tweets')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)