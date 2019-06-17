import plotly.graph_objs as go
from dash.dependencies import Input, Output
from .utils import create_trace, read_files_from_directory

data, dnames = read_files_from_directory()


def register_callbacks(dashapp):
    @dashapp.callback(Output("my-graph", "figure"), [Input('selected-value', 'value')])
    def update_figure(selected):
        trace = []
        nomenclature = "Сравнительный график заказов, реализаций, остатков"
        if type(selected) == list:
            for code in selected:
                ltrace, nomenclature = create_trace(data, dnames, code)
                trace += ltrace
        else:
            ltrace, nomenclature = create_trace(data, dnames, selected)
            trace += ltrace

        return {"data": trace,
                "layout": go.Layout(title=nomenclature, margin=go.layout.Margin(b=50), colorway=['#fdae61', '#abd9e9', '#2c7bb6'], yaxis={"title": "Количество, шт"}, xaxis={"title": "Месяцы"})}


