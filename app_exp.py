
import json
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import base64
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

df2 = pd.read_csv('/home/jaskiratk/capp30122/30122-project-hot-or-not/main/sources/average_sentiments_data.csv')

cols = ['declarationTitle', 'declarationDate', 'Avg_Sentiment_Before', 'Avg_Sentiment_After']
df_plt = df2.loc[:, cols]
df = df_plt.sort_values(by="declarationDate", ascending=True)
df['Year_Month'] = df['declarationDate'].apply(lambda x: x[:7])

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H1("Average Sentiment of Tweets Before & After a Disaster Declaration"),
                width={"size": 12},
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="sentiment-plot", 
                    figure=px.scatter(
                        df, 
                        x="Year_Month", 
                        y=["Avg_Sentiment_Before", "Avg_Sentiment_After"], 
                        color_discrete_sequence=["blue", "red"], 
                        hover_data=['declarationTitle']
                    ).update_layout(
                        title="Average Sentiment of Tweets Before & After a Disaster Declaration", 
                        xaxis_title="Declaration Date", 
                        yaxis_title="Average Sentiment"
                    )
                ),
                width={"size": 12},
            ))
        ],
        fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True)