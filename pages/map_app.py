
import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import numpy as np
from map_instructions import *

from config import TOKEN

dash.register_page(__name__)

#https://plotly.github.io/plotly.py-docs/generated/plotly.express.scatter_mapbox.html
px.set_mapbox_access_token(TOKEN)
df = pd.read_csv('full_tweet_list.csv')

color_map = {
    "negative": "#F28268",
    "positive": "#38C477",
    "neutral": "tan"}

layout = html.Div([
    html.H1(children='Sentiment Map', style={'textAlign':'center'}),
    html.P(children='''
        A map allows you to look at what parts of the world are engaging with the event conversation on Twitter. Coloring this map by sentiment allows you to examine
        if certain parts of the world react positively/negatively to the same actions as other parts of the world. 
        '''),
    
    html.Br(),
    dcc.Graph(id='graph-content'), 
    html.Br(),

    html.Div([
        html.H2(children='How can I recreate this code?'),

        html.Br(),

        html.P(children='''
            This tutorial shows you how to make a Dash Webpage, but to replicate the graph itself, use the plotly.express "scatter_mapbox" tool like so: 
            '''),
                
        dcc.Markdown(f'```python\n{c_itself}\n```'),

        html.P(children='''
            However, to replicate the full webpage, use the following tutorial. Begin with import statements:
            '''),
                
        dcc.Markdown(f'```python\n{c_import}\n```'),

        html.Br(),

        html.P(children='''
            Then, declare your "app" variable NOTE TO SELF: PROBABLY EXPLAIN HOW THE WEBPAGE WORKS IN THE HOME PAGE? 
            '''),

        dcc.Markdown(f'```python\n{c_app}\n```'),

        html.Br(),

        html.P(children='''
            Set px.set_mapbox_access_token(<YOUR TOKEN HERE>) with your mapbox token. 
            Create a mapbox account and access your default public token at https://account.mapbox.com/access-tokens/. NOTE TO SELF MAKE SURE thIS LINK WORKS
            '''),

        dcc.Markdown(f'```python\n{c_mapbox}\n```'),

        html.Br(),

        html.P(children='''
            Create a color map to organize what hex codes correspond with negative, positive, and neutral sentiment tweets.
            '''),

        dcc.Markdown(f'```python\n{c_colormap}\n```'),

        html.Br(),

        html.P(children='''
            Create the layout (the elements on the webpage) and callback (setting the input/output elements) of the app.
            '''),

        dcc.Markdown(f'```python\n{c_lay_callback}\n```'),

        html.Br(),

        html.P(children='''
            Create the update_graph function that regenerates the map when the user refreshes the page. 
            Since the longitude/latitude values are the same for all tweets that map to the same city, we need to offset the point values to avoid overlap in the map. 
            In other words, if 50 tweets are from Houston, all 50 tweets would have the same longitude/latitude value and appear as one point on the map. With the offset, they appear
            as a group of points in Houston. This offset changes randomly everytime the user the refreshes, the points for a given city move around within the area. This helps avoid
            confusion that a particular tweet is from a specific location/neighborhood/district of a city, instead of the city in general.
            '''),

        dcc.Markdown(f'```python\n{c_update}\n```'),

        html.Br(),

        html.P(children='''
            Launch the web server and start the application. When running this script in your terminal, the terminal will return a link for you to view the page on
            your web browser.
            '''),

        dcc.Markdown(f'```python\n{c_run}\n```'),

        html.Br(),
        ]),

    #now, do the actual coding of the text
])

@callback(Output('graph-content', 'figure'), 
              [Input('graph-content', 'id')])

def update_graph(_):
    # Introduce random offset to the coordinates (so that points in the same location don't stack together)
    offset = 0.05  # Adjust this value based on the density of your data
    df['lat'] = df['lat'] + np.random.uniform(low=-offset, high=offset, size=len(df))
    df['long'] = df['long'] + np.random.uniform(low=-offset, high=offset, size=len(df))

    fig = px.scatter_mapbox(df, lat="lat", lon="long", color="sentiment", size_max=15, zoom=2,
                            hover_name='Location', color_discrete_map=color_map)

    return fig


#fig = px.scatter_mapbox(df, lat="lat", lon="long", color="sentiment", size_max=15, zoom=2, 
                        #hover_name = 'Location', color_discrete_map=color_map)

# Introduce random offset to the coordinates (so that points in the same location don't stack together)
# offset = 0.05  # Adjust this value based on the density of your data
# df['lat'] = df['lat'] + np.random.uniform(low=-offset, high=offset, size=len(df))
# df['long'] = df['long'] + np.random.uniform(low=-offset, high=offset, size=len(df))