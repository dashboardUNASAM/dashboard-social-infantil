# conexion.py - Para SQLite (Streamlit Cloud y local)
import sqlite3
import pandas as pd
import streamlit as st
import os

# Nombre del archivo SQLite (DEBE coincidir con el exportado)
DB_PATH = 'base_padron_yungay.db'

@st.cache_data(ttl=3600)  # Cache por 1 hora para mejor rendimiento
def execute_query(query):
    """
    Ejecuta una consulta SQL y retorna un DataFrame
    Usa SQLite para Streamlit Cloud y local
    """
    try:
        # Verificar si existe la base de datos
        if not os.path.exists(DB_PATH):
            st.error(f"❌ No se encontró la base de datos: {DB_PATH}")
            st.info("📌 Asegúrate de tener el archivo en la raíz del proyecto")
            st.info("📌 Si estás en local, ejecuta: python exportar_yungay.py")
            return pd.DataFrame()
        
        # Conectar y ejecutar consulta
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    
    except Exception as e:
        st.error(f"❌ Error al ejecutar consulta: {e}")
        return pd.DataFrame()

# Función de prueba para verificar conexión
def test_connection():
    """Prueba la conexión a SQLite"""
    try:
        df = execute_query("SELECT COUNT(*) as total FROM PERSONA")
        if not df.empty:
            total = df['total'].iloc[0]
            st.success(f"✅ Conexión exitosa! {total:,} personas en Yungay")
            return True
        else:
            st.warning("⚠️ La consulta no retornó datos")
            return False
    except Exception as e:
        st.error(f"❌ Error de conexión: {e}")
        return False