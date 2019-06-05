import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
select_data['label'] = select_data.apply(lambda x: "{}, {}".format(x['nom'], x['art']), axis=1)
select_data['value'] = select_data['code']

multiselect_options = select_data[['label', 'value']].to_dict('records')


app.layout = html.Div([
    html.Div([html.H1("Графики заказов и реализаций")], style={'textAlign': 'center'}),
    html.Div([dcc.Dropdown(id="selected-value",value="Ц1025719", multi=True, options=multiselect_options)], className='row', style={"display": "block", "margin-left": "auto", "margin-right": "auto"}),
    html.Div([dcc.Graph(id="my-graph")], style={"height": "100%"}),
    # html.Div([dcc.RangeSlider])
], className="container-fluid")


def create_trace(code):
    real_df = real[real['code'].isin([code])]
    order_df = orders[orders['code'].isin([code])]
    nomenclature = "{}, {}".format(real_df['nom'].values[0], real_df['art'].values[0])

    local_trace = [
        go.Scatter(
            x=months_ru,
            y=real_df.iloc[0, 3:],
            name="{} (реализации)".format(nomenclature),
            mode='lines',
            marker={'size': 8, "opacity": 0.6, "line": {"width": 0.5}}
        ),
        go.Scatter(
            x=months_ru,
            y=order_df.iloc[0, 3:],
            name="{} (заказы)".format(nomenclature),
            mode='lines',
            marker={'size': 8, "opacity": 0.6, "line": {"width": 0.5}}
        )
    ]

    return local_trace


@app.callback(Output("my-graph", "figure"), [Input('selected-value', 'value')])
def update_figure(selected):
    trace = []
    if type(selected) == list:
        for code in selected:
            trace += create_trace(code)
    else:
        trace += create_trace(selected)

    return {"data": trace,
            "layout": go.Layout(title="Сравнительный график заказов и реализаций", colorway=['#fdae61', '#abd9e9', '#2c7bb6'], yaxis={"title": "Количество, шт"}, xaxis={"title": "Месяцы"})}


if __name__ == '__main__':
    app.run_server(debug=True)
