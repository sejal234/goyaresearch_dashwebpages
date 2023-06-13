
import dash
from dash import Dash, dcc, html, Input, Output
from sklearn.decomposition import PCA
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
import re
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets)

bow = pd.read_csv('bagofwords_en.csv')
bow_vals = bow.drop(['ID_', 'TWEET_', 'FINAL_', 'FINAL_VALUE_', 'TWEET_CLEANED_'], axis=1).reset_index(drop=True)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

#this is what i was going off of for the interactive feature, its being weird: https://plotly.com/python/pca-visualization/#pca-analysis-in-dash

# app.layout = html.Div([
#     html.H4("Visualization of PCA's explained variance"),
#     dcc.Graph(id="graph"),
#     html.P("Number of components:"),
#     dcc.Slider(
#         id='slider',
#         min=2, max=5, value=3, step=1)
# ])

# @app.callback(
#     Output("graph", "figure"), 
#     Input("slider", "value"))

# def run_and_plot(n_components):
#     pca = PCA(n_components=n_components)
#     #components = pca.fit_transform(bow_vals.values)
#     components = pca.fit_transform(bow_vals)

#     var = pca.explained_variance_ratio_.sum() * 100

#     labels = {str(i): f"PC {i+1}" for i in range(n_components)}
#     labels['color'] = 'FINAL_VALUE_'

#     fig = px.scatter_matrix(
#         components,
#         #color=bow['FINAL_VALUE_'],  # Use ''FINAL_VALUE_'' as the color column
#         dimensions=range(n_components),
#         labels=labels,
#         title=f'Total Explained Variance: {var:.2f}%')
#     fig.update_traces(diagonal_visible=False)
#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=True, host='0.0.0.0', port=8050)