# app.py - Dashboard Social Infantil Yungay
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
    page_title="Dashboard Social Infantil - Yungay",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# ESTILOS CSS AVANZADOS
# ============================================

st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e1a 0%, #111827 50%, #0f1729 100%) !important;
        padding-top: 0 !important;
        border-right: 1px solid rgba(255,255,255,0.03) !important;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        padding: 8px 14px !important;
        border-radius: 8px !important;
        font-weight: 400 !important;
        font-size: 13px !important;
        border-left: 3px solid transparent !important;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.05) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stRadio label[data-selected="true"] {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #ffffff !important;
        border-left: 3px solid #3b82f6 !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: transparent !important;
        padding: 0 !important;
        gap: 2px !important;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(59, 130, 246, 0.02) 100%);
        padding: 20px 16px 16px 16px;
        margin: 0 -8px 12px -8px;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        text-align: center;
    }
    
    .sidebar-header .logo-icon {
        font-size: 28px;
        color: #3b82f6;
        display: block;
        margin-bottom: 4px;
    }
    
    .sidebar-header h2 {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
    }
    
    .sidebar-header .subtitle {
        font-size: 10px !important;
        color: rgba(255,255,255,0.3) !important;
        margin: 2px 0 0 0 !important;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    .sidebar-header .subtitle span {
        color: #3b82f6 !important;
    }
    
    .nav-label {
        font-size: 9px !important;
        font-weight: 700 !important;
        color: rgba(255,255,255,0.12) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.2px !important;
        padding: 8px 0 4px 4px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: rgba(255,255,255,0.35) !important;
        font-weight: 500 !important;
        font-size: 10px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 8px !important;
        min-height: 38px !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="button"] {
        color: #ffffff !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 8px !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.6) !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"] {
        color: rgba(255,255,255,0.6) !important;
        padding: 8px 14px !important;
        border-radius: 6px !important;
        font-size: 13px !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"]:hover {
        background: rgba(59, 130, 246, 0.12) !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] div[role="listbox"] div[role="option"][aria-selected="true"] {
        background: rgba(59, 130, 246, 0.18) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .block-container {
        padding: 1.5rem 2rem 0rem 2rem !important;
        max-width: 100% !important;
        background: #f1f5f9;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: 0 4px 24px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.05) 0%, transparent 70%);
        border-radius: 50%;
    }
    
    .main-header .title {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin: 0 !important;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .main-header .title .highlight {
        color: #3b82f6 !important;
    }
    
    .main-header .subtitle {
        font-size: 14px !important;
        color: rgba(255,255,255,0.35) !important;
        margin: 4px 0 0 0 !important;
        position: relative;
        z-index: 1;
    }
    
    .main-header .badge {
        display: inline-block;
        background: rgba(59,130,246,0.12);
        color: #60a5fa;
        font-size: 11px;
        font-weight: 600;
        padding: 4px 14px;
        border-radius: 20px;
        border: 1px solid rgba(59,130,246,0.15);
        margin-top: 8px;
        position: relative;
        z-index: 1;
    }
    
    .main-header .filtro-info {
        font-size: 12px;
        color: rgba(255,255,255,0.2);
        margin-top: 6px;
        position: relative;
        z-index: 1;
    }
    
    .main-header .filtro-info span {
        color: #60a5fa;
    }
    
    .section-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 20px 24px 24px 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        margin-bottom: 20px;
    }
    
    .section-card .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin: 0 0 2px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-card .section-title .icon {
        font-size: 20px;
        color: #3b82f6;
        width: 28px;
        text-align: center;
    }
    
    .section-card .section-desc {
        font-size: 13px;
        color: #64748b;
        margin: 0 0 16px 0;
    }
    
    .insight-box {
        background: #eff6ff;
        border-radius: 10px;
        padding: 14px 18px;
        border-left: 4px solid #3b82f6;
        margin: 12px 0;
    }
    
    .insight-box .insight-title {
        font-size: 12px;
        font-weight: 700;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .insight-box .insight-text {
        font-size: 14px;
        color: #0f172a;
        margin: 2px 0 0 0;
        font-weight: 500;
    }
    
    .table-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        background: #ffffff;
    }
    
    .table-container table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .table-container thead th {
        background: #0f172a;
        color: #ffffff;
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 12px 16px;
        text-align: left;
    }
    
    .table-container tbody td {
        padding: 10px 16px;
        font-size: 13px;
        color: #0f172a;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .table-container tbody tr:hover {
        background: #f8fafc;
    }
    
    .table-container tbody tr:last-child td {
        border-bottom: none;
    }
    
    .footer {
        text-align: center;
        padding: 16px 0 8px 0;
        color: #94a3b8;
        font-size: 12px;
        border-top: 1px solid #e2e8f0;
        margin-top: 24px;
    }
    
    .footer strong {
        color: #0f172a;
    }
    
    .footer i {
        color: #3b82f6;
        margin: 0 4px;
    }
    
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
    .metric-console .highlight-blue { color: #3b82f6 !important; }
    .metric-console .highlight-orange { color: #f39c12 !important; }
    .metric-console .highlight-red { color: #e74c3c !important; }
    
    .map-container {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        background: #ffffff;
        padding: 4px;
    }
    
    @media (max-width: 768px) {
        .main-header .title {
            font-size: 20px !important;
        }
        .block-container {
            padding: 1rem 1rem 0rem 1rem !important;
        }
        .metric-box .value {
            font-size: 22px !important;
        }
        .metric-console .value {
            font-size: 22px !important;
        }
        [data-testid="stSidebar"] {
            width: 280px !important;
        }
    }
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

def get_filter_conditions(provincia_id, distrito_id):
    conditions = ["dep.nombre_departamento = 'ANCASH'"]
    
    if provincia_id and provincia_id != 0:
        conditions.append(f"prov.id_provincia = {provincia_id}")
    
    if distrito_id and distrito_id != 0:
        conditions.append(f"dist.id_distrito = {distrito_id}")
    
    return " AND ".join(conditions)

def get_filter_label(provincia_nombre, distrito_nombre):
    parts = []
    if provincia_nombre and provincia_nombre != 'Todas':
        parts.append(provincia_nombre)
    if distrito_nombre and distrito_nombre != 'Todos':
        parts.append(distrito_nombre)
    
    if parts:
        return " · ".join(parts)
    return "Todos los registros"

# ============================================
# FUNCIONES DE DATOS - CACHE OPTIMIZADO
# ============================================

@st.cache_data(ttl=3600)
def obtener_datos_completos(provincia_id, distrito_id):
    where = get_filter_conditions(provincia_id, distrito_id)
    
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
        prov.id_provincia,
        dist.nombre_distrito,
        dist.id_distrito
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

@st.cache_data(ttl=3600)
def obtener_estadisticas(provincia_id, distrito_id):
    where = get_filter_conditions(provincia_id, distrito_id)
    
    query = f"""
    SELECT 
        COUNT(DISTINCT p.id_persona) AS total_personas,
        AVG(f.ingreso_familiar) AS ingreso_promedio,
        MIN(f.ingreso_familiar) AS ingreso_minimo,
        MAX(f.ingreso_familiar) AS ingreso_maximo,
        AVG(f.nro_hijos) AS hijos_promedio,
        AVG(f.indice_pobreza) AS pobreza_promedio,
        MIN(f.indice_pobreza) AS pobreza_minimo,
        MAX(f.indice_pobreza) AS pobreza_maximo,
        SUM(CASE WHEN f.ingreso_familiar < 1000 THEN 1 ELSE 0 END) AS hogares_bajo_ingreso,
        SUM(CASE WHEN f.indice_pobreza > 45 THEN 1 ELSE 0 END) AS hogares_pobreza_alta,
        SUM(CASE WHEN ps.nombre_programa IS NOT NULL THEN 1 ELSE 0 END) AS total_con_programa,
        SUM(CASE WHEN ps.nombre_programa = 'JUNTOS' THEN 1 ELSE 0 END) AS total_juntos,
        SUM(CASE WHEN ps.nombre_programa = 'CUNA MAS' THEN 1 ELSE 0 END) AS total_cuna_mas
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

@st.cache_data(ttl=3600)
def obtener_datos_analisis_socioeconomico(provincia_id, distrito_id):
    where = get_filter_conditions(provincia_id, distrito_id)
    
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
# FUNCIONES DE VISUALIZACIÓN
# ============================================

def crear_grafico_barras_agrupadas(df, x, y, color, titulo, etiqueta_x=None, etiqueta_y=None, colores=None, ancho_barra=0.35):
    """Crea gráfico de barras agrupadas con ancho controlado"""
    if df.empty or df[y].sum() == 0:
        return None
    
    color_seq = colores or {'CUNA MAS': '#f97316', 'JUNTOS': '#3b82f6', 'Sin programa': '#94a3b8'}
    
    fig = go.Figure()
    
    if color and color in df.columns:
        categorias = sorted(df[color].unique())
        for i, cat in enumerate(categorias):
            df_cat = df[df[color] == cat]
            color_val = color_seq.get(cat, '#94a3b8') if isinstance(color_seq, dict) else color_seq[i % len(color_seq)]
            
            fig.add_trace(go.Bar(
                x=df_cat[x],
                y=df_cat[y],
                name=cat,
                marker_color=color_val,
                text=df_cat[y].apply(lambda v: f'{v:,.0f}' if v > 0 else ''),
                textposition='inside',
                textfont=dict(size=11, color='white', weight='bold'),
                hovertemplate='<b>%{x}</b><br>%{y:,.0f} personas<br>Programa: %{fullData.name}<extra></extra>',
                width=ancho_barra,
                customdata=df_cat[color].values
            ))
    else:
        fig.add_trace(go.Bar(
            x=df[x],
            y=df[y],
            marker_color=color_seq[0] if isinstance(color_seq, list) else '#3b82f6',
            text=df[y].apply(lambda v: f'{v:,.0f}' if v > 0 else ''),
            textposition='inside',
            textfont=dict(size=12, color='white', weight='bold'),
            hovertemplate='<b>%{x}</b><br>%{y:,.0f}<extra></extra>',
            width=ancho_barra
        ))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=460,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, family='Inter'),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        title=dict(
            text=titulo,
            font=dict(size=20, weight=700, color='#0f172a', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=85, b=60, l=60, r=40),
        xaxis=dict(
            tickfont=dict(size=13, color='#0f172a', family='Inter', weight='bold'),
            gridcolor='rgba(0,0,0,0.04)',
            showgrid=False,
            title=dict(
                text=etiqueta_x or '',
                font=dict(size=14, weight=600, color='#0f172a')
            )
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.06)',
            gridwidth=1,
            showgrid=True,
            title=dict(
                text=etiqueta_y or 'Número de Beneficiarios',
                font=dict(size=14, weight=600, color='#0f172a')
            ),
            zeroline=False
        ),
        hoverlabel=dict(
            font=dict(size=12, family='Inter'),
            bgcolor='white',
            bordercolor='#e2e8f0'
        ),
        bargap=0.25,
        bargroupgap=0.15
    )
    
    fig.update_traces(
        marker_line_color='rgba(255,255,255,0.8)',
        marker_line_width=1.5,
        opacity=0.92
    )
    
    return fig

def crear_grafico_pastel_moderno(df, nombres, valores, titulo, colores=None, hole=0.4):
    if df.empty or df[valores].sum() == 0:
        return None
    
    color_seq = colores or ['#3b82f6', '#f97316', '#94a3b8', '#22c55e', '#ef4444', '#8b5cf6', '#06b6d4', '#f59e0b']
    
    fig = go.Figure(data=[go.Pie(
        labels=df[nombres],
        values=df[valores],
        hole=hole,
        textposition='outside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>%{value:,.0f} personas (%{percent})<extra></extra>',
        marker=dict(
            colors=color_seq[:len(df)],
            line=dict(color='white', width=3)
        ),
        showlegend=False,
        textfont=dict(size=13, family='Inter', color='#0f172a', weight='bold'),
        insidetextorientation='horizontal',
        pull=[0.02] * len(df)
    )])
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=420,
        title=dict(
            text=titulo,
            font=dict(size=18, weight=700, color='#0f172a', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=70, b=20, l=20, r=20)
    )
    
    return fig

def crear_grafico_tendencia_ingreso(df):
    if df.empty:
        return None
    
    df_geo = df.groupby('nombre_distrito').agg({
        'ingreso_familiar': ['mean', 'min', 'max'],
        'id_persona': 'count'
    }).reset_index()
    df_geo.columns = ['nombre_distrito', 'ingreso_promedio', 'ingreso_minimo', 'ingreso_maximo', 'total_personas']
    df_geo = df_geo.sort_values('ingreso_promedio', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_geo['nombre_distrito'],
        y=df_geo['ingreso_promedio'],
        mode='lines+markers+text',
        name='Ingreso Promedio',
        line=dict(color='#3b82f6', width=3, shape='spline'),
        marker=dict(size=12, color='#3b82f6', symbol='circle', line=dict(width=2, color='white')),
        text=df_geo['ingreso_promedio'].apply(lambda x: f'S/.{x:,.0f}'),
        textposition='top center',
        textfont=dict(size=10, color='#3b82f6', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Ingreso Promedio: S/.%{y:,.0f}<br>Personas: %{customdata:,.0f}<extra></extra>',
        customdata=df_geo['total_personas']
    ))
    
    fig.add_trace(go.Scatter(
        x=df_geo['nombre_distrito'],
        y=df_geo['ingreso_promedio'],
        fill='tozeroy',
        line=dict(color='rgba(59, 130, 246, 0)'),
        fillcolor='rgba(59, 130, 246, 0.08)',
        name='Tendencia'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_geo['nombre_distrito'],
        y=df_geo['ingreso_minimo'],
        mode='lines',
        name='Mínimo',
        line=dict(color='#ef4444', width=1.5, dash='dash'),
        opacity=0.6
    ))
    
    fig.add_trace(go.Scatter(
        x=df_geo['nombre_distrito'],
        y=df_geo['ingreso_maximo'],
        mode='lines',
        name='Máximo',
        line=dict(color='#22c55e', width=1.5, dash='dash'),
        opacity=0.6
    ))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        title=dict(
            text='Ingreso Promedio por Distrito',
            font=dict(size=16, weight=700, color='#0f172a', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, color='#0f172a', family='Inter'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        margin=dict(t=80, b=50, l=50, r=30),
        xaxis=dict(
            tickfont=dict(size=11, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.04)',
            gridwidth=0.5,
            showgrid=True,
            tickangle=45
        ),
        yaxis=dict(
            tickfont=dict(size=11, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.04)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Ingreso (S/)', font=dict(size=13, weight=600, color='#0f172a'))
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='white', bordercolor='#e2e8f0')
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
        line=dict(color='#ef4444', width=3, shape='spline'),
        marker=dict(size=12, color='#ef4444', symbol='diamond', line=dict(width=2, color='white')),
        text=df_dist['indice_pobreza'].apply(lambda x: f'{x:.1f}%'),
        textposition='top center',
        textfont=dict(size=10, color='#ef4444', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Pobreza: %{y:.1f}%<br>Personas: %{customdata:,.0f}<extra></extra>',
        customdata=df_dist['total_personas']
    ))
    
    fig.add_trace(go.Scatter(
        x=df_dist['nombre_distrito'],
        y=df_dist['indice_pobreza'],
        fill='tozeroy',
        line=dict(color='rgba(239, 68, 68, 0)'),
        fillcolor='rgba(239, 68, 68, 0.08)',
        name='Tendencia'
    ))
    
    fig.add_hline(
        y=45,
        line_dash="dash",
        line_color="#f97316",
        opacity=0.6,
        annotation_text="Umbral Pobreza Alta (45%)",
        annotation_font=dict(size=10, color='#64748b')
    )
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        title=dict(
            text='Índice de Pobreza por Distrito (Top 20)',
            font=dict(size=16, weight=700, color='#0f172a', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=11, color='#0f172a', family='Inter'),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e2e8f0',
            borderwidth=1
        ),
        margin=dict(t=80, b=50, l=50, r=30),
        xaxis=dict(
            tickfont=dict(size=10, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.04)',
            gridwidth=0.5,
            showgrid=True,
            tickangle=45
        ),
        yaxis=dict(
            tickfont=dict(size=11, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.04)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Índice de Pobreza (%)', font=dict(size=13, weight=600, color='#0f172a')),
            range=[0, 70]
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='white', bordercolor='#e2e8f0')
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
    
    colors = ['#3b82f6', '#f97316', '#ef4444']
    
    fig = go.Figure()
    
    for i, row in df_hijos.iterrows():
        fig.add_trace(go.Bar(
            x=[row['categoria']],
            y=[row['cantidad']],
            marker=dict(color=colors[i % len(colors)], line=dict(width=2, color='white')),
            text=[f"{row['cantidad']:,}"],
            textposition='outside',
            textfont=dict(size=14, weight='bold', color='#0f172a'),
            hovertemplate=f'<b>{row["categoria"]}</b><br>Hogares: {row["cantidad"]:,}<extra></extra>',
            width=0.5
        ))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        title=dict(
            text='Distribución de Hogares por Número de Hijos',
            font=dict(size=18, weight=700, color='#0f172a', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=80, b=50, l=60, r=60),
        xaxis=dict(
            tickfont=dict(size=13, color='#0f172a', family='Inter', weight='bold'),
            gridcolor='rgba(0,0,0,0.04)',
            showgrid=False,
            title=dict(text='Número de Hijos', font=dict(size=14, weight=600, color='#0f172a'))
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.04)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Número de Hogares', font=dict(size=14, weight=600, color='#0f172a'))
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='white', bordercolor='#e2e8f0'),
        bargap=0.4,
        showlegend=False
    )
    
    return fig

def crear_grafico_correlacion_variables(df):
    if df.empty:
        return None
    
    df['tiene_programa_num'] = df['tiene_programa'].map({'No': 0, 'Sí': 1})
    
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
    
    colors = ['#22c55e' if x > 0 else '#ef4444' if x < 0 else '#94a3b8' for x in df_corr['Correlación']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_corr['Variable'],
        y=df_corr['Correlación'],
        marker=dict(color=colors, line=dict(width=2, color='white')),
        text=df_corr['Correlación'].apply(lambda x: f'{x:.3f}'),
        textposition='outside',
        textfont=dict(size=14, weight='bold', color='#0f172a'),
        hovertemplate='<b>%{x}</b><br>Correlación: %{y:.3f}<br>Fuerza: %{customdata[0]}<br>Dirección: %{customdata[1]}<extra></extra>',
        customdata=df_corr[['Fuerza', 'Interpretación']].values,
        width=0.5
    ))
    
    fig.add_hline(y=0, line_dash="solid", line_color="rgba(0,0,0,0.1)", opacity=0.5)
    fig.add_hline(y=0.3, line_dash="dash", line_color="rgba(34,197,94,0.2)", 
                  annotation_text="Moderada (0.3)", annotation_font=dict(size=10, color='#64748b'))
    fig.add_hline(y=-0.3, line_dash="dash", line_color="rgba(239,68,68,0.2)",
                  annotation_text="Moderada (-0.3)", annotation_font=dict(size=10, color='#64748b'))
    
    fig.update_layout(
        font=dict(family='Inter, sans-serif', size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,
        title=dict(
            text='Correlación con Acceso a Programas Sociales (Coeficiente de Pearson)',
            font=dict(size=18, weight=700, color='#0f172a', family='Inter'),
            x=0.5,
            xanchor='center'
        ),
        margin=dict(t=80, b=50, l=60, r=60),
        xaxis=dict(
            tickfont=dict(size=13, color='#0f172a', family='Inter', weight='bold'),
            gridcolor='rgba(0,0,0,0.04)',
            showgrid=False,
            title=dict(text='Variables Independientes', font=dict(size=14, weight=600, color='#0f172a'))
        ),
        yaxis=dict(
            tickfont=dict(size=12, color='#64748b', family='Inter'),
            gridcolor='rgba(0,0,0,0.04)',
            gridwidth=0.5,
            showgrid=True,
            title=dict(text='Coeficiente de Correlación', font=dict(size=14, weight=600, color='#0f172a')),
            range=[-1, 1]
        ),
        hoverlabel=dict(font=dict(size=12, family='Inter'), bgcolor='white', bordercolor='#e2e8f0'),
        bargap=0.4,
        showlegend=False
    )
    
    return fig

# ============================================
# MAPA DE POBREZA PARA YUNGAY
# ============================================

def crear_mapa_pobreza_yungay(df):
    """
    Crea un mapa profesional de Yungay mostrando el nivel de pobreza por centro poblado.
    """
    if df.empty:
        return None

    df_clean = df.dropna(subset=['indice_pobreza', 'nombre_distrito'])
    if df_clean.empty:
        return None

    try:
        import folium
        from folium.plugins import Fullscreen, MarkerCluster
        import numpy as np
    except ImportError:
        st.warning("Para ver el mapa, instala: pip install folium streamlit-folium")
        return None

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
        return None

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

    coords_centros = {}
    np.random.seed(42)

    for distrito, (base_lat, base_lon) in coords_distritos.items():
        centros_distrito = df_centros[df_centros['nombre_distrito'] == distrito]
        if centros_distrito.empty:
            continue

        n = len(centros_distrito)
        max_radius = 0.025
        step = max_radius / max(1, n / 4)

        for i, (_, row) in enumerate(centros_distrito.iterrows()):
            centro = row['nombre_centro_poblado']
            angle = i * 1.5
            radius = step * (i + 1) * 0.6
            radius = min(radius, max_radius)

            lat_offset = radius * np.sin(angle)
            lon_offset = radius * np.cos(angle)

            coords_centros[centro] = [
                base_lat + lat_offset,
                base_lon + lon_offset
            ]

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

    max_personas = max([d.get('personas', 0) for d in dict_pobreza.values()], default=1)

    for _, row in df_centros.iterrows():
        centro = row['nombre_centro_poblado']
        distrito = row['nombre_distrito']

        coords = coords_centros.get(centro)
        if coords is None:
            continue

        lat, lon = coords

        if centro in dict_pobreza:
            datos = dict_pobreza[centro]
            pobreza = datos['pobreza']
            personas = datos['personas']
            ingreso = datos['ingreso']
            hijos = datos['hijos']
        else:
            pobreza = df_clean[df_clean['nombre_distrito'] == distrito]['indice_pobreza'].mean()
            pobreza = float(pobreza) if not pd.isna(pobreza) else 40.0
            personas = 0
            ingreso = 0
            hijos = 0

        if pobreza < 30:
            color, fill_color, nivel = '#2ecc71', '#2ecc71', 'Bajo'
        elif pobreza < 45:
            color, fill_color, nivel = '#f1c40f', '#f1c40f', 'Medio'
        elif pobreza < 55:
            color, fill_color, nivel = '#e67e22', '#e67e22', 'Medio-Alto'
        else:
            color, fill_color, nivel = '#e74c3c', '#e74c3c', 'Alto'

        radius = 4 + (personas / max_personas) * 14 if max_personas > 0 and personas > 0 else 5
        radius = min(radius, 18)

        tooltip_text = f"""
        <div style="font-family: 'Inter', sans-serif; padding: 6px 8px; min-width: 180px;">
            <b style="font-size: 14px; color: #1a2d4a;">{centro}</b><br>
            <span style="font-size: 11px; color: #7a8ba3;">{distrito}</span>
            <hr style="margin: 4px 0; border-color: #eef2f7;">
            <span style="font-size: 12px;">Pobreza: <b>{pobreza:.1f}%</b></span><br>
            <span style="font-size: 12px;">Nivel: <b>{nivel}</b></span>
            {f'<span style="font-size: 12px;">Personas: <b>{personas:,}</b></span>' if personas > 0 else '<span style="font-size: 11px; color: #95a5a6;">Sin datos</span>'}
        </div>
        """

        popup_html = f"""
        <div style="font-family: 'Inter', sans-serif; padding: 14px 18px; min-width: 260px; background: #ffffff; border-radius: 12px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                <div>
                    <h4 style="margin: 0; color: #1a2d4a; font-size: 17px; font-weight: 700;">{centro}</h4>
                    <span style="font-size: 12px; color: #7a8ba3;">{distrito} · Yungay</span>
                </div>
            </div>
            <div style="border-bottom: 2px solid #f0f4f8; margin: 8px 0 10px 0;"></div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px 16px; font-size: 13px;">
                <div style="color: #7a8ba3;">Pobreza</div>
                <div style="font-weight: 700; color: {fill_color};">{pobreza:.1f}%</div>
                <div style="color: #7a8ba3;">Nivel</div>
                <div style="font-weight: 600; color: #1a2d4a;">{nivel}</div>
                {f'<div style="color: #7a8ba3;">Personas</div><div style="font-weight: 600; color: #1a2d4a;">{personas:,}</div>' if personas > 0 else ''}
                {f'<div style="color: #7a8ba3;">Ingreso Prom.</div><div style="font-weight: 600; color: #1a2d4a;">S/. {ingreso:,.0f}</div>' if ingreso > 0 else ''}
                {f'<div style="color: #7a8ba3;">Hijos Prom.</div><div style="font-weight: 600; color: #1a2d4a;">{hijos:.1f}</div>' if hijos > 0 else ''}
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

    for distrito, (lat, lon) in coords_distritos.items():
        folium.Circle(
            location=[lat, lon],
            radius=1500,
            color='#3b82f6',
            fill=True,
            fill_color='#3b82f6',
            fill_opacity=0.08,
            weight=2,
            opacity=0.4,
            popup=f"<b>{distrito}</b>"
        ).add_to(m)

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
            <span style="font-size: 11px; font-weight: 700; color: #1a2d4a;">Nivel de Pobreza</span>
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
            <span style="font-size: 7px; color: #b0bfd0;">Hover para info | Pantalla completa</span>
        </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

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
        <span style="font-size: 13px; font-weight: 700;">Pobreza por Centro Poblado</span>
        <span style="font-size: 10px; color: #7a8ba3; margin-left: 6px;">Yungay · 2025</span>
        <span style="display: inline-block; margin-left: 6px; padding: 1px 8px; background: #3b82f6; color: white; border-radius: 12px; font-size: 8px; font-weight: 600;">{len(df_centros)} centros</span>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    return m

# ============================================
# FUNCIONES DE UTILIDAD
# ============================================

def render_section_card(title, icon, desc=None):
    st.markdown(f'''
    <div class="section-card">
        <div class="section-title">
            <span class="icon"><i class="fas {icon}"></i></span>
            {title}
        </div>
        {f'<div class="section-desc">{desc}</div>' if desc else ''}
    ''', unsafe_allow_html=True)
    return True

def close_section_card():
    st.markdown('</div>', unsafe_allow_html=True)

def render_insight(title, text):
    st.markdown(f'''
    <div class="insight-box">
        <div class="insight-title"><i class="fas fa-lightbulb"></i> {title}</div>
        <div class="insight-text">{text}</div>
    </div>
    ''', unsafe_allow_html=True)

def render_main_header():
    filtro_label = get_filter_label(
        st.session_state.filtro_provincia_nombre,
        st.session_state.filtro_distrito_nombre
    )
    
    st.markdown(f"""
    <div class="main-header">
        <div class="title"><i class="fas fa-chart-pie" style="color:#3b82f6;margin-right:10px;"></i>Factores Socioeconómicos <span class="highlight">Familiares</span> y Acceso a Programas Sociales</div>
        <div class="subtitle"><i class="fas fa-map-pin"></i> Población infantil registrada · Yungay · 2025</div>
        <div class="badge"><i class="fas fa-university"></i> UNASAM - Facultad de Ciencias</div>
        <div class="filtro-info"><i class="fas fa-filter"></i> Filtro activo: <span>{filtro_label}</span></div>
    </div>
    """, unsafe_allow_html=True)

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

def crear_tabla_bidimensional(df, titulo=None):
    """Crea una tabla bidimensional con formato correcto (filas y columnas)"""
    if titulo:
        st.markdown(f"""
        <div style="margin-bottom:12px;">
            <span style="font-weight:700;color:#0f172a;font-size:15px;">{titulo}</span>
        </div>
        """, unsafe_allow_html=True)
    
    df_display = df.copy()
    for col in df_display.columns:
        if df_display[col].dtype in ['int64', 'float64']:
            df_display[col] = df_display[col].apply(lambda x: f'{x:,.0f}' if pd.notna(x) else '-')
    
    st.markdown(f'''
    <div class="table-container">
        {df_display.to_html(index=False, escape=False)}
    </div>
    ''', unsafe_allow_html=True)

def scroll_to_top():
    st.markdown("""
    <script>
        window.scrollTo({top: 0, behavior: 'smooth'});
    </script>
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

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div class="logo-icon"><i class="fas fa-university"></i></div>
        <h2>UNASAM</h2>
        <div class="subtitle">Facultad de Ciencias · <span>Estadística e Informática</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        df_total = execute_query("SELECT COUNT(*) as total FROM PERSONA")
        total = df_total['total'].iloc[0] if not df_total.empty else 0
        st.markdown(f"""
        <div style="text-align:center;padding:8px 0;background:rgba(255,255,255,0.02);border-radius:8px;margin:0 0 8px 0;">
            <span style="font-size:10px;color:rgba(255,255,255,0.25);text-transform:uppercase;letter-spacing:0.5px;"><i class="fas fa-database"></i> Total registros</span>
            <br>
            <span style="font-size:22px;font-weight:800;color:#ffffff;">{total:,}</span>
        </div>
        """, unsafe_allow_html=True)
    except:
        pass
    
    st.markdown('<div class="nav-label"><i class="fas fa-compass"></i> Navegación</div>', unsafe_allow_html=True)
    
    seccion = st.radio(
        "", 
        [
            "Características",
            "Programas Sociales",
            "Ingreso Familiar",
            "Número de Hijos",
            "Índice de Pobreza",
            "Análisis Socioeconómico"
        ], 
        index=0, 
        label_visibility="collapsed",
        key="sidebar_nav_radio"
    )
    
    
    st.markdown("---")
    
    if st.button("Diagnosticar Datos"):
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
# SECCIÓN CARACTERÍSTICAS (Fusión de Inicio + Caracterización)
# ============================================

def seccion_caracteristicas():
    scroll_to_top()
    render_main_header()
    
    df = obtener_datos_completos(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    stats = obtener_estadisticas(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if stats.empty:
        st.warning("No se pudieron obtener estadísticas.")
        return
    
    total = stats['total_personas'].iloc[0]
    ing_prom = stats['ingreso_promedio'].iloc[0]
    pob_prom = stats['pobreza_promedio'].iloc[0]
    hijos_prom = stats['hijos_promedio'].iloc[0]
    con_programa = stats['total_con_programa'].iloc[0]
    pct_programa = (con_programa / total * 100) if total > 0 else 0
    
    # KPI GRID
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:18px;color:#3b82f6;margin-bottom:4px;"><i class="fas fa-users"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Total Menores</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{total:,}</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:100%;background:linear-gradient(90deg,#3b82f6,#3b82f6);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ing_pct = min((ing_prom / 5000) * 100, 100)
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:18px;color:#22c55e;margin-bottom:4px;"><i class="fas fa-money-bill-wave"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Ingreso Promedio</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">S/ {ing_prom:,.0f}</div>
            <div style="font-size:12px;color:#64748b;font-weight:500;">Min: {stats['ingreso_minimo'].iloc[0]:,.0f} | Max: {stats['ingreso_maximo'].iloc[0]:,.0f}</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{ing_pct:.1f}%;background:linear-gradient(90deg,#16a34a,#22c55e);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:18px;color:#f97316;margin-bottom:4px;"><i class="fas fa-chart-line"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Pobreza Promedio</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{pob_prom:.1f}%</div>
            <div style="font-size:12px;color:#64748b;font-weight:500;">Min: {stats['pobreza_minimo'].iloc[0]:.1f}% | Max: {stats['pobreza_maximo'].iloc[0]:.1f}%</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{min(pob_prom, 100):.1f}%;background:linear-gradient(90deg,#ea580c,#f97316);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        hijos_pct = min((hijos_prom / 5) * 100, 100)
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);">
            <div style="font-size:18px;color:#8b5cf6;margin-bottom:4px;"><i class="fas fa-people-arrows"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Hijos por Hogar</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{hijos_prom:.1f}</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{hijos_pct:.1f}%;background:linear-gradient(90deg,#7c3aed,#8b5cf6);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # KPI GRID 2
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);margin-top:16px;">
            <div style="font-size:18px;color:#22c55e;margin-bottom:4px;"><i class="fas fa-hand-holding-heart"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Con Programa Social</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{con_programa:,}</div>
            <div style="font-size:12px;color:#64748b;font-weight:500;">{pct_programa:.1f}% del total</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{pct_programa:.1f}%;background:linear-gradient(90deg,#16a34a,#22c55e);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        juntos = stats['total_juntos'].iloc[0]
        pct_juntos = (juntos / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);margin-top:16px;">
            <div style="font-size:18px;color:#3b82f6;margin-bottom:4px;"><i class="fas fa-handshake"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">JUNTOS</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{juntos:,}</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{pct_juntos:.1f}%;background:linear-gradient(90deg,#2563eb,#3b82f6);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cuna = stats['total_cuna_mas'].iloc[0]
        pct_cuna = (cuna / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);margin-top:16px;">
            <div style="font-size:18px;color:#f97316;margin-bottom:4px;"><i class="fas fa-school"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">CUNA MÁS</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{cuna:,}</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{pct_cuna:.1f}%;background:linear-gradient(90deg,#ea580c,#f97316);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        sin_programa = total - con_programa
        pct_sin = (sin_programa / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;box-shadow:0 1px 3px rgba(0,0,0,0.04);margin-top:16px;">
            <div style="font-size:18px;color:#ef4444;margin-bottom:4px;"><i class="fas fa-times-circle"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;">Sin Programa</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px;">{sin_programa:,}</div>
            <div style="font-size:12px;color:#64748b;font-weight:500;">{pct_sin:.1f}% del total</div>
            <div style="height:3px;border-radius:3px;margin-top:10px;background:#f1f5f9;">
                <div style="height:100%;border-radius:3px;width:{pct_sin:.1f}%;background:linear-gradient(90deg,#dc2626,#ef4444);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_card("Distribución por Programa Social", "fa-chart-pie")
        df_prog = df.groupby('programa_social').size().reset_index(name='frecuencia')
        fig = crear_grafico_pastel_moderno(df_prog, 'programa_social', 'frecuencia', 
                                           'Distribución de Programas Sociales')
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        close_section_card()
    
    with col2:
        render_section_card("Distribución por Sexo", "fa-venus-mars")
        df_sexo = df.groupby('sexo').size().reset_index(name='frecuencia')
        fig = crear_grafico_pastel_moderno(df_sexo, 'sexo', 'frecuencia',
                                           'Distribución por Sexo',
                                           colores=['#3b82f6', '#ef4444'])
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        close_section_card()
    
    st.markdown("---")
    
    # Distribución de Sexo por Distrito (Top 20)
    render_section_card("Distribución de Sexo por Distrito (Top 20)", "fa-chart-bar")
    
    df_sexo_dist = df.groupby(['nombre_distrito', 'sexo']).size().reset_index(name='frecuencia')
    top_distritos_sexo = df.groupby('nombre_distrito').size().sort_values(ascending=False).head(20).index.tolist()
    df_sexo_dist = df_sexo_dist[df_sexo_dist['nombre_distrito'].isin(top_distritos_sexo)]
    
    if not df_sexo_dist.empty:
        dist_order_sexo = df_sexo_dist.groupby('nombre_distrito')['frecuencia'].sum().sort_values(ascending=True).index.tolist()
        
        fig = px.bar(
            df_sexo_dist,
            x='frecuencia',
            y='nombre_distrito',
            color='sexo',
            title='Distribución de Sexo por Distrito (Top 20)',
            labels={'frecuencia': 'Número de Personas', 'nombre_distrito': 'Distrito'},
            barmode='group',
            orientation='h',
            color_discrete_sequence=['#3b82f6', '#ef4444'],
            text_auto=True
        )
        fig.update_layout(
            font=dict(family='Inter, sans-serif', size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=max(460, len(dist_order_sexo) * 40),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5,
                font=dict(size=11, family='Inter'),
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor='#e2e8f0',
                borderwidth=1
            ),
            title=dict(
                text='Distribución de Sexo por Distrito (Top 20)',
                font=dict(size=20, weight=700, color='#0f172a', family='Inter'),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(t=85, b=50, l=50, r=30),
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=11, family='Inter'),
                title=dict(text='Número de Personas', font=dict(size=14, weight=600, color='#0f172a'))
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=11, family='Inter'),
                title=dict(text='Distrito', font=dict(size=14, weight=600, color='#0f172a')),
                categoryorder='array',
                categoryarray=dist_order_sexo
            ),
            hoverlabel=dict(
                font=dict(size=12, family='Inter'),
                bgcolor='white',
                bordercolor='#e2e8f0'
            ),
            bargap=0.2,
            bargroupgap=0.1
        )
        fig.update_traces(
            marker_line_width=1,
            marker_line_color='white',
            textfont=dict(size=10, weight='bold', family='Inter'),
            opacity=0.9
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # Distribución por Edad
    render_section_card("Distribución por Edad", "fa-calendar-alt")
    df_edad = df[df['edad_anios'].notna()].groupby('edad_anios').size().reset_index(name='frecuencia')
    df_edad = df_edad.sort_values('edad_anios')
    if not df_edad.empty:
        fig = crear_grafico_barras_agrupadas(
            df_edad, 'edad_anios', 'frecuencia', None,
            'Distribución por Edad',
            'Edad (años)', 'Frecuencia',
            colores=['#3b82f6']
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # Tabla de Edad
    render_section_card("Detalle por Edad", "fa-table")
    if not df_edad.empty:
        df_edad.columns = ['Edad (años)', 'Frecuencia']
        total_edad = df_edad['Frecuencia'].sum()
        df_edad['Porcentaje'] = (df_edad['Frecuencia'] / total_edad * 100).round(1)
        
        st.markdown(f'''
        <div class="table-container">
            {df_edad.to_html(index=False, escape=False)}
        </div>
        ''', unsafe_allow_html=True)
    close_section_card()
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if pct_programa > 50:
            render_insight(
                "Alta Cobertura de Programas",
                f"El {pct_programa:.1f}% de la población infantil tiene acceso a programas sociales, superando el 50% del total."
            )
        else:
            render_insight(
                "Baja Cobertura de Programas",
                f"Solo el {pct_programa:.1f}% de la población infantil tiene acceso a programas sociales. Se recomienda ampliar la cobertura."
            )
    
    with col2:
        if pob_prom > 45:
            render_insight(
                "Nivel de Pobreza Alto",
                f"El índice de pobreza promedio es del {pob_prom:.1f}%, superando el umbral del 45% considerado como alto."
            )
        else:
            render_insight(
                "Nivel de Pobreza Moderado",
                f"El índice de pobreza promedio es del {pob_prom:.1f}%, manteniéndose por debajo del umbral del 45%."
            )

# ============================================
# SECCIÓN PROGRAMAS SOCIALES
# ============================================

def seccion_programas():
    scroll_to_top()
    render_main_header()
    
    df = obtener_datos_completos(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    stats = obtener_estadisticas(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    total = stats['total_personas'].iloc[0]
    con_programa = stats['total_con_programa'].iloc[0]
    juntos = stats['total_juntos'].iloc[0]
    cuna = stats['total_cuna_mas'].iloc[0]
    sin_programa = total - con_programa
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#3b82f6;"><i class="fas fa-users"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Total</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        pct_j = (juntos / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#3b82f6;"><i class="fas fa-handshake"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">JUNTOS</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{juntos:,}</div>
            <div style="font-size:12px;color:#64748b;">{pct_j:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        pct_c = (cuna / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#f97316;"><i class="fas fa-school"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">CUNA MÁS</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{cuna:,}</div>
            <div style="font-size:12px;color:#64748b;">{pct_c:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        pct_s = (sin_programa / total * 100) if total > 0 else 0
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#ef4444;"><i class="fas fa-times-circle"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Sin Programa</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{sin_programa:,}</div>
            <div style="font-size:12px;color:#64748b;">{pct_s:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráfica 1: Distribución de Programas Sociales
    render_section_card("Distribución de Programas Sociales", "fa-chart-pie", "Análisis de la cobertura de programas sociales en la población infantil")
    
    df_prog = df.groupby('programa_social').size().reset_index(name='frecuencia')
    fig = crear_grafico_pastel_moderno(df_prog, 'programa_social', 'frecuencia', 
                                       'Distribución de Programas Sociales')
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # Gráfica 2: Programas Sociales por Distrito
    render_section_card("Programas Sociales por Distrito", "fa-chart-bar")
    
    df_prog_dist = df.groupby(['nombre_distrito', 'programa_social']).size().reset_index(name='frecuencia')
    dist_order = df.groupby('nombre_distrito').size().sort_values(ascending=False).head(20).index.tolist()
    df_prog_dist = df_prog_dist[df_prog_dist['nombre_distrito'].isin(dist_order)]
    
    if not df_prog_dist.empty:
        order = df_prog_dist.groupby('nombre_distrito')['frecuencia'].sum().sort_values(ascending=True).index.tolist()
        
        fig = px.bar(
            df_prog_dist,
            x='frecuencia',
            y='nombre_distrito',
            color='programa_social',
            title='Programas Sociales por Distrito',
            labels={'frecuencia': 'Número de Beneficiarios', 'nombre_distrito': 'Distrito'},
            barmode='stack',
            orientation='h',
            color_discrete_sequence=['#3b82f6', '#f97316', '#94a3b8', '#22c55e', '#ef4444'],
            text_auto=True
        )
        fig.update_layout(
            font=dict(family='Inter, sans-serif', size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=max(460, len(order) * 35),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='center',
                x=0.5,
                font=dict(size=11, family='Inter'),
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor='#e2e8f0',
                borderwidth=1
            ),
            title=dict(
                text='Programas Sociales por Distrito',
                font=dict(size=20, weight=700, color='#0f172a', family='Inter'),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(t=85, b=50, l=50, r=30),
            xaxis=dict(
                gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=11, family='Inter'),
                title=dict(text='Número de Beneficiarios', font=dict(size=14, weight=600, color='#0f172a'))
            ),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.04)',
                tickfont=dict(size=11, family='Inter'),
                title=dict(text='Distrito', font=dict(size=14, weight=600, color='#0f172a')),
                categoryorder='array',
                categoryarray=order
            ),
            hoverlabel=dict(
                font=dict(size=12, family='Inter'),
                bgcolor='white',
                bordercolor='#e2e8f0'
            )
        )
        fig.update_traces(
            marker_line_width=1,
            marker_line_color='white',
            textfont=dict(size=10, weight='bold', family='Inter'),
            opacity=0.9
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    render_section_card("Detalle de Beneficiarios", "fa-table")
    df_prog.columns = ['Programa Social', 'Beneficiarios']
    total_prog = df_prog['Beneficiarios'].sum()
    df_prog['Porcentaje'] = (df_prog['Beneficiarios'] / total_prog * 100).round(1)
    
    st.markdown(f'''
    <div class="table-container">
        {df_prog.to_html(index=False, escape=False)}
    </div>
    ''', unsafe_allow_html=True)
    close_section_card()

# ============================================
# SECCIÓN INGRESO FAMILIAR
# ============================================

def seccion_ingreso():
    scroll_to_top()
    render_main_header()
    
    df = obtener_datos_completos(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    stats = obtener_estadisticas(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    total = stats['total_personas'].iloc[0]
    ing_prom = stats['ingreso_promedio'].iloc[0]
    ing_min = stats['ingreso_minimo'].iloc[0]
    ing_max = stats['ingreso_maximo'].iloc[0]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#22c55e;"><i class="fas fa-money-bill-wave"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Ingreso Promedio</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">S/ {ing_prom:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#ef4444;"><i class="fas fa-arrow-down"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Ingreso Mínimo</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">S/ {ing_min:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#22c55e;"><i class="fas fa-arrow-up"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Ingreso Máximo</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">S/ {ing_max:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#3b82f6;"><i class="fas fa-users"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Total Personas</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRÁFICA 1: Acceso a Programas según Nivel de Ingreso
    df['nivel_ingreso'] = pd.cut(
        df['ingreso_familiar'],
        bins=[-float('inf'), 1000, 3000, float('inf')],
        labels=['Bajo (< S/1000)', 'Medio (S/1000-3000)', 'Alto (> S/3000)']
    )
    
    orden_ingreso = ['Bajo (< S/1000)', 'Medio (S/1000-3000)', 'Alto (> S/3000)']
    df['nivel_ingreso'] = pd.Categorical(df['nivel_ingreso'], categories=orden_ingreso, ordered=True)
    
    df_ingreso = df.groupby(['nivel_ingreso', 'programa_social']).size().reset_index(name='frecuencia')
    df_ingreso = df_ingreso.sort_values(['nivel_ingreso', 'programa_social'])
    
    render_section_card("Acceso a Programas según Nivel de Ingreso", "fa-chart-bar")
    
    fig = crear_grafico_barras_agrupadas(
        df_ingreso, 'nivel_ingreso', 'frecuencia', 'programa_social',
        'Acceso a Programas Sociales según Nivel de Ingreso',
        'Nivel de Ingreso', 'Número de Beneficiarios',
        colores={'CUNA MAS': '#f97316', 'JUNTOS': '#3b82f6', 'Sin programa': '#94a3b8'},
        ancho_barra=0.35
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # GRÁFICA 2: Ingreso Promedio por Distrito
    render_section_card("Ingreso Promedio por Distrito", "fa-chart-line")
    
    fig = crear_grafico_tendencia_ingreso(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    render_section_card("Detalle por Nivel de Ingreso", "fa-table")
    df_pivot = df_ingreso.pivot(index='nivel_ingreso', columns='programa_social', values='frecuencia').fillna(0)
    df_pivot['Total'] = df_pivot.sum(axis=1)
    crear_tabla_bidimensional(df_pivot, "Distribución por Nivel de Ingreso")
    close_section_card()

# ============================================
# SECCIÓN NÚMERO DE HIJOS
# ============================================

def seccion_hijos():
    scroll_to_top()
    render_main_header()
    
    df = obtener_datos_completos(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    stats = obtener_estadisticas(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    total = stats['total_personas'].iloc[0]
    hijos_prom = stats['hijos_promedio'].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#8b5cf6;"><i class="fas fa-people-arrows"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Promedio Hijos/Hogar</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{hijos_prom:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#3b82f6;"><i class="fas fa-users"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Total Personas</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        max_hijos = df['nro_hijos'].max()
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#f97316;"><i class="fas fa-arrow-up"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Máximo Hijos</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{max_hijos:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRÁFICA 1: Acceso a Programas según Número de Hijos
    df['categoria_hijos'] = pd.cut(
        df['nro_hijos'],
        bins=[-float('inf'), 1, 3, float('inf')],
        labels=['0-1 hijos', '2-3 hijos', '4+ hijos']
    )
    
    orden_hijos = ['0-1 hijos', '2-3 hijos', '4+ hijos']
    df['categoria_hijos'] = pd.Categorical(df['categoria_hijos'], categories=orden_hijos, ordered=True)
    
    df_hijos = df.groupby(['categoria_hijos', 'programa_social']).size().reset_index(name='frecuencia')
    df_hijos = df_hijos.sort_values(['categoria_hijos', 'programa_social'])
    
    render_section_card("Acceso a Programas según Número de Hijos", "fa-chart-bar")
    
    fig = crear_grafico_barras_agrupadas(
        df_hijos, 'categoria_hijos', 'frecuencia', 'programa_social',
        'Acceso a Programas Sociales según Número de Hijos',
        'Número de Hijos', 'Número de Beneficiarios',
        colores={'CUNA MAS': '#f97316', 'JUNTOS': '#3b82f6', 'Sin programa': '#94a3b8'},
        ancho_barra=0.35
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # GRÁFICA 2: Distribución de Hogares por Número de Hijos
    render_section_card("Distribución de Hogares por Número de Hijos", "fa-chart-bar")
    
    df_hijos_agrupado = df.groupby('categoria_hijos').size().reset_index(name='cantidad')
    df_hijos_agrupado = df_hijos_agrupado.sort_values('categoria_hijos')
    
    fig = crear_grafico_barras_agrupadas(
        df_hijos_agrupado, 'categoria_hijos', 'cantidad', None,
        'Distribución de Hogares por Número de Hijos',
        'Número de Hijos', 'Número de Hogares',
        colores=['#8b5cf6']
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # Tabla bidimensional: Programa Social vs Número de Hijos
    render_section_card("Detalle por Número de Hijos", "fa-table")
    df_pivot_hijos = df_hijos.pivot(index='programa_social', columns='categoria_hijos', values='frecuencia').fillna(0)
    df_pivot_hijos['Total'] = df_pivot_hijos.sum(axis=1)
    crear_tabla_bidimensional(df_pivot_hijos, "Distribución por Programa Social y Número de Hijos")
    close_section_card()

# ============================================
# SECCIÓN ÍNDICE DE POBREZA
# ============================================

def seccion_pobreza():
    scroll_to_top()
    render_main_header()
    
    df = obtener_datos_completos(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    stats = obtener_estadisticas(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    total = stats['total_personas'].iloc[0]
    pob_prom = stats['pobreza_promedio'].iloc[0]
    pob_min = stats['pobreza_minimo'].iloc[0]
    pob_max = stats['pobreza_maximo'].iloc[0]
    pobres = stats['hogares_pobreza_alta'].iloc[0]
    pct_pobres = (pobres / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#f97316;"><i class="fas fa-chart-line"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Pobreza Promedio</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{pob_prom:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#22c55e;"><i class="fas fa-arrow-down"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Pobreza Mínima</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{pob_min:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#ef4444;"><i class="fas fa-arrow-up"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Pobreza Máxima</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{pob_max:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#ef4444;"><i class="fas fa-exclamation-triangle"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Pobreza Alta (>45%)</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{pobres:,}</div>
            <div style="font-size:12px;color:#64748b;">{pct_pobres:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRÁFICA 1: Acceso a Programas según Nivel de Pobreza
    df['nivel_pobreza'] = pd.cut(
        df['indice_pobreza'],
        bins=[-float('inf'), 30, 45, float('inf')],
        labels=['Bajo (≤30%)', 'Medio (30-45%)', 'Alto (>45%)']
    )
    
    orden_pobreza = ['Bajo (≤30%)', 'Medio (30-45%)', 'Alto (>45%)']
    df['nivel_pobreza'] = pd.Categorical(df['nivel_pobreza'], categories=orden_pobreza, ordered=True)
    
    df_pobreza = df.groupby(['nivel_pobreza', 'programa_social']).size().reset_index(name='frecuencia')
    df_pobreza = df_pobreza.sort_values(['nivel_pobreza', 'programa_social'])
    
    render_section_card("Acceso a Programas según Nivel de Pobreza", "fa-chart-bar")
    
    fig = crear_grafico_barras_agrupadas(
        df_pobreza, 'nivel_pobreza', 'frecuencia', 'programa_social',
        'Acceso a Programas Sociales según Nivel de Pobreza',
        'Nivel de Pobreza', 'Número de Beneficiarios',
        colores={'CUNA MAS': '#f97316', 'JUNTOS': '#3b82f6', 'Sin programa': '#94a3b8'},
        ancho_barra=0.35
    )
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    
    # GRÁFICA 2: Índice de Pobreza por Distrito
    render_section_card("Índice de Pobreza por Distrito", "fa-chart-line")
    
    fig = crear_grafico_tendencia_pobreza(df)
    if fig:
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    close_section_card()
    
    st.markdown("---")
    render_section_card("Detalle por Nivel de Pobreza", "fa-table")
    df_pivot = df_pobreza.pivot(index='nivel_pobreza', columns='programa_social', values='frecuencia').fillna(0)
    df_pivot['Total'] = df_pivot.sum(axis=1)
    crear_tabla_bidimensional(df_pivot, "Distribución por Nivel de Pobreza")
    close_section_card()

# ============================================
# SECCIÓN ANÁLISIS SOCIOECONÓMICO
# ============================================

def seccion_analisis_socioeconomico():
    scroll_to_top()
    render_main_header()
    
    df = obtener_datos_analisis_socioeconomico(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    if df.empty:
        st.warning("No se encontraron datos para el filtro seleccionado.")
        return
    
    stats = obtener_estadisticas(
        st.session_state.filtro_provincia_id,
        st.session_state.filtro_distrito_id
    )
    
    total = stats['total_personas'].iloc[0]
    ing_prom = stats['ingreso_promedio'].iloc[0]
    pob_prom = stats['pobreza_promedio'].iloc[0]
    hijos_prom = stats['hijos_promedio'].iloc[0]
    con_programa = stats['total_con_programa'].iloc[0]
    pct_programa = (con_programa / total * 100) if total > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#3b82f6;"><i class="fas fa-users"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Total</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{total:,}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#22c55e;"><i class="fas fa-money-bill-wave"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Ingreso Prom.</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">S/ {ing_prom:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#f97316;"><i class="fas fa-chart-line"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Pobreza Prom.</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{pob_prom:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#8b5cf6;"><i class="fas fa-people-arrows"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Prom. Hijos</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{hijos_prom:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div style="background:#ffffff;border-radius:14px;padding:18px 20px;border:1px solid #e2e8f0;">
            <div style="font-size:18px;color:#22c55e;"><i class="fas fa-hand-holding-heart"></i></div>
            <div style="font-size:11px;font-weight:600;color:#64748b;text-transform:uppercase;">Con Programa</div>
            <div style="font-size:28px;font-weight:800;color:#0f172a;">{pct_programa:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabla general por distrito (interactiva y clickeable)
    render_section_card("Resumen General por Distrito", "fa-table", 
                       "Tabla interactiva con todos los distritos - Haz click en las columnas para ordenar")
    
    df_distrito = df.groupby('nombre_distrito').agg({
        'id_persona': 'count',
        'ingreso_familiar': 'mean',
        'indice_pobreza': 'mean',
        'nro_hijos': 'mean'
    }).reset_index()
    df_distrito.columns = ['Distrito', 'Total', 'Ingreso Promedio', 'Índice de Pobreza', 'Prom. Hijos']
    df_distrito = df_distrito.sort_values('Total', ascending=False)
    
    st.dataframe(
        df_distrito,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Distrito": st.column_config.TextColumn("Distrito", width="medium"),
            "Total": st.column_config.NumberColumn("Total Personas", format="%d"),
            "Ingreso Promedio": st.column_config.NumberColumn("Ingreso Promedio", format="S/ %.0f"),
            "Índice de Pobreza": st.column_config.NumberColumn("Índice de Pobreza", format="%.1f%%"),
            "Prom. Hijos": st.column_config.NumberColumn("Prom. Hijos", format="%.1f")
        }
    )
    close_section_card()
    
    st.markdown("---")
    
    # MAPA DE POBREZA PARA YUNGAY
    render_section_card("Mapa de Nivel de Pobreza por Centro Poblado", "fa-map", 
                       "Visualización geoespacial de los niveles de pobreza en la provincia de Yungay")
    
    try:
        from streamlit_folium import folium_static
        mapa = crear_mapa_pobreza_yungay(df)
        if mapa:
            folium_static(mapa, width=1100, height=650)
        else:
            st.info("No hay suficientes datos para generar el mapa.")
    except ImportError:
        st.warning("Para ver el mapa, instala: pip install folium streamlit-folium")
    except Exception as e:
        st.error(f"Error al generar el mapa: {e}")
    
    close_section_card()
    
    st.markdown("---")
    
    # Gráficas de tendencia
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_card("Ingreso Promedio por Distrito", "fa-chart-line")
        fig = crear_grafico_tendencia_ingreso(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        close_section_card()
    
    with col2:
        render_section_card("Índice de Pobreza por Distrito (Top 20)", "fa-chart-line")
        fig = crear_grafico_tendencia_pobreza(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        close_section_card()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_card("Distribución de Hogares por Número de Hijos", "fa-chart-bar")
        fig = crear_grafico_barras_hijos(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        close_section_card()
    
    with col2:
        render_section_card("Correlación con Programas Sociales", "fa-link")
        fig = crear_grafico_correlacion_variables(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        close_section_card()

# ============================================
# NAVEGACIÓN PRINCIPAL
# ============================================

secciones_map = {
    "Características": seccion_caracteristicas,
    "Programas Sociales": seccion_programas,
    "Ingreso Familiar": seccion_ingreso,
    "Número de Hijos": seccion_hijos,
    "Índice de Pobreza": seccion_pobreza,
    "Análisis Socioeconómico": seccion_analisis_socioeconomico
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

st.markdown("""
<div class="footer">
    <i class="fas fa-university"></i> <strong>Universidad Nacional "Santiago Antúnez de Mayolo"</strong> · 
    Facultad de Ciencias · Escuela Profesional de Estadística e Informática
    <br>
    <i class="fas fa-calendar-alt"></i> Investigación Formativa · 2025
</div>
""", unsafe_allow_html=True)
