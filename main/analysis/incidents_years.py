from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


#with bubbles representing incident type
#y axis = incident
#x axis =year or date

#pd.to_datetime(df'date']).dt.year

df = pd.read_csv("../sources/merged_date_county.csv")
#df_tweet_date = pd.read_csv("../sources/merged_twitter_text_county.csv")
print(len(df))

df_columns = ['disasterNumber', 'state', 'declarationType', 'declarationDate',
       'incidentBeginDate', 'incidentEndDate', 'fyDeclared', 'incidentType',
       'declarationTitle', 'fipsStateCode', 'fipsCountyCode', 'date',
       'county_FIP', 'topic', 'stance', 'gender', 'aggressiveness',
       'state_name', 'county_name', 'temperature_avg', 'sentiment', 'id']

app = Dash(__name__)

                 #size="temperature_avg"
fig = px.scatter(df, x='declarationDate', y='incidentType'
                 , color='incidentType', hover_name='state_name',
                 log_x=True, size_max=60)

app.layout = html.Div([
    dcc.Graph(
        id='incidents-time',
        figure=fig
    )
])

if _name_ == '_main_':
    app.run_server(debug=True)