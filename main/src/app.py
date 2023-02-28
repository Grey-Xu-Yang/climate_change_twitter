import json
import plotly.express as px

# Load the geojson data
with open('/content/drive/My Drive/CS2_Project/us_county/us-states.json', 'r') as f:
    geojson_data = json.load(f)


# Define a function that takes a year as input and returns a new Choropleth map with the sentiment scores for that year.
def update_map(year):
    fig = px.choropleth_mapbox(sentiment_df[sentiment_df['year'] == year], geojson=geojson_data, color='sentiment',
                               locations='state_FIP', featureidkey='properties.STATE',
                               center={'lat': 37.0902, 'lon': -95.7129}, mapbox_style="carto-positron", zoom=3,
                               color_continuous_scale='rdylgn', range_color=(-0.3, 0.3))
    return fig

# Create the initial Choropleth map using the sentiment scores for the first year in the data
fig = update_map(sentiment_df['year'].min())

# Define the list of year options that will be displayed in the dropdown menu.
year_options = sentiment_df['year'].unique()

# Create a list of dictionaries that define the behavior of the dropdown menu. Each dictionary corresponds to a dropdown menu button,
# and contains the label of the button and the behavior when the button is clicked. In this case, we want to call the update_map
# function with the selected year.
dropdown_buttons = [
    {
        'label': str(year),
        'method': 'update',
        'args': [{'z': [sentiment_df[sentiment_df['year'] == year]['sentiment'].tolist()]}]
    }
    for year in year_options
]

# Add the dropdown menu to the Plotly Figure object using the update_layout method.
fig.update_layout(
    updatemenus=[
        {
            'buttons': dropdown_buttons,
            'direction': 'down',
            'pad': {'r': 10, 't': 10},
            'showactive': True,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.1,
            'yanchor': 'top'
        }
    ]
)

# Show the plot
fig.show()