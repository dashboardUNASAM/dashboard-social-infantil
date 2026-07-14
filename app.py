# app.py - Dashboard Social Infantil
# Universidad Nacional "Santiago Antúnez de Mayolo"

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from conexion import execute_query
import traceback

# ============================================
# CONFIGURACIÓN
# ============================================

st.set_page_config(
    page_title="Dashboard Social Infantil",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ESTILOS - SIDEBAR OSCURO CON SELECTORES OSCUROS FORZADOS
# ============================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    /* SIDEBAR - OSCURO */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e17 0%, #141a24 50%, #1a202a 100%) !important;
        padding-top: 5px !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
        border-right: 1px solid rgba(255,255,255,0.03) !important;
    }
    [data-testid="stSidebar"] * { color: #e8edf5 !important; }
    
    [data-testid="stSidebar"] .element-container { margin-bottom: 2px !important; }
    [data-testid="stSidebar"] .stMarkdown { margin-bottom: 2px !important; }
    [data-testid="stSidebar"] hr { margin: 6px 0 !important; }
    
    /* ENCABEZADO DEL SIDEBAR */
    .sidebar-header {
        background: linear-gradient(135deg, rgba(46, 134, 193, 0.12) 0%, rgba(46, 134, 193, 0.03) 100%);
        border-radius: 12px;
        padding: 14px 16px;
        margin-bottom: 10px;
        border: 1px solid rgba(46, 134, 193, 0.08);
        display: flex;
        align-items: center;
        gap: 14px;
    }
    
    .sidebar-header .icon-container {
        width: 44px;
        height: 44px;
        background: linear-gradient(135deg, #2e86c1, #1a5276);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(46, 134, 193, 0.2);
    }
    
    .sidebar-header .text-container h3 {
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.3px;
    }
    
    .sidebar-header .text-container p {
        font-size: 10px !important;
        color: rgba(255,255,255,0.35) !important;
        margin: 2px 0 0 0 !important;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    .sidebar-header .text-container p span {
        color: rgba(46, 134, 193, 0.6) !important;
    }
    
    /* SELECTORES - FONDO OSCURO FORZADO */
    [data-testid="stSidebar"] .stSelectbox label {
        color: rgba(255,255,255,0.5) !important;
        font-weight: 500 !important;
        font-size: 11px !important;
        margin-bottom: 3px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: #1a1f2a !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 6px !important;
        min-height: 36px !important;
        transition: all 0.2s !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]:hover {
        border-color: rgba(46, 134, 193, 0.4) !important;
        background: #222833 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]:focus-within {
        border-color: rgba(46, 134, 193, 0.5) !important;
        box-shadow: 0 0 0 2px rgba(46, 134, 193, 0.15) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
        background: transparent !important;
        padding: 2px 8px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="button"] {
        color: #ffffff !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="button"] > span {
        color: #ffffff !important;
        opacity: 1 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] input {
        color: #ffffff !important;
        font-size: 13px !important;
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox svg {
        fill: rgba(255,255,255,0.5) !important;
        width: 16px !important;
        height: 16px !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] {
        background: #1a1f2a !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 6px !important;
        padding: 4px !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.5) !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"] {
        color: rgba(255,255,255,0.7) !important;
        padding: 6px 12px !important;
        border-radius: 4px !important;
        font-size: 13px !important;
        margin: 1px 0 !important;
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"]:hover {
        background: rgba(46, 134, 193, 0.2) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"][aria-selected="true"] {
        background: rgba(46, 134, 193, 0.25) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* RADIO BUTTONS */
    [data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        padding: 0 !important;
        gap: 2px !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        padding: 7px 12px !important;
        border-radius: 6px !important;
        color: rgba(255,255,255,0.5) !important;
        font-weight: 400 !important;
        font-size: 13px !important;
        min-height: 32px !important;
        transition: all 0.2s !important;
        border-left: 3px solid transparent !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.04) !important;
        color: rgba(255,255,255,0.8) !important;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-selected="true"] {
        background: rgba(46, 134, 193, 0.12) !important;
        color: #ffffff !important;
        border-left: 3px solid #2e86c1 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.05) !important;
        color: rgba(255,255,255,0.6) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 6px !important;
        padding: 6px 14px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background: rgba(46, 134, 193, 0.12) !important;
        color: #ffffff !important;
        border-color: rgba(46, 134, 193, 0.2) !important;
    }
    
    [data-testid="stSidebar"] .stMetric {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 6px !important;
        padding: 6px 10px !important;
        margin: 2px 0 !important;
    }
    [data-testid="stSidebar"] .stMetric label {
        color: rgba(255,255,255,0.35) !important;
        font-size: 10px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    [data-testid="stSidebar"] .stMetric div {
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }
    
    .sidebar-label {
        font-size: 9px !important;
        font-weight: 600 !important;
        color: rgba(255,255,255,0.20) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin: 4px 0 2px 0 !important;
    }
    
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .metric-box {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid #e8edf4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .metric-box:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    .metric-box .label {
        font-size: 11px;
        color: #7a8ba3;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    
    .metric-box .value {
        font-size: 28px;
        font-weight: 800;
        color: #0f1a2e;
        margin-top: 4px;
        letter-spacing: -0.5px;
    }
    
    .metric-box .sub {
        font-size: 12px;
        color: #7a8ba3;
        margin-top: 2px;
        font-weight: 500;
    }
    
    .main-title {
        padding: 10px 0 14px 0;
        border-bottom: 3px solid #2e86c1;
        margin-bottom: 20px;
    }
    
    .main-title h1 {
        font-size: 26px;
        font-weight: 800;
        color: #0f1a2e;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-title p {
        color: #7a8ba3;
        font-size: 14px;
        margin: 4px 0 0 0;
        font-weight: 400;
    }
    
    .section-title {
        border-left: 4px solid #2e86c1;
        padding-left: 14px;
        margin: 28px 0 16px 0;
    }
    
    .section-title h2 {
        font-size: 20px;
        font-weight: 700;
        color: #0f1a2e;
        margin: 0;
    }
    
    .section-title p {
        font-size: 13px;
        color: #7a8ba3;
        margin: 2px 0 0 0;
    }
    
    .metric-console {
        background: linear-gradient(135deg, #0f1a2e 0%, #1a2d4a 100%);
        border-radius: 12px;
        padding: 16px 20px;
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        height: 100%;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-console:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    }
    
    .metric-console .value {
        font-size: 28px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    .metric-console .label {
        font-size: 11px;
        color: rgba(255,255,255,0.4);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
        font-weight: 500;
    }
    
    .metric-console .sub {
        font-size: 12px;
        color: rgba(255,255,255,0.25);
        margin-top: 2px;
    }
    
    .metric-console .highlight-green { color: #2ecc71 !important; }
    .metric-console .highlight-blue { color: #2e86c1 !important; }
    .metric-console .highlight-orange { color: #f39c12 !important; }
    .metric-console .highlight-red { color: #e74c3c !important; }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCIONES DE FILTROS
# ============================================

@st.cache_data(ttl=3600)
def obtener_provincias():
    df = execute_query("""
        SELECT DISTINCT id_provincia, nombre_provincia 
        FROM PROVINCIA 
        ORDER BY nombre_provincia
    """)
    return [{'id': 0, 'nombre': 'Todas'}] + [
        {'id': row['id_provincia'], 'nombre': row['nombre_provincia']} 
        for _, row in df.iterrows()
    ] if not df.empty else [{'id': 0, 'nombre': 'Todas'}]

@st.cache_data(ttl=3600)
def obtener_distritos(provincia_id=None):
    if provincia_id and provincia_id != 0:
        df = execute_query(f"""
            SELECT DISTINCT id_distrito, nombre_distrito 
            FROM DISTRITO 
            WHERE id_provincia = {provincia_id}
            ORDER BY nombre_distrito
        """)
    else:
        df = execute_query("""
            SELECT DISTINCT id_distrito, nombre_distrito 
            FROM DISTRITO 
            ORDER BY nombre_distrito
        """)
    
    return [{'id': 0, 'nombre': 'Todos'}] + [
        {'id': row['id_distrito'], 'nombre': row['nombre_distrito']} 
        for _, row in df.iterrows()
    ] if not df.empty else [{'id': 0, 'nombre': 'Todos'}]

@st.cache_data(ttl=3600)
def obtener_centros_poblados(distrito_id=None):
    if distrito_id and distrito_id != 0:
        df = execute_query(f"""
            SELECT DISTINCT id_centro_poblado, nombre_centro_poblado 
            FROM CENTRO_POBLADO 
            WHERE id_distrito = {distrito_id}
            ORDER BY nombre_centro_poblado
        """)
    else:
        df = execute_query("""
            SELECT DISTINCT id_centro_poblado, nombre_centro_poblado 
            FROM CENTRO_POBLADO 
            ORDER BY nombre_centro_poblado
        """)
    
    return [{'id': 0, 'nombre': 'Todos'}] + [
        {'id': row['id_centro_poblado'], 'nombre': row['nombre_centro_poblado']} 
        for _, row in df.iterrows()
    ] if not df.empty else [{'id': 0, 'nombre': 'Todos'}]

def get_filter_conditions(provincia_id, distrito_id, centro_id):
    conditions = ["dep.nombre_departamento = 'ANCASH'"]
    
    if provincia_id and provincia_id != 0:
        conditions.append(f"prov.id_provincia = {provincia_id}")
    
    if distrito_id and distrito_id != 0:
        conditions.append(f"dist.id_distrito = {distrito_id}")
    
    if centro_id and centro_id != 0:
        conditions.append(f"cp.id_centro_poblado = {centro_id}")
    
    return " AND ".join(conditions)

def get_filter_label(provincia_nombre, distrito_nombre, centro_nombre):
    parts = []
    if provincia_nombre and provincia_nombre != 'Todas':
        parts.append(provincia_nombre)
    if distrito_nombre and distrito_nombre != 'Todos':
        parts.append(distrito_nombre)
    if centro_nombre and centro_nombre != 'Todos':
        parts.append(centro_nombre)
    
    if parts:
        return " · " + " > ".join(parts)
    return " · Todos los registros"

def metric_card(titulo, valor, subtitulo=None):
    html = f"""
    <div class="metric-box">
        <div class="label">{titulo}</div>
        <div class="value">{valor}</div>
        {f'<div class="sub">{subtitulo}</div>' if subtitulo else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def crear_metric_console(valor, titulo, subtitulo=None, color=None):
    color_class = ""
    if color == "green":
        color_class = "highlight-green"
    elif color == "blue":
        color_class = "highlight-blue"
    elif color == "orange":
        color_class = "highlight-orange"
    elif color == "red":
        color_class = "highlight-red"
    
    html = f"""
    <div class="metric-console">
        <div class="value {color_class}">{valor}</div>
        <div class="label">{titulo}</div>
        {f'<div class="sub">{subtitulo}</div>' if subtitulo else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# ============================================
# FUNCIONES DE FILTROS Y CACHE - OPTIMIZADAS
# ============================================

@st.cache_data(ttl=3600)
def obtener_datos_analisis_socioeconomico(provincia_id, distrito_id, centro_id):
    """Obtiene todos los datos necesarios para el análisis socioeconómico en una sola consulta"""
    where = get_filter_conditions(provincia_id, distrito_id, centro_id)
    
    query = f"""
    SELECT 
        p.id_persona,
        p.sexo,
        p.edad_anios,
        f.ingreso_familiar,
        f.nro_hijos,
        f.indice_pobreza,
        CASE 
            WHEN ps.nombre_programa IS NOT NULL THEN 'Sí'
            ELSE 'No'
        END AS tiene_programa,
        CASE 
            WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
            ELSE ps.nombre_programa
        END AS programa_social,
        prov.nombre_provincia,
        dist.nombre_distrito
    FROM PERSONA p
    INNER JOIN FAMILIA f ON p.id_familia = f.id_familia
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
    INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
    INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
    LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
    LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
    WHERE {where}
    """
    
    df = execute_query(query)
    return df

# ============================================
# GRÁFICAS ESTILO CONSOLA
# ============================================

def crear_grafico_tendencia_ingreso(df):
    if df.empty:
        return None
    
    df_prov = df.groupby('nombre_provincia').agg({
        'ingreso_familiar': ['mean', 'min', 'max'],
        'id_persona': 'count'
    }).reset_index()
    df_prov.columns = ['nombre_provincia', 'ingreso_promedio', 'ingreso_minimo', 'ingreso_maximo', 'total_personas']
    df_prov = df_prov.sort_values('ingreso_promedio', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_prov['nombre_provincia'],
        y=df_prov['ingreso_promedio'],
        mode='lines+markers+text',
        name='Ingreso Promedio',
        line=dict(color='#2e86c1', width=3, shape='spline'),
        marker=dict(size=12, color='#2e86c1', symbol='circle', line=dict(width=2, color='white')),
        text=df_prov['ingreso_promedio'].apply(lambda x: f'S/.{x:,.0f}'),
        textposition='top center',
        textfont=dict(size=10, color='#2e86c1', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Ingreso Promedio: S/.%{y:,.0f}<br>Personas: %{customdata:,.0f}<extra></extra>',
        customdata=df_prov['total_personas']
    ))
    
    fig.add_trace(go.Scatter(
        x=df_prov['nombre_provincia'],
        y=df_prov['ingreso_promedio'],
        fill='tozeroy',
        line=dict(color='rgba(46, 134, 193, 0)'),
        fillcolor='rgba(46, 134, 193, 0.15)',
        name='Tendencia'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_prov['nombre_provincia'],
        y=df_prov['ingreso_minimo'],
        mode='lines',
        name='Mínimo',
        line=dict(color='#e74c3c', width=1.5, dash='dash'),
        opacity=0.6
    ))
    
    fig.add_trace(go.Scatter(
        x=df_prov['nombre_provincia'],
        y=df_prov['ingreso_maximo'],
        mode='lines',
        name='Máximo',
        line=dict(color='#2ecc71', width=1.5, dash='dash'),
        opacity=0.6
    ))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='#0f1a2e',
        paper_bgcolor='#0f1a2e',
        height=400,
        title=dict(
            text='📈 Ingreso Promedio por Provincia',
            font=dict(size=16, weight=700, color='#ffffff', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, color='#ffffff', family='Inter'),
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        margin=dict(t=80, b=50, l=50, r=30),
        xaxis=dict(
            tickfont=dict(size=11, color='rgba(255,255,255,0.6)', family='Inter'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            tickangle=45
        ),
        yaxis=dict(
            tickfont=dict(size=11, color='rgba(255,255,255,0.6)', family='Inter'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Ingreso (S/)', font=dict(size=13, weight=600, color='rgba(255,255,255,0.5)'))
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='#1a2d4a', bordercolor='rgba(255,255,255,0.1)')
    )
    
    return fig

def crear_grafico_tendencia_pobreza(df):
    if df.empty:
        return None
    
    df_dist = df.groupby('nombre_distrito').agg({
        'indice_pobreza': 'mean',
        'id_persona': 'count'
    }).reset_index()
    df_dist.columns = ['nombre_distrito', 'indice_pobreza', 'total_personas']
    df_dist = df_dist.sort_values('indice_pobreza', ascending=False)
    
    if len(df_dist) > 20:
        df_dist = df_dist.head(20)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_dist['nombre_distrito'],
        y=df_dist['indice_pobreza'],
        mode='lines+markers+text',
        name='Índice de Pobreza',
        line=dict(color='#e74c3c', width=3, shape='spline'),
        marker=dict(size=12, color='#e74c3c', symbol='diamond', line=dict(width=2, color='white')),
        text=df_dist['indice_pobreza'].apply(lambda x: f'{x:.1f}%'),
        textposition='top center',
        textfont=dict(size=10, color='#e74c3c', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Pobreza: %{y:.1f}%<br>Personas: %{customdata:,.0f}<extra></extra>',
        customdata=df_dist['total_personas']
    ))
    
    fig.add_trace(go.Scatter(
        x=df_dist['nombre_distrito'],
        y=df_dist['indice_pobreza'],
        fill='tozeroy',
        line=dict(color='rgba(231, 76, 60, 0)'),
        fillcolor='rgba(231, 76, 60, 0.15)',
        name='Tendencia'
    ))
    
    fig.add_hline(
        y=45,
        line_dash="dash",
        line_color="#f39c12",
        opacity=0.6,
        annotation_text="Umbral Pobreza Alta (45%)",
        annotation_font=dict(size=10, color='rgba(255,255,255,0.4)')
    )
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='#0f1a2e',
        paper_bgcolor='#0f1a2e',
        height=400,
        title=dict(
            text='📉 Índice de Pobreza por Distrito (Top 20)',
            font=dict(size=16, weight=700, color='#ffffff', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, color='#ffffff', family='Inter'),
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1
        ),
        margin=dict(t=80, b=50, l=50, r=30),
        xaxis=dict(
            tickfont=dict(size=10, color='rgba(255,255,255,0.6)', family='Inter'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            tickangle=45
        ),
        yaxis=dict(
            tickfont=dict(size=11, color='rgba(255,255,255,0.6)', family='Inter'),
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Índice de Pobreza (%)', font=dict(size=13, weight=600, color='rgba(255,255,255,0.5)')),
            range=[0, 70]
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='#1a2d4a', bordercolor='rgba(255,255,255,0.1)')
    )
    
    return fig

def crear_grafico_barras_hijos(df):
    if df.empty:
        return None
    
    df_hijos = df.groupby('nro_hijos').size().reset_index(name='cantidad')
    df_hijos['categoria'] = df_hijos['nro_hijos'].apply(
        lambda x: '0-1 hijos' if x <= 1 else ('2-3 hijos' if x <= 3 else '4+ hijos')
    )
    df_hijos = df_hijos.groupby('categoria')['cantidad'].sum().reset_index()
    
    colors = ['#2e86c1', '#f39c12', '#e74c3c']
    
    fig = go.Figure()
    
    for i, row in df_hijos.iterrows():
        fig.add_trace(go.Bar(
            x=[row['categoria']],
            y=[row['cantidad']],
            marker=dict(color=colors[i % len(colors)], line=dict(width=2, color='white')),
            text=[f"{row['cantidad']:,}"],
            textposition='outside',
            textfont=dict(size=14, weight='bold', color='#ffffff'),
            hovertemplate=f'<b>{row["categoria"]}</b><br>Hogares: {row["cantidad"]:,}<extra></extra>',
            width=0.5
        ))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='#0f1a2e',
        paper_bgcolor='#0f1a2e',
        height=400,
        title=dict(
            text='📊 Distribución de Hogares por Número de Hijos',
            font=dict(size=18, weight=700, color='#ffffff', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=80, b=50, l=60, r=60),
        xaxis=dict(
            tickfont=dict(size=13, color='rgba(255,255,255,0.8)', family='Inter', weight='bold'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=False,
            title=dict(text='Número de Hijos', font=dict(size=14, weight=600, color='rgba(255,255,255,0.5)'))
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='rgba(255,255,255,0.6)', family='Inter'),
            gridcolor='rgba(255,255,255,0.08)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Número de Hogares', font=dict(size=14, weight=600, color='rgba(255,255,255,0.5)'))
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='#1a2d4a', bordercolor='rgba(255,255,255,0.1)'),
        bargap=0.4,
        showlegend=False
    )
    
    return fig

def crear_grafico_correlacion_variables(df):
    if df.empty:
        return None
    
    # Convertir tiene_programa a numérico
    df['tiene_programa_num'] = df['tiene_programa'].map({'No': 0, 'Sí': 1})
    
    # Calcular correlaciones (Coeficiente de Pearson)
    corr_ingreso = df['ingreso_familiar'].corr(df['tiene_programa_num'])
    corr_hijos = df['nro_hijos'].corr(df['tiene_programa_num'])
    corr_pobreza = df['indice_pobreza'].corr(df['tiene_programa_num'])
    
    df_corr = pd.DataFrame({
        'Variable': ['Ingreso Familiar', 'Número de Hijos', 'Índice de Pobreza'],
        'Correlación': [corr_ingreso, corr_hijos, corr_pobreza],
        'Interpretación': [
            'Inversa' if corr_ingreso < 0 else 'Directa',
            'Inversa' if corr_hijos < 0 else 'Directa',
            'Inversa' if corr_pobreza < 0 else 'Directa'
        ],
        'Fuerza': [
            'Fuerte' if abs(corr_ingreso) > 0.5 else 'Moderada' if abs(corr_ingreso) > 0.3 else 'Débil',
            'Fuerte' if abs(corr_hijos) > 0.5 else 'Moderada' if abs(corr_hijos) > 0.3 else 'Débil',
            'Fuerte' if abs(corr_pobreza) > 0.5 else 'Moderada' if abs(corr_pobreza) > 0.3 else 'Débil'
        ]
    })
    
    colors = ['#2ecc71' if x > 0 else '#e74c3c' if x < 0 else '#95a5a6' for x in df_corr['Correlación']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_corr['Variable'],
        y=df_corr['Correlación'],
        marker=dict(color=colors, line=dict(width=2, color='white')),
        text=df_corr['Correlación'].apply(lambda x: f'{x:.3f}'),
        textposition='outside',
        textfont=dict(size=14, weight='bold', color='#ffffff'),
        hovertemplate='<b>%{x}</b><br>Correlación: %{y:.3f}<br>Fuerza: %{customdata[0]}<br>Dirección: %{customdata[1]}<extra></extra>',
        customdata=df_corr[['Fuerza', 'Interpretación']].values,
        width=0.5
    ))
    
    fig.add_hline(y=0, line_dash="solid", line_color="rgba(255,255,255,0.3)", opacity=0.5)
    fig.add_hline(y=0.3, line_dash="dash", line_color="rgba(46, 204, 113, 0.2)", 
                  annotation_text="Moderada (0.3)", annotation_font=dict(size=10, color='rgba(255,255,255,0.2)'))
    fig.add_hline(y=-0.3, line_dash="dash", line_color="rgba(231, 76, 60, 0.2)",
                  annotation_text="Moderada (-0.3)", annotation_font=dict(size=10, color='rgba(255,255,255,0.2)'))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='#0f1a2e',
        paper_bgcolor='#0f1a2e',
        height=450,
        title=dict(
            text='🔗 Correlación con Acceso a Programas Sociales (Coeficiente de Pearson)',
            font=dict(size=18, weight=700, color='#ffffff', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=80, b=50, l=60, r=60),
        xaxis=dict(
            tickfont=dict(size=13, color='rgba(255,255,255,0.8)', family='Inter', weight='bold'),
            gridcolor='rgba(255,255,255,0.05)',
            showgrid=False,
            title=dict(text='Variables Independientes', font=dict(size=14, weight=600, color='rgba(255,255,255,0.5)'))
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='rgba(255,255,255,0.6)', family='Inter'),
            gridcolor='rgba(255,255,255,0.08)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Coeficiente de Correlación', font=dict(size=14, weight=600, color='rgba(255,255,255,0.5)')),
            range=[-1, 1]
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='#1a2d4a', bordercolor='rgba(255,255,255,0.1)'),
        bargap=0.4,
        showlegend=False
    )
    
    return fig

def crear_mapa_pobreza_profesional(df):
    """
    Crea un mapa profesional de Yungay mostrando el nivel de pobreza por centro poblado.
    Distribuye los centros poblados en espiral alrededor del centro de cada distrito.
    """
    if df.empty:
        return None

    df_clean = df.dropna(subset=['indice_pobreza', 'nombre_distrito'])
    if df_clean.empty:
        st.warning("⚠️ No hay datos válidos de pobreza para generar el mapa")
        return None

    try:
        import folium
        from folium.plugins import Fullscreen, MarkerCluster
        import numpy as np
        import pandas as pd
    except ImportError as e:
        st.warning(f"⚠️ Error importando librerías: {e}. Asegúrate de tener instalado: pip install folium streamlit-folium numpy")
        return None

    # ==========================================
    # COORDENADAS BASE POR DISTRITO (centro aproximado)
    # ==========================================
    coords_distritos = {
        'YUNGAY': [-9.1383, -77.7433],
        'CASCAPARA': [-9.2050, -77.7550],
        'MANCOS': [-9.1883, -77.7217],
        'MATACOTO': [-9.1717, -77.7383],
        'QUILLO': [-9.1217, -77.7717],
        'RANRAHIRCA': [-9.1550, -77.7050],
        'SHUPLUY': [-9.1883, -77.7383],
        'YANAMA': [-9.1717, -77.7550],
    }

    # ==========================================
    # CONSULTA CENTROS POBLADOS
    # ==========================================
    query_centros = """
    SELECT 
        cp.id_centro_poblado,
        cp.nombre_centro_poblado,
        cp.cod_cp,
        d.nombre_distrito,
        prov.nombre_provincia
    FROM CENTRO_POBLADO cp
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    INNER JOIN PROVINCIA prov ON d.id_provincia = prov.id_provincia
    WHERE prov.nombre_provincia = 'YUNGAY'
    ORDER BY d.nombre_distrito, cp.nombre_centro_poblado
    """
    df_centros = execute_query(query_centros)

    if df_centros.empty:
        st.warning("⚠️ No se encontraron centros poblados para Yungay")
        return None

    # ==========================================
    # CONSULTA DATOS DE POBREZA POR CENTRO
    # ==========================================
    query_pobreza = """
    SELECT 
        cp.nombre_centro_poblado,
        d.nombre_distrito,
        ROUND(AVG(f.indice_pobreza), 2) AS pobreza_promedio,
        COUNT(DISTINCT p.id_persona) AS total_personas,
        ROUND(AVG(f.ingreso_familiar), 0) AS ingreso_promedio,
        ROUND(AVG(f.nro_hijos), 1) AS hijos_promedio
    FROM PERSONA p
    INNER JOIN FAMILIA f ON p.id_familia = f.id_familia
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    INNER JOIN PROVINCIA prov ON d.id_provincia = prov.id_provincia
    WHERE prov.nombre_provincia = 'YUNGAY'
    GROUP BY cp.nombre_centro_poblado, d.nombre_distrito
    """
    df_pobreza = execute_query(query_pobreza)

    # Diccionario rápido de pobreza
    dict_pobreza = {}
    if not df_pobreza.empty:
        for _, row in df_pobreza.iterrows():
            dict_pobreza[row['nombre_centro_poblado']] = {
                'pobreza': float(row['pobreza_promedio']) if row['pobreza_promedio'] is not None else 0,
                'personas': int(row['total_personas']) if row['total_personas'] is not None else 0,
                'ingreso': float(row['ingreso_promedio']) if row['ingreso_promedio'] is not None else 0,
                'hijos': float(row['hijos_promedio']) if row['hijos_promedio'] is not None else 0,
                'distrito': row['nombre_distrito']
            }

    # ==========================================
    # GENERAR COORDENADAS EN ESPIRAL
    # ==========================================
    coords_centros = {}
    np.random.seed(42)  # Para reproducibilidad

    for distrito, (base_lat, base_lon) in coords_distritos.items():
        centros_distrito = df_centros[df_centros['nombre_distrito'] == distrito]
        if centros_distrito.empty:
            continue

        n = len(centros_distrito)
        # Radio máximo de dispersión
        max_radius = 0.025  # Aprox 2.5 km
        step = max_radius / max(1, n / 4)

        for i, (_, row) in enumerate(centros_distrito.iterrows()):
            centro = row['nombre_centro_poblado']
            # Fórmula de espiral: ángulo aumenta, radio aumenta progresivamente
            angle = i * 1.5  # Ángulo en radianes
            radius = step * (i + 1) * 0.6
            # Limitar radio máximo para que no se desparramen demasiado
            radius = min(radius, max_radius)

            lat_offset = radius * np.sin(angle)
            lon_offset = radius * np.cos(angle)

            coords_centros[centro] = [
                base_lat + lat_offset,
                base_lon + lon_offset
            ]

    # ==========================================
    # CREAR MAPA
    # ==========================================
    m = folium.Map(
        location=[-9.15, -77.74],
        zoom_start=12,
        tiles='CartoDB positron',
        control_scale=True,
        zoom_control=True,
        prefer_canvas=True,
        min_zoom=10,
        max_zoom=15
    )
    Fullscreen(position='topleft').add_to(m)
    marker_cluster = MarkerCluster().add_to(m)

    # ==========================================
    # AGREGAR MARCADORES
    # ==========================================
    max_personas = max([d.get('personas', 0) for d in dict_pobreza.values()], default=1)

    for _, row in df_centros.iterrows():
        centro = row['nombre_centro_poblado']
        distrito = row['nombre_distrito']

        coords = coords_centros.get(centro)
        if coords is None:
            continue

        lat, lon = coords

        # Obtener datos de pobreza
        if centro in dict_pobreza:
            datos = dict_pobreza[centro]
            pobreza = datos['pobreza']
            personas = datos['personas']
            ingreso = datos['ingreso']
            hijos = datos['hijos']
        else:
            # Usar promedio del distrito si no tiene datos individuales
            pobreza = df_clean[df_clean['nombre_distrito'] == distrito]['indice_pobreza'].mean()
            pobreza = float(pobreza) if not pd.isna(pobreza) else 40.0
            personas = 0
            ingreso = 0
            hijos = 0

        # Determinar color y nivel
        if pobreza < 30:
            color, fill_color, nivel, icono = '#2ecc71', '#2ecc71', 'Bajo', '🟢'
        elif pobreza < 45:
            color, fill_color, nivel, icono = '#f1c40f', '#f1c40f', 'Medio', '🟡'
        elif pobreza < 55:
            color, fill_color, nivel, icono = '#e67e22', '#e67e22', 'Medio-Alto', '🟠'
        else:
            color, fill_color, nivel, icono = '#e74c3c', '#e74c3c', 'Alto', '🔴'

        # Tamaño del círculo según población
        radius = 4 + (personas / max_personas) * 14 if max_personas > 0 and personas > 0 else 5
        radius = min(radius, 18)

        # ---- TOOLTIP (hover) ----
        tooltip_text = f"""
        <div style="font-family: 'Inter', sans-serif; padding: 6px 8px; min-width: 180px;">
            <b style="font-size: 14px; color: #1a2d4a;">{centro}</b><br>
            <span style="font-size: 11px; color: #7a8ba3;">{distrito}</span>
            <hr style="margin: 4px 0; border-color: #eef2f7;">
            <span style="font-size: 12px;">📊 Pobreza: <b>{pobreza:.1f}%</b></span><br>
            <span style="font-size: 12px;">🏷️ Nivel: <b>{nivel}</b></span>
            {f'<span style="font-size: 12px;">👨‍👩‍👦 Personas: <b>{personas:,}</b></span>' if personas > 0 else '<span style="font-size: 11px; color: #95a5a6;">Sin datos</span>'}
        </div>
        """

        # ---- POPUP (click) ----
        popup_html = f"""
        <div style="font-family: 'Inter', sans-serif; padding: 14px 18px; min-width: 260px; background: #ffffff; border-radius: 12px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                <span style="font-size: 32px;">{icono}</span>
                <div>
                    <h4 style="margin: 0; color: #1a2d4a; font-size: 17px; font-weight: 700;">{centro}</h4>
                    <span style="font-size: 12px; color: #7a8ba3;">{distrito} · Yungay</span>
                </div>
            </div>
            <div style="border-bottom: 2px solid #f0f4f8; margin: 8px 0 10px 0;"></div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px 16px; font-size: 13px;">
                <div style="color: #7a8ba3;">📊 Pobreza</div>
                <div style="font-weight: 700; color: {fill_color};">{pobreza:.1f}%</div>
                <div style="color: #7a8ba3;">🏷️ Nivel</div>
                <div style="font-weight: 600; color: #1a2d4a;">{nivel}</div>
                {f'<div style="color: #7a8ba3;">👨‍👩‍👦 Personas</div><div style="font-weight: 600; color: #1a2d4a;">{personas:,}</div>' if personas > 0 else ''}
                {f'<div style="color: #7a8ba3;">💰 Ingreso Prom.</div><div style="font-weight: 600; color: #1a2d4a;">S/. {ingreso:,.0f}</div>' if ingreso > 0 else ''}
                {f'<div style="color: #7a8ba3;">👶 Hijos Prom.</div><div style="font-weight: 600; color: #1a2d4a;">{hijos:.1f}</div>' if hijos > 0 else ''}
            </div>
            <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #f0f4f8; font-size: 10px; color: #b0bfd0; text-align: center;">
                🖱️ Click para cerrar
            </div>
        </div>
        """

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=380),
            tooltip=folium.Tooltip(tooltip_text, sticky=True),
            color='#ffffff',
            weight=2.5,
            fill=True,
            fill_color=fill_color,
            fill_opacity=0.85,
            opacity=0.95,
            shadow=True,
            shadow_size=4
        ).add_to(marker_cluster)

    # ==========================================
    # CÍRCULOS DE DISTRITO (fondo)
    # ==========================================
    for distrito, (lat, lon) in coords_distritos.items():
        folium.Circle(
            location=[lat, lon],
            radius=1500,
            color='#2e86c1',
            fill=True,
            fill_color='#2e86c1',
            fill_opacity=0.08,
            weight=2,
            opacity=0.4,
            popup=f"<b>{distrito}</b>"
        ).add_to(m)

    # ==========================================
    # LEYENDA MEJORADA
    # ==========================================
    legend_html = """
    <div style="
        position: fixed; 
        top: 80px; 
        right: 15px; 
        background: rgba(255, 255, 255, 0.95);
        border-radius: 14px;
        padding: 12px 16px;
        border: 1px solid #e8edf4;
        font-family: 'Inter', -apple-system, sans-serif;
        z-index: 1000;
        color: #1a2d4a;
        box-shadow: 0 8px 32px rgba(0,0,0,0.10);
        min-width: 130px;
        backdrop-filter: blur(8px);
    ">
        <div style="text-align: center; margin-bottom: 6px;">
            <span style="font-size: 11px; font-weight: 700; color: #1a2d4a;">📊 Nivel de Pobreza</span>
            <div style="height: 2px; background: linear-gradient(90deg, #2ecc71, #f1c40f, #e67e22, #e74c3c); margin: 3px 0; border-radius: 4px;"></div>
        </div>
        <div style="display: flex; align-items: center; gap: 5px; margin: 2px 0; padding: 2px 4px; border-radius: 4px; background: #f0faf0;">
            <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #2ecc71; border: 1px solid white;"></span>
            <span style="font-size: 10px; font-weight: 500;">Bajo</span>
            <span style="font-size: 8px; color: #7a8ba3; margin-left: auto;">&lt; 30%</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px; margin: 2px 0; padding: 2px 4px; border-radius: 4px; background: #fef9e7;">
            <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #f1c40f; border: 1px solid white;"></span>
            <span style="font-size: 10px; font-weight: 500;">Medio</span>
            <span style="font-size: 8px; color: #7a8ba3; margin-left: auto;">30-45%</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px; margin: 2px 0; padding: 2px 4px; border-radius: 4px; background: #fef5e7;">
            <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #e67e22; border: 1px solid white;"></span>
            <span style="font-size: 10px; font-weight: 500;">Medio-Alto</span>
            <span style="font-size: 8px; color: #7a8ba3; margin-left: auto;">45-55%</span>
        </div>
        <div style="display: flex; align-items: center; gap: 5px; margin: 2px 0; padding: 2px 4px; border-radius: 4px; background: #fdedec;">
            <span style="display: inline-block; width: 9px; height: 9px; border-radius: 50%; background: #e74c3c; border: 1px solid white;"></span>
            <span style="font-size: 10px; font-weight: 500;">Alto</span>
            <span style="font-size: 8px; color: #7a8ba3; margin-left: auto;">> 55%</span>
        </div>
        <div style="border-top: 1px solid #eef2f7; margin-top: 4px; padding-top: 4px; text-align: center;">
            <span style="font-size: 7px; color: #b0bfd0;">🖱️ Hover para info | ⛶ Pantalla completa</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # ==========================================
    # TÍTULO
    # ==========================================
    title_html = f"""
    <div style="
        position: fixed; 
        top: 15px; 
        left: 50%; 
        transform: translateX(-50%);
        background: rgba(255,255,255,0.92);
        border-radius: 12px;
        padding: 5px 18px;
        border: 1px solid #e8edf4;
        font-family: 'Inter', -apple-system, sans-serif;
        z-index: 1000;
        color: #1a2d4a;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        backdrop-filter: blur(8px);
    ">
        <span style="font-size: 13px; font-weight: 700;">🗺️ Pobreza por Centro Poblado</span>
        <span style="font-size: 10px; color: #7a8ba3; margin-left: 6px;">Yungay · 2025</span>
        <span style="display: inline-block; margin-left: 6px; padding: 1px 8px; background: #2e86c1; color: white; border-radius: 12px; font-size: 8px; font-weight: 600;">{len(df_centros)} centros</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    return m

# ============================================
# GRÁFICAS MEJORADAS (EXISTENTES)
# ============================================

def crear_grafico_barras_profesional(df, x, y, color, titulo, etiqueta_x=None, etiqueta_y=None, colores=None):
    if df.empty or df[y].sum() == 0:
        return None
    
    color_seq = colores or ['#2e86c1', '#f39c12', '#95a5a6', '#27ae60', '#e74c3c']
    
    fig = px.bar(df, x=x, y=y, color=color, title=titulo,
                 labels={x: etiqueta_x or x, y: etiqueta_y or y, color: ''},
                 barmode='group', text_auto=True,
                 color_discrete_sequence=color_seq)
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=420,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Inter'),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e8edf4',
            borderwidth=1
        ),
        title=dict(
            text=titulo,
            font=dict(size=18, weight=700, color='#0f1a2e', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=80, b=50, l=50, r=30),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.04)',
            tickfont=dict(size=12, family='Inter'),
            title_font=dict(size=13, weight=600, color='#0f1a2e'),
            showgrid=True,
            gridwidth=0.5
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.04)',
            tickfont=dict(size=12, family='Inter'),
            title_font=dict(size=13, weight=600, color='#0f1a2e'),
            showgrid=True,
            gridwidth=0.5
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='white', bordercolor='#e8edf4'),
        bargap=0.15,
        bargroupgap=0.1
    )
    
    fig.update_traces(
        marker_line_width=1,
        marker_line_color='white',
        textfont=dict(size=11, weight=600, family='Inter'),
        hovertemplate='<b>%{x}</b><br>%{y:,.0f} personas<extra></extra>',
        opacity=0.9
    )
    
    return fig

def crear_grafico_pastel_profesional(df, nombres, valores, titulo, colores=None):
    if df.empty or df[valores].sum() == 0:
        return None
    
    color_seq = colores or ['#2e86c1', '#f39c12', '#95a5a6', '#27ae60', '#e74c3c']
    
    fig = go.Figure(data=[go.Pie(
        labels=df[nombres],
        values=df[valores],
        hole=0.42,
        textposition='outside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} personas (%{percent})<extra></extra>',
        marker=dict(
            colors=color_seq[:len(df)],
            line=dict(color='white', width=2)
        ),
        showlegend=True,
        textfont=dict(size=12, family='Inter', color='#0f1a2e'),
        insidetextorientation='horizontal'
    )])
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=420,
        title=dict(
            text=titulo,
            font=dict(size=18, weight=700, color='#0f1a2e', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.12,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Inter'),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e8edf4',
            borderwidth=1
        ),
        margin=dict(t=70, b=70, l=20, r=20)
    )
    
    return fig

# ============================================
# TABLAS MEJORADAS
# ============================================

def crear_tabla_profesional(df, titulo=None):
    if titulo:
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <span style="font-weight: 600; color: #0f1a2e; font-size: 15px;">{titulo}</span>
        </div>
        """, unsafe_allow_html=True)
    
    styled_df = df.style.set_properties(**{
        'background-color': 'white',
        'border-color': '#e8edf4',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '8px 14px',
        'font-family': 'Inter, sans-serif',
        'font-size': '13px',
        'color': '#1a2d4a'
    }).set_table_styles([
        {'selector': 'thead th', 'props': [
            ('background-color', '#0f1a2e'),
            ('color', 'white'),
            ('font-weight', '600'),
            ('font-size', '12px'),
            ('text-transform', 'uppercase'),
            ('letter-spacing', '0.5px'),
            ('padding', '10px 14px'),
            ('font-family', 'Inter, sans-serif'),
            ('border', 'none')
        ]},
        {'selector': 'tbody tr', 'props': [
            ('transition', 'background-color 0.2s ease')
        ]},
        {'selector': 'tbody tr:hover', 'props': [
            ('background-color', '#f0f4f8')
        ]},
        {'selector': 'tbody td', 'props': [
            ('padding', '8px 14px'),
            ('font-size', '13px'),
            ('font-family', 'Inter, sans-serif'),
            ('border-bottom', '1px solid #f0f2f5')
        ]},
        {'selector': 'table', 'props': [
            ('border-collapse', 'collapse'),
            ('width', '100%'),
            ('border-radius', '10px'),
            ('overflow', 'hidden'),
            ('box-shadow', '0 2px 8px rgba(0,0,0,0.04)')
        ]}
    ])
    
    st.markdown(styled_df.to_html(escape=False), unsafe_allow_html=True)

def mensaje_seccion(titulo, descripcion=None):
    st.markdown(f"""
    <div class="section-title">
        <h2>{titulo}</h2>
        {f'<p>{descripcion}</p>' if descripcion else ''}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# INICIALIZAR SESSION STATE
# ============================================

if 'filtro_provincia_id' not in st.session_state:
    st.session_state.filtro_provincia_id = 0
    st.session_state.filtro_provincia_nombre = 'Todas'
if 'filtro_distrito_id' not in st.session_state:
    st.session_state.filtro_distrito_id = 0
    st.session_state.filtro_distrito_nombre = 'Todos'
if 'filtro_centro_id' not in st.session_state:
    st.session_state.filtro_centro_id = 0
    st.session_state.filtro_centro_nombre = 'Todos'

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="icon-container">🏛️</div>
        <div class="text-container">
            <h3>UNASAM</h3>
            <p>Facultad de Ciencias · <span>Estadística e Informática</span></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        df_total = execute_query("SELECT COUNT(*) as total FROM PERSONA")
        total = df_total['total'].iloc[0] if not df_total.empty else 0
        st.metric("Total Menores", f"{total:,}")
    except:
        pass
    
    st.markdown("---")
    st.markdown('<p class="sidebar-label">Navegación</p>', unsafe_allow_html=True)
    
    seccion = st.radio("", [
        "Inicio",
        "Caracterización",
        "Programas Sociales",
        "Ingreso Familiar",
        "Número de Hijos",
        "Índice de Pobreza",
        "Análisis por Distrito",
        "📊 Análisis Socioeconómico"
    ], index=0, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown('<p class="sidebar-label">Filtros Geográficos</p>', unsafe_allow_html=True)
    
    provincias = obtener_provincias()
    prov_nombres = [p['nombre'] for p in provincias]
    
    prov_idx = 0
    for i, p in enumerate(provincias):
        if p['id'] == st.session_state.filtro_provincia_id:
            prov_idx = i
            break
    
    prov_sel = st.selectbox("Provincia", prov_nombres, index=prov_idx, key="prov_selector")
    
    for p in provincias:
        if p['nombre'] == prov_sel:
            if p['id'] != st.session_state.filtro_provincia_id:
                st.session_state.filtro_provincia_id = p['id']
                st.session_state.filtro_provincia_nombre = p['nombre']
                st.session_state.filtro_distrito_id = 0
                st.session_state.filtro_distrito_nombre = 'Todos'
                st.session_state.filtro_centro_id = 0
                st.session_state.filtro_centro_nombre = 'Todos'
            break
    
    distritos = obtener_distritos(st.session_state.filtro_provincia_id)
    dist_nombres = [d['nombre'] for d in distritos]
    
    dist_idx = 0
    for i, d in enumerate(distritos):
        if d['id'] == st.session_state.filtro_distrito_id:
            dist_idx = i
            break
    
    dist_sel = st.selectbox("Distrito", dist_nombres, index=dist_idx, key="dist_selector")
    
    for d in distritos:
        if d['nombre'] == dist_sel:
            if d['id'] != st.session_state.filtro_distrito_id:
                st.session_state.filtro_distrito_id = d['id']
                st.session_state.filtro_distrito_nombre = d['nombre']
                st.session_state.filtro_centro_id = 0
                st.session_state.filtro_centro_nombre = 'Todos'
            break
    
    centros = obtener_centros_poblados(st.session_state.filtro_distrito_id)
    cent_nombres = [c['nombre'] for c in centros]
    
    cent_idx = 0
    for i, c in enumerate(centros):
        if c['id'] == st.session_state.filtro_centro_id:
            cent_idx = i
            break
    
    cent_sel = st.selectbox("Centro Poblado", cent_nombres, index=cent_idx, key="cent_selector")
    
    for c in centros:
        if c['nombre'] == cent_sel:
            st.session_state.filtro_centro_id = c['id']
            st.session_state.filtro_centro_nombre = c['nombre']
            break
    
    st.markdown("---")
    
    if st.button("🔍 Diagnosticar Datos"):
        try:
            df_check = execute_query("""
                SELECT 
                    prov.nombre_provincia,
                    COUNT(DISTINCT p.id_persona) as total
                FROM PERSONA p
                INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
                INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
                INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
                GROUP BY prov.nombre_provincia
                ORDER BY total DESC
            """)
            st.write("Datos por provincia:", df_check)
        except Exception as e:
            st.error(f"Error: {e}")

# ============================================
# SECCIONES EXISTENTES (COMPLETAS)
# ============================================

def seccion_inicio():
    filtro_label = get_filter_label(
        st.session_state.filtro_provincia_nombre,
        st.session_state.filtro_distrito_nombre,
        st.session_state.filtro_centro_nombre
    )
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    st.markdown(f"""
    <div class="main-title">
        <h1>Factores Socioeconómicos Familiares y Acceso a Programas Sociales</h1>
        <p>Población infantil registrada · 2025{filtro_label}</p>
    </div>
    """, unsafe_allow_html=True)
    
    query_total = f"""
        SELECT COUNT(*) as total 
        FROM PERSONA p
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        WHERE {where}
    """
    df_total = execute_query(query_total)
    total = df_total['total'].iloc[0] if not df_total.empty else 0
    
    if total == 0:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    query_prog = f"""
        SELECT
            CASE WHEN ps.nombre_programa IS NULL THEN 'SIN PROGRAMA' ELSE ps.nombre_programa END AS programa_social,
            COUNT(DISTINCT p.id_persona) AS cantidad
        FROM PERSONA p
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
        LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
        WHERE {where}
        GROUP BY ps.nombre_programa
    """
    df_prog = execute_query(query_prog)
    
    if df_prog.empty:
        juntos = 0
        cuna = 0
        sin = total
        pct_j = 0
        pct_c = 0
        pct_s = 100
    else:
        juntos = df_prog[df_prog['programa_social'] == 'JUNTOS']['cantidad'].iloc[0] if not df_prog[df_prog['programa_social'] == 'JUNTOS'].empty else 0
        cuna = df_prog[df_prog['programa_social'] == 'CUNA MAS']['cantidad'].iloc[0] if not df_prog[df_prog['programa_social'] == 'CUNA MAS'].empty else 0
        sin = df_prog[df_prog['programa_social'] == 'SIN PROGRAMA']['cantidad'].iloc[0] if not df_prog[df_prog['programa_social'] == 'SIN PROGRAMA'].empty else 0
        
        if juntos == 0 and cuna == 0 and sin == 0:
            sin = total
        
        pct_j = (juntos / total * 100) if total > 0 else 0
        pct_c = (cuna / total * 100) if total > 0 else 0
        pct_s = (sin / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Menores", f"{total:,}")
    with col2:
        metric_card("JUNTOS", f"{juntos:,}", f"{pct_j:.1f}%")
    with col3:
        metric_card("CUNA MÁS", f"{cuna:,}", f"{pct_c:.1f}%")
    with col4:
        metric_card("Sin Programa", f"{sin:,}", f"{pct_s:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not df_prog.empty and df_prog['cantidad'].sum() > 0:
            fig = crear_grafico_pastel_profesional(df_prog, 'programa_social', 'cantidad', 'Distribución de Programas Sociales')
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        query_sexo = f"""
            SELECT p.sexo, COUNT(*) as frecuencia
            FROM PERSONA p
            INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
            INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
            INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
            INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
            WHERE {where}
            GROUP BY p.sexo
        """
        df_sexo = execute_query(query_sexo)
        if not df_sexo.empty and df_sexo['frecuencia'].sum() > 0:
            fig = crear_grafico_pastel_profesional(df_sexo, 'sexo', 'frecuencia', 'Distribución por Sexo')
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================
# SECCIONES EXISTENTES (CARACTERIZACIÓN, PROGRAMAS, INGRESO, HIJOS, POBREZA, DISTRITOS)
# ============================================

def seccion_caracterizacion():
    mensaje_seccion("Caracterización de la Población Infantil")
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    query_total = f"""
        SELECT COUNT(*) as total 
        FROM PERSONA p
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        WHERE {where}
    """
    df_total = execute_query(query_total)
    total = df_total['total'].iloc[0] if not df_total.empty else 0
    
    if total == 0:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    query_sexo = f"""
        SELECT 
            p.sexo, 
            COUNT(*) as frecuencia
        FROM PERSONA p
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        WHERE {where}
        GROUP BY p.sexo
    """
    df_sexo = execute_query(query_sexo)
    
    masc = 0
    fem = 0
    
    for _, row in df_sexo.iterrows():
        sexo_val = str(row['sexo']).upper().strip() if row['sexo'] else ''
        if 'MASCULINO' in sexo_val or sexo_val == 'MASCULINO':
            masc = row['frecuencia']
        elif 'FEMENINO' in sexo_val or sexo_val == 'FEMENINO':
            fem = row['frecuencia']
    
    pct_m = (masc / total * 100) if total > 0 else 0
    pct_f = (fem / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Total Menores", f"{total:,}")
    with col2:
        metric_card("Masculino", f"{masc:,}", f"{pct_m:.1f}%")
    with col3:
        metric_card("Femenino", f"{fem:,}", f"{pct_f:.1f}%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not df_sexo.empty and df_sexo['frecuencia'].sum() > 0:
            fig = crear_grafico_pastel_profesional(df_sexo, 'sexo', 'frecuencia', 'Distribución por Sexo')
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        query_edad = f"""
            SELECT p.edad_anios, COUNT(*) as frecuencia
            FROM PERSONA p
            INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
            INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
            INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
            INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
            WHERE {where} AND p.edad_anios IS NOT NULL
            GROUP BY p.edad_anios
            ORDER BY p.edad_anios
        """
        df_edad = execute_query(query_edad)
        if not df_edad.empty:
            fig = crear_grafico_barras_profesional(df_edad, 'edad_anios', 'frecuencia', None, 
                                                  'Distribución por Edad', 'Edad (años)', 'Frecuencia',
                                                  colores=['#2e86c1'])
            if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    if not df_edad.empty:
        df_edad.columns = ['Edad (años)', 'Frecuencia']
        crear_tabla_profesional(df_edad, "Distribución de la Población por Edad")

def seccion_programas():
    mensaje_seccion("Acceso a Programas Sociales")
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    query = f"""
        SELECT
            CASE WHEN ps.nombre_programa IS NULL THEN 'SIN PROGRAMA' ELSE ps.nombre_programa END AS programa_social,
            COUNT(DISTINCT p.id_persona) AS cantidad
        FROM PERSONA p
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
        LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
        WHERE {where}
        GROUP BY ps.nombre_programa
    """
    df = execute_query(query)
    
    if df.empty or df['cantidad'].sum() == 0:
        st.warning("No se encontraron datos de programas sociales")
        return
    
    fig = crear_grafico_pastel_profesional(df, 'programa_social', 'cantidad', 'Distribución de Programas Sociales')
    if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    crear_tabla_profesional(df, "Beneficiarios por Programa Social")

def seccion_ingreso():
    mensaje_seccion("Ingreso Familiar y Programas Sociales")
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    query = f"""
        SELECT
            CASE 
                WHEN f.ingreso_familiar < 1000 THEN 'Bajo'
                WHEN f.ingreso_familiar <= 3000 THEN 'Medio'
                ELSE 'Alto'
            END AS nivel_ingreso,
            CASE 
                WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
                ELSE ps.nombre_programa
            END AS programa_social,
            COUNT(DISTINCT p.id_persona) AS frecuencia
        FROM PERSONA p
        INNER JOIN FAMILIA f ON p.id_familia = f.id_familia
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
        LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
        WHERE {where}
        GROUP BY 
            CASE WHEN f.ingreso_familiar < 1000 THEN 'Bajo'
                 WHEN f.ingreso_familiar <= 3000 THEN 'Medio'
                 ELSE 'Alto' END,
            CASE WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
                 ELSE ps.nombre_programa END
        ORDER BY nivel_ingreso, programa_social
    """
    df = execute_query(query)
    
    if df.empty:
        st.warning("No se encontraron datos de ingreso familiar")
        return
    
    fig = crear_grafico_barras_profesional(df, 'nivel_ingreso', 'frecuencia', 'programa_social',
                                           'Acceso a Programas Sociales según Nivel de Ingreso',
                                           'Nivel de Ingreso', 'Número de Beneficiarios',
                                           colores=['#2e86c1', '#f39c12', '#95a5a6'])
    if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    df_pivot = df.pivot(index='nivel_ingreso', columns='programa_social', values='frecuencia').fillna(0)
    df_pivot['Total'] = df_pivot.sum(axis=1)
    crear_tabla_profesional(df_pivot, "Distribución por Nivel de Ingreso")

def seccion_hijos():
    mensaje_seccion("Número de Hijos y Programas Sociales")
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    query = f"""
        SELECT
            CASE
                WHEN f.nro_hijos <= 1 THEN '0 - 1 hijos'
                WHEN f.nro_hijos <= 3 THEN '2 - 3 hijos'
                ELSE '4 o más hijos'
            END AS categoria_hijos,
            CASE
                WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
                ELSE ps.nombre_programa
            END AS programa_social,
            COUNT(DISTINCT p.id_persona) AS cantidad
        FROM PERSONA p
        INNER JOIN FAMILIA f ON p.id_familia = f.id_familia
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
        LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
        WHERE {where}
        GROUP BY
            CASE WHEN f.nro_hijos <= 1 THEN '0 - 1 hijos'
                 WHEN f.nro_hijos <= 3 THEN '2 - 3 hijos'
                 ELSE '4 o más hijos' END,
            CASE WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
                 ELSE ps.nombre_programa END
        ORDER BY categoria_hijos, programa_social
    """
    df = execute_query(query)
    
    if df.empty:
        st.warning("No se encontraron datos de número de hijos")
        return
    
    fig = crear_grafico_barras_profesional(df, 'categoria_hijos', 'cantidad', 'programa_social',
                                           'Acceso a Programas Sociales según Número de Hijos',
                                           'Número de Hijos', 'Número de Beneficiarios',
                                           colores=['#2e86c1', '#f39c12', '#95a5a6'])
    if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    df_pivot = df.pivot(index='categoria_hijos', columns='programa_social', values='cantidad').fillna(0)
    df_pivot['Total'] = df_pivot.sum(axis=1)
    crear_tabla_profesional(df_pivot, "Distribución por Número de Hijos")

def seccion_pobreza():
    mensaje_seccion("Índice de Pobreza y Programas Sociales")
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    query = f"""
        SELECT
            CASE
                WHEN f.indice_pobreza <= 30 THEN 'Bajo'
                WHEN f.indice_pobreza <= 45 THEN 'Medio'
                ELSE 'Alto'
            END AS nivel_pobreza,
            CASE
                WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
                ELSE ps.nombre_programa
            END AS programa_social,
            COUNT(DISTINCT p.id_persona) AS cantidad
        FROM PERSONA p
        INNER JOIN FAMILIA f ON p.id_familia = f.id_familia
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
        LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
        WHERE {where}
        GROUP BY
            CASE WHEN f.indice_pobreza <= 30 THEN 'Bajo'
                 WHEN f.indice_pobreza <= 45 THEN 'Medio'
                 ELSE 'Alto' END,
            CASE WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
                 ELSE ps.nombre_programa END
        ORDER BY nivel_pobreza, programa_social
    """
    df = execute_query(query)
    
    if df.empty:
        st.warning("No se encontraron datos de índice de pobreza")
        return
    
    fig = crear_grafico_barras_profesional(df, 'nivel_pobreza', 'cantidad', 'programa_social',
                                           'Acceso a Programas Sociales según Nivel de Pobreza',
                                           'Nivel de Pobreza', 'Número de Beneficiarios',
                                           colores=['#2e86c1', '#f39c12', '#95a5a6'])
    if fig: st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    df_pivot = df.pivot(index='nivel_pobreza', columns='programa_social', values='cantidad').fillna(0)
    df_pivot['Total'] = df_pivot.sum(axis=1)
    crear_tabla_profesional(df_pivot, "Distribución por Nivel de Pobreza")

def seccion_distritos():
    mensaje_seccion("Análisis por Distrito")
    where = get_filter_conditions(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    query = f"""
        SELECT
            dist.nombre_distrito,
            COUNT(DISTINCT p.id_persona) AS total_menores,
            COUNT(DISTINCT CASE WHEN ps.nombre_programa = 'JUNTOS' THEN p.id_persona END) AS juntos,
            COUNT(DISTINCT CASE WHEN ps.nombre_programa = 'CUNA MAS' THEN p.id_persona END) AS cuna_mas,
            COUNT(DISTINCT CASE WHEN ps.nombre_programa IS NULL THEN p.id_persona END) AS sin_programa
        FROM PERSONA p
        INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
        INNER JOIN DISTRITO dist ON cp.id_distrito = dist.id_distrito
        INNER JOIN PROVINCIA prov ON dist.id_provincia = prov.id_provincia
        INNER JOIN DEPARTAMENTO dep ON prov.id_departamento = dep.id_departamento
        LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
        LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
        WHERE {where}
        GROUP BY dist.nombre_distrito
        ORDER BY total_menores DESC
    """
    df = execute_query(query)
    
    if df.empty:
        st.warning("No se encontraron datos por distrito")
        return
    
    df_melt = df.melt(id_vars=['nombre_distrito'], 
                      value_vars=['juntos', 'cuna_mas', 'sin_programa'],
                      var_name='programa_social', value_name='cantidad')
    df_melt['programa_social'] = df_melt['programa_social'].map({
        'juntos': 'JUNTOS', 'cuna_mas': 'CUNA MÁS', 'sin_programa': 'Sin Programa'
    })
    
    fig = px.bar(df_melt, x='cantidad', y='nombre_distrito', color='programa_social',
                 title='Programas Sociales por Distrito',
                 labels={'cantidad': 'Número de Beneficiarios', 'nombre_distrito': 'Distrito'},
                 barmode='group', orientation='h',
                 color_discrete_sequence=['#2e86c1', '#f39c12', '#95a5a6'],
                 text_auto=True)
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=max(380, len(df) * 45),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Inter'),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e8edf4',
            borderwidth=1
        ),
        title=dict(
            text='Programas Sociales por Distrito',
            font=dict(size=18, weight=700, color='#0f1a2e', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=80, b=50, l=50, r=30),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.04)',
            tickfont=dict(size=11, family='Inter'),
            title_font=dict(size=13, weight=600, color='#0f1a2e')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.04)',
            tickfont=dict(size=11, family='Inter'),
            title_font=dict(size=13, weight=600, color='#0f1a2e')
        )
    )
    fig.update_traces(
        marker_line_width=1,
        marker_line_color='white',
        textfont=dict(size=10, weight=600, family='Inter'),
        opacity=0.9
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    df.columns = ['Distrito', 'Total Menores', 'JUNTOS', 'CUNA MÁS', 'Sin Programa']
    crear_tabla_profesional(df, "Resumen por Distrito")

# ============================================
# NUEVA SECCIÓN: ANÁLISIS SOCIOECONÓMICO - OPTIMIZADA
# ============================================

def seccion_analisis_socioeconomico():
    mensaje_seccion(
        "📊 Panel de Monitoreo Socioeconómico",
        "Análisis de tendencias y distribución de variables socioeconómicas"
    )
    
    # Obtener todos los datos en una sola consulta (cacheada)
    df = obtener_datos_analisis_socioeconomico(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id,
        st.session_state.filtro_centro_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    # ==========================================
    # 1. MÉTRICAS DE CONSOLA
    # ==========================================
    
    ing_prom = df['ingreso_familiar'].mean()
    ing_max = df['ingreso_familiar'].max()
    ing_min = df['ingreso_familiar'].min()
    hijos_prom = df['nro_hijos'].mean()
    pob_prom = df['indice_pobreza'].mean()
    pob_max = df['indice_pobreza'].max()
    pob_min = df['indice_pobreza'].min()
    total_fam = df['id_persona'].nunique()
    
    df_bajos = df[df['ingreso_familiar'] < 1000]
    bajos = df_bajos['id_persona'].nunique()
    pct_bajos = (bajos / total_fam * 100) if total_fam > 0 else 0
    
    df_pobres = df[df['indice_pobreza'] > 45]
    pobres = df_pobres['id_persona'].nunique()
    pct_pobres = (pobres / total_fam * 100) if total_fam > 0 else 0
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        crear_metric_console(f"S/. {ing_prom:,.0f}", "Ingreso Promedio", f"Min: {ing_min:,.0f} | Max: {ing_max:,.0f}", "blue")
    with col2:
        crear_metric_console(f"{total_fam:,}", "Total Familias", "Hogares registrados", "green")
    with col3:
        crear_metric_console(f"{hijos_prom:.1f}", "Prom. Hijos/Hogar", "Carga familiar", "blue")
    with col4:
        crear_metric_console(f"{pob_prom:.1f}%", "Pobreza Promedio", f"Min: {pob_min:.1f}% | Max: {pob_max:.1f}%", "orange")
    with col5:
        crear_metric_console(f"{bajos:,}", "Hogares Ingreso Bajo", f"{pct_bajos:.1f}% del total", "red")
    with col6:
        crear_metric_console(f"{pobres:,}", "Hogares Pobreza Alta", f"{pct_pobres:.1f}% del total", "orange")
    
    st.markdown("---")
    
    # ==========================================
    # 2. GRÁFICO DE TENDENCIA: INGRESO POR PROVINCIA
    # ==========================================
    
    fig = crear_grafico_tendencia_ingreso(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # ==========================================
    # 3. GRÁFICO DE TENDENCIA: POBREZA POR DISTRITO
    # ==========================================
    
    fig = crear_grafico_tendencia_pobreza(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # ==========================================
    # 4. DISTRIBUCIÓN DE HIJOS POR HOGAR
    # ==========================================
    
    fig = crear_grafico_barras_hijos(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # ==========================================
    # 5. CORRELACIÓN DE VARIABLES CON PROGRAMA SOCIAL
    # ==========================================
    
    fig = crear_grafico_correlacion_variables(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    st.markdown("---")
    
    # ==========================================
    # 6. MAPA DE POBREZA PROFESIONAL
    # ==========================================

    st.markdown("""
    <div style="margin-bottom: 15px;">
        <span style="font-weight: 700; color: #0f1a2e; font-size: 18px;">🗺️ Mapa de Pobreza por Distrito - Ancash</span>
        <p style="color: #7a8ba3; font-size: 13px; margin: 2px 0 0 0;">Visualización geográfica de los niveles de pobreza en la región</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        mapa = crear_mapa_pobreza_profesional(df)
        if mapa:
            from streamlit_folium import folium_static
            # Usar width=100% para que ocupe todo el ancho disponible
            folium_static(mapa, width=1100, height=650)
        else:
            st.info("ℹ️ No hay suficientes datos para generar el mapa")
    except ImportError:
        st.warning("⚠️ Para ver el mapa, instala: pip install folium streamlit-folium branca")
    except Exception as e:
        st.error(f"Error al generar el mapa: {e}")

# ============================================
# NAVEGACIÓN PRINCIPAL
# ============================================

secciones_map = {
    "Inicio": seccion_inicio,
    "Caracterización": seccion_caracterizacion,
    "Programas Sociales": seccion_programas,
    "Ingreso Familiar": seccion_ingreso,
    "Número de Hijos": seccion_hijos,
    "Índice de Pobreza": seccion_pobreza,
    "Análisis por Distrito": seccion_distritos,
    "📊 Análisis Socioeconómico": seccion_analisis_socioeconomico
}

try:
    if seccion in secciones_map:
        secciones_map[seccion]()
except Exception as e:
    st.error(f"Error: {e}")
    st.code(traceback.format_exc())

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 12px 0; color: #7a8ba3; font-size: 12px; font-family: 'Inter', sans-serif;">
    <strong style="color: #0f1a2e;">Universidad Nacional "Santiago Antúnez de Mayolo"</strong><br>
    Facultad de Ciencias · Escuela Profesional de Estadística e Informática<br>
    Investigación Formativa · 2025
</div>
""", unsafe_allow_html=True)

# == streamlit run app.py