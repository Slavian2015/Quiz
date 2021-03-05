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
                               children=column_left()),
                       dbc.Col(style={"textAlign": "center",
                                      "overflowY": "hidden",
                                      'align': 'center',
                                      "margin": "0",
                                      "padding": "0",
                                      "padding-top": "2%"
                                      },
                               align="center",
                               width=8,
                               className="no-scrollbars",
                               children=column_right()),
                   ],
                   no_gutters=True)

    return cont


def column_left():
    cont = [
        html.Div(style={'display': 'none'},
                 children=html.P("",
                                 id="mymail")),
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

                        ]),
                        dbc.CardFooter(dbc.Button("create account >>", id="save_email", color="success"))
                    ])

    return card


def quiz_tab(mymail):
    answered = dbrools.check_person(mymail)
    for i in dbrools.get_list():
        if f"{i['option1']}_{i['option2']}" not in answered:
            cont = [
                dbc.Row(style={"width": "100%",
                               "margin": "0",
                               "padding": "0"},
                        id="quiz_list",
                        no_gutters=False,
                        children=create_quiz(i['option1'], i['option2'], i['option1'])),
            ]

            return cont


def create_quiz(opt1, opt2, num):
    card = dbc.Card(color="secondary",
                    style={"width": "100%",
                           "padding": "0",
                           "margin": "10px",
                           "margin-bottom": "0px"
                           },
                    inverse=True,
                    children=[
                        html.Div(style={'display': 'none'},
                                 children=html.P("",
                                                 id={"type": "symbol",
                                                     "index": num}, )),
                        dbc.CardBody(dbc.Row([
                            dbc.Col(style={"textAlign": "center",
                                           "margin": "0",
                                           "padding": "0"
                                           },
                                    width=6,
                                    className="no-scrollbars",
                                    children=[dbc.Button(opt1,
                                                         id={"type": "next_btn1",
                                                             "index": num},
                                                         color="info")]),
                            dbc.Col(style={"textAlign": "center",
                                           "margin": "0",
                                           "padding": "0"
                                           },
                                    width=6,
                                    className="no-scrollbars",
                                    children=[dbc.Button(opt2,
                                                         id={"type": "next_btn2",
                                                             "index": num},
                                                         color="info")]),
                        ])),
                        dbc.CardFooter(dbc.Button("NEXT >>",
                                                  id={"type": "next_btn",
                                                      "index": num},
                                                  color="success"))
                    ])

    return card
