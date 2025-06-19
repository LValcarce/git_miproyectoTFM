import pandas as pd
import requests
import plotly.express as px
from dash import html, dcc, Input, Output, State, callback, dash_table
from flask_login import current_user
import dash_bootstrap_components as dbc
import plotly.io as pio
from fpdf import FPDF
import base64
import uuid
import os

from components.navbar import navbar
from components.logout_button import logout_button

API_URL = "https://api-cafecito.onrender.com/matches/competition/europe-champions-league-2024-2025"
HEADERS = {
    "Authorization": "Bearer EAAHlp1ycWFIBOzFZASIPjVtB1n30C8jUBKHo"
}

TEMP_DIR = "assets/pdf_exports"
os.makedirs(TEMP_DIR, exist_ok=True)

def get_matches():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

def get_players(match_id):
    url = f"https://api-cafecito.onrender.com/match/players/{match_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def get_events(match_id):
    url = f"https://api-cafecito.onrender.com/match/events/{match_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None

def layout():
    if not current_user.is_authenticated:
        return dcc.Location(pathname="/login", id="redirect-champions")

    partidos_df = get_matches()
    if partidos_df.empty:
        return html.Div([navbar, logout_button(), html.H4("No se pudieron cargar datos desde la API.")])

    columnas = ["date", "home_team", "away_team", "home_score", "away_score", "match_id"]
    nombres_columnas = {
        "date": "Fecha",
        "home_team": "Local",
        "away_team": "Visitante",
        "home_score": "Goles Local",
        "away_score": "Goles Visitante",
        "match_id": "ID Partido"
    }

    df_reducido = partidos_df[columnas].rename(columns=nombres_columnas)
    df_reducido['Fecha'] = pd.to_datetime(df_reducido['Fecha'], errors='coerce')
    df_reducido = df_reducido.sort_values(by='Fecha')
    df_reducido['Fecha'] = df_reducido['Fecha'].dt.strftime('%A, %d/%m/%Y')

    return html.Div([
        navbar,
        logout_button(),
        html.H3("🌍 Partidos Champions League 24/25", className="text-center my-4 text-primary"),
        dash_table.DataTable(
            data=df_reducido.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df_reducido.columns],
            style_table={"overflowX": "auto", "marginBottom": "30px"},
            style_cell={"textAlign": "center", "padding": "10px", "fontFamily": "Arial"},
            style_header={"backgroundColor": "#003366", "color": "white", "fontWeight": "bold"},
            style_data={"backgroundColor": "#f9f9f9", "color": "#333"},
            page_size=10,
        ),
        dcc.Dropdown(
            id="match-selector",
            options=[{"label": f"{row['Fecha']}: {row['Local']} vs {row['Visitante']}", "value": row["ID Partido"]}
                     for _, row in df_reducido.iterrows()],
            placeholder="Selecciona un partido...",
            className="my-3"
        ),
        html.Div(id="players-output"),
        html.Div(id="eventos-jugador"),
        html.Div(id="download-link-container", className="text-center my-4")
    ])

@callback(
    Output("players-output", "children"),
    Input("match-selector", "value")
)
def mostrar_jugadores(match_id):
    if not match_id:
        return ""

    data = get_players(match_id)
    if not data:
        return html.Div([html.P("❌ No se pudieron obtener los jugadores.")])

    home_players = data.get("homePlayers", [])
    away_players = data.get("awayPlayers", [])

    equipo_local = data.get("homeTeamName", "Equipo Local")
    equipo_visitante = data.get("awayTeamName", "Equipo Visitante")

    for jugador in home_players:
        jugador["equipo"] = equipo_local
    for jugador in away_players:
        jugador["equipo"] = equipo_visitante

    jugadores_totales = home_players + away_players
    df = pd.DataFrame(jugadores_totales)

    columnas_mostrar = ["playerName", "jerseyNumber", "formationSlot", "matchStart", "equipo"]
    columnas_existentes = [col for col in columnas_mostrar if col in df.columns]
    df = df[columnas_existentes]
    df.columns = ["Jugador", "Dorsal", "Posición", "Titular", "Equipo"]

    jugadores_opciones = df[["Jugador", "Equipo"]].drop_duplicates()

    return html.Div([
        html.H5(f"👥 Jugadores: {equipo_local} vs {equipo_visitante}", className="text-secondary mt-4"),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df.columns],
            style_table={"overflowX": "auto", "marginBottom": "20px"},
            style_cell={"textAlign": "center", "padding": "8px", "fontFamily": "Arial"},
            style_header={"backgroundColor": "#006699", "color": "white", "fontWeight": "bold"},
            page_size=10
        ),
        dcc.Dropdown(
            id="player-selector",
            options=[{"label": f"{row['Jugador']} ({row['Equipo']})", "value": row['Jugador']}
                     for _, row in jugadores_opciones.iterrows()],
            placeholder="Selecciona un jugador...",
            className="my-3"
        )
    ])

