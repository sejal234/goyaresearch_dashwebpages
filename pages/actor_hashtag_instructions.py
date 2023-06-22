#actor_hashtag_instructions

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

c_toy_actor = '''
def create_percents(df):
    df["total"] = df["negative"] + df["neutral"] + df["positive"]
    df["neg_percent"] = df["negative"] / df["total"] * 100
    df["neu_percent"] = df["neutral"] / df["total"] * 100
    df["pos_percent"] = df["positive"] / df["total"] * 100
    df = df.sort_values('neg_percent', ascending=False)
    return df

toy_actor_df = df.groupby('sentiment').sum()[['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo']].T.reset_index()
toy_actor_df = create_percents(toy_actor_df)  
'''

c_toy_hashtag = '''
def create_percents(df):
    df["total"] = df["negative"] + df["neutral"] + df["positive"]
    df["neg_percent"] = df["negative"] / df["total"] * 100
    df["neu_percent"] = df["neutral"] / df["total"] * 100
    df["pos_percent"] = df["positive"] / df["total"] * 100
    df = df.sort_values('neg_percent', ascending=False)
    return df 

hasht = df.groupby('sentiment').sum()[['#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']].T.reset_index()
hasht = create_percents(hasht)  
'''

c_actor_fig = '''
fig = px.bar(toy_actor_df, x="index", y=["neg_percent", "pos_percent"], 
                 color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
                  barmode='group', title="Sentiment by Actor")
fig.update_layout(xaxis_title='Actor', yaxis_title='Percent of Tweets')
'''

c_hashtag_fig = '''
fig = px.bar(hasht, x="index", y=["neg_percent", "pos_percent"], 
                 color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
                  barmode='group', title="Sentiment by Hashtag")
fig.update_layout(xaxis_title='Hashtag', yaxis_title='Percent of Tweets')
'''

c_final = '''
app.layout = html.Div(children=[
    html.H1(children='<title>'),
    html.Div(children='<description here>'),
    dcc.Graph(id='fig', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
'''