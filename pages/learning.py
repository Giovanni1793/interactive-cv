import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from .sidebar import sidebar
import pandas as pd
import plotly.express as px
from scipy import stats
dash.register_page(__name__)


import math

def black_scholes (cp, s, k, t, v, rf, div):
        """ Price an option using the Black-Scholes model.
        s: initial stock price
        k: strike price
        t: expiration time
        v: volatility
        rf: risk-free rate
        div: dividend
        cp: +1/-1 for call/put
        """

        d1 = (math.log(s/k)+(rf-div+0.5*math.pow(v,2))*t)/(v*math.sqrt(t))
        d2 = d1 - v*math.sqrt(t)

        optprice = (cp*s*math.exp(-div*t)*stats.norm.cdf(cp*d1)) - (cp*k*math.exp(-rf*t)*stats.norm.cdf(cp*d2))
        return optprice

def compute_ZCB(rate,funding,tenor):
    par = 1
    return par/((1+(rate+funding))**tenor)

df = pd.DataFrame()
df['tenor (years)'] = [0,0.5,1,1.5,2,3,4,5]
df['4% PV'] = df['tenor (years)'].apply(lambda x: compute_ZCB(0.04,0.002,x))
df['3% PV'] = df['tenor (years)'].apply(lambda x: compute_ZCB(0.03,0.002,x))
df['2% PV'] = df['tenor (years)'].apply(lambda x: compute_ZCB(0.02,0.002,x))
df['1% PV'] = df['tenor (years)'].apply(lambda x: compute_ZCB(0.01,0.002,x))
fig = px.line(df, x="tenor (years)", y = ['1% PV','2% PV','3% PV','4% PV'],labels={"variable": "prices",'value':'prices'}).update_traces(mode='lines+markers')

df2 = pd.DataFrame()
df2['Tenor'] = [0.5,1,1.5,2,3,4,5]
df2['Price 15 vol'] = df2['Tenor'].apply(lambda x: black_scholes(1,1,1,x,0.15,0.04,0.05))
df2['Price 20 vol'] = df2['Tenor'].apply(lambda x: black_scholes(1,1,1,x,0.20,0.04,0.05))
df2['Price 25 vol'] = df2['Tenor'].apply(lambda x: black_scholes(1,1,1,x,0.25,0.04,0.05))
df2['Price 30 vol'] = df2['Tenor'].apply(lambda x: black_scholes(1,1,1,x,0.30,0.04,0.05))
df2['Price 40 vol'] = df2['Tenor'].apply(lambda x: black_scholes(1,1,1,x,0.40,0.04,0.05))
df2['Price 50 vol'] = df2['Tenor'].apply(lambda x: black_scholes(1,1,1,x,0.50,0.04,0.05))
options = px.line(df2, x="Tenor", y = df2.columns, labels={"variable": "prices",'value':'prices'}).update_traces(mode='lines+markers')

def layout():
    return html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar()
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.H3('Learning Interactively', style={'textAlign':'center'}),
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),

            html.Div([
    html.H1('Structured Products Interactive Learning'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Capital Protected Note', value='tab-1-example-graph'),
        dcc.Tab(label='Capital Protected Note Pricer', value='tab-2-example-graph'),
    ]),
    html.Div(id='tabs-content-example-graph')
])
        ]
    )
])


