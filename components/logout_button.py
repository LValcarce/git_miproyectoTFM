from dash import html

def logout_button():
    return html.Div(
        html.A("Cerrar sesión 🔒", href="/logout", className="btn btn-danger"),
        style={"textAlign": "right", "margin": "10px"}
    )
