
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
from .data4dash import add_state_column
import dash_bootstrap_components as dbc


# load dataframes for the three stances
believer_df = pd.read_csv("./main/sources/believer_twitter.csv")
denier_df = pd.read_csv("./main/sources/denier_twitter.csv")
neutral_df = pd.read_csv("./main/sources/neutral_twitter.csv")

final_df = pd.concat([believer_df, denier_df, neutral_df])

with open("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/us-states.json", 'r') as f:
    geojson_file = json.load(f)

# ******************************** Data cleaning ***************************** #

df = add_state_column(final_df)

# --------------------------------- App Layout ------------------------------- #
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            [
                html.H1("Hot or Not: An Enquiry into Climate Change Perceptions", style = {'textAlign': 'center', "padding-top": "70px"}),
                html.P(
                    "Welcome to our climate sentiment analysis dashboard! Our project is dedicated"
                    " to analyzing the sentiment towards climate change across the United States."
                    " We gathered and merged data from Twitter and FEMA to understand the sentiment"
                    " towards climate change based on the stance of the user (Believer, Denier or Neutral." 
                    " Explore our dashboard to gain insights into how people feel about this critical issue"
                    " in different regions of the country.",
                    style={"font-size": 16, "text-align": 'left', 'marginTop': 15},
                ),
            ]
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
                    html.H2("Sentiment Map by Stance and Year", className="text-center mb-4"),        
                    html.P(
                        "The map displays the average sentiment score for each state. "            
                        "Use the slider below to select a year and see the average sentiment towards "            
                        "climate change by state for the chosen stance.",
                        style={"font-size": 16, "text-align": 'left', 'marginTop': 15}
                    )
                ],
                width={"size": 4},
                className="my-3", align = "center"
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
                html.P("""
                The word cloud provides a visual representation of the most salient "
                "and frequently used terms related to climate change on Twitter over time. " 
                "This can be a useful tool for understanding public discourse around climate "
                "change and identifying trends and shifts in language and rhetoric."
                """),

                dcc.Dropdown(
                    options=[
                        {'label': 'Denier', 'value': 'denier'},
                        {'label': 'Believer', 'value': 'believer'},
                        {'label': 'Neutral', 'value': 'neutral'}
                    ],
                    value='Words',
                    id='wordcloud-dropdown',
                    style={'width': '100%'}
                ),
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
            )
        ], width=6),
        dbc.Col([
            html.H3("2019", style={'textAlign': 'center'}),
            html.Img(
                style={'width': '100%', 'display': 'inline-block', },
                id = "wordcloud-2019",
                title = "2019"
            )
        ], width=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3("Comparison Of Tweets Sentiment in Relation to Disaster Event Declaration"),
                html.P("""
                The word cloud provides a visual representation of the most salient "
                "and frequently used terms related to climate change on Twitter over time. " 
                "This can be a useful tool for understanding public discourse around climate "
                "change and identifying trends and shifts in language and rhetoric."
                """),

                dcc.Dropdown(
                    options=[
                        {'label': 'Before', 'value': 'before'},
                        {'label': 'After', 'value': 'after'},
                        {'label': 'Before and After', 'value': 'before and after'}
                    ],
                    value='Words',
                    id='wordcloud-dropdown',
                    style={'width': '100%'}
                ),
            ]),

        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("2009", style={'textAlign': 'center'}),
            html.Img(
                style={'width': '100%', 'display': 'inline-block'},
                id = "disaster_sentiment",
                title = "2009"
            )
        ], width=10, align = "center"),
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("2009", style={'textAlign': 'center'}),
            html.Img(
                style={'width': '100%', 'display': 'inline-block'},
                id = "disaster_sentiment",
                title = "2009"
            )
        ], width=10, align = "center"),
    ]),
    dbc.Row(
        dbc.Col(
            [
                html.P(
                    "This project was developed by Jonathan Juarez, Jaskirat Kaur, "
                    "Ridhi Purohit, and Grey Xu as part of the Spring 2023 course "
                    "'CAPP 30122: Computer Science and Applications II' at the University of Chicago",
                    className="text-muted",
                ),
            ],
            width={"size": 10, "offset": 1},
            className="my-3",
        )
    ),
], fluid=True)

# ********************************** App callbacks *****************************
# Callback for displaying the map
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
        image_path = "./main/images/wordcloud_believer_2009.png"
    elif stance == "denier":
        image_path = "./main/images/wordcloud_denier_2009.png"
    else:
        image_path = "./main/images/wordcloud_neutral_2009.png"
       
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
        image_path = "./main/images/wordcloud_believer_2018.png"
    elif stance == "denier":
        image_path = "./main/images/wordcloud_denier_2018.png"
    else:
        image_path = "./main/images/wordcloud_neutral_2018.png"

    encoded_image = base64.b64encode(open(image_path, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(
    Output(component_id = "disaster_sentiment", component_property = "src"),
    Input(component_id = "wordcloud-dropdown", component_property = "value")
)
def display_wordclouds_2019(stance):
    """
    
    This function displays the average sentiment of people before and after a
    disaster event
    
    """
    if stance == "after":
        image_path = "./main/images/Average Sentiment of Tweets After a Disaster Declaration.png"
    elif stance == "before":
        image_path = "./main/images/Average Sentiment of Tweets Before a Disaster Declaration.png"
    else:
        image_path = "./main/images/Average Sentiment of Tweets Before & After a Disaster Declaration.png"

    encoded_image = base64.b64encode(open(image_path, 'rb').read())

    return 'data:image/png;base64,{}'.format(encoded_image.decode())

if __name__ == '__main__':
    app.run_server(debug=True)