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
    html.P(children='''
    A bar chart broken down by political actor and sentiment helps you understand how the connotation of the conversation changes as different political actors are being mentioned. 
    For instance, highly positive language or negative language around a specific actor helps show the commentator's emotions towards said actor.
        '''),

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
            Then, declare your "app" variable NOTE TO SELF: PROBABLY EXPLAIN HOW THE WEBPAGE WORKS IN THE HOME PAGE? 
            '''),

        dcc.Markdown(f'```python\n{c_app}\n```'),

        html.Br(),

        html.P('''
        Your actor columns must be represented as a binary variable (a 1 if the actor is mentioned in the test, a 0 if not). 
        If you have not yet created actor columns (or found sentiment), reference the data cleaning page to learn more about what these columns are and get the steps to create them.
        Create a dataframe that groups by the sentiment and, for each actor, find the percent of tweets that are positive, negative, and neutral.
        We sort the values by negative %. 
            ''', html.A('data cleaning page', href='/data-cleaning')),
                
        dcc.Markdown(f'```python\n{c_toy_actor}\n```'),

        html.Br(),

        html.P('''
        Create a bar chart figure, where the actor is shown on the x-axis and two corresponding bars, 
        the positive and negative percent (you can add "neu_percent" to the y), appear for each one.'''),
                
        dcc.Markdown(f'```python\n{c_actor_fig}\n```'),

        html.Br(),

        html.P('''
        Create a bar chart figure, where the actor is shown on the x-axis and two corresponding bars, 
        the positive and negative percent (you can add "neu_percent" to the y), appear for each one.'''),
                
        dcc.Markdown(f'```python\n{c_actor_fig}\n```'),

        html.Br(),

        html.P('''
        Create the app layout. Launch the web server and start the application. When running this script in your terminal (in the virtual environment),
        the terminal will return a link for you to view the page on your web browser. '''),
                
        dcc.Markdown(f'```python\n{c_final}\n```'),

        html.Br(),
        html.P('''
        Note: this tutorial is very similar to the one on creating a sentiment bar chart by hashtag.
            ''', html.A('on creating a sentiment bar chart by hashtag', href='/hashtag_barchart_app.py')),
        ])
    ])
