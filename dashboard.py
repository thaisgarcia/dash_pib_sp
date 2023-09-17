from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Inicialização do aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Leitura dos dados de todas as planilhas em um arquivo Excel
excel_file = 'PIB dos Municípios.xlsx'
xls = pd.ExcelFile(excel_file)

# Crie um dicionário para armazenar os DataFrames de cada cidade
dfs = {}
for sheet_name in xls.sheet_names:
    dfs[sheet_name] = xls.parse(sheet_name)

# Defina um estilo CSS personalizado para o fundo escuro
app.layout = html.Div(style={'fontFamily': 'Arial'}, children=[
    html.H4("ANÁLISE DE PIB DOS MUNICÍPIOS PAULISTAS COM POPULAÇÃO ENTRE 100 MIL E 116 MIL HABITANTES"),

    html.Div(style={'width': '90%', 'margin': 'auto'}, children=[

        html.Label("Selecione a cidade para análise:"),

        dcc.Dropdown(
            id='city-dropdown',
            options=[
                {'label': city, 'value': city}
                for city in dfs.keys()  # Use as chaves do dicionário como opções
            ],
            value=list(dfs.keys())[0],  # Selecione a primeira cidade como valor padrão
            style={'margin-bottom': '10px'}
        ),

        dcc.Graph(id='line-chart')
    ])
])

# Callback para atualizar o gráfico de linhas com base na cidade selecionada
@app.callback(
    Output('line-chart', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_line_chart(selected_city):
    df = dfs[selected_city]

    # Selecione as colunas de anos para o gráfico de linhas
    anos = df.columns[1:]  # Ignora a primeira coluna que contém os setores

    # Crie o gráfico de linhas
    fig = px.line(df, x='SETORES', y=anos, title=f'PIB por Setores para {selected_city}')

    return fig

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)

