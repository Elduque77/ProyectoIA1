import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="LaLiga & Fantasy Dashboard",
    page_icon="⚽",
    layout="wide"
)

# Título Principal
st.title("⚽ LaLiga & Fantasy Football Dashboard")
st.markdown("Visualiza la clasificación, analiza datos de los equipos y consulta los mejores consejos para tu plantilla **Fantasy**.")

# ---------------------------------------------------------
# DATOS SIMULADOS / API DE LALIGA
# ---------------------------------------------------------
@st.cache_data
def cargar_datos_laliga():
    # Datos de ejemplo estructurados de la clasificación
    data = {
        "Posición": list(range(1, 11)),
        "Equipo": [
            "FC Barcelona", "Real Madrid", "Atlético de Madrid", "Athletic Club",
            "Villarreal", "Real Betis", "Real Sociedad", "Girona FC", "Celta de Vigo", "Sevilla FC"
        ],
        "PJ": [28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
        "PG": [21, 20, 17, 15, 14, 12, 11, 10, 9, 8],
        "PE": [3, 4, 6, 7, 6, 8, 8, 7, 7, 8],
        "PP": [4, 4, 5, 6, 8, 8, 9, 11, 12, 12],
        "GF": [72, 65, 48, 42, 49, 38, 32, 35, 34, 30],
        "GC": [28, 25, 20, 26, 38, 32, 29, 39, 41, 38],
        "Puntos": [66, 64, 57, 52, 48, 44, 41, 37, 34, 32]
    }
    df = pd.DataFrame(data)
    df["DG"] = df["GF"] - df["GC"] # Diferencia de Goles
    return df

@st.cache_data
def cargar_consejos_fantasy():
    data = {
        "Jugador": ["Lamine Yamal", "Kylian Mbappé", "Julian Alvarez", "Oihan Sancet", "Joan García"],
        "Equipo": ["FC Barcelona", "Real Madrid", "Atlético de Madrid", "Athletic Club", "RCD Espanyol"],
        "Posición": ["Delantero", "Delantero", "Delantero", "Centrocampista", "Portero"],
        "Precio (M€)": [18.5, 21.0, 14.2, 8.5, 4.8],
        "Puntos Promedio": [8.2, 7.9, 6.8, 6.1, 5.4],
        "Estado / Recomendación": ["🔥 Capitán Fijo", "🎯 Compra Recomendada", "📈 En Racha", "💡 Chollo / Calidad-Precio", "🛡️ Portero Recomendado"]
    }
    return pd.DataFrame(data)

df_liga = cargar_datos_laliga()
df_fantasy = cargar_consejos_fantasy()

# ---------------------------------------------------------
# BARRA LATERAL (FILTROS)
# ---------------------------------------------------------
st.sidebar.header("⚙️ Filtros del Dashboard")
equipo_seleccionado = st.sidebar.selectbox(
    "Selecciona un equipo:",
    options=["Todos"] + list(df_liga["Equipo"].unique())
)

# ---------------------------------------------------------
# PESTAÑAS PRINCIPALES
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📊 Tabla de Clasificación", "🧙 Consejos Fantasy"])

# PESTAÑA 1: CLASIFICACIÓN
with tab1:
    st.subheader("Tabla de Posiciones de LaLiga")
    
    # Filtrar si se selecciona un equipo
    if equipo_seleccionado != "Todos":
        df_mostrar = df_liga[df_liga["Equipo"] == equipo_seleccionado]
    else:
        df_mostrar = df_liga

    # Métricas clave arriba
    col1, col2, col3, col4 = st.columns(4)
    lider = df_liga.iloc[0]["Equipo"]
    puntos_lider = df_liga.iloc[0]["Puntos"]
    max_goleador_eq = df_liga.loc[df_liga['GF'].idxmax()]["Equipo"]
    
    col1.metric("Líder Actual", lider)
    col2.metric("Puntos del Líder", f"{puntos_lider} pts")
    col3.metric("Equipo Más Goleador", max_goleador_eq)
    col4.metric("Partidos Jugados", "28")

    st.markdown("---")
    
    # Mostrar la tabla formateada
    st.dataframe(
        df_mostrar,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Posición": st.column_config.NumberColumn("Pos", format="%d"),
            "Puntos": st.column_config.NumberColumn("PTS", format="%d"),
            "DG": st.column_config.NumberColumn("DG", format="%+d")
        }
    )

# PESTAÑA 2: CONSEJOS FANTASY
with tab2:
    st.subheader("💡 Consejos y Jugadores Recomendados para LaLiga Fantasy")
    
    pos_filtro = st.multiselect(
        "Filtrar por Posición Fantasy:",
        options=list(df_fantasy["Posición"].unique()),
        default=list(df_fantasy["Posición"].unique())
    )
    
    df_fantasy_filtrado = df_fantasy[df_fantasy["Posición"].isin(pos_filtro)]

    st.dataframe(
        df_fantasy_filtrado,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("📌 Tips Rápidos de la Jornada")
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Estrategia de Alineación:** Revisa la rotación de los equipos con partidos europeos entre semana antes de definir tu 11.")
    with col_b:
        st.warning("**Chollo de la Semana:** Mantén ojo en los porteros de equipos revelación que reciben muchos tiros pero encajan poco.")
