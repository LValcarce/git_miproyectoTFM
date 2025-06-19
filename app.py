import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from flask import Flask
from flask_login import current_user
from flask_caching import Cache

from utils.auth import configure_login, add_logout_route
from layouts.login import layout as login_layout
from layouts.champions_api import layout as champions_layout
from layouts.home import layout as home_layout
from layouts.teams import layout as teams_layout, mostrar_equipo_o_plantilla  # ✅ Nuevo: layout de plantillas
from callbacks.login_callbacks import register_login_callback

import layouts.champions_api  # ← Ejecuta los callbacks de champions
import layouts.teams          # ← Ejecuta los callbacks de teams
import warnings
warnings.filterwarnings("ignore", module="urllib3")

# === Servidor Flask + Dash ===
server = Flask(__name__)
server.secret_key = "clave_supersecreta"

# === Configurar cache ===
cache = Cache(server, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
})

app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# === Agregar objeto cache al objeto app para uso global ===
app.server.cache = cache

# === Configuración del login ===
configure_login(server)
add_logout_route(server)

# === Registrar callbacks ===
register_login_callback(app)

# === Layout principal ===
app.layout = html.Div([
    dcc.Location(id='url'),
    html.Div(id='page-content')
])

# === Rutas (navegación básica) ===
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def mostrar_pagina(pathname):
    if pathname == "/login":
        return login_layout
    elif pathname == "/logout":
        return html.Div()
    elif not current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="forzar-login")
    elif pathname.startswith("/teams"):
        return mostrar_equipo_o_plantilla(pathname)
    elif pathname == "/champions":
        return champions_layout()
    elif pathname == "/":
        return home_layout()
    else:
        return html.H1("Página no encontrada", className="text-danger text-center mt-5")
# === Ejecutar ===
if __name__ == "__main__":
    app.run(debug=True)