import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from .sidebar import sidebar
import pandas as pd
import plotly.express as px
from scipy import stats
import plotly.graph_objects as go
dash.register_page(__name__)


import math

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

def plotly_formatter(fig):
    #fig.update_traces(marker={"size": 3})
    fig.update_layout(paper_bgcolor='white')
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(title_font_color='black')
    fig.update_layout(font_color='black')
    #fig.update_yaxes(tick0=10, dtick=10.0)
    #fig.update_xaxes(tick0=10, dtick=10.0)
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')
    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title_font_family="Arial",
        title_font_color="black",
        legend_title_font_color="black"
    )

    return fig

def payoff(x,k,l):
    if x>=k: 
        return 100+ l* (x-k)
    else:
        return 100+0

def payoff_straddle(x,k,l):
        return 100+ l* abs(x-k)

def barrier_up(x,b,r,k,l):
    if x >= b:
        return 100+r
    else:
        return payoff(x,100,1)
        

def double_barrier(x,b1,b2,r,k,l):
    if x >= b1:
        return 100+r
    elif x <= b2:
        return 100 + r
    else:
        return payoff_straddle(x,100,1)

plot = [i for i in range(200)]

cpn = list(map(lambda x: barrier_up(x,200,0,100,1), plot))

shark = list(map(lambda x: barrier_up(x,130,0,100,1), plot))

payoff = pd.DataFrame()
payoff['Spot (%)'] = plot
payoff['Payoff'] = shark

D = list(map(lambda x: double_barrier(x,130,70,0,100,1), plot))

payoff_2 = pd.DataFrame()
payoff_2['Spot (%)'] = plot
payoff_2['Payoff'] = D


payoff_3 = pd.DataFrame()
payoff_3['Spot (%)'] = plot
payoff_3['Payoff'] = cpn

SN = plotly_formatter(px.line(payoff, x='Spot (%)', y="Payoff"))
DKO = plotly_formatter(px.line(payoff_2, x='Spot (%)', y="Payoff"))
CPN = plotly_formatter(px.line(payoff_3, x='Spot (%)', y="Payoff"))


chapters = ['Basics - The Forward', 'Capital Protected Note', 'Shark Note', 'Double Knock-Out Note']


menu = html.Div([html.Label('Learning Menu',style={'font-weight': 'bold', "text-align": "center",'color':'white'}),
                dcc.Dropdown(
                    id= 'menu',
                    options=[{'label': i, 'value': i} for i in chapters],
                    multi=False,
                    value=['Basics - The Forward'],
                    style = {'width':'50%', 'color':'white'}),
                    ],style={'display': 'inline-block', 'width':'100%', 'color':'white'})



doublek_10v = pd.read_csv('assets/bko_eu_10rebate.csv')
doublek_5v = pd.read_csv('assets/dko_eu_0_rebate_5vol.csv')
doublek_0v = pd.read_csv('assets/dko_eu_0rebate_0vol.csv')


data = doublek_10v.merge(doublek_5v, how = 'inner', on = 'Moneyness')
data = data.merge(doublek_0v, how = 'inner', on = 'Moneyness')

data.head()


price_vol_dko = plotly_formatter(px.line(data, x = 'Moneyness',y=["Price % European Double KO",
                                                  "Price % European Double KO +5 vol",
                                                  "Price % European Double KO +10 vol"],
                        title = 'European Double KO Price by Volatility'))

delta_vol_dko = plotly_formatter(px.line(data, x = 'Moneyness',y=["Delta % European Double KO",
                                                  "Delta % European Double KO +5 vol",
                                                  "Delta % European Double KO +10 vol"],
                         title = 'European Double KO Delta by Volatility'))

vega_vol_dko = plotly_formatter(px.line(data, x = 'Moneyness',y=["Vega European Double KO",
                                                  "Vega European Double KO +5 vol",
                                                  "Vega European Double KO +10 vol"],
                         title = 'European Double KO Vega by Volatility'))

upouteu0 = pd.read_csv('assets/up_out_eu_0_rebate.csv')
upouteu5 = pd.read_csv('assets/up_out_eu_5_rebate.csv')
upoutco0 = pd.read_csv('assets/up_out_us_0_rebate.csv')
upoutco5 = pd.read_csv('assets/up_out_us_5_rebate.csv')
vanilla = pd.read_csv('assets/up_out_vanilla.csv')

