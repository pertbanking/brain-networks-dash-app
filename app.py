#!/usr/bin/env python3

# core imports
# import whatevah

# import Dash
from dash import Dash, html, dcc

# import Pandas
import pandas as pd

# retrieve all of our data
from data.load import brain_data


# first, do some data inspection
# it's hard to not make assumptions on this data ;P
network_and_nodes = brain_data.loc[0].to_frame().reset_index()
network_and_hemi  = brain_data.loc[1].to_frame().reset_index()

magnitudes = brain_data.loc[3:].reset_index().set_index('network').head()
magnitudes = magnitudes.drop(columns='index')

num_trials = len(magnitudes.index)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(-5, 10, 1, value=-3)
])

if __name__ == '__main__':
    app.run_server(debug=True)
