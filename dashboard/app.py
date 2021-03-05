import time

import dash, json, sys, os
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, MATCH, ALL
import flask
import layouts
import warnings
import dbrools

warnings.filterwarnings("ignore")

main_path_data = os.path.expanduser('/usr/local/WB/data')


def output_reader(proc, file):
    while True:
        byte = proc.stdout.read(1)
        if byte:
            sys.stdout.buffer.write(byte)
            sys.stdout.flush()
            file.buffer.write(byte)
        else:
            break


external_stylesheets = [dbc.themes.DARKLY]
app = flask.Flask(__name__)
dash_app = dash.Dash(__name__,
                     url_base_pathname="/",
                     server=app,
                     external_stylesheets=external_stylesheets,
                     meta_tags=[
                         {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                     ])
dash_app.title = 'Ejaw quiz'

dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    html.Div("TEST", id="hidden_port", style={'display': 'none'})
])


@dash_app.callback(Output('page-content', 'children'),
                   [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return layouts.my_view()
    elif pathname == '/987':
        return "Admin"
    else:
        return "404"


# # ##############################    Refresh RATES    ##################################
# @dash_app.callback(
#     [Output("sub_column_left", "children")],
#     [Input("interval_graf", 'n_intervals')])
# def modal_content_coll(n):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]['prop_id'].split('.')
#
#     if button_id[0] == 'interval_graf':
#         reponse = layouts.sub_column_left()
#         return [reponse]
#     else:
#         raise PreventUpdate
#
#

@dash_app.callback(
    [Output("main_list", "children"),
     Output("mymail", "children")],
    [Input("save_email", "n_clicks")],
    [State("new_email", "value")]
)
def tab_content(n1, mail):
    trigger = dash.callback_context.triggered[0]
    button = trigger["prop_id"].split(".")[0]

    if not button:
        raise PreventUpdate
    else:
        if button == "save_email":
            if mail not in dbrools.get_all_personal():
                dbrools.add_person(mail)
                return layouts.quiz_tab(mail), mail
            else:
                return layouts.quiz_tab(mail), mail
        else:
            raise PreventUpdate


# ##############################   Questions   ##################################
@dash_app.callback(
    [Output({'type': 'symbol', 'index': MATCH}, "value")],

    [Input({'type': 'next_btn1', 'index': MATCH}, 'n_clicks'),
     Input({'type': 'next_btn2', 'index': MATCH}, 'n_clicks')],

    [State({'type': 'next_btn1', 'index': MATCH}, 'children'),
     State({'type': 'next_btn2', 'index': MATCH}, 'children')]
)
def toggle_modal(n1, n2, symbol1, symbol2):
    trigger = dash.callback_context.triggered[0]
    button = trigger["prop_id"].split(".")[0]

    if not button:
        raise PreventUpdate
    else:
        if type(button) is str:
            button = json.loads(button.replace("'", "\""))
        if button["type"] == 'next_btn1':
            print(symbol1)
            return [symbol1]
        elif button["type"] == 'next_btn2':
            print(symbol2)
            return [symbol2]
        else:
            raise PreventUpdate


# ##############################   Questions   ##################################
@dash_app.callback(
    [Output('quiz_list', "children")],
    [Input({'type': 'next_btn', 'index': ALL}, 'n_clicks')],
    [State({'type': 'symbol', 'index': ALL}, 'value'),
     State({'type': 'next_btn1', 'index': ALL}, 'children'),
     State({'type': 'next_btn2', 'index': ALL}, 'children'),
     State("mymail", 'children')]
)
def toggle_modal(n1, symbol, btn1, btn2, mymail):
    trigger = dash.callback_context.triggered[0]
    button = trigger["prop_id"].split(".")[0]

    if not button:
        raise PreventUpdate
    else:
        if type(button) is str:
            button = json.loads(button.replace("'", "\""))
        if button["type"] == 'next_btn':

            dbrools.insert_answer(btn1[0], btn2[0], symbol[0], mymail)
            time.sleep(0.5)
            answered = dbrools.check_person(mymail)
            for i in dbrools.get_list():
                if f"{i['option1']}_{i['option2']}" in answered:
                    pass
                else:
                    return [layouts.create_quiz(i['option1'], i['option2'], i['option1'])]
            return [html.H1("You have already finished the test")]
        else:
            raise PreventUpdate


if __name__ == '__main__':
    dash_app.run_server(host="0.0.0.0", port=5075, debug=False)
