
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

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
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="sentiment-dropdown",
                        options=[
                            {"label": "Before", "value": "before"},
                            {"label": "After", "value": "after"},
                            {"label": "Both", "value": "both"},
                        ],
                        value="both",
                        clearable=False,
                    ),
                    width={"size": 2},
                )
            ],
            justify="center",
        ),
        dbc.Row(
            dbc.Col(dcc.Graph(id="sentiment-plot"), width={"size": 12}),
            justify="center",
        ),
    ],
    fluid=True,
)

@app.callback(
    Output("sentiment-plot", "figure"),
    Input("sentiment-dropdown", "value"),
)
def update_sentiment_plot(selected_value):
    # Filter the data based on the selected option
    if selected_value == "before":
        data = df[["declarationDate", "Year_Month", "Avg_Sentiment_Before"]].dropna()
        title = "Average Sentiment of Tweets Before a Disaster Declaration"
    elif selected_value == "after":
        data = df[["declarationDate", "Year_Month", "Avg_Sentiment_After"]].dropna()
        title = "Average Sentiment of Tweets After a Disaster Declaration"
    else:
        data = df[["declarationDate", "Year_Month", "Avg_Sentiment_Before", "Avg_Sentiment_After"]].dropna()
        title = "Average Sentiment of Tweets Before & After a Disaster Declaration"
    
    # Create the plot
    fig = px.scatter(data, x="Year_Month", y=["Avg_Sentiment_Before", "Avg_Sentiment_After"], color_discrete_sequence=["blue", "red"])
    fig.update_layout(title=title, xaxis_title="Declaration Date", yaxis_title="Average Sentiment")
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)