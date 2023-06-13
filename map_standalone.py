
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

#https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
px.set_mapbox_access_token("pk.eyJ1Ijoic2VqYWwyMzQiLCJhIjoiY2xla2hiODI3MGFrYTN5cm40dWg5d2dyaiJ9.mwYlGueLwABEg82Ujm0PBQ")
df = pd.read_csv('full_tweet_list.csv')

color_map = {
    "negative": "#F28268",
    "positive": "#38C477",
    "neutral": "tan"}

app.layout = html.Div([
    html.H1(children='Sentiment Map', style={'textAlign': 'center'}),
    dcc.Graph(id='graph-content')  # react library in dash
])

@app.callback(Output('graph-content', 'figure'), 
              [Input('graph-content', 'id')])

def update_graph(_):
    # Introduce random offset to the coordinates (so that points in the same location don't stack together)
    offset = 0.05  # Adjust this value based on the density of your data
    df['lat'] = df['lat'] + np.random.uniform(low=-offset, high=offset, size=len(df))
    df['long'] = df['long'] + np.random.uniform(low=-offset, high=offset, size=len(df))

    fig = px.scatter_mapbox(df, lat="lat", lon="long", color="sentiment", size_max=15, zoom=2,
                            hover_name='Location', color_discrete_map=color_map)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

# # Introduce random offset to the coordinates (so that points in the same location don't stack together)
# offset = 0.05  # Adjust this value based on the density of your data
# df['lat'] = df['lat'] + np.random.uniform(low=-offset, high=offset, size=len(df))
# df['long'] = df['long'] + np.random.uniform(low=-offset, high=offset, size=len(df))

# fig = px.scatter_mapbox(df, lat="lat", lon="long", color="sentiment", size_max=15, zoom=2, 
#                         hover_name = 'Location', color_discrete_map=color_map)

# app.layout = html.Div([
#     html.H1(children='Sentiment Map', style={'textAlign':'center'}),
#     dcc.Graph(id='graph-content', figure = fig) #react library in dash
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True, host='0.0.0.0', port=8050)