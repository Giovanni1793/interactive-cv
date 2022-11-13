import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from .sidebar import sidebar
#import quandl
from datetime import datetime
import copy

dash.register_page(__name__, title='Backtester Demo', order=1)

today = datetime.today()

df = pd.read_csv('assets/data.csv')
# initialize parameters
start = datetime(2015, 1, 1)

df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y'))

end = today
"""
df = quandl.get(['NYSE/AAPL','NASDAQ/MSFT'], start_date = start,
                end_date = end, 
                authtoken = 'DTgFTvhLszbZ-oWbxgtk')

"""
print(df.head())

MAPPING = {
    '3months':'3m',
    '6months':'6m',
    '1year':'1y',
    'single':'s',
    'basket':'b',
    'worst-of':'wo',
    'best-of':'bo',
    'tracker':'tracker',
    'capital protected note':'cpn',
    'ATM call':'atmc',
    'ATM Put':'atmp'
}

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
                    dcc.Markdown('This is an example of a simple demo backtester for SPs. The underliers used as example here are Apple, Microsoft and Google.\n'
                 'In this demo the user can select only product tenor, basket type and the type of structure \n'
                 'In general is possible (as an example) to extend the app via:\n' 
                 '- Giving the user the possibility to select underliers by retrieving data via a API\n'
                 '- Increasing the number of parameters in control of the user\n'
                 '- increasing the variety of payoff\n',

                 style={'textAlign': 'center', 'white-space': 'pre'}),
                 html.Div(['tenor',
                    dcc.Dropdown(id='tenor',
                                 options=['3months','6months','1year'],
                                 value=["1year"],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                                 html.Div(['basket type',
                    dcc.Dropdown(id='und_type',
                                 options=['basket','worst-of','best-of'],
                                 value=["worst-of"],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                                 html.Div(['product type',
                    dcc.Dropdown(id='product-type',
                                 options=['tracker','capital protected note','ATM call','ATM Put'],
                                 value=["tracker"],
                                 multi=True,
                                 style={'color':'black'}
                                 ),]),
                    html.Hr(),
                    dcc.Graph(id='line_chart-3', figure={}),

                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
])

@callback(
    Output("line_chart-3", "figure"),
    Input("tenor", "value"),
    Input("und_type", "value"),
    Input("product-type", "value")

)
def update_graph_card(tenor,und,product):
    if (len(tenor) == 0) or (len(und)== 0) or (len(product)==0):
        return dash.no_update
    else:
        tenor = MAPPING[tenor[0]]
        und = MAPPING[und[0]]
        product = MAPPING[product[0]]

        dataf  = copy.deepcopy(df)

        filt = und+tenor+product

        df_filtered = dataf[['Date',filt]].sort_values('Date')
        df_filtered = df_filtered.dropna()
        df_filtered[filt] = df_filtered[filt].apply(lambda x: float(x))
        print(df_filtered)
        fig = px.line(df_filtered, x="Date", y=filt,
                      labels={filt: "Backtest Redemption", 'Date':'Aquisition Date'})
        return fig
