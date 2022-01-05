import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import base64
app = Dash(
    external_stylesheets=[dbc.themes.MORPH]
)
server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
df = pd.read_csv("data_clean.csv")
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                [html.Img(src='https://lh3.googleusercontent.com/proxy/GH9UO075XxMGxW6m0g_7e1J8wao82_8at5VM8Tf1_F6rI0F-_gKGAUmaXHWE0BfTEhPNS92vodBhQsmWgsgDxWSdHrtSULIMmgX-tMmFSbiJesWI3GZsqqsdPKmGwnq7S0_vchYoCoj8sf3MDwkmQiWpWAA',
                         height=100,
                         width=200,
                         style={'text-align': 'center'},
                         ),
                 ],
                    width=True,
                ),

                dbc.Col(
                    [

                        html.H1("BOPP-Consumption Trends", style={'text-align': 'centre'}),
                    ],
                    width=True,
                ),

            ],
            align="end",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [


                                html.H3("Select the parameter"),
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=[
                                        {'label': 'Capacity', 'value': 'Capacity'},
                                        {'label': 'Production', 'value': 'Production'},
                                    ],
                                    value='Capacity'),
                            ]),
                        html.H3("Select the region"),
                        dcc.RadioItems(
                            id='checklist',
                            options=[
                                {'label': 'World', 'value': 'world'},
                                {'label': 'Asia', 'value': 'asia'},
                                {'label': 'Africa', 'value': 'africa'},
                                {'label': 'Europe', 'value': 'europe'},
                                {'label': 'North America', 'value': 'north america'},
                                {'label': 'South America', 'value': 'south america'},
                            ],
                            labelStyle={'display': 'flex'}),
                    ]

                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id=('graph-with-slider')),
                    ],
                    width={'size': 9},

                ),
                dcc.Slider(
                    id='year-slider',
                    min=df['Year'].min(),
                    max=df['Year'].max(),
                    value=df['Year'].min(),
                    marks={str(year): str(year) for year in df['Year'].unique()},
                    step=None,

                ),

            ]
        )])


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('dropdown', 'value'),
    Input('checklist', 'value'))
def update_figure(selected_year, dropdown_value, checklist_value):
    filtered_df = df[df.Year == selected_year]
    fig = px.choropleth(
        data_frame=filtered_df,
        locations='Country Name',
        locationmode='country names',
        color=dropdown_value,
        scope=checklist_value,
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