price = upouteu0.merge(upouteu5, how = 'inner', on = 'Moneyness')
price = price.merge(upoutco0, how = 'inner', on = 'Moneyness')
price = price.merge(upoutco5, how = 'inner', on = 'Moneyness')
price = price.merge(vanilla, how = 'inner', on = 'Moneyness')
#data = data.merge(doublek_0v, how = 'inner', on = 'Moneyness')
#data.head()
price.head()




df_p = ['European UP&OUT Price % Rebate = 0%',
        'European UP&OUT Price % Rebate = 5%',
        'American UP&OUT Price % Rebate = 0%',
        'American UP&OUT Price % Rebate = 5%',
       ]

df_d = ['European UP&OUT Delta % Rebate = 0%',
        'European UP&OUT Delta % Rebate = 5%',
        'American UP&OUT Delta % Rebate = 0%',
        'American UP&OUT Delta % Rebate = 5%'
       ]

df_v = ['European UP&OUT Vega Rebate = 0%',
        'European UP&OUT Vega Rebate = 5%',
        'American UP&OUT Vega Rebate = 0%',
        'American UP&OUT Vega Rebate = 5%'
       ]

up_out_price = plotly_formatter(px.line(price, x = 'Moneyness', y = df_p)).update_layout(legend=dict(
    yanchor="top"))
"""
up_out_price.add_trace(
    go.Line(x=price['Moneyness'], y=price['Price % Vanilla Call'], name="Vanilla Call Price %"),
    secondary_y=True,
)
"""
up_out_delta = plotly_formatter(px.line(price, x = 'Moneyness', y = df_d))
up_out_vega = plotly_formatter(px.line(price, x = 'Moneyness', y = df_v))









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

                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    html.H3('Learning Interactively', style={'textAlign':'center'}),
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10),

            html.Div([
    html.H1('Structured Products Interactive Learning'),
    menu,

    ]),
    html.Div(id='tabs-content-example-graph')
])
        ]
    )





@callback(Output('tabs-content-example-graph', 'children'),
              Input('menu', 'value'))