@callback(
    Output("eventos-jugador", "children"),
    Output("download-link-container", "children"),
    Input("player-selector", "value"),
    State("match-selector", "value")
)
def mostrar_eventos(jugador_nombre, match_id):
    if not jugador_nombre or not match_id:
        return "", ""

    data = get_players(match_id)
    if not data:
        return html.Div("⚠️ Datos no disponibles."), ""

    jugadores_totales = data.get("homePlayers", []) + data.get("awayPlayers", [])
    player_id = next((j["playerId"] for j in jugadores_totales if j["playerName"] == jugador_nombre), None)
    if not player_id:
        return html.Div("Jugador no encontrado."), ""

    eventos_data = get_events(match_id)
    eventos = eventos_data.get("events", []) if eventos_data else []
    eventos_jugador = [e for e in eventos if e.get("playerId") == player_id]

    if not eventos_jugador:
        return html.Div("Este jugador no tiene eventos registrados."), ""

    df_eventos = pd.DataFrame(eventos_jugador)

    def extraer_display_name(x):
        import json
        try:
            if isinstance(x, str):
                x = json.loads(x)
            return x.get("displayName", "Desconocido") if isinstance(x, dict) else "Desconocido"
        except:
            return "Desconocido"

    df_eventos["tipo_evento"] = df_eventos["type"].apply(extraer_display_name)

    if "outcomeType" in df_eventos.columns:
        df_eventos["outcomeType"] = df_eventos["outcomeType"].apply(
            lambda x: "Éxito" if "success" in str(x).lower() else "Fallido"
        )

    resumen = df_eventos["tipo_evento"].value_counts().reset_index()
    resumen.columns = ["Tipo de Evento", "Total"]

    detalle_columnas = [col for col in ["minute", "tipo_evento", "outcomeType"] if col in df_eventos.columns]
    df_detalle = df_eventos[detalle_columnas].copy()

    fig = px.bar(resumen, x="Tipo de Evento", y="Total", color="Tipo de Evento", text="Total",
                 title=f"Eventos de {jugador_nombre}")
    
    # === Exportar PDF ===
    pdf_id = str(uuid.uuid4())
    pdf_path = f"{TEMP_DIR}/{pdf_id}.pdf"
    img_path = f"{TEMP_DIR}/{pdf_id}.png"

    fig.write_image(img_path, width=800, height=400)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Estadísticas de {jugador_nombre}", ln=True, align="C")
    pdf.image(img_path, x=10, y=30, w=180)
    pdf.ln(100)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Resumen de eventos", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, row in resumen.iterrows():
        pdf.cell(200, 8, f"{row['Tipo de Evento']}: {row['Total']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Detalle de eventos", ln=True)
    pdf.set_font("Arial", "", 10)
    for _, row in df_detalle.iterrows():
        pdf.cell(200, 8, f"Minuto {row['minute']} - {row['tipo_evento']} - {row['outcomeType']}", ln=True)

    pdf.output(pdf_path)

    download_link = html.A("📥 Descargar informe en PDF", href=f"/assets/pdf_exports/{pdf_id}.pdf", target="_blank", className="btn btn-danger")

    return html.Div([
        html.H4("📊 Resumen de eventos", className="text-success mt-4"),
        dash_table.DataTable(
            data=resumen.to_dict("records"),
            columns=[{"name": col, "id": col} for col in resumen.columns],
            style_table={"overflowX": "auto", "marginBottom": "20px"},
            style_cell={"textAlign": "center", "fontFamily": "Arial"},
            style_header={"backgroundColor": "#228B22", "color": "white", "fontWeight": "bold"},
            style_data={"backgroundColor": "#f4fff4"},
            page_size=10
        ),
        html.Br(),
        dcc.Graph(figure=fig),
        html.Br(),
        html.H4("📝 Detalle completo de eventos", className="text-info mt-4"),
        dash_table.DataTable(
            data=df_detalle.to_dict("records"),
            columns=[{"name": col, "id": col} for col in df_detalle.columns],
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center", "fontFamily": "Arial"},
            style_header={"backgroundColor": "#1E90FF", "color": "white", "fontWeight": "bold"},
            style_data={"backgroundColor": "#f0f8ff"},
            page_size=15
        )
    ]), download_link
