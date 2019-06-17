import os
import pandas as pd
import plotly.graph_objs as go

# Наименование элементов (месяцы)
months = ['january', 'february', 'march', 'april', 'may']
months_ru = ['Январь 2019', 'Февраль 2019', 'Март 2019', 'Апрель 2019', 'Май 2019']

# Цвета и типы линий
colors = {
    0: ['rgb(2, 71, 254)', None],
    1: ['rgb(254, 39, 18)', 'dash'],
    2: ['rgb(101, 175, 50)', 'dashdot']
}


def read_files_from_directory():
    """Чтение файлов из директории"""
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

    return data, dnames


def make_list_for_dropdown(data):
    """Формирует список label, value для dropdown меню"""
    select_data = pd.concat(data)
    unique_codes = select_data['code'].unique()
    select_data = select_data[select_data['code'].isin(unique_codes)]
    select_data['label'] = select_data.apply(
        lambda x: "{}, {} ({}): {}".format(x['nom'], x['art'], x['code'], x['manuf']), axis=1)
    select_data['value'] = select_data['code']

    multiselect_options = select_data[['label', 'value']].to_dict('records')

    return multiselect_options


def create_trace(data, dnames, code):
    """Создать диаграммы"""
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