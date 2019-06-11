import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from flask import Flask

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)


colors = {
    "background": "#fff",
    "text": "#7FDBFF"
}

months = ['january', 'february', 'march', 'april', 'may']

real = pd.read_excel(
    'files/Реализация за 01.2019-05.2019г. пономенклатурно.xlsx',
    skiprows=10,
    usecols=list(range(1,9)),
    names=['nom', 'art', 'code'] + months
).fillna(0)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[
    html.H1(
        children="Hello Dash (changed)",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),

    html.Div(children="Dash: A web application framework for Python." , style={
        "textAlign": "center",
        "color": colors["text"]
    }),

    dcc.Graph(
        id="example-graph",
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [4, 2, 2], "type": "bar", "name": "SF"},
                {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "Montreal"},
            ],
            "layout": {
                "title": "Dash Data Visualization",
                "plot_bgcolor": colors["background"],
                "paper_bgcolor": colors["background"],
                "font": {
                    "color": colors["text"]
                }
            }
        }
    ),

    dcc.Graph(
        id="life-exp-vs_gdp",
        figure={
            "data": [
              go.Scatter(
                  x=[1,2,3,4,5],
                  y=real.iloc[i, 3:],
                  # text=real.iloc[i, 0],
                  mode="lines+markers",
                  opacity=0.7,
                  marker={
                      "size": 15,
                      "line": {"width": 0.5}
                  },
                  name=real.iloc[i, 0]
              ) for i in range(100, 106)
            ],
            "layout": go.Layout(
                xaxis={"type": "log", "title": "Months"},
                yaxis={"title": "Qty"},
                margin={"l": 40, "b": 40, "t": 10, "r": 10},
                legend={"x": 0, "y": 1},
                hovermode="closest"
            )
        }
    ),

    html.Div(children=[
        html.H4(children="Table: Realizations"),
        generate_table(real)
    ]),

    html.Div([
        dcc.Input(id="my-id", value="initial value", type="text"),
        html.Div(id="my-div")
    ])
])


@app.callback(
    Output(component_id='my-div', component_property="children"),
    [Input(component_id="my-id", component_property="value")]
)
def update_output_div(input_value):
    return "You've entered '{}'".format(input_value)


if __name__ == "__main__":
    app.run_server(debug=True)