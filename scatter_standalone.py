    
#BARCHART ATTEMPT 1

import dash
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import *
import datetime
import numpy as np
import json
import re
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)

#https://plotly.com/python/line-and-scatter/ 
df = pd.read_csv('full_tweet_list.csv')
df[['date', 'time']] = df['created_at'].str.split(" ",expand=True)
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%B %Y')
df['final_value'].fillna('Unclassified', inplace=True)

#this is based off https://dash.plotly.com/basic-callbacks

#PUTTING DATA INTO LONG FORM
# Specify the columns to keep
columns_to_keep = ['date', 'month', 'tweet', 'sentiment',  "final_value", 'like_count', 'quote_count', 'reply_count', 
                   'retweet_count', 'compound_score']
# Replace 'column1', 'column2', 'column3' with your desired column names

# Create a new DataFrame with the specified columns
new_df = df[columns_to_keep].copy()

# Reshape the DataFrame to long format using pd.melt()
df = pd.melt(new_df, id_vars=['date', 'month', 'tweet', 'sentiment',  "final_value"],
                 var_name='Indicator Name', value_name='Value')

#REQUIRES DATA IN LONG FORM
app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                df['Indicator Name'].unique(),
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
                df['Indicator Name'].unique(),
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

    dcc.Graph(id='indicator-graphic'),

    # dcc.Slider(
    #     min=datetime.datetime.strptime(df['month'].min(), '%B %Y').timestamp(),
    #     max=datetime.datetime.strptime(df['month'].max(), '%B %Y').timestamp(),
    #     step=None,
    #     id='month--slider',
    #     value=datetime.datetime.strptime(df['month'].max(), '%B %Y').timestamp(),
    #     marks={datetime.datetime.strptime(month, '%B %Y').timestamp(): month for month in df['month'].unique()},
    # )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value')
    ) #took out Input('date--slider', 'value') Input('month--slider', 'value')
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type): #took out date_value #month_value
    
    #dff = df[df['date'] == date_value]
    #dff = df[df['month'] == month_value]
    dff = df

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

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)






#THIS IS WHEN I WAS TRYING TO DO A DATE SLIDER
# start_date = datetime.datetime(2020, 7, 7)
# end_date = datetime.datetime(2021, 2, 1)

# app.layout = html.Div([
#     html.H4('Interactive scatter plot with Iris dataset'),
#     dcc.Graph(id="scatter-plot"),
#     html.P("Filter by petal width:"),
#     dcc.RangeSlider(
#         id='range-slider',
#         min=df['date'].min().timestamp(),  # Convert the minimum date to timestamp
#         max=df['date'].max().timestamp(),  # Convert the maximum date to timestamp
#         step=86400,  # Number of seconds in a day (1 day step)
#         marks={min: 'earliest', max: 'latest'},
#         value=[start_date.timestamp(), end_date.timestamp()]  # Set initial range values to the desired date range
#     ),
# ])

# @app.callback(
#     Output("scatter-plot", "figure"), 
#     Input("range-slider", "value"))

# def update_bar_chart(slider_range):
#     low, high = slider_range
#     low = pd.Timestamp(low, unit='s')
#     high = pd.Timestamp(high, unit='s')
#     mask = (df['date'] > low) & (df['date'] < high)
#     fig = px.scatter(
#         df[mask], 
#         x="retweet_count", 
#         y="like_count", 
#         color="sentiment", 
#         hover_data=['sentiment'])
#     return fig


# app.layout = html.Div([
#     html.H4('Scatter Plot'),
#     dcc.Dropdown(
#         id='x-axis-dropdown',
#         options=[
#             {'label': 'Column X', 'value': 'x'},
#             {'label': 'Column A', 'value': 'a'},
#             {'label': 'Column B', 'value': 'b'},
#             # Add more options for x-axis columns
#         ],
#         value='x'  # Set the default selected value
#     ),
#     dcc.Dropdown(
#         id='y-axis-dropdown',
#         options=[
#             {'label': 'Column Y', 'value': 'y'},
#             {'label': 'Column C', 'value': 'c'},
#             {'label': 'Column D', 'value': 'd'},
#             # Add more options for y-axis columns
#         ],
#         value='y'  # Set the default selected value
#     ),
#     dcc.Graph(id='scatter-plot')
# ])

# # Step 2: Create the callback function
# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('x-axis-dropdown', 'value'),
#     Input('y-axis-dropdown', 'value')
# )
# def update_scatter_plot(x_axis, y_axis):
#     # Create the scatter plot with the selected x and y axes
#     fig = {
#         'data': [{
#             'x': df[x_axis],
#             'y': df[y_axis],
#             'type': 'scatter',
#             'mode': 'markers'
#         }],
#         'layout': {
#             'title': f'Scatter Plot ({x_axis} vs {y_axis})',
#             'xaxis': {'title': x_axis},
#             'yaxis': {'title': y_axis}
#         }
#     }
#     return fig

