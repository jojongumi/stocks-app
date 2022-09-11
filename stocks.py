import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

df = pd.read_csv('data.csv')
df['date'] = pd.to_datetime(df['date'])
date = df['date']
price = df['price']
ticker_names = df['ticker'].unique().tolist()

app.layout = html.Div([
    html.H4('NSE Stock price analysis'),
    dcc.Graph(id="NSE-time-series-chart"),
    html.P("Select stock:"),
    dcc.Dropdown(
        id="ticker",
        options=[{'label': x, 'value': x} for x in ticker_names],
        value="ABSA",
        clearable=False,
    ),
])


@app.callback(
    Output("NSE-time-series-chart", "figure"),
    Input("ticker", "value"))
def display_time_series(ticker):
    data = df[df['ticker'] == ticker].sort_values(by='date')
    fig = px.line(data, x=data['date'], y=data['price'])
    fig.update_layout(yaxis={'title': ticker}, xaxis={'title': 'Date'})
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)