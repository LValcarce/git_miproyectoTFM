from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    html.Div([
        html.Div([
            html.Img(
                src="/assets/imagen.webp",
                style={
                    "width": "200px",
                    "marginBottom": "10px",
                    "display": "block",
                    "marginLeft": "auto",
                    "marginRight": "auto"
                }
            ),
            html.H4("II Máster en Python Aplicado al Deporte", className="text-center"),
            html.H5("TFM – Luis Valcarce Vidal", className="text-center text-secondary")
        ],
        className="logo-header-box"),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Input(id="username", placeholder="Usuario", type="text", className="mb-2"),
                        dbc.Input(id="password", placeholder="Contraseña", type="password", className="mb-2"),
                        dbc.Button("Iniciar sesión", id="login-button", color="primary", className="mb-2 w-100"),
                        html.Div(id="login-message", className="text-danger text-center")
                    ]),
                    className="shadow"
                ),
                width=12, md=8, lg=6, className="mx-auto"
            )
        )
    ],
    className="login-container")
],
className="login-page-wrapper")
