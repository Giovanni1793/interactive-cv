import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, order=3)

green_text = {'color':'green'}

def layout():
    return dbc.Row([
        dbc.Col([
    dcc.Markdown('# Giovanni Midolo', className='mt-3'),
    dcc.Markdown('### Personal info', style={'color':'gray'}),
    dcc.Markdown('Address', style=green_text),
    dcc.Markdown('Uster, Switzerland 8610'),
    dcc.Markdown('Phone Number', style=green_text),
    dcc.Markdown('+41 77 963 29 04'),
    dcc.Markdown('Email', style=green_text),
    dcc.Markdown('giovanni.midolo@outlook.com'),
    dcc.Markdown('Linkedin', style=green_text),
    dcc.Markdown('[Click here for Linkedin](https://ch.linkedin.com/in/giovanni-midolo-1834b8123)', link_target='_blank'),
        ], width={'size':6, 'offset':2})
], justify='center')
