import json
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Load the geojson data
with open("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/us-states.json", 'r') as f:
    geojson_data = json.load(f)

# Load sentiment data file
sentiment_data = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_year_state.csv")
sentiment_df = sentiment_data[(sentiment_data['year'] != 2006) & (sentiment_data['year'] != 2007)]

# county data for time series
time_series_data = pd.read_csv("/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/twitter_year_county.csv")

# Create the app
app = dash.Dash(__name__)

# Define a function that takes a year as input and returns a new Choropleth map with the sentiment scores for that year.
def update_map(year):
    fig = px.choropleth_mapbox(sentiment_df[sentiment_df['year'] == year], geojson=geojson_data, color='sentiment',
                               locations='state_FIP', featureidkey='properties.STATE',
                               center={'lat': 37.0902, 'lon': -95.7129}, mapbox_style="carto-positron", zoom=3,
                               color_continuous_scale='rdylgn', range_color=(-0.3, 0.3))
    return fig

# Create the initial Choropleth map using the sentiment scores for the first year in the data
fig = update_map(sentiment_df['year'].min())

# Define the range of years for the slider
year_range = [sentiment_df['year'].min(), sentiment_df['year'].max()]

# Create the slider
slider = dcc.RangeSlider(
    id='year-slider',
    min=year_range[0],
    max=year_range[1],
    value=[year_range[0], year_range[1]],
    marks={str(year): str(year) for year in sentiment_df['year'].unique()}
)

# Define the app layout
app.layout = html.Div([
    dcc.Graph(id='map', figure=fig),
    slider
])

# Define the app callback
@app.callback(
    Output('map', 'figure'),
    Input('year-slider', 'value')
)
def update_map_callback(years):
    return update_map(years[0])

if __name__ == '__main__':
    app.run_server(debug=True)