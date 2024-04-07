# ssh -N -f -L 8080:localhost:8050 cloudlab 
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px

# Sample data 
df = px.data.iris() 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children=[
    html.H1(children='My Plotly Dashboard'),

    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=px.scatter(df, x="sepal_length", y="sepal_width", color="species"))
        ),
        dbc.Col(
            dcc.Graph(figure=px.bar(df, x='species', y='petal_length'))
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)