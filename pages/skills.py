import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


dash.register_page(__name__, order=2)




it = {'IT':['Python','C++','C#','VBA','Lexifi'],'score':[6,2,3,5,6]}
language = {'languages':['English','Italian','French','German'],'score':[6,6,4,2]}
it_profile = {'it':['Front-end','Back-end','Api','Algorithms','Machine Learning'],'score':[5,4,3,4,4]}

finance = {'fields':['Derivatives','Structured Products','Stochastic Calculus','Portfolio Management','Corporate Finance','General Finance'],'score':[6,6,5,3,4,3]}



df = pd.DataFrame(it)
df1 = pd.DataFrame(it_profile)
df2 = pd.DataFrame(language)
df3 = pd.DataFrame(finance)


fig = px.line_polar(df,r="score", theta="IT",  line_close=True,
                    template="plotly_dark",)
fig1 = px.line_polar(df1,r="score", theta="it",  line_close=True,
                    template="plotly_dark",)

fig2 = px.line_polar(df2,r="score", theta="languages",  line_close=True,
                    template="plotly_dark",)

fig3 = px.line_polar(df3,r="score", theta="fields",  line_close=True,
                    template="plotly_dark",)
fig2.update_layout(paper_bgcolor = '#0F2537', plot_bgcolor='#FFFFFF')
fig3.update_layout(paper_bgcolor = '#0F2537', plot_bgcolor='#FFFFFF')
fig1.update_layout(paper_bgcolor = '#0F2537')
fig.update_layout(paper_bgcolor = '#0F2537')

def layout():
    return html.Div([
    html.H3("Skills", style={'textAlign':'center'}, className='my-3'),
    html.Hr(),
    html.Div([
        dcc.Graph(id='IT', figure= fig, style = {'width':'50%'}),
        dcc.Graph(id='IT1', figure= fig1, style = {'width':'50%'}),
        ], style = {'display':'flex'} ),
    html.Div([
        dcc.Graph(id='lg', figure= fig2, style = {'width':'50%'}),
        dcc.Graph(id='lg1', figure= fig3, style = {'width':'50%'}),
        ], style = {'display':'flex'} ),
    
    

])


