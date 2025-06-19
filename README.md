# git_miproyectoTFM
mi pequeño trabajo de final del master de python aplicado al deporte: 

# 📊 Champions League Data Dashboard

Bienvenido a `mi_proyectoTFM`, un dashboard interactivo desarrollado con **Dash + Flask** que permite explorar datos de la UEFA Champions League 2024/25, consultar plantillas de equipos, eventos por partido y estadísticas detalladas por jugador. También incluye funcionalidades avanzadas como exportación a PDF y filtros visuales.

---

## 🧱 Estructura del Proyecto

```plaintext
mi_proyectoTFM/
│
├── app.py                        # App principal: rutas, servidor, login, layout
├── requirements.txt              # Dependencias Python del proyecto
│
├── assets/                       # Estilos personalizados y recursos gráficos
│   ├── custom.css                # Estilos visuales generales
│   ├── styles.css                # Estilos adicionales (si existen)
│   ├── copa.jpg.webp             # Fondo de pantalla para `home.py`
│   ├── FONDO1.png / imagen.webp  # Imágenes adicionales
│   └── pdf_exports/              # Carpeta donde se guardan los PDFs exportados
│
├── components/                   # Componentes reutilizables para la interfaz
│   ├── navbar.py                 # Navbar superior
│   └── logout_button.py          # Botón de logout
│
├── callbacks/                    # Callbacks del sistema de login
│   └── login_callbacks.py
│
├── layouts/                      # Páginas principales del dashboard
│   ├── home.py                   # Página de bienvenida (con fondo visual)
│   ├── login.py                  # Login de usuario
│   ├── teams.py                  # Vista de equipos, jugadores, estadísticas y exportación PDF
│   └── champions_api.py          # Vista de partidos, eventos por jugador y exportación PDF
│
├── data/                         # Datos CSV utilizados para estadísticas por jugador
│   ├── attacking_data.csv
│   ├── attempts_data.csv
│   ├── defending_data.csv
│   ├── disciplinary_data.csv
│   ├── distribution_data.csv
│   ├── goalkeeping_data.csv
│   ├── goals_data.csv
│   ├── key_stats_data.csv
│   ├── players_data.csv
│   └── teams_data.csv
│
├── utils/                        # Funciones auxiliares
│   └── auth.py                   # Configuración de Flask-Login
│
└── venv/                         # Entorno virtual de Python
├── MachineLearning_TFMA_LVV.ipynb #  Notebook con el análisis de Machine Learning completo
├── modelo_knn.pkl                 # Modelo entrenado y guardado con joblib
├── requirements.txt               # Dependencias necesarias del proyecto
---

## 🚀 Funcionalidades destacadas

- Login seguro mediante `Flask-Login`
- Visualización de:
  - Partidos de Champions vía API externa
  - Jugadores por partido y sus eventos
  - Equipos y sus plantillas completas
  - Estadísticas individuales por jugador
- Comparación de eventos de dos jugadores en un mismo partido
- Exportación a PDF personalizada desde las vistas de eventos y estadísticas
- Estilo visual adaptado con Bootstrap y CSS personalizado

---

## 📦 Instalación

1. Clona el repositorio y entra al proyecto:

```bash
git clone <url>
cd mi_proyectoTFM
```

2. Activa el entorno virtual e instala dependencias:

```bash
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

3. Ejecuta la app:

```bash
python app.py
```

---

## 🛠️ Tecnologías utilizadas

- Dash + Plotly
- Dash Bootstrap Components
- Flask (servidor y login)
- Pandas
- Requests
- fpdf (para exportación PDF)

---