import dash
from dash import Dash, html, dcc, Input, Output, callback
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server,external_stylesheets=external_stylesheets, use_pages = True)

app.layout = html.Div([
	html.H1('Examining the Goya Boycott through Twitter Data'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])
	
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=8050)