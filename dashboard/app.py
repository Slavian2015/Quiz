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
# # ##############################   Orders   ##################################
# @dash_app.callback(
#     [Output({'type': 'order_result', 'index': MATCH}, "children")],
#
#     [Input({'type': 'order_buy_btn', 'index': MATCH}, 'n_clicks'),
#      Input({'type': 'order_sell_btn', 'index': MATCH}, 'n_clicks'),
#      Input({'type': 'order_sec_btn', 'index': MATCH}, 'value'),
#      Input({'type': 'order_qty_btn', 'index': MATCH}, 'value'),
#      Input({'type': 'order_price_btn', 'index': MATCH}, 'value')],
#
#     [State({'type': 'order_sec_btn', 'index': MATCH}, 'value'),
#      State({'type': 'order_price_btn', 'index': MATCH}, 'value'),
#      State({'type': 'order_qty_btn', 'index': MATCH}, 'value')]
# )
# def toggle_modal(n1, n2, n3, n4, n5, symbol, price, qty):
#     trigger = dash.callback_context.triggered[0]
#     button = trigger["prop_id"].split(".")[0]
#
#     if not button:
#         raise PreventUpdate
#     else:
#         if type(button) is str:
#             button = json.loads(button.replace("'", "\""))
#         if button["type"] == 'order_sec_btn':
#             if symbol in full_list2 and qty is not None:
#                 return [None]
#             else:
#                 raise PreventUpdate
#         elif button["type"] == 'order_price_btn':
#             if price is not None and qty is not None:
#                 result = float(price) * float(qty)
#                 return [f"{result} $"]
#             else:
#                 raise PreventUpdate
#         elif button["type"] == 'order_qty_btn':
#             if symbol in full_list2 and qty is not None:
#                 # my_new_price = dbrools.get_my_data()
#                 # result = float(my_new_price["data"][symbol]["a"][-1]) * float(qty)
#                 return [None]
#             else:
#                 raise PreventUpdate
#         elif button["type"] == 'order_buy_btn':
#             if not symbol or not qty:
#                 return ["ERROR"]
#             reponse = Orders.my_order(symbol=symbol, side=1, amount=qty, price=price)
#             if reponse["error"]:
#                 return [f"{reponse['result']}"]
#             return [f"You bought {symbol}"]
#         elif button["type"] == 'order_sell_btn':
#             if not symbol or not qty:
#                 return ["ERROR"]
#             reponse = Orders.my_order(symbol=symbol, side=2, amount=qty, price=price)
#             if reponse["error"]:
#                 return [f"{reponse['result']}"]
#             return [f"You sold {symbol}"]
#         else:
#             raise PreventUpdate
#
#
@dash_app.callback(
    [Output("main_list", "children")],
    [Input("save_email", "n_clicks")],
    [State("new_email", "value")]
)
def tab_content(n1, mail):
    trigger = dash.callback_context.triggered[0]
    button = trigger["prop_id"].split(".")[0]

    print(mail)
    if not button:
        raise PreventUpdate
    else:
        if button == "save_email":
            if mail not in dbrools.get_all_personal():
                dbrools.add_person(mail)
                return ["Success"]
            else:
                return [html.H1("This mail has been used")]
        else:
            raise PreventUpdate

# ###############################    REGIM BUTTONS    ##################################
# @dash_app.callback([Output('main_buttons', 'children')],
#                    [Input('parser_on', 'n_clicks'),
#                     Input('regim_on', 'n_clicks'),
#                     Input('regim_off', 'n_clicks'),
#                     Input('balance_btn', 'n_clicks'),
#                     ])
# def trigger_by_modify(n1, n2, n3, n4):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]['prop_id'].split('.')
#     # print(button_id[0])
#     if button_id[0] == 'parser_on':
#         a_file1 = open(main_path_data + "/bal.json", "r")
#         rools = json.load(a_file1)
#         a_file1.close()
#         if rools["bin"] == 5000:
#             rools["bin"] = 1000
#         else:
#             rools["bin"] = 5000
#
#         f = open(main_path_data + "/bal.json", "w")
#         json.dump(rools, f)
#         f.close()
#
#         # with subprocess.Popen(["python", '/usr/local/WB/dashboard/My_parser.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc1, \
#         #         open('/usr/local/WB/data/Parser_Main.log', 'w') as file1:
#         #     t1 = threading.Thread(target=output_reader, args=(proc1, file1))
#         #     t1.start()
#         #     t1.join()
#         return [layouts.start_buttons_card(b1=True, b2=False, b3=False, b4=False)]
#     # elif button_id[0] == 'parser_off':
#     #     # script = "/usr/local/WB/dashboard/My_parser.py"
#     #     # subprocess.check_call(["pkill", "-9", "-f", script])
#     #     return [layouts.start_buttons_card(b1=False, b2=True, b3=False, b4=False)]
#     elif button_id[0] == 'regim_on':
#         with subprocess.Popen(["python", '/usr/local/WB/dashboard/BOT.py'], stdout=subprocess.PIPE,
#                               stderr=subprocess.PIPE) as proc1, \
#                 open('/usr/local/WB/data/BOT_log.txt', 'w') as file1:
#             t1 = threading.Thread(target=output_reader, args=(proc1, file1))
#             t1.start()
#             t1.join()
#         return [layouts.start_buttons_card(b1=False, b2=False, b3=True, b4=False)]
#     elif button_id[0] == 'regim_off':
#         script = "/usr/local/WB/dashboard/BOT.py"
#         subprocess.check_call(["pkill", "-9", "-f", script])
#         return [layouts.start_buttons_card(b1=False, b2=False, b3=False, b4=True)]
#     elif button_id[0] == 'balance_btn':
#         Orders.my_balance()
#         return [layouts.start_buttons_card(b1=False, b2=False, b3=False, b4=False)]
#     else:
#         raise PreventUpdate
#
#
# ###############################    BALANCE  BUTTONS    ##################################
# @dash_app.callback([Output('full_list', 'children')],
#                    [
#                        Input('parser_on', 'n_clicks'),
#                        Input('balance_btn', 'n_clicks'),
#                    ])
# def trigger_by_modify(n1, n2):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]['prop_id'].split('.')
#
#     if button_id[0] == 'balance_btn':
#         return [layouts.full_list()]
#     elif button_id[0] == 'parser_on':
#         return [layouts.full_list()]
#     else:
#         raise PreventUpdate
#
#
# # ##############################    Refresh GRAFS    ##################################
# @dash_app.callback(
#     my_grafs,
#     [Input("interval_graf_full", 'n_intervals')])
# def modal_content_coll(n):
#     ctx = dash.callback_context
#     button_id = ctx.triggered[0]['prop_id'].split('.')
#
#     if button_id[0] == 'interval_graf_full':
#
#         reponse = day_trader.refresh_grafs()
#
#         return reponse
#     else:
#         raise PreventUpdate


if __name__ == '__main__':
    dash_app.run_server(host="0.0.0.0", port=5075, debug=False)