@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H3('What is a Capital Protected Participation Note?'),
             dcc.Markdown(
                                    """
                                    A Capital Protected Participation Note is one of the most simple and common SP traded in marketplace. In 2022 it is back in fashion, thanks to higher interest rates all over the place.

                                    The product can be structured in different ways and has different names in relation to the
                                    optionality embedded, however the main drivers and its risk can be decomposed easily as follow:\n
                                    - Client is long a Zero-Coupon-Bond\n
                                    - Client is long option strategies (calls or put) vanila or exotic\n
                                    """
                                ), html.Hr(),
                                dcc.Markdown(
                                    """
                                    The Zero Coupon Bond:\n
                                    Capital Protected Notes are issued by banks, are funded and therefore are highly dependent on interest rates.
                                    In particular the components that enter in play when computing the fair value of the ZCB are:\n
                                    - The risk free rate\n
                                    - The issuer funding, driven also by the credit risk profile of the issuer.\n

                                    The Zero Coupon Bond Risks:\n
                                    - The ZCB is issued at discount (assuming positive rates) and is exposed to interest rates movement.\n
                                    - The ZCB has a duration comparable to the maturity of the product, the longer the maturity, the higher the price impact.\n
                                    - In an environment where rates are volatile, the investor should be mindful of the above duration sensitivity, as sometimes rates move can lead to counterintuitive price movements, if looked together with the optionality.
                        
                                    """
                                ),
                                 html.Hr(),

                                dcc.Graph( figure = fig),
                                 html.Hr(),
 
                                dcc.Markdown(
                                    """
                                    The Optionality:\n
                                    As seen above, the main driver for understanding if we can afford or not capital protection is mainly driven by the interest rates.
                                    However once we know how much we can spend, it is important to understand how we can maximise the option component according to our needs.

                                    It is not the purpose of this chapter to enter in details on all the optionality that exists and we will focus mostly on "vanilla" however the below structures
                                    deserve to be mentioned due their popularity among practitioners and we will be object of discussion in other chapters:
                                    - Shark Notes (Zero Coupon Bond + Up&Out call option w/wo rebate)
                                    - Capital Protected Digital (Zero Coupon Bond + strip of digitals)
                                    - Capital Protected Twin Win
                                    - Capita Protected Double Knock-Out
                                    - Autocallable/Issuer Callable Capital Protected Participation Note

                                    So what do we buy? We buy vanilla calls, call spreads or a put?..

                                    The optionality depends mainly on 2 main market observable drivers:
                                    - The forward of the underlier
                                    - The implied volatility of the underlier

                                    Altought option price depends also on the time to maturity and on the moneyness, the above parameters will give us a better idea how different underliers compare to each other.

                                    The forward of an underlier depends on the carry and in particular (for equities):
                                    - long rates
                                    - short dividends (descrete.. important when pricing)

                                    In general, the higher the carry, the higher the expected value of the underlier in the future, and vicevera and therefore, assuming same levels of implied volatility, 
                                    call options on lower forward underliers will be cheaper and puts will be more expensive.

                                    The higher the implied volatility the higher will be the price of the option, usually a rule of thumb use to proxy prices for
                                    at-the-money option pricng is the following formula
                                    (assuming, flat forward, no skew ecc...):

                                    0.4 x sigma x sqrt(T)

                                    Below some ATM call option quotes priced using BS model assuming 4% constat interest rates and 5% constant dividend rates to check how option prices change with respect to implied volatility.

                        
                                    """
                                ), html.Hr(),
                                dcc.Graph( figure = options),
                                 html.Hr(),

                                dcc.Markdown(
                                    """
                                    Will a cap cheap the optionality? YES BUT:\n

                                    Usually, in order to be able to afford more optionality the investor might decide to cap the exposure and decide to go for a call spread.
                                    Nothing bad with that BUT the investor should be mindful about the mark-to-market trade off of such product.

                                    Selling an option, altough OTM is in fact going to act as a delta tranquilliser. The investor should be mindful that the product will underperform the underlier
                                    should the underlier rally above the cap at maturity.
                                    
                                    In fact, due to the short call position, the product will have a cap on the delta as the spot rallies, and especially for longer dated product, the product might 
                                    start earning theta (with the short option entering moneyness) causing the option strategy to quote below intrinsic.

                                    The above recipe, mixed in together with ralling interest rates can raise questions from the investor on the product's performance.

    

                    
                                    """
                                ),

        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H3('Price your Capital Protected Participation Note'),
  
                    html.Hr(),
                    html.Div(['volatility',
                     dcc.Dropdown(
                        id='volatility',
                                 options=[0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50],
                                 value=[0.20],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),
                     html.Div(['rates',
                     dcc.Dropdown(id='rates',
                    
                     
                                 options=[0.01,0.02,0.03,0.04,0.05],
                                 value=[0.04],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),
                     html.Div(['dividend yield',
                    dcc.Dropdown(id='dividend',
                    
                                 options=[0.01,0.02,0.03,0.04,0.05],
                                 value=[0.04],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),
                     html.Div(['option type',
                    dcc.Dropdown(id='option-type',
                    
                                 options=['call','put'],
                                 value=['call'],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),

                    dcc.Graph(id = 'out')
        ])
@callback(
    Output("out", "figure"),
    Input("volatility", "value"),
    Input("rates", "value"),
    Input("dividend", "value"),
    Input("option-type", "value"),
)
def update_graph_card(vol,r,d,type):
    if len(vol) == 0 or len(r) ==0 or len(d)==0 or len(type)==0 :
        return dash.no_update
    else:
        tenors = [0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.5,3,4,5]
        zcb = []
        pr = []
        if type[0] == 'call':
            for tenor in tenors:
                pr.append(black_scholes(1,1,1,tenor,vol[0],r[0],d[0]))
                zcb.append(compute_ZCB(r[0],0.002,tenor))
        else:
            for tenor in tenors:
                pr.append(black_scholes(1,1,1,tenor,vol[0],r[0],d[0]))

        cpn = pd.DataFrame()
        cpn['tenor (years)'] = tenors
        cpn['ZCB'] = zcb
        cpn['option'] = pr
        cpn['capital protected note'] =  cpn['option'] + cpn['ZCB']

        fig = px.line(cpn, x="tenor (years)", y=cpn.columns,
                      labels={"variable": "prices",'value':'prices'}).update_traces(mode='lines+markers')
        return fig
