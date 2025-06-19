from dash import Input, Output, State, dcc
from flask_login import login_user
from utils.auth import User

def register_login_callback(app):
    @app.callback(
        Output("login-message", "children"),
        Input("login-button", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        prevent_initial_call=True
    )
    def authenticate(n_clicks, username, password):
        if username == "admin" and password == "admin":
            login_user(User("admin"))
            return dcc.Location(pathname="/", id="redirect")
        return "Usuario o contraseña incorrectos"
