import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import subprocess

script_path = "/pbsusers/trace_0/submit_trace.sh"

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button('Run Script', id='run-script-button', style={'disabled': False}), 
    html.Div(id='output-div'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

@app.callback(
    [Output('run-script-button', 'disabled'),
     Output('output-div', 'children'),
     Output('interval', 'n_intervals')],
    Input('run-script-button', 'n_clicks'),
    Input('interval', 'n_intervals'),
    State('run-script-button', 'disabled')
)
def trigger_script_and_check(n_clicks, n_intervals, button_disabled):
    script_process = None

    if n_clicks and not button_disabled: 
        script_process = subprocess.Popen(script_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, 'Script started in the background!', 0 

    elif script_process:
        # Check if process finished, get output or errors
        if script_process.poll() is not None:  # Finished
            output, errors = script_process.communicate()
            result_message = 'Script finished!'
            if output:
                result_message += f'\nOutput:\n{output.decode()}'
            if errors:
                result_message += f'\nErrors:\n{errors.decode()}'
            return False, result_message, 0  # Re-enable button 

    return button_disabled, 'Script is running...', n_intervals + 1 

if __name__ == '__main__':
    app.run_server(debug=True)
