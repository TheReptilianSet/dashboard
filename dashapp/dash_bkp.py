import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from app import create_app
from config import Config


server = create_app(Config)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets, url_base_pathname='/dashboard')
dash_app.config.suppress_callback_exceptions = True

months = ['january', 'february', 'march', 'april', 'may']
months_ru = ['Январь 2019', 'Февраль 2019', 'Март 2019', 'Апрель 2019', 'Май 2019']

colors = {
    0: ['rgb(2, 71, 254)', None],
    1: ['rgb(254, 39, 18)', 'dash'],
    2: ['rgb(101, 175, 50)', 'dashdot']
}

directory = 'files'
dnames = []
data = []
for file in os.listdir(directory):
    dnames.append(file.split(' ')[1])
    data.append(pd.read_excel(
        os.path.join(directory, file),
        skiprows=2,
        # usecols=list(range(9)),
        names=['nom', 'art', 'manuf', 'code'] + months
    ).fillna(0))

select_data = pd.concat(data)
unique_codes = select_data['code'].unique()
select_data = select_data[select_data['code'].isin(unique_codes)]
select_data['label'] = select_data.apply(lambda x: "{}, {} ({}): {}".format(x['nom'], x['art'], x['code'], x['manuf']), axis=1)
select_data['value'] = select_data['code']

multiselect_options = select_data[['label', 'value']].to_dict('records')


def create_trace(code):
    local_trace = []
    nomenclature = ''
    for i in range(len(dnames)):
        df = data[i][data[i]['code'].isin([code])]
        nomenclature = "{}, {} ({}): <b>{}</b>".format(df['nom'].values[0], df['art'].values[0], df['code'].values[0], df['manuf'].values[0])
        local_trace.append(go.Scatter(
            x=months_ru,
            y=df.iloc[0, 4:],
            name=dnames[i],
            mode='lines+markers',
            # opacity=0.6,
            line=dict(
                color=(colors[i][0]),
                width=4-i,
                dash=colors[i][1]
            )
        ))
    return local_trace, nomenclature


@dash_app.callback(Output("my-graph", "figure"), [Input('selected-value', 'value')])
def update_figure(selected):
    trace = []
    nomenclature = "Сравнительный график заказов, реализаций, остатков"
    if type(selected) == list:
        for code in selected:
            ltrace, nomenclature = create_trace(code)
            trace += ltrace
    else:
        ltrace, nomenclature = create_trace(selected)
        trace += ltrace

    return {"data": trace,
            "layout": go.Layout(title=nomenclature, margin=go.layout.Margin(b=50), colorway=['#fdae61', '#abd9e9', '#2c7bb6'], yaxis={"title": "Количество, шт"}, xaxis={"title": "Месяцы"})}
