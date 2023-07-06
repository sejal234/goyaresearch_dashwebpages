#import statements
import dash
from dash import Dash, html, dcc, Input, Output, callback #dash is used to make the webpage
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import *
import datetime
import numpy as np
from scatter_instructions import *

dash.register_page(__name__,
    path='/scatter',
    title='Plot: Scatter',
    name='Plot: Scatter',
    order = 7)

#https://plotly.com/python/line-and-scatter/ 
#df = pd.read_csv('full_tweet_list.csv')
df = pd.read_csv('https://raw.githubusercontent.com/sejal234/goyaresearch_dashwebpages/main/full_tweet_list.csv')
df[['date', 'time']] = df['created_at'].str.split(" ",expand=True)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%B %Y')
df['final_value'].fillna('Unclassified', inplace=True)

#this is based off https://dash.plotly.com/basic-callbacks

#PUTTING DATA INTO LONG FORM
# Specify the columns to keep
columns_to_keep = ['date', 'month', 'tweet', 'sentiment',  "final_value", 'like_count', 'quote_count', 'reply_count', 
                   'retweet_count', 'compound_score']

# Create a new DataFrame with the specified columns
new_df = df[columns_to_keep].copy()

# Reshape the DataFrame to long format using pd.melt()
dff = pd.melt(new_df, id_vars=['date', 'month', 'tweet', 'sentiment',  "final_value"],
                 var_name='Indicator Name', value_name='Value')

#REQUIRES DATA IN LONG FORM
layout = html.Div([ 

    html.H1(children='Scatter Plot', style={'textAlign':'center'}),
     html.P(children='''
        A scatter plot allows to compare numeric variables against each other to see how certain characteristics of a tweet may correlate with one another. 
        For instance, comparing retweet count to compound score (where a low score indicates negative sentiment and a high score indiciates positive sentiment)
        can help show if more negative/positive tweets tend to be more popular (more retweeted).
        '''),
        html.Br(),

        html.Div([
            dcc.Dropdown(
                dff['Indicator Name'].unique(),
                'retweet_count',
                id='xaxis-column' ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='xaxis-type',
                inline=True)], 
        style={'width': '48%', 'display': 'inline-block'}),

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
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),


    dcc.Graph(id='indicator-graphic'),
    html.Br(),

        html.Div([
            html.H2(children='How can I recreate this code?'),

            html.Br(),

            html.P(children='''
            This tutorial shows you how to make a Dash Webpage, but to replicate the graph itself, use the plotly.express "scatter" tool with your x and y axis variables of choice.
            To replicate this webpage, use the following tutorial. Referencing https://plotly.com/python/line-and-scatter/ and 
                https://dash.plotly.com/basic-callbacks may be helpful. Begin with import statements:
                '''),
                   
            dcc.Markdown(f'```python\n{c_import}\n```'),

            html.Br(),

            html.P(children='''
               Then, declare your "app" variable to create your Dash web app.
                '''),

            dcc.Markdown(f'```python\n{c_app}\n```'),

            html.Br(),

            html.P(children='''
                Clean your data. Since the scatterplot tests all numeric variables against each other, we convert our numeric variable columns to long form.
                Since we classified about 2000 datapoints into "Audience", "Pro-Goya", and "Anti-Goya" as part of a machine learning project, we decided to color 
                the points by their category. Coloring the points is optional. 
                '''),

            dcc.Markdown(f'```python\n{c_clean}\n```'),

            html.Br(),

            html.P(children='''
                Create the layout (the elements on the webpage) and callback (setting the input/output elements) of the app. The "Indicator Name" dropdowns are the callbacks that allows the user
                to choose what variable to put for both the x and y axis. We set retweet score and compound score as the defaults, with both axis being linear.
                '''),

            dcc.Markdown(f'```python\n{c_layout_callback}\n```'),

            html.Br(),

            html.P(children='''
                Create the update_graph function that regenerates the graph when the user refreshes the page. 
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
])

@callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value')
    ) 

def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type): 

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['tweet'],
                     color=dff[dff['Indicator Name'] == yaxis_column_name]['final_value'])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig

