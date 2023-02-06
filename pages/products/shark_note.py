import pandas as pd
import plotly.express as px
from backtest import *


def plotly_formatter(fig):
    #fig.update_traces(marker={"size": 3})
    fig.update_layout(paper_bgcolor='white')
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(title_font_color='black')
    fig.update_layout(font_color='black')
    #fig.update_yaxes(tick0=10, dtick=10.0)
    #fig.update_xaxes(tick0=10, dtick=10.0)
    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='Grey')
    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title_font_family="Arial",
        title_font_color="black",
        legend_title_font_color="black"
    )

    return fig



def is_capped(cap,cap_level):
    if cap == False:
        return 'NA'
    else:
        return str(cap_level) + ' %'


def underlyings_to_string(underlyings):
    """
    Convert the list of tickers to a string
    """

    if len(underlyings) == 1:
        underlyings_info = underlyings[0]
    else:
        underlyings_info = ""
        for index, underlying in enumerate(underlyings):
            if index != len(underlyings)-1:
                underlyings_info += underlying + ' / '
            else:
                underlyings_info += underlying

    return underlyings_info

class CapitalProtectedNote:

    def __init__(self, underlyings,
                 maturity: int,
                 currency: str,
                 basket_type: str,
                 strike: float,
                 capital_protection: float,
                leverage: float,
                 capped = False,
                 cap_level = False,
                 backtest_tenor = None ):

        CapitalProtectedNote.underlyings = underlyings
        CapitalProtectedNote.underlyings_string = underlyings_to_string(underlyings)
        CapitalProtectedNote.maturity = maturity
        CapitalProtectedNote.currency = currency
        CapitalProtectedNote.strike = strike
        CapitalProtectedNote.basket_type = basket_type
        CapitalProtectedNote.capital_protection = capital_protection
        CapitalProtectedNote.leverage = leverage
        CapitalProtectedNote.capped = capped
        CapitalProtectedNote.cap_level = cap_level
        CapitalProtectedNote.backtest_tenor = backtest_tenor

    def payoff_formula(self):

        if self.capped == False:
            return f'{self.capital_protection}% + {self.leverage}% * MAX[0,S(T)/S(0)- {self.strike}%]'
        else:
            return f'{self.capital_protection}% + {self.leverage}% * MIN[{self.cap_level -100}%,MAX[0,S(T)/S(0)- {self.strike}%]]'

    def payoff_diagram(self):
        S = [t / 5 for t in range(0, 1001)]
        if self.capped == True:
            P = list(map(lambda x: self.capital_protection + self.leverage*(min(self.cap_level -100,max(x - self.strike, 0))), S))
        else:
            P = list(map(lambda x: self.capital_protection + self.leverage * max(x - self.strike, 0), S))
        payoff = pd.DataFrame()
        payoff['Spot %'] = S
        payoff['Redemption %'] = P
        fig = px.line(payoff, x="Spot %", y="Redemption %", title='Payoff Diagram at Maturity')
        print('-------------payoff completed -----------------')
        return payoff, plotly_formatter(fig)

    def backtest(self):

        print('-------------backtest initiated -----------------')
        data = backtest_setup(self.backtest_tenor,self.underlyings,self.maturity,self.basket_type)

        #print(data)
        if self.capped == True:
            P = list(map(lambda x: self.capital_protection + self.leverage * (
                min(self.cap_level - 100, max(x, 0))), data['Performance'].to_list()))

        else:
           P =  list(map(lambda x: self.capital_protection + self.leverage * max(x, 0), data['Performance'].to_list()))

        data['Redemption %'] = P

        fig = px.line(data, x="Acquisition Date", y="Redemption %", title='Backtest')
        print('-------------backtest 1 -----------------')
        modifed_df = data.set_index('Acquisition Date')
        quantile_df = modifed_df.quantile([0.25, 0.5])
        quantile_df.index = ["First Quartile", "Median"]
        min_df = pd.DataFrame(modifed_df.min()).T
        min_df.index = ["Min"]
        avg_df = pd.DataFrame(modifed_df.mean()).T
        avg_df.index = ["Average"]
        q3_df = modifed_df.quantile([0.75])
        q3_df.index = ["Third Quartile"]
        max_df = pd.DataFrame(modifed_df.max()).T
        max_df.index = ["Max"]

        stat_df = pd.concat([min_df, quantile_df, avg_df, q3_df, max_df])

        print('-------------backtest 2 -----------------')

        fig_2 = px.histogram(
            data,
            x="Redemption %",
            barmode="overlay",
            marginal="box",
            opacity=1,
            hover_data=data.columns,
        )

        print('-------------backtest 3 -----------------')
        return data, stat_df,plotly_formatter(fig), plotly_formatter(fig_2)










    def get_info(self):
        """
        Returns a formatted info table to display on the PDF
        """

        return pd.DataFrame([

            {'field':'Underlyings','value':self.underlyings_string},
                {'field':'Maturity','value':str(self.maturity) + ' Months'},
                {'field':'Currency','value':str(self.currency)},
                {'field':'Strike','value':str(self.strike) + ' %'},
                {'field':'Basket Type','value':self.basket_type},
                {'field':'Capital Protection','value':str(self.capital_protection) + ' %'},
                {'field':'Leverage','value':str(self.leverage) + ' %'},
                {'field': 'Capped', 'value': str(self.capped)},
                {'field': 'Cap Level', 'value': is_capped(self.capped, self.cap_level)},
                {'field': 'Payoff at Maturity', 'value': self.payoff_formula()},
             ]).rename(columns = {'field':'Product Type','value':'Capital Protected Note'})