def render_content(tab):
    if tab == 'Capital Protected Note':
        return html.Div([
            html.H3('What is a Capital Protected Participation Note?'),
            html.Hr(),
                                dcc.Graph( figure = plotly_formatter(CPN)),
             dcc.Markdown(
                                    """
                                    A Capital Protected Participation Note is one of the most simple and common SP traded in marketplace. In 2022 it is back in fashion, thanks to higher interest rates all over the place.

                                    The product can be structured in different ways and has different names in relation to the
                                    optionality embedded, however the main drivers and its risk can be decomposed easily as follow:\n
                                    - Client is long a Zero-Coupon-Bond\n
                                    - Client is long option strategies (calls or put) vanilla or exotic\n
                                    """
                                ), html.Hr(),
                                dcc.Markdown(
                                    """
                                    The Zero-Coupon-Bond:\n
                                    Capital Protected Notes are issued by banks, are funded and therefore are highly dependent on interest rates.
                                    In particular the components that enter in play when computing the fair value of the ZCB are:\n
                                    - The risk-free rate\n
                                    - The issuer funding, driven also by the credit risk profile of the issuer.\n

                                    The Zero-Coupon-Bond Risks:\n
                                    - The ZCB is issued at discount (assuming positive rates) and is exposed to interest rates movement.\n
                                    - The ZCB has a duration comparable to the maturity of the product, the longer the maturity, the higher the price impact.\n
                                    - In an environment where rates are volatile, the investor should be mindful of the above duration sensitivity, as sometimes rates move can lead to counterintuitive price movements, if looked together with the optionality.

                                    """
                                ),
                                 html.Hr(),

                                dcc.Graph( figure = plotly_formatter(fig)),
                                 html.Hr(),

                                dcc.Markdown(
                                    """
                                    The Optionality:\n
                                    As seen above, the main driver for understanding if we can afford or not capital protection is mainly driven by the interest rates.
                                    However, once we know how much we can spend, it is important to understand how we can maximise the option component according to our needs.

                                    It is not the purpose of this chapter to enter in detail on all the optionality that exists and we will focus mostly on "vanilla" however the below structures
                                    deserve to be mentioned due their popularity among practitioners and we will be object of discussion in other chapters:
                                    - Shark Notes (Zero Coupon Bond + Up&Out call option w/wo rebate)
                                    - Capital Protected Digital (Zero Coupon Bond + strip of digitals)
                                    - Capital Protected Twin Win (Zero Coupon Bond + straddle or strangle)
                                    - Capita Protected Double Knock-Out (Zero Coupon Bond + straddle or strangle with UP&OUT/DOWN&OUT Knock-out)
                                    - Autocallable/Issuer Callable Capital Protected Participation Note

                                    Now that we have our base, we need to decide on what to spend the rest of the money.

                                    So, what do we buy? We buy vanilla calls, call spreads or a put?..

                                    The optionality depends mainly on 2 main market observable drivers:

                                    - The forward of the underlier
                                    - The implied volatility of the underlier

                                    Although option price depends also on the time to maturity and on the moneyness, the above parameters will give us a better idea how different underliers compare to each other.

                                    The forward of an underlier depends on the carry and (for equities):
                                    - long rates
                                    - short dividends (discrete modelled.. important when pricing)

                                    In general, the higher the carry, the higher the expected value of the underlier in the future, and therefore, assuming same levels of implied volatility,
                                    call options on lower forward underliers will be cheaper and puts will be more expensive.

                                    The higher the implied volatility the higher will be the price of the option, usually a rule of thumb use to proxy prices for
             

                                    Below the reader can find some ATM call option quotes priced using BS model assuming 4% p.a. constant interest rates and 5% p.a. constant dividend yield to check how option prices change with respect to implied volatility.


                                    """
                                ,mathjax=True), html.Hr(),
                                dcc.Graph( figure = plotly_formatter(options)),
                                 html.Hr(),

                                dcc.Markdown(
                                    """
                                    Will a cap cheap the optionality? YES BUT:\n

                                    Usually, to be able to afford more optionality the investor might decide to cap the exposure and decide to go for a call spread.
                                    Nothing bad with that BUT the investor should be mindful about the mark-to-market trade off of such product.

                                    Selling an option, although OTM is in fact going to act as a delta tranquilliser. The investor should be mindful that the product will underperform the underlier
                                    should the underlier rally above the cap at maturity.

                                    In fact, due to the short call position, the product will have a cap on the delta as the spot rallies, and especially for longer dated product, the product might
                                    start earning theta (with the short option entering moneyness) causing the option strategy to quote below intrinsic.

                                    The above recipe, mixed in together with rallying interest rates can raise questions from the investor on the product's performance.




                                    """
                                ),
                            html.H3('Price your Capital Protected Participation Note'),

        ])

    elif tab == 'Basics - The Forward':
        return html.Div([
            html.H3('The Forward'),

                    html.Hr(),
                    dcc.Markdown(
                                    """
                                When talking about options or SPs you will always hear me talking about the forward of the underlier but what is the Forward?
                                Under risk neutral probability Q the expectation of the asset S can be written as below:\n
                                $$E_{Q}(S_{T}) = S_{0}e^{rT}$$
                                Forward contract: contract to buy a stock at time T at a price K and can be written as per below:\n
                                $$F(0,K,T) = e^{-rT} E(S(T) - K)$$
                                Expanding:\n
                                $$F(0,K,T) = e^{-rT} E_{Q}(S_{T}) - K e^{-rT} = S_{0} - K e^{-rT}$$ \n
                                The reader can easily proof that $$F(0,K,T) > S_{0} - K e^{-rT}$$ as well as $$F(0,K,T) < S_{0} - K e^{-rT}$$ would lead to arbitrage strategy.\n
                                The above definition of forward is however incomplete as in the market we observe assets generating income (dividends) and the possibility to place the stock in repo.
                                The forward can therefore be written in presence of dividends and repos for stocks. The non-arbitrage relation would still hold:\n
                                $$E_{Q}(S_{T}) = S_{0}e^{rT}$$ \n
                                $$E_{Q}(S_{T}) = S_{0}e^{(r -q)T}$$ \n
                                $$E_{Q}(S_{T}) = S_{0}e^{(r-q-b)T}$$ \n
                                Forwards deliver a payout linear in the future value of the underlying asset. Hence, they can be replicated statically by a simple cash & carry replication strategy.
                                But how the forward does relate to option pricing?\n
                                Let’s now summarise a bit and let’s rewrite the above as below:\n
                                $$F(0,T) = S_{0}e^{fT}$$\n
                                With $$f$$ reflecting the cost of funding the equity purchase and carrying it. If we assume proportional dividends and no jumps then the risk-neutral dynamics of an asset can be written as below:\n
                                $$dS_{t}/S_{t} = f(t)dt +\sigma(t) dW_{t}$$\n
                                Or\n
                                $$dS_{t}/S_{t} ={\partial{F(0,t)/S_{0}}\over \partial{t}}dt+\sigma(t)dW_{t}$$ \n
                                So, the investor can see how the forward curve indeed intervenes. therefore, the market forward prices could be interpreted as a way of extracting the implied funding cost and hence (partly) marking your model to the market.
                                This is independent of the volatility model used $$\sigma(t)$$ (it could be BS, Heston, Local volatility à la Dupire).
                                Mathematically, this is also understandable as follows: the forward curve characterises the first moment of $$S_{t}$$under the risk-neutral measure knowing the current information, so it will have an impact the pricing since it's part of the characterisation of the pdf of $$S_{t}$$\n
                                If you assume BS, then adding the volatility surface to the forward curve gives you the full representation of the future distributions of $$S_{t}|S_{0}$$ under the risk-neutral measure.

                                The above forward details are taken looking at Equity asset class, but the main principles are valid also for other asset classes. \n

                                During our journey on Structured Products however, we will also encounter more complex instruments that differ from being simple stock options. \n
                                Our underlier can be a specific (more complex) function of our stock, and the underlier could not be single anymore but involing multiple assets (multiassets). \n

                                For this reason it is important for the reader to conceptualise and refer, (when we talk about forward dynamics) to $$E_{Q}(X_{T})$$ with $$X_{T}$$ being anything, not necesseraly a single stock \n
                                """,mathjax=True),
                                html.H3('Check out the forward price'),

                    
            
                    html.Hr(),
                     html.Div(['interest rates',
                     dcc.Dropdown(id='rates-forward',


                                 options=[0.01,0.02,0.03,0.04,0.05],
                                 value=[0.04],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),
                     html.Div(['dividend yield',
                    dcc.Dropdown(id='dividend-forward',

                                 options=[0.01,0.02,0.03,0.04,0.05],
                                 value=[0.04],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),
                    html.Div([
                        html.Button('Price', id='click', n_clicks=0, style = my_button_style)]),
                
    

                    dcc.Graph(id = 'forw')])
                    

                    


    elif tab == 'Shark Note':
        return html.Div([
        html.H3('Shark Note'),
html.Hr(),
dcc.Graph( figure = plotly_formatter(SN)),
html.Hr(),
dcc.Markdown(
"""
In the capital protected notes chapter we introduced the simple capital protected notes in terms of Zero-Coupon Bonds dynamics and simple vanilla strategies. Let’s dive into another form of optionality, exotics. \n
Among the most famous products traded in the market in capital protected format are the so called "Shark Note", taking their name from their typical payoff diagram shaped like a shark's fin.\n
The Zero-Coupon-Bond profile is the same as "vanilla" capital protected notes, however the optionality differ as their payoff depends on a barrier levels, observable at maturity only or discretely and/or continuously over time.\n
To get to the root of why those capital protected notes are so often proposed as solutions, we should dive (not too deep) on their optionality (up-and-out calls and/or down-and-out puts) and on the risks and rewards that investors should expect when investing in such products.\n
Shark Note = ZCB + UP&OUT Call option\n
Up & Out Calls deliver the payout of a vanilla call option $$C(K,T)$$ if $$S(T) < Barrier$$ or a $$Rebate$$ otherwise (usually  = 0).\n
Up & Out Calls are cheaper than vanilla calls and therefore, are suitable for capital protected products.\n
To illustrate by example, below some UP&OUT calls priced on SPX over 2Y tenor in USD\n
The barrier is 125.00% of the initial fixing(spot).
""",mathjax=True),
 html.Hr(),
 html.Div([
dcc.Graph( figure = up_out_price, style = {'width':'100.00%'}),
dcc.Graph( figure = up_out_delta,style = {'width':'100.00%'}),
]),
dcc.Graph( figure = up_out_vega ,style = {'width':'100.00%'}),
dcc.Markdown(
"""
From the delta and vega profile of the options it appears clear that the risks are not same as a vanilla option and in particular, the investor should understand the implications to best make sense of the MtM.\n

Few points deserve attention on the behaviour of such notes: \n
- Calls with continuous KO (European also) get’s cheaper the higher the probability of $$S(T) > Barrier$$ as long as the rebate is low enough. (this depends mainly on the volatility of the underlier and on it’s forward)\n
- The more OTM the barrier the more the price approach the vanilla call \n
- The delta get's negative when the spot start moving in the client's direction \n
- The vega profile of the product is overall negative at inception.\n

The key to intuitively understanding the reason for the different behavior from vanilla options lies in the digital nature of the barrier on which the payout is conditional.\n
Though it is true that volatility increases the price of vanilla options, it is also true that OTM digital options increase in price with volatility as the probability of exercising the digit increases. \n
The higher the spot moves, and the higher the forward of the security, the more the digital option price will increase and therefore decrease the price of the up & out call \n
As a result of that, the investor should be aware of counter-intuitive MtM movements on the price of the derivative.\n

From the vega profile of the options, it is also intuitive how these options can also be seen as a bet on the realized volatility of the underlier (especially in the double knock-out).\n

In general Shark Notes (ZCB + up&out call) works best with underliers having high forward and high elevated of implied volatility.

            """,mathjax=True),
])

    elif tab == 'Double Knock-Out Note':
        return html.Div([
        html.H3('Double Knock-out Note'),
html.Hr(),
dcc.Graph( figure = plotly_formatter(DKO)),
dcc.Markdown(
"""
In the shark notes chapter we introduced the shark note capital protected in terms of Zero-Coupon Bonds dynamics and knock out optionality (up&out).\n
Let’s dive now more in general on the extension of the knock-out feature on both side (knock out straddle / knock out strangle). \n
A product that look cosmetically great to investors in bearish market regime with high interest rates is the Double Knock Out Capital Protected Note.
Their profile is similar is similar to Capital Protected Shark Notes, however the optionality differ as their payoff depends on a double KO barrier levels (usually symmetric) on both sides. The investor can also participate both on the uspide and the downside.\n
The same counter intuitive relationship on greeks such as delta/vega still holds for double KO structures, however the volaility of the underlier will play a major role in determining the product's price.\n
Double Knock Out Capital Protected Note = ZCB + Knock Out Straddle/Strangle \n
Double Knock Out options deliver the payout of a vanilla straddle option $$SD(K,T)$$ if $$S(T) < Up Barrier$$ AND $$S(T) > Down Barrier$$ a $$Rebate$$ otherwise (usually  = 0) is paid to the investor.\n
Double Knock Out options are cheaper than vanilla straddles and therefore, are suitable for capital protected products.\n
To illustrate by example, below some Double Knock Out options priced on SPX over 2Y tenor in USD\n
The barrier (European) is symmetric +-25.00% of the initial fixing(spot).
""",mathjax=True),
 html.Hr(),
 html.Div([
dcc.Graph( figure = price_vol_dko, style = {'width':'100.00%'}),
dcc.Graph( figure = delta_vol_dko,style = {'width':'100.00%'}),
]),
dcc.Graph( figure = vega_vol_dko ,style = {'width':'100.00%'}),
dcc.Markdown(
"""
\n

Few points deserve attention on the behaviour of such notes: \n
- Calls with continuous KO (European also) get’s cheaper the higher the probability of $$S(T) > UpBarrier$$ or $$S(T) < DownBarrier$$ as long as the rebate is low enough. (this depends mainly on the volatility of the underlier and on it’s forward)\n
- The more OTM the barriers the more the price approach the vanilla straddle \n
- The delta get's negative when the spot start moving in the client's direction \n
- The vega profile of the product is overall negative at inception.\n

The investor willing to invest into these structures should be mindfull about the low delta of such products as well as their implied volatility entry point. \n
The changes in implied volatility as well as interest rates drive the product a lot more compared to classical vanilla capital protected notes  \n
The key to intuitively understand what is the reason for the different behaviour from vanilla options lies on the digital nature of the barrier on which the payout is conditional.\n



            """,mathjax=True),
])
@callback(
                            Output("forw", "figure"),
                            Input("click", "n_clicks"),
                            State("rates-forward", "value"),
                            State("dividend-forward", "value"),

                        )
def filter_data(_,rate,div):
    if _ is None:
        raise PreventUpdate

    plot = [i for i in range(0,5*12)]
                          
    P = list(map(lambda x: 100 * (1+(rate[0]-div[0]))**(x/12), plot))
    payoff = pd.DataFrame()
    payoff['Tenor'] = plot
    payoff['forward'] = P
    fig = px.line(payoff, x="Tenor", y="forward")
    return fig