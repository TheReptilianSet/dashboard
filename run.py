import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from flask import Flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
# server = app.server
app.config.suppress_callback_exceptions = True

months = ['january', 'february', 'march', 'april', 'may']
months_ru = ['Январь 2019', 'Февраль 2019', 'Март 2019', 'Апрель 2019', 'Май 2019']

real = pd.read_excel(
    'files/Реализация за 01.2019-05.2019г. пономенклатурно.xlsx',
    skiprows=10,
    usecols=list(range(1,9)),
    names=['nom', 'art', 'code'] + months
).fillna(0)

orders = pd.read_excel(
    'files/Заказы покупателей за 01.2019-05.2019г. пономенклатурно.xlsx',
    skiprows=11,
    usecols=list(range(1,9)),
    names=['nom', 'art', 'code'] + months
).fillna(0)


select_data = pd.concat([real[['nom', 'art', 'code']], orders[['nom', 'art', 'code']]])
unique_codes = select_data['code'].unique()
select_data = select_data[select_data['code'].isin(unique_codes)]
select_data['label'] = select_data.apply(lambda x: "{}, {} ({})".format(x['nom'], x['art'], x['code']), axis=1)
select_data['value'] = select_data['code']

multiselect_options = select_data[['label', 'value']].to_dict('records')


app.layout = html.Div([
    html.Div([html.H1("Графики заказов и реализаций")], style={'textAlign': 'center'}),
    html.Div([dcc.Dropdown(id="selected-value", value="Ц1025556", options=multiselect_options)], className='row', style={"display": "block", "margin-left": "auto", "margin-right": "auto"}),
    html.Div([dcc.Graph(id="my-graph")], style={"height": "100%"}),
    # html.Div([dcc.RangeSlider])
], className="container-fluid")


def create_trace(code):
    real_df = real[real['code'].isin([code])]
    order_df = orders[orders['code'].isin([code])]
    nomenclature = "{}, {} ({})".format(real_df['nom'].values[0], real_df['art'].values[0], real_df['code'].values[0])

    local_trace = [
        go.Scatter(
            x=months_ru,
            y=real_df.iloc[0, 3:],
            name="Реализации",
            mode='lines+markers',
            opacity = 0.6,
            line = dict(
                color=('rgb(22, 96, 167)'),
                width=4,
            )
        ),
        go.Scatter(
            x=months_ru,
            y=order_df.iloc[0, 3:],
            name="Заказы",
            mode='lines+markers',
            # marker={'size': 8, "opacity": 0.6, "line": {"width": 0.5}}
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=2,
                dash='dash'
            )
        )
    ]

    return local_trace, nomenclature


@app.callback(Output("my-graph", "figure"), [Input('selected-value', 'value')])
def update_figure(selected):
    trace = []
    nomenclature = "Сравнительный график заказов и реализаций"
    if type(selected) == list:
        for code in selected:
            ltrace, nomenclature = create_trace(code)
            trace += ltrace
    else:
        ltrace, nomenclature = create_trace(selected)
        trace += ltrace


    return {"data": trace,
            "layout": go.Layout(title=nomenclature, margin=go.layout.Margin(b=50), colorway=['#fdae61', '#abd9e9', '#2c7bb6'], yaxis={"title": "Количество, шт"}, xaxis={"title": "Месяцы"})}


if __name__ == '__main__':
    app.run_server(debug=True)
