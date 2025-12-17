import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import io

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Финансовый дашборд", style={'textAlign': 'center', 'color': '#2c3e50'}),
    html.P("Загрузите CSV-файл с данными или используйте тестовые данные:", style={'margin': '10px'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Перетащите файл сюда или ',
            html.A('выберите файл')
        ]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        },
        multiple=False
    ),

    html.Br(),

    html.Label("Выберите период анализа:"),
    dcc.Dropdown(id='period-dropdown', placeholder="Не выбрано"),

    html.Br(),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='scatter-plot'),

    html.H3("Таблица данных", style={'marginTop': '30px'}),
    html.Div(id='table-container')
])

@app.callback(
    [Output('line-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('period-dropdown', 'options'),
     Output('table-container', 'children')],
    [Input('upload-data', 'contents'),
     Input('period-dropdown', 'value')],
    [State('upload-data', 'filename')]
)
def update_dashboard(contents, selected_period, filename):
    if contents is None:
        # Используем тестовые данные из data.csv
        df = pd.read_csv('data.csv')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    df['date'] = pd.to_datetime(df['date'])
    df['period'] = df['date'].dt.to_period('M').astype(str)

    if selected_period:
        df = df[df['period'] == selected_period]

    periods = [{'label': p, 'value': p} for p in df['period'].unique()]

    line_fig = px.line(df, x='date', y=['income', 'expense'], title='Доходы и расходы')
    pie_fig = px.pie(df, values='expense', names='category', title='Расходы по категориям')
    scatter_fig = px.scatter(df, x='marketing_cost', y='profit', color='category', title='Прибыль vs Рекламные затраты')

    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in df.columns])),
        html.Tbody([
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(min(len(df), 5))
        ])
    ], style={'border': '1px solid #ddd', 'borderCollapse': 'collapse', 'width': '100%'})

    return line_fig, pie_fig, scatter_fig, periods, table

if __name__ == '__main__':
    app.run_server(debug=True)