c_import = '''
import dash
from dash import Dash, html, dcc, Input, Output, callback #dash is used to make the webpage
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import *
import datetime
import numpy as np
'''

c_app = '''
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)
'''

c_clean = '''
#read in your dataframe
df = pd.read_csv('full_tweet_list.csv')

# if you want to color by category, label the non-categorized as "Unclassified" so it will still appear in the plot (final_value is the categorization column)
df['final_value'].fillna('Unclassified', inplace=True)

# put data in long form - we kept all columns we'd want for hover text (first three in the list) and numeric columns for the axis (remaining five in the list)
columns_to_keep = ['tweet', 'sentiment',  "final_value", 'like_count', 'quote_count', 'reply_count', 
                   'retweet_count', 'compound_score'] # replace with your desired column names

# create a new DataFrame with the specified columns
new_df = df[columns_to_keep].copy()

# reshape the DataFrame to long format using pd.melt(), keeping the values you will use for coloring and hover text
dff = pd.melt(new_df, id_vars=['tweet', 'sentiment',  "final_value"],
                 var_name='Indicator Name', value_name='Value')
'''

c_layout_callback ='''
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                dff['Indicator Name'].unique(),
                'retweet_count',
                id='xaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                dff['Indicator Name'].unique(),
                'compound_score',
                id='yaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),])

    @app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value')) 
'''

c_update = '''

def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type): 

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['tweet'],
                     color=dff[dff['Indicator Name'] == yaxis_column_name]['final_value']) #choose what to color points by (in this example, we color by final_value) - remove the line if you are not coloring points

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig
'''

c_run = '''
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)
'''