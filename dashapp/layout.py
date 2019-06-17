import dash_core_components as dcc
import dash_html_components as html
from .utils import read_files_from_directory, make_list_for_dropdown
from flask_security import current_user

data, dnames = read_files_from_directory()
multiselect_options = make_list_for_dropdown(data)


layout = html.Div([
    html.Div([html.H1("Графики заказов, реализаций, остатков")], style={'textAlign': 'center'}),
    html.Div([dcc.Dropdown(id="selected-value", value="Ц1019105", options=multiselect_options)], className='row', style={"display": "block", "margin-left": "auto", "margin-right": "auto"}),
    html.Div([dcc.Graph(id="my-graph")], style={"height": "100%"}),
    html.Div([dcc.Upload(
        id='upload-data',
        children=html.Div([
            "Перетащите файлы или ",
            html.A('Выберите Файлы')
        ])
    )])
    # html.Div([dcc.RangeSlider])
], className="container-fluid")