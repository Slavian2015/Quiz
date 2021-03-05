# -*- coding: utf-8 -*-
import json
import time

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import sys, base64, os
import dbrools

sys.path.insert(0, r'/usr/local/WB')
main_path_data2 = os.path.expanduser('/usr/local/WB/data/')


def my_view():
    layout = [
              html.Div(
                  style={
                      "height": "100vh",
                      "minHeight": "100vh",
                      "maxHeight": "100vh",
                      "overflowY": "hidden"
                  },
                  children=content())]
    return layout


def content():
    cont = dbc.Row(style={"width": "100%", "height": "100vh", "margin": "0", "padding": "0"},
                   justify="center",
                   align="center",
                   children=[
                       dbc.Col(style={"textAlign": "center",
                                      "height": "100vh",
                                      "minHeight": "100vh",
                                      "maxHeight": "100vh",
                                      "overflowY": "scroll",
                                      "margin": "0",
                                      "padding": "0"
                                      },
                               width=4,
                               className="no-scrollbars",
                               children=[]),
                       dbc.Col(style={"textAlign": "center",
                                      "overflowY": "hidden",
                                      'align': 'center',
                                      "margin": "0",
                                      "padding": "0",
                                      "padding-top": "2%"
                                      },
                               align="center",
                               width=4,
                               className="no-scrollbars",
                               children=column_left()),
                       dbc.Col(style={"textAlign": "center",
                                      "height": "100vh",
                                      "minHeight": "100vh",
                                      "maxHeight": "100vh",
                                      "overflowY": "hidden",
                                      "margin": "0",
                                      "padding": "0"},
                               width=4,
                               children=[]),
                   ],
                   no_gutters=True)

    return cont


def column_left():
    cont = [
        html.Div(style={'display': 'none'}, children=html.P("", id='symbol1')),
        dbc.Row(style={"width": "100%",
                       "margin": "0",
                       "padding": "0"},
                id="main_list",
                no_gutters=False,
                children=create_email()),
    ]

    return cont


def create_email():

    card = dbc.Card(color="secondary",
                    style={"width": "100%",
                           "padding": "0",
                           "margin": "10px",
                           "margin-bottom": "0px"
                           },
                    inverse=True,
                    children=[
                        dbc.CardBody([
                            dbc.InputGroup([
                                dbc.InputGroupAddon(html.P("Your E-mail",
                                                           style={"width": "100%"}),
                                                    style={"width": "80px"},
                                                    addon_type="prepend"),
                                dbc.Input(placeholder="test@test.com",
                                          id="new_email",
                                          type="email"),

                            ]),
                            dbc.CardFooter(dbc.Button("create account >>", id="save_email", color="success"))
                        ])
                    ])

    return card


def sub_column_left():
    df = pd.read_csv(os.path.expanduser('/usr/local/WB/data/prices_bd.csv'))
    trend = new_trend(df, 1)
    trend_up = new_trend(df, 2)

    cont = [
        dbc.Row(style={"width": "100%",
                       "margin": "0",
                       "padding": "0"},
                no_gutters=False,
                children=trend),
        dbc.Row(style={"width": "100%",
                       "margin": "0",
                       "padding": "0"},
                no_gutters=False,
                children=trend_up),
    ]

    return cont





