import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    brand=" UEFA CHAMPIONS LEAGUE 2024/2025 ⚽️",
    brand_href="/",
    color="primary",
    dark=True,
    children=[
        dbc.NavItem(dbc.NavLink("🏠 Home", href="/")),
        dbc.NavItem(dbc.NavLink("📊 Champions API", href="/champions")),
        dbc.NavItem(dbc.NavLink("👥 Equipos", href="/teams")),
        dbc.NavItem(dbc.NavLink("🔓 Logout", href="/logout", external_link=True)),
    ],
    className="mb-4"
)