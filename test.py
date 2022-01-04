import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


app = Dash(
    external_stylesheets=[dbc.themes.MINTY]
)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
df = pd.read_csv("/Users/priyanshpradhan/Desktop/My work/Uflex Dashoard/data_clean.csv")
app.layout = html.Div(
    html.H1("BOPP-Consumption Trends", style={'text-align': 'center'}),
    dbc.Row(dbc.Col(dcc.Graph(
            id=('graph-with-slider',),
            width={'size': 9, 'offset': 3},),

    dbc.Row(dbc.Col(dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Capacity', 'value': 'Capacity'},
            {'label': 'Production', 'value': 'Production'},
        ],
        value='Capacity'),
        width={'size': 3},
        align='start')),
    dbc.Row(dbc.Col(dcc.RadioItems(
        id='checklist',
        options=[
            {'label': 'Asia', 'value': 'asia'},
            {'label': 'World', 'value': 'world'},
            {'label': 'Africa', 'value': 'africa'},
            {'label': 'Europe', 'value': 'europe'},
            {'label': 'North America', 'value': 'north america'},
            {'label': 'South America', 'value': 'south america'},
        ],
        labelStyle={'display': 'flex'}),
        width=True)),

    dcc.Slider(
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None,
        style={
            'textAlign': 'center',
            'color': colors['text']

    )))

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown', 'value'),
    Input('checklist', 'value'))

def update_figure(selected_year , dropdown_value, checklist_value):

    filtered_df = df[df.Year == selected_year]
    fig = px.choropleth(
        data_frame=filtered_df,
        locations='Country Name',
        locationmode='country names',
        color=dropdown_value,
        scope=checklist_value,
        animation_frame='Year',
        animation_group='Country Name',
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)