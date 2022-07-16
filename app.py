#!/usr/bin/env python3

# import Dash
from dash import (
    Dash, html, dcc, Input, Output
)

# import plotly's go
import plotly.graph_objects as go

# import plotly's express library
import plotly.express as px

# import Pandas
import pandas as pd

# retrieve all of our data
from data.load import brain_data


# first, do some data inspection
# it's hard to not make assumptions on this data ;P
network_and_nodes = brain_data.loc[0].to_frame().reset_index()
network_and_hemi  = brain_data.loc[1].to_frame().reset_index()

magnitudes = brain_data.loc[3:].reset_index().set_index('network')
magnitudes = magnitudes.drop(columns='index')
magnitudes = magnitudes.astype(float)

num_trials = len(magnitudes.index)


# start up the app
app = Dash(__name__)

app.layout = html.Div([
        html.Div([
                dcc.Graph(id='magnitudes-graph'),
            ], style={'paddingBottom': 20}
        ),
        html.H4("Select trials to visualize: "),
        html.P([
            'Min trial number: ', 
            dcc.Input(
                type='number',
                value=0,
                min=0,
                max=num_trials-1,
                step=1,
                debounce=True,
                placeholder='min range',
                size='2',
                id='input-min'
            ),
            html.Span(style={'marginLeft': 20}),
            'Max trial number: ', 
            dcc.Input(
                type='number',
                value=1,
                min=1,
                max=num_trials,
                step=1,
                debounce=True,
                placeholder='max range',
                size='2',
                id='input-max'
            ),
        ]),
    ])


# set up a callback
@app.callback(
    Output('magnitudes-graph', 'figure'),
    Input('input-min', 'value'),
    Input('input-max', 'value'),
)
def slider_callback(trial_no_min, trial_no_max):
    # make sure to sanitize our input
    try:
        trial_no_min = int(trial_no_min)
        trial_no_min = trial_no_min if trial_no_min >= 0 else 0
        trial_no_min = trial_no_min if trial_no_min <= num_trials-1 else num_trials-1
    except:
        trial_no_min = 0

    try:
        trial_no_max = int(trial_no_max) + 1
        trial_no_max = trial_no_max if trial_no_max >= 1 else 1
        trial_no_max = trial_no_max if trial_no_max <= num_trials else num_trials
    except:
        trial_no_max = 1

    # arrange the magnitudes in order
    plot = go.Figure()

    for i in range(trial_no_min, trial_no_max):
        plot.add_trace(
            go.Scatter(
                x=list(range(len(magnitudes.columns))),
                y=magnitudes.loc[str(i)],
                mode='lines',
                name=f'Trial no. {i}',
            )
        )

    plot.update_layout(transition_duration=100)

    return plot


if __name__ == '__main__':
    app.run_server(debug=True)
