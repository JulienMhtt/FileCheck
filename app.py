from dash import Dash, html, dcc, callback, Output, Input, State
from file_check import FileCheck
import pandas as pd

# Colors
colors = {
    'general_background' : '#FC4C4C',
    'head_title' : '#383838',
    'text' : '#000000'
}


# Initialize the app
app = Dash()


# App layout
app.layout = html.Div(
    style={'backgroundColor': colors['general_background'], 'height': '100vh', 'padding': '20px'},
    children=[
        # Title
        html.H1(
            children='CHECKFILE APP',
            style={
                'textAlign': 'center',
                'color': colors['head_title']
            }
        ),

        html.Div(
            children='The app that helps you verify your data',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        # Input field
        html.Div(
            children=['add your file path',
                      html.Br(),
                      dcc.Input(id='filepath-input', type='text'),
                      html.Button('Submit', id='submit-button', n_clicks=0)
                      ],
            style={
                'textAlign': 'left',
                'color': colors['text']
            }
        ),

        # Store to keep the file data
        dcc.Store(
            id='file-data', storage_type='session'
            ),

        # Output div to display the input value
        html.Div(
            id='display-filepath', style={'color': colors['text']}
        )

    ])

# CALLBACKS

# Get the filepath from input and display it
@app.callback(
    Output('display-filepath', 'children'),
    Input('submit-button', 'n_clicks'),
    State('filepath-input', 'value')
)
def create_filecheck_object(n_clicks, filepath):
    if n_clicks > 0 and filepath:
        file_checker = FileCheck(filepath)
        file_checker.file_read()
        return filepath
    return ''



# Load the csv file
@app.callback(
    Output('file-data', 'data'),
    Input('submit-button', 'n_clicks'),
    State('filepath-input', 'value')
)
def load_csv_store_data(n_clicks, filepath):
    if n_clicks > 0 and filepath:
        df = pd.read_csv(filepath)
        return df.to_json(date_format='iso', orient='split')
    return ''


# Display table stats
@app.callback(
    Output('output-div', 'children'),
    Input('file-data', 'data')
)
def display_file_stats(data):
    if data:
        df = pd.read_json(data, orient='split')
        file_checker = FileCheck('')
        file_checker.df = df
        stats = file_checker.file_stats().to_string(index=False)
        return html.Pre(f"File Statistics:\n{stats}")
    return 'No file data available.'





if __name__ == '__main__':
    app.run(debug=True)