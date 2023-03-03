import json
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from stance_define import stance_data
import dash_bootstrap_components as dbc

df = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_compressing_effort.csv")

with open("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/us-states.json", 'r') as f:
    geojson_file = json.load(f)


# Add title and authors
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.title = 'Climate Change Sentiment Analysis'
# authors = "Jonathan Juarez, Jaskirat Kaur, Ridhi Purohit, Grey Xu"


app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                html.H4("Sentiment of US states", className="mb-0"),
                html.P(
                    "† This project aims to analyze the sentiment towards climate change across the United States. We collected data from social media platforms such as Twitter and analyzed the sentiment towards climate change based on the stance of the user (Believer, Denier or Neutral). The map below shows the average sentiment towards climate change by state for the selected year and stance.",
                    className="text-muted",
                ),
            ],
            width={"size": 8, "offset": 2},
            className="my-3",
        )
    ),
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Label(['Choose stance:'],style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='stance_dropdown',
                        options=[
                            {'label': 'Believer', 'value': 'believer'},
                            {'label': 'Denier', 'value': 'denier'},
                            {'label': 'Neutral', 'value': 'neutral'}
                        ],
                        value='believer',
                        style={'width': '100%'}
                    ),
                    html.Br(),
                    dcc.Graph(id='map-graph')
                ],
                width={"size": 8},
                className="my-3",
            ),
            dbc.Col(
                [
                    html.Label(['Choose year:'],style={'font-weight': 'bold'}),
                    dcc.Slider(
                        id='year_slider',
                        min=2009,
                        max=2019,
                        value=2009,
                        marks={str(year): str(year) for year in range(2009, 2020, 1)},
                        step=None
                    ),
                ],
                width={"size": 8},
                className="my-3 align-self-end",
            ),
        ]
    ),
    dbc.Row(
        dbc.Col(
            [
                html.P(
                    "† This project was developed by Jonathan Juarez, Jaskirat Kaur, Ridhi Purohit, and Grey Xu as part of the Spring 2023 course 'CAPP 30122: Computer Science and Applications II' at the University of Chicago",
                    className="text-muted",
                ),
            ],
            width={"size": 10, "offset": 1},
            className="my-3",
        )
    ),
], fluid=True)

@app.callback(
    Output('map-graph', 'figure'),
    [Input('stance_dropdown', 'value'),
     Input('year_slider', 'value')]
)
def update_map(stance, year):
    filtered_df = df[(df['stance'] == stance) & (df['year'] == year)]
    avg_sentiment_df = filtered_df.groupby('state_FIP')['sentiment'].mean().reset_index()
    fig = px.choropleth_mapbox(avg_sentiment_df, geojson=geojson_file, color='sentiment',
                                  locations='state_FIP', featureidkey='properties.STATE',
                                  center={'lat': 37.0902, 'lon': -95.7129}, mapbox_style="carto-positron", zoom=3,
                                  color_continuous_scale='rdylgn', range_color=(-0.3, 0.3))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)