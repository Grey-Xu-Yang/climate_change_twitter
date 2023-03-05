# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd

app = Dash(__name__)

df = pd.read_csv('/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/merged_date_state.csv')
df['year'] = pd.to_datetime(int(df['date'])).dt.year

fig = px.scatter(df, x='year', y='sentiment', color='incidentType', size='incidentType',
                 hover_data=['incidentType'], title='Sentiment vs. Incident Type by Year')

app.layout = html.Div([
    dcc.Graph(
        id='incident-type',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)