import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np

dash.register_page(__name__)

# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('full_tweet_list.csv')
# # if your variable columns is represented as counts, convert count values to binary (0 or 1)
#columns_to_convert = ['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo', '#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']
columns_to_convert = ['#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']
df[columns_to_convert] = np.where(df[columns_to_convert] > 0, 1, 0)

def create_percents(df):
    df["total"] = df["negative"] + df["neutral"] + df["positive"]
    df["neg_percent"] = df["negative"] / df["total"] * 100
    df["neu_percent"] = df["neutral"] / df["total"] * 100
    df["pos_percent"] = df["positive"] / df["total"] * 100
    df = df.sort_values('neg_percent', ascending=False)
    return df

# toy_actor_df = df.groupby('sentiment').sum()[['aoc', 'ivanka', 'donald', 'unanue', 'cruz', 'castro', 'cuomo']].T.reset_index()
# toy_actor_df = create_percents(toy_actor_df)  

hasht = df.groupby('sentiment').sum()[['#BuycottGoya','#BuyGoya', '#BoycottGoya', '#Goyaway']].T.reset_index()
hasht = create_percents(hasht)  

fig = px.bar(hasht, x="index", y=["neg_percent", "pos_percent"], 
                 color_discrete_map={"neg_percent": "#F28268", "pos_percent": "#38C477"}, 
                  barmode='group', title="Sentiment by Hashtag")
fig.update_layout(xaxis_title='Hashtag', yaxis_title='Percent of Tweets')

layout = html.Div(children=[
    html.H2(children='Sentiment by Hashtag'),
    html.Div(children='''update'''),
    dcc.Graph(id='graph-content', figure = fig),
    html.Div(children='''Want to reproduce this code? Refer to this script. (note to self: insert script)'''),
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