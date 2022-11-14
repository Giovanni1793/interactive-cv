import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', order=0)

# resume sample template from https://zety.com/
layout = html.Div([
    dcc.Markdown('# Giovanni Midolo', style={'textAlign':'center'}),
    dcc.Markdown('Uster, 8610 Switzerland', style={'textAlign': 'center'}),

    dcc.Markdown('### Professional Summary', style={'textAlign': 'center'}),
    html.Hr(),
    dcc.Markdown('Cross Asset Structurer with focus on Structured Products and Derivatives. \n'
                 'Hands on experience in structuring, dealing, software engineering, pricing, and automatization of processes. \n'
                 'Strategic thinker, able to synergically integrate technical skills and a business-oriented  approach.',
                 style={'textAlign': 'center', 'white-space': 'pre'}),

    

    dcc.Markdown('### Work History', style={'textAlign': 'center'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Sept-2019 to current', style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Financial Engineering - Cross Asset Structuring \n'
                         'Anova Partners AG - Zurich, Switzerland',
                         style={'white-space': 'pre'},
                         className='ms-3'),
            html.Ul([
                
                html.Li('Responsible for the execution and pricing of flow and non-flow structured products for primary and secondary market transactions.'),
                html.Li('Responsible for managing the relationships within the issuers company portfolio on a day-to-day basis.'),
                html.Li('Managing the structured products book of the company on a day-to-day basis (pricings, life-cycle management, booking, quality checks)'),
                html.Li('Supporting the head of financial engineering on the idea generation of trading ideas among different asset classes using structured products'),
                html.Li('Developed various web applications and in-house tools for various purposes (Automatic checks, documentation, marketing templating, pricing infrastructure)'),
                html.Li('Developed various quantitative tools for studies, back-testing, optimization as well as integrations with pricing engine.')
            ])
        ], width=5)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Oct 2018 to Sept 2019',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Sales and Structuring Team Assistant \n'
                         'TFS Structured Products - London, United Kingdom',
                         style={'white-space': 'pre'},
                         className='ms-3'),
            html.Ul([
                html.Li(
                    'Developed good practical knowledge for implementation of structured products in a portfolio contest (risk diversification, hedging)'),
                html.Li(
                    'Priced products and executed back-tests for various products and strategies on cross asset payoffs using Lexifi and Excel'),
                html.Li(
                    'Responsible for post trade-monitoring and settlement as well as drafting of documentation'),
                html.Li(
                    'Responsible for drafting of marketing materials, termsheets, as well as brochures')
            ])
        ], width=5)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('Dec 2017 to May 2018',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Product Management SPs (Intern) \n'
                         'Deutsche Bank - Luxembourg, Luxembourg',
                         style={'white-space': 'pre'},
                         className='ms-3'),
            html.Ul([
                html.Li(
                    'Assisted in primary market transactions, communication and booking process of the trades)'),
                html.Li(
                    'Built relationships both internally and externally for solving operational issues at different levels of the value chain'),
                html.Li(
                    'Contributed on the communication for the onboarding of issuers for MiFID II communication, policies & distribution agreements'),
                html.Li(
                    'Responsible for drafting of marketing materials')
            ])
        ], width=5)
    ], justify='center'),

    dcc.Markdown('### Education', style={'textAlign': 'center'}),
    html.Hr(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('2018',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Master of Science: Business Administration\n'
                         'Grenoble École de Management - Grenoble France/London United Kingdom',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5)
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('2016',
                         style={'textAlign': 'center'})
        ], width=2),
        dbc.Col([
            dcc.Markdown('Bachelor of Arts: Business Administration\n'
                         'Università degli Studi di Catania - Catania, Italy',
                         style={'white-space': 'pre'},
                         className='ms-3'),
        ], width=5)
    ], justify='center'),

    dcc.Markdown('### Interests', style={'textAlign': 'center'}),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
            * Chess
            * Running
            * Basketball
            ''')
        ], width={"size": 3, "offset": 1}),
        dbc.Col([
            dcc.Markdown('''
            * Gaming
            * Philosophy
            * Software Design
            ''')
        ], width=3)
    ], justify='center'),
])

