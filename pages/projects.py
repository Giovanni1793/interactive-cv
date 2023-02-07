import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from .sidebar import sidebar
#import quandl
from datetime import datetime
import copy
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), "products"))
from backtest import *
from capital_protected_note import *

dash.register_page(__name__, title='Backtester Demo', order=2)


df = pd.read_csv('assets/tickers_filtered.csv')

names = df['Name'].to_list()

my_button_style = {'background-color': '#e1e1e1',
                      'color': '#323e54',
                      'height': '50px',
                      'width': '20%',
                      'textAlign':'center',
                      #'margin-top': '3%',
                      'margin-left': '40%',
                      'fontWeight': 'bold',
                      'font-family':'Arial, sans-serif',
                      'fontSize':15,
                      }


def get_yahoo_ticker(data,names):

    filtered = data[data['Name'].isin(names)].drop_duplicates('Name',keep = 'first')
    tickers = filtered['Ticker'].to_list()
    return tickers
# initialize parameters

map_capped = {'yes':True,'no':False}

"""
df = quandl.get(['NYSE/AAPL','NASDAQ/MSFT'], start_date = start,
                end_date = end,
                authtoken = 'DTgFTvhLszbZ-oWbxgtk')

"""
progress = html.Div(
                    [
                        dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
                        dbc.Progress(id="progress"),
                    ]
                )

dash.register_page(__name__)
def layout():
    return  html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.H3('Backtester DEMO', style={'textAlign':'center'}),
                    html.Hr(),
                    dcc.Markdown('This is an example of a simple demo back-tester for SPs. The data are linked to Yahoo finance API\n'
                 'In this demo the user can select only the capital protected note structure \n'
                 'In general, is possible (as an example) to extend the app via:\n'
                 '- Increasing the number of outputs\n'
                 '- Giving the user the possibility to download results in a spreadsheet or in other formats\n'
                 '- Increasing the number of parameters in control of the user\n'
                 '- increasing the variety of payoff\n',

                 style={'textAlign': 'center', 'white-space': 'pre'}),

                 html.Div([


                 html.Div(['tenor backtest (in years)',
                    dcc.Dropdown(id='backtest-tenor',
                                 options=[i for i in range(0,21)],
                                 value=[],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'33.33%'}),

                html.Div(['Underliers',
                   dcc.Dropdown(id='underlyings',
                                 options=[
                {"label": i, "value": i }
                for i in names[0:5000]
                ],

                                value=[],
                                multi=True,
                                style={'color':'black'}
                                ),],style = {'width':'33.33%'}),

                 html.Div(['product tenor (in months)',
                    dcc.Dropdown(id='product-tenor',
                                 options=[3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57,60],
                                 value=[],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'33.33%'}),

                                  ], style = {'display':'flex','width':'100%'}),

                html.Div([

                    html.Div(['basket type',
                       dcc.Dropdown(id='basket-type',
                                    options=['basket','worst-of','best-of'],
                                    value=[],
                                    multi=False,
                                    style={'color':'black'}
                                    ),],style = {'width':'25.00%'}),
                        html.Div(['product type',
                    dcc.Dropdown(id='product-type',
                                 options=['capital protected note'],
                                 value=['capital protected note'],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'25.00%'}),


                        html.Div(['strike',
                    dcc.Dropdown(id='strike',
                                 options= [i for i in range(0,151)],
                                 value=[],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'25.00%'}),
                                 html.Div(['capital protection',
                    dcc.Dropdown(id='capital-protection',
                                 options= [i for i in range(0,151)],
                                 value=[100],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'25.00%'}),
                                  ], style = {'display':'flex'}),
                        html.Div([
                                 html.Div(['leverage',
                    dcc.Dropdown(id='leverage',
                                 options= [i for i in range(0,500)],
                                 value=[],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'33.33%'}),
                    html.Div(['capped',
                    dcc.Dropdown(id='capped',
                                 options= ['yes','no'],
                                 value=[],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'33.33%'}),
                        html.Div(['cap level',
                    dcc.Dropdown(id='cap-level',
                                 options= [i for i in range(0,151)],
                                 value=[],
                                 multi=False,
                                 style={'color':'black'}
                                 ),],style = {'width':'33.33%'}),
                                  ], style = {'display':'flex'}),
                    html.Hr(),

                     html.Div([
            html.Button('launch backtest', id='backtest', n_clicks=0, style = my_button_style),]),
                    html.Hr(),


                    html.Div([
                    dcc.Graph(id='payoff', figure={}),
                    dcc.Graph(id='payoff-backtest', figure={}),
                    dcc.Graph(id='distribution', figure={}),
                    ])


                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
])







@callback(
    Output("payoff", "figure"),
    Output("payoff-backtest", "figure"),
    Output("distribution", "figure"),
    Input("backtest", "n_clicks"),
    State("backtest-tenor", "value"),
    State("underlyings", "value"),
    State("product-tenor", "value"),
    State("basket-type", "value"),
    State('strike','value'),
    State("capital-protection", "value"),
    State("leverage", "value"),
    State("capped", "value"),
    State("cap-level", "value"),

)
def filter_data(_,backtest_tenor,underlyings,product_tenor,basket_type,strike,capital_protection,leverage,capped,cap_level):
    if _ is None:
        raise PreventUpdate

    print(product_tenor)
    print(float(product_tenor))

    product = CapitalProtectedNote(

    underlyings = get_yahoo_ticker(df,underlyings),
    maturity = float(product_tenor)/12,
    currency = 'USD',
    strike = strike,
    basket_type = basket_type,
    capital_protection = capital_protection,
    leverage = leverage/100,
    capped = map_capped[capped],
    cap_level = cap_level,
    backtest_tenor = backtest_tenor
    )



    payoff_diagram  = product.payoff_diagram()[1]
    backtest_payoff  = product.backtest()[2]
    backtest_distribution  = product.backtest()[3]


    return payoff_diagram, backtest_payoff , backtest_distribution

"""
@callback(
    [Output("progress", "value"), Output("progress", "label")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""
"""
