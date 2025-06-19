import pandas as pd
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_login import current_user
from components.navbar import navbar
from components.logout_button import logout_button

# === Cargar datos ===
teams_df = pd.read_csv("data/teams_data.csv")
players_df = pd.read_csv("data/players_data.csv")
goals_df = pd.read_csv("data/goals_data.csv")
discipline_df = pd.read_csv("data/disciplinary_data.csv").drop(columns=["Unnamed: 0"], errors="ignore")
attacking_df = pd.read_csv("data/attacking_data.csv")
defending_df = pd.read_csv("data/defending_data.csv")
goalkeeping_df = pd.read_csv("data/goalkeeping_data.csv")
attempts_df = pd.read_csv("data/attempts_data.csv")
distribution_df = pd.read_csv("data/distribution_data.csv")
key_stats_df = pd.read_csv("data/key_stats_data.csv")[["id_player", "top_speed"]]

# === Layout de vista general de equipos ===
def layout():
    if not current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="redirect-teams")

    equipos = teams_df.sort_values("country")
    tarjetas = []

    for _, row in equipos.iterrows():
        tarjeta = dbc.Card([
            dbc.CardImg(src=row["logo"], top=True, style={"height": "100px", "object-fit": "contain", "padding": "10px"}),
            dbc.CardBody([
                html.H5(row["team"], className="card-title text-center"),
                html.P(row["country"], className="card-text text-center"),
            ]),
            dbc.CardFooter(
                dbc.Button("Ver plantilla", href=f"/teams/{row['team_id']}", color="primary", style={"width": "100%"})
            )
        ], style={"width": "12rem", "margin": "10px"})
        tarjetas.append(tarjeta)

    tarjetas_distribuidas = html.Div(
        [dbc.Row([dbc.Col(card, width=2) for card in tarjetas[i:i+6]], justify="center")
         for i in range(0, len(tarjetas), 6)]
    )

    return html.Div([
        navbar,
        logout_button(),
        html.H3("🌍 Equipos Champions League 24/25", className="text-center mb-4"),
        tarjetas_distribuidas
    ])

# === Vista individual de plantilla ===
def plantilla_equipo(team_id):
    if not current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="redirect-team")

    jugadores = players_df[players_df["id_team"] == team_id]
    if jugadores.empty:
        return html.Div([
            navbar,
            logout_button(),
            html.H4("🚫 No se encontró la plantilla del equipo.", className="text-center")
        ])

    nombre_equipo = teams_df.loc[teams_df["team_id"] == team_id, "team"].values[0]

    tarjetas_jugadores = []
    for _, row in jugadores.iterrows():
        tarjeta = dbc.Card([
            dbc.CardImg(src=row["player_image"], top=True, style={"height": "220px", "objectFit": "cover"}),
            dbc.CardBody([
                html.H5(row["player_name"], className="card-title text-center", style={"fontSize": "16px"}),
                html.P(f"🌍 {row['nationality']}", className="card-text text-center text-muted"),
                html.P(f"🧭 {row['field_position']}", className="card-text text-center text-muted"),
                html.P(f"🎂 {row['age']} años", className="card-text text-center text-muted"),
                dbc.Button("Estadísticas", href=f"/teams/{team_id}/{row['id_player']}", color="info", size="sm", className="d-block mx-auto")
            ])
        ], style={"width": "200px", "margin": "10px"})
        tarjetas_jugadores.append(tarjeta)

    tarjetas_distribuidas = html.Div(
        [dbc.Row([dbc.Col(card, width="auto") for card in tarjetas_jugadores[i:i+4]], justify="center")
         for i in range(0, len(tarjetas_jugadores), 4)]
    )

    return html.Div([
        navbar,
        logout_button(),
        html.Div([
            dbc.Button("⬅ Volver", href="/teams", color="secondary", className="mb-3"),
            html.H3(f"🧾 Plantilla de {nombre_equipo}", className="text-center my-4")
        ], style={"paddingLeft": "2rem", "paddingTop": "1rem"}),
        tarjetas_distribuidas
    ])

# === Vista individual de jugador ===
def vista_estadisticas_jugador(team_id, player_id):
    if not current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="redirect-player")

    jugador = players_df[players_df["id_player"] == player_id]
    if jugador.empty:
        return html.Div("🚫 Jugador no encontrado.")

    nombre = jugador["player_name"].values[0]
    posicion = jugador["field_position"].values[0]
    foto = jugador["player_image"].values[0]

    datasets = [
        ("🟦 Goles", goals_df, "blue"),
        ("🔴 Disciplina", discipline_df, "red"),
        ("🟢 Ataque", attacking_df, "teal"),
        ("🟠 Defensa", defending_df, "orange"),
        ("🟣 Remates", attempts_df, "purple"),
        ("🟩 Distribución", distribution_df, "green"),
        ("⚫ Velocidad máxima", key_stats_df, "black")
    ]

    if posicion.lower() == "goalkeeper":
        datasets.append(("🟤 Portería", goalkeeping_df, "brown"))

    merged = jugador
    for _, df, _ in datasets:
        merged = pd.merge(merged, df, on="id_player", how="left")

    stats_rows = []
    for titulo, df, color in datasets:
        columnas = list(df.columns)
        columnas.remove("id_player")
        bloque = merged[columnas].T.reset_index()
        bloque.columns = ["Estadística", "Valor"]

        if titulo.endswith("Goles"):
            bloque = pd.concat([
                bloque[bloque["Estadística"] == "goals"],
                bloque[bloque["Estadística"] != "goals"]
            ])
            goles = bloque[bloque["Estadística"] == "goals"]["Valor"].values[0]
            if pd.isna(goles) or goles == 0:
                bloque = bloque[~bloque["Estadística"].isin([
                    "inside_area", "outside_area", "right_foot", "left_foot", "head", "other", "penalties_scored"
                ])]

        stats_rows.append(html.H4(titulo, style={
            "color": color,
            "marginTop": "2rem",
            "fontWeight": "bold",
            "borderBottom": f"2px solid {color}",
            "paddingBottom": "4px"
        }))
        stats_rows.append(dbc.Table.from_dataframe(
            bloque, striped=True, bordered=True, hover=True,
            style={"textAlign": "center", "fontSize": "14px"}
        ))

    return html.Div([
        navbar,
        logout_button(),
        html.Div([
            dbc.Button("⬅ Volver a plantilla", href=f"/teams/{team_id}", color="secondary", className="mb-3"),
            html.H3(f"📊 Estadísticas de {nombre}", className="text-center my-4"),
            html.Div(
                html.Img(src=foto, style={"height": "250px", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0,0,0,0.2)"}),
                className="text-center my-3"
            ),
            html.Hr(),
            html.Div(stats_rows, style={"padding": "2rem"})
        ])
    ])

# === Función principal de navegación ===
def mostrar_equipo_o_plantilla(pathname):
    if not pathname.startswith("/teams/"):
        return layout()

    partes = pathname.strip("/").split("/")
    if len(partes) == 2:
        try:
            team_id = int(partes[1])
            return plantilla_equipo(team_id)
        except:
            return layout()
    elif len(partes) == 3:
        try:
            team_id = int(partes[1])
            player_id = int(partes[2])
            return vista_estadisticas_jugador(team_id, player_id)
        except:
            return layout()
    else:
        return layout()