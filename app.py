import dash
from dash import html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import io

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("📊 Процесс управления инвестициями", style={'textAlign': 'center', 'color': '#1f77b4'}),

    html.P("Загрузите CSV-файл с данными по инвестициям или используйте демо-набор:", style={'textAlign': 'center'}),

    dcc.Upload(
        id='upload-data',
        children=html.Div(['Перетащите файл или ', html.A('выберите')]),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        },
        multiple=False
    ),

    html.Br(),

    html.Label("Фильтр по портфелю:", style={'margin': '10px'}),
    dcc.Dropdown(id='portfolio-dropdown', placeholder="Все портфели", multi=True),

    html.Label("Фильтр по уровню риска:", style={'margin': '10px'}),
    dcc.Dropdown(id='risk-dropdown', placeholder="Все уровни", multi=True),

    dcc.Graph(id='return-bar'),
    dcc.Graph(id='allocation-pie'),
    dcc.Graph(id='value-scatter'),

    html.H3("📊 Таблица инвестиционных активов", style={'marginTop': '30px'}),
    html.Div(id='table-container')
])

@app.callback(
    [Output('return-bar', 'figure'),
     Output('allocation-pie', 'figure'),
     Output('value-scatter', 'figure'),
     Output('portfolio-dropdown', 'options'),
     Output('risk-dropdown', 'options'),
     Output('table-container', 'children')],
    [Input('upload-data', 'contents'),
     Input('portfolio-dropdown', 'value'),
     Input('risk-dropdown', 'value')],
    [State('upload-data', 'filename')]
)
def update_dashboard(contents, selected_portfolios, selected_risks, filename):
    if contents is None:
        df = pd.read_csv('data.csv')
    else:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Фильтрация
    filtered_df = df.copy()
    if selected_portfolios:
        filtered_df = filtered_df[filtered_df['portfolio'].isin(selected_portfolios)]
    if selected_risks:
        filtered_df = filtered_df[filtered_df['risk_level'].isin(selected_risks)]

    # Опции для dropdown'ов
    portfolio_options = [{'label': p, 'value': p} for p in df['portfolio'].unique()]
    risk_options = [{'label': r, 'value': r} for r in df['risk_level'].unique()]

    # График 1: Доходность по активам
    bar_fig = px.bar(
        filtered_df,
        x='investment_type',
        y='return_percent',
        color='portfolio',
        title='Доходность по типам инвестиций (%)',
        labels={'return_percent': 'Доходность (%)', 'investment_type': 'Тип актива'}
    )

    # График 2: Распределение портфеля
    pie_fig = px.pie(
        filtered_df,
        values='current_value',
        names='investment_type',
        title='Распределение текущей стоимости портфеля'
    )

    # График 3: Текущая стоимость vs начальные вложения
    scatter_fig = px.scatter(
        filtered_df,
        x='initial_investment',
        y='current_value',
        size='return_percent',
        color='risk_level',
        hover_name='investment_type',
        title='Начальные вложения vs Текущая стоимость (размер = доходность)'
    )

    # Таблица
    table = html.Table([
        html.Thead(html.Tr([html.Th(col) for col in filtered_df.columns])),
        html.Tbody([
            html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns])
            for i in range(min(len(filtered_df), 10))
        ])
    ], style={
        'border': '1px solid #ccc',
        'borderCollapse': 'collapse',
        'width': '100%',
        'fontSize': '14px'
    })

    return bar_fig, pie_fig, scatter_fig, portfolio_options, risk_options, table


if __name__ == '__main__':
    app.run(debug=True)  # ← ИСПРАВЛЕНО! Не run_server, а run