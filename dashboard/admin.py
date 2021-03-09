# -*- coding: utf-8 -*-
import json
import time

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import sys, base64, os
import dbrools
import plotly.graph_objs as go
from collections import Counter

sys.path.insert(0, r'/usr/local/WB')
main_path_data2 = os.path.expanduser('/usr/local/WB/data/')

candidat = {"Freedom": 10,
            "Mastery": 9,
            "Power": 8,
            "Goal": 7,
            "Curiosity": 6,
            "Honor": 5,
            "Acceptance": 4,
            "Relatedness": 3,
            "Order": 2,
            "Status": 1,
            }

office = {"Acceptance": 10,
          "Curiosity": 9,
          "Freedom": 8,
          "Status": 7,
          "Goal": 6,
          "Honor": 5,
          "Mastery": 4,
          "Order": 3,
          "Power": 2,
          "Relatedness": 1,
          }


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
                                      "overflowY": "scroll",
                                      "height": "100vh",
                                      "minHeight": "100vh",
                                      "maxHeight": "100vh",
                                      'align': 'center',
                                      "margin": "0",
                                      "padding": "0",
                                      "padding-top": "2%"
                                      },
                               align="center",
                               width=8,
                               id='a_graph',
                               className="no-scrollbars",
                               children=column_right()),
                   ],
                   no_gutters=True)

    return cont


def column_left():
    cont = []

    for i in dbrools.get_all_personal():
        cont.append(
            dbc.Row(style={"width": "100%",
                           "margin": "0",
                           "margin-top": "5px",
                           "padding": "0"},
                    id="person_list",
                    no_gutters=False,
                    children=dbc.Button(
                        html.H4(i, style={"margin": "0",
                                          "padding": "0",
                                          "color": "white"}),
                        outline=True,
                        id={"type": "persons",
                            "index": i},
                        color="info",
                        block=True
                    )))

    return cont


def column_right(mail="test@test.com"):
    lt = dbrools.check_person_answers(mail)
    d = Counter(lt)
    if mail == "test@test.com":
        d = candidat

    fig = go.Figure(go.Bar(
        x=[*d.values()],
        y=[*d.keys()],
        orientation='h'))
    # new_candidat = {}
    #
    # for k, v in d.items():
    #     if k != "test":
    #         new_candidat[k] = v * candidat[k]
    #
    # new_office = {}
    # for k, v in d.items():
    #     if k != "test":
    #         new_office[k] = v * office[k]
    #
    # fig = go.Figure(go.Bar(
    #     x=[*new_candidat.values()],
    #     y=[*new_candidat.keys()],
    #     orientation='h'))
    #
    # fig2 = go.Figure(go.Bar(
    #     x=[*new_office.values()],
    #     y=[*new_office.keys()],
    #     orientation='h'))

    layout = [dbc.Row(
        # style={"max-height": "45vh", "height": "45vh"},
                      children=html.Div([dcc.Graph(figure=fig, style={"margin": "0", "padding": "0"}, )])),
              # dbc.Row(
              #     # style={"max-height": "45vh", "height": "45vh"},
              #         children=html.Div([dcc.Graph(figure=fig2, style={"margin": "0", "padding": "0"}, )]))
              ]

    return layout
