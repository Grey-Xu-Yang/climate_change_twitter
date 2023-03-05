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
from .src.data4dash import add_state_column
from .src.app import app

if __name__ == '__main__':
    app.run_server(debug=True)
