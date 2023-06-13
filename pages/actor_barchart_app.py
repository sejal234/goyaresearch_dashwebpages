#BARCHART ATTEMPT 1

import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np

from actor_hashtag_instructions import *

dash.register_page(__name__)

# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('full_tweet_list.csv')
# # if your variable columns is represented as counts, convert count values to binary (0 or 1)
columns_to_convert = ['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo']
df[columns_to_convert] = np.where(df[columns_to_convert] > 0, 1, 0)

def create_percents(df):
    df["total"] = df["negative"] + df["neutral"] + df["positive"]
    df["neg_percent"] = df["negative"] / df["total"] * 100
    df["neu_percent"] = df["neutral"] / df["total"] * 100
    df["pos_percent"] = df["positive"] / df["total"] * 100
    df = df.sort_values('neg_percent', ascending=False)
    return df

toy_actor_df = df.groupby('sentiment').sum()[['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo']].T.reset_index()
toy_actor_df = create_percents(toy_actor_df)  


fig = px.bar(toy_actor_df, x="index", y=["neg_percent", "pos_percent"], 
                 color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
                  barmode='group', title="Sentiment by Actor")
fig.update_layout(xaxis_title='Actor', yaxis_title='Percent of Tweets')

layout = html.Div(children=[
    html.H1(children='Sentiment by Actor', style={'textAlign':'center'}),
    html.Br(),
    html.Div(children='''update'''),
    dcc.Graph(id='graph-content', figure = fig),
    html.Br(),

    html.Div([
        html.H2(children='How can I recreate this code?'),

        html.Br(),

        html.P(children='''
            This tutorial shows you how to make a Dash Webpage, but to replicate the graph itself, use the plotly.express "bar" tool. 
            You can also follow the cleaning/graphing parts of this tutorial and ignore the configuration of the dash webpage. 
            To replicate the full webpage, use the following tutorial. Begin with import statements:
            '''),
                
        dcc.Markdown(f'```python\n{c_import}\n```'),

        html.Br(),

        html.P(children='''
        For this tutorial to work, 
            '''),
                
        dcc.Markdown(f'```python\n{c_import}\n```'),

        html.Br(),


        ]),


    ])

# layout = html.Div(children=[
#     html.H2(children='Sentiment by Variable'),
#     html.Div(children='''Exploring the sentiment behind reactions to the Goya Boycott. Use the dropdown to select the variable to examine.'''),
#     # dcc.Dropdown(
#     #     id='input-dropdown',
#     #     options=[
#     #         {'label': 'Actor', 'value': 'actor'},
#     #         {'label': 'Hashtag', 'value': 'hashtag'}
#     #     ],
#     #     value='actor'),
#     #dcc.Graph(id='example-graph'),
#     html.Div(children='''Want to reproduce this code? Refer to this script. (note to self: insert script)'''),
# ])

# @callback(
#     Output('example-graph', 'figure'),
#     Input('input-dropdown', 'value')
# )
# def update_graph(input_value):
    #print('Input Value:', input_value)
    # if input_value == 'actor':
    #     fig = px.bar(toy_actor_df, x="index", y=["neg_percent", "pos_percent"], 
    #                  color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
    #                  barmode='group', title="Sentiment by Actor")
    #     fig.update_layout(xaxis_title='Actor', yaxis_title='Percent of Tweets')

    # elif input_value == 'hashtag':
    #     fig = px.bar(hasht, x="index", y=["neg_percent", "pos_percent"], 
    #                  color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
    #                  barmode='group', title="Sentiment by Hashtag")
    #     fig.update_layout(xaxis_title='Hashtag', yaxis_title='Percent of Tweets')

    # return fig
