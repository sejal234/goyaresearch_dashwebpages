c_import = """
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
"""

c_itself = '''fig = px.scatter_mapbox(df, lat="lat", lon="long", color="sentiment", size_max=15, zoom=2)'''

c_app = '''
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)
'''

c_mapbox = '''
px.set_mapbox_access_token(<YOUR TOKEN HERE>)
df = pd.read_csv('full_tweet_list.csv')
'''

c_colormap = '''
color_map = {
    "negative": "#F28268",
    "positive": "#38C477",
    "neutral": "tan"}
'''

c_lay_callback = '''
app.layout = html.Div([
    html.H1(children='Sentiment Map', style={'textAlign': 'center'}),
    dcc.Graph(id='graph-content') 
])

@app.callback(Output('graph-content', 'figure'), 
              [Input('graph-content', 'id')])
'''

c_update = '''
def update_graph(_):
    # Introduce random offset to the coordinates (so that points in the same location don't stack together)
    offset = 0.05  # Adjust this value based on the density of your data
    df['lat'] = df['lat'] + np.random.uniform(low=-offset, high=offset, size=len(df))
    df['long'] = df['long'] + np.random.uniform(low=-offset, high=offset, size=len(df))

    fig = px.scatter_mapbox(df, lat="lat", lon="long", color="sentiment", size_max=15, zoom=2,
                            hover_name='Location', color_discrete_map=color_map)

    return fig
'''

c_run = '''
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
'''