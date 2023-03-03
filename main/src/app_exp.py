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


# Load the sentiment data
sentiment_df = pd.read_csv('/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_year_state.csv')
sentiment_df = sentiment_df[(sentiment_df["year"] != 2006) & (sentiment_df["year"] != 2007)]
# Load the geojson data
with open("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/us-states.json", 'r') as f:
    geojson_data = json.load(f)


app = dash.Dash(__name__)

# Define the layout of the app


app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("Climate Change Sentiment Analysis", className="text-center mb-4"),
        )
    ), 
    dbc.Row(
        dbc.Col(
            html.H1("Jonathan Juarez, Jaskirat Kaur, Ridhi Purohit, Grey Xu",
                style={"font-style": "italic", "font-size": 16, "text-align": 'center'})
        )
    ),
    dbc.Row(
        dbc.Col(
            html.H1(" This project aims to analyze the sentiment towards climate change across the United States. \
                    We collected data from social media platforms such as Twitter  \ and analyzed the sentiment towards climate change based on the stance of the user (Believer, Denier or Neutral).' \
                    The map below shows the average sentiment towards climate change by state for the selected year and stance.",
                style={"font-size": 16, "text-align": 'left', 'marginTop': 15})
        )
    ),
    dbc.Row(
        [
            html.H3("Mapping sentiment on US states", style={'marginBottom': 10, 'marginTop': 20}),
        ]
    ),
    dbc.Row(
        dbc.Col(
            html.Div(
                children=[
                    html.H1('Sentiment Analysis of Tweets by State'),
                    html.Div(
                        children=[
                            html.Label('Select Year: '),
                            dcc.Dropdown(
                                id='year-dropdown',
                                options=[{'label': year, 'value': year} for year in sentiment_df['year'].unique()],
                                value=sentiment_df['year'].min()
                            ),
                        ], 
                        style={'width': '50%', 'display': 'inline-block'}
                    ),
                    dcc.Graph(id='choropleth-map')
                ]
            )
        )
    ),
], className="mt-4")


# Define the callback function to update the Choropleth map when a new year is selected
@app.callback(
    dash.dependencies.Output('choropleth-map', 'figure'),
    [dash.dependencies.Input('year-dropdown', 'value')]
)
def update_map(year):
    fig = px.choropleth_mapbox(sentiment_df[sentiment_df['year'] == year], geojson=geojson_data, color='sentiment',
                               locations='state_FIP', featureidkey='properties.STATE',
                               center={'lat': 37.0902, 'lon': -95.7129}, mapbox_style="carto-positron", zoom=3,
                               color_continuous_scale='rdylgn', range_color=(-0.3, 0.3))
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)