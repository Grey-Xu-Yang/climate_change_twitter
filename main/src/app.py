
'''
Dashboard

JASKIRAT KAUR

Main file for building the dashboard.

Run the app with `python3 app.py` and visit
http://127.0.0.1:8050/ in your web browser.
'''

import json
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import base64
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

believer_df = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/believer/believer_twitter.csv")
denier_df = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/denier_twitter.csv")
neutral_df = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/neutral_twitter.csv")

df = pd.concat([believer_df, denier_df, neutral_df])

with open("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/us-states.json", 'r') as f:
    geojson_file = json.load(f)

# ******************************** Data cleaning ****************************** #
fip_to_state = {
    '01': 'Alabama','02': 'Alaska','04': 'Arizona','05': 'Arkansas','06': 'California',
    '08': 'Colorado','09': 'Connecticut','10': 'Delaware','11': 'District of Columbia','12': 'Florida',
    '13': 'Georgia','15': 'Hawaii','16': 'Idaho','17': 'Illinois','18': 'Indiana','19': 'Iowa','20': 'Kansas',
    '21': 'Kentucky','22': 'Louisiana','23': 'Maine','24': 'Maryland','25': 'Massachusetts','26': 'Michigan',
    '27': 'Minnesota','28': 'Mississippi','29': 'Missouri','30': 'Montana','31': 'Nebraska','32': 'Nevada',
    '33': 'New Hampshire','34': 'New Jersey','35': 'New Mexico','36': 'New York','37': 'North Carolina',
    '38': 'North Dakota','39': 'Ohio','40': 'Oklahoma','41': 'Oregon','42': 'Pennsylvania','44': 'Rhode Island',
    '45': 'South Carolina','46': 'South Dakota','47': 'Tennessee','48': 'Texas','49': 'Utah','50': 'Vermont',
    '51': 'Virginia','53': 'Washington','54': 'West Virginia','55': 'Wisconsin','56': 'Wyoming'
}
df = df.dropna()
df['state_FIP'] = df['state_FIP'].astype(str).str.zfill(2)
df['state_name'] = df['state_FIP'].map(fip_to_state)

# ------------------------- App Layout ------------------------------- #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

L_FONT = "Work Sans, sans-serif"
LT_SIZE = 16
L_SIZE = 12

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                html.H1("Sentiment of US states", className="text-center mb-4"),
                html.P(
                    "† This project aims to analyze the sentiment towards climate change across the United States." 
                    "We collected data from social media platforms such as Twitter and analyzed the sentiment towards"
                    "climate change based on the stance of the user (Believer, Denier or Neutral). The map below shows" 
                    "the average sentiment towards climate change by state for the selected year and stance.",style={"font-size": 16, "text-align": 'left', 'marginTop': 15}
                ),
            ],
        )
    ),
    dbc.Row(
        [
            dbc.Col(
                [html.Label(['Choose stance:'],style={'font-weight': 'bold'}),
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
        [html.P("Use the slider below to select a year and see the average sentiment towards"
                "climate change by state for the chosen stance."
            ),
            html.P(
                "The map displays the average sentiment score for each state," 
                "where higher scores indicate more positive sentiment towards climate change."
            )
        ],
        width={"size": 4},
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
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Word Clouds by Stance"),

                dcc.Dropdown(
                    options = ["Denier", "Believer", "Neutral"],
                    value = "Words",
                    id = "wordcloud-dropdown",
                    style={'width': '100%'}
                ),
                html.P("""
                The word cloud provides a visual representation of the most salient and frequently used terms related to climate change on Twitter over time. 
                This can be a useful tool for understanding public discourse around climate change and identifying trends and shifts in language and rhetoric. 
                """)

            ]),

        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("2009", style={'textAlign': 'center'}),
            html.Img(
                style={'width': '100%', 'display': 'inline-block'},
                id = "wordcloud-2009",
                title = "2009"
                )], width=6),

        dbc.Col([
            html.H3("2019", style={'textAlign': 'center'}),
            html.Img(
                style={'width': '100%', 'display': 'inline-block', },
                id = "wordcloud-2019",
                title = "2019"
            )
        ], width=6),
    ]),
    dbc.Row(
        dbc.Col(
            [
                html.P(
                    "This project was developed by Jonathan Juarez, Jaskirat Kaur, Ridhi Purohit, and Grey Xu"
                    "as part of the Spring 2023 course 'CAPP 30122: Computer Science and Applications II' at the University of Chicago",
                    className="text-muted",
                ),
            ],
            width={"size": 10, "offset": 1},
            className="my-3",
        )
    ),
], fluid=True)

# ********************************** App callbacks *****************************
# Callback and function for displaying the map
@app.callback(
    Output('map-graph', 'figure'),
    [Input('stance_dropdown', 'value'),
     Input('year_slider', 'value')]
)

def update_map(stance, year):
    """
    This function takes the year and stance from the dropdown menu and updates the
    choropleth map on the app
    
    """
    filtered_df = df[(df['stance'] == stance) & (df['year'] == year)]
    avg_sentiment_df = filtered_df.groupby('state_name')['sentiment'].mean().reset_index()
    fig = px.choropleth_mapbox(avg_sentiment_df, geojson=geojson_file, color='sentiment',
                                  locations='state_name', featureidkey='properties.NAME',
                                  center={'lat': 37.0902, 'lon': -95.7129}, mapbox_style="carto-positron", zoom=3,
                                  color_continuous_scale='rdylgn', range_color=(-0.3, 0.3))
    return fig


# Juxtaposing word clouds from year 2009 and 2019
@app.callback(
    Output(component_id = "wordcloud-2009", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_2009(stance):
    """
    This function displayed the word cloud for the year 2009
    
    """
    if stance == "believer":
        image_path = "path_here"
    elif stance == "denier":
        image_path = "path_here"
    else:
        image_path = "path_here"
       
    encoded_image = base64.b64encode(open(image_path, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(
    Output(component_id = "wordcloud-2019", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_2019(stance):
    """
    This function displayed the word cloud for the year 2019
    
    """
    if stance == "believer":
        image_path = "path_here"
    elif stance == "denier":
        image_path = "path_here"
    else:
        image_path = "path_here"

    encoded_image = base64.b64encode(open(image_path, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

if __name__ == '__main__':
    app.run_server(debug=True)