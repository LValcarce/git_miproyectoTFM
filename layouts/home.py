from dash import html, dcc
from flask_login import current_user
from components.logout_button import logout_button
from components.navbar import navbar

def layout():
    if not current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="redirect-home")

    return html.Div([
        navbar,
        logout_button(),
        html.Div([
            html.Div([
                html.H1("Bienvenido a tu Centro de Datos de la Champions League ⚽️"),
                html.P("Navega por las siguientes secciones:"),
                html.Ul([
                    html.Li(dcc.Link("📊 Dashboard partidos Champions", href="/champions")),
                    html.Li(dcc.Link("👥 Plantillas de Equipos", href="/teams"))
                ], style={"listStyleType": "none", "padding": 0})
            ], className="home-card")
        ], className="home-background")
    ])
