import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from filter_sentiment import clean_viz, filter_for_visualization

# Load the geojson data
with open('/sources/us-states.json', 'r') as f:
    geojson_data = json.load(f)

# Load sentiment data file
sentiment_df = filter_for_visualization("state_FIP")

# Define a function that takes a year as input and returns a new Choropleth map with the sentiment scores for that year.
def update_map(year):
    fig = px.choropleth_mapbox(sentiment_df[sentiment_df['year'] == year], geojson=geojson_data, color='sentiment',
                               locations='state_FIP', featureidkey='properties.STATE',
                               center={'lat': 37.0902, 'lon': -95.7129}, mapbox_style="carto-positron", zoom=3,
                               color_continuous_scale='rdylgn', range_color=(-0.3, 0.3))
    return fig

# Create the initial Choropleth map using the sentiment scores for the first year in the data
fig_map = update_map(sentiment_df['year'].min())

# Define the list of year options that will be displayed in the dropdown menu.
year_options = sentiment_df['year'].unique()

# Create a list of dictionaries that define the behavior of the dropdown menu for the Choropleth map.
map_dropdown_buttons = [
    {
        'label': str(year),
        'method': 'update',
        'args': [{'z': [sentiment_df[sentiment_df['year'] == year]['sentiment'].tolist()]}]
    }
    for year in year_options
]

# Add the dropdown menu to the Choropleth map using the update_layout method.
fig_map.update_layout(
    updatemenus=[
        {
            'buttons': map_dropdown_buttons,
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

# Create a function to generate a box plot of sentiment scores and climate change topic for a given year.
def generate_box_plot(year):
    filtered_df = sentiment_df[sentiment_df['year'] == year]
    box_fig = px.box(filtered_df, x="climate_change_topic", y="sentiment")
    return box_fig

# Create the initial box plot using the sentiment scores for the first year in the data.
fig_box = generate_box_plot(sentiment_df['year'].min())

# Create the list of dictionaries that define the behavior of the dropdown menu for the box plot.
box_dropdown_buttons = [
    {
        'label': str(year),
        'method': 'update',
        'args': [{'data': [go.Box({'x': sentiment_df[sentiment_df['year'] == year]['climate_change_topic'], 
                                    'y': sentiment_df[sentiment_df['year'] == year]['sentiment'], 
                                    'type': 'box'})]}]
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

Define a function to create a year-wise box plot of sentiment score and climate change topic
def create_boxplot(year):
# Filter data for the selected year
year_df = sentiment_df[sentiment_df['year'] == year]

# Filter data for climate change topic
cc_df = year_df[year_df['clean_text'].str.contains('climate change')]

# Create the box plot
fig = px.box(cc_df, x='year', y='sentiment', title=f'Sentiment Score and Climate Change Topic in {year}', 
             color_discrete_sequence=['#636EFA'])

return fig
# Create the initial box plot using the first year in the data
box_fig = create_boxplot(sentiment_df['year'].min())

# Define the list of year options that will be displayed in the dropdown menu.
year_options = sentiment_df['year'].unique()

# Create a list of dictionaries that define the behavior of the dropdown menu. Each dictionary corresponds to a dropdown menu button,
# and contains the label of the button and the behavior when the button is clicked. In this case, we want to call the create_boxplot
# function with the selected year.
dropdown_buttons = [
{
'label': str(year),
'method': 'update',
'args': [{'title': f'Sentiment Score and Climate Change Topic in {year}',
'y': [sentiment_df[sentiment_df['year'] == year][sentiment_df[sentiment_df['year'] == year]['clean_text'].str.contains('climate change')]['sentiment'].tolist()]}]
}
for year in year_options
]

#Add the dropdown menu to the Plotly Figure object using the update_layout method.
box_fig.update_layout(
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

Create the dashboard layout
dashboard = html.Div([
html.H1('Climate Change Sentiment Analysis Dashboard'),
html.Div([
html.Div([
dcc.Graph(id='map', figure=fig),
], className='six columns'),
html.Div([
dcc.Graph(id='box', figure=box_fig)
], className='six columns')
], className='row')
])

Run the app
if name == 'main':
app.run_server(debug=True)