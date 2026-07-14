# exportar_yungay.py
# Script para exportar SOLO los datos de Yungay a SQLite

import pyodbc
import pandas as pd
import sqlite3
import os
import sys

print("=" * 70)
print("🚀 EXPORTANDO DATOS DE YUNGAY A SQLITE")
print("=" * 70)

# ============================================
# PASO 1: CONECTAR A SQL SERVER
# ============================================

print("\n📌 Conectando a SQL Server...")

try:
    conn_sql = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=base_padron;'
        'Trusted_Connection=yes;'
    )
    print("✅ Conexión exitosa a SQL Server")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("\n💡 Soluciones posibles:")
    print("  1. Verifica que SQL Server esté ejecutándose")
    print("  2. Revisa que la base de datos 'base_padron' exista")
    print("  3. Confirma que el driver 'ODBC Driver 17 for SQL Server' esté instalado")
    sys.exit(1)

# ============================================
# PASO 2: OBTENER ID DE YUNGAY
# ============================================

print("\n📌 Buscando la provincia de Yungay...")

df_yungay = pd.read_sql("""
    SELECT id_provincia, nombre_provincia 
    FROM PROVINCIA 
    WHERE nombre_provincia = 'YUNGAY'
""", conn_sql)

if df_yungay.empty:
    print("❌ No se encontró la provincia de YUNGAY en la base de datos")
    print("📌 Provincias disponibles:")
    df_prov_all = pd.read_sql("SELECT nombre_provincia FROM PROVINCIA", conn_sql)
    for prov in df_prov_all['nombre_provincia'].tolist():
        print(f"   - {prov}")
    conn_sql.close()
    sys.exit(1)

yungay_id = df_yungay['id_provincia'].iloc[0]
print(f"✅ YUNGAY encontrada (ID: {yungay_id})")

# ============================================
# PASO 3: EXPORTAR CADA TABLA
# ============================================

print("\n📌 Exportando tablas...")

# 3.1 DEPARTAMENTO (todas)
print("   ⏳ Exportando DEPARTAMENTO...", end=" ")
df_dep = pd.read_sql("SELECT * FROM DEPARTAMENTO", conn_sql)
print(f"✅ {len(df_dep)} registros")

# 3.2 PROVINCIA (todas)
print("   ⏳ Exportando PROVINCIA...", end=" ")
df_prov = pd.read_sql("SELECT * FROM PROVINCIA", conn_sql)
print(f"✅ {len(df_prov)} registros")

# 3.3 DISTRITO (solo Yungay)
print("   ⏳ Exportando DISTRITO (solo Yungay)...", end=" ")
df_dist = pd.read_sql(f"""
    SELECT * FROM DISTRITO 
    WHERE id_provincia = {yungay_id}
""", conn_sql)
print(f"✅ {len(df_dist)} registros")

# 3.4 CENTRO_POBLADO (TODOS los de Yungay, CON o SIN personas)
print("   ⏳ Exportando CENTRO_POBLADO (TODOS los de Yungay)...", end=" ")
df_cp = pd.read_sql(f"""
    SELECT cp.* 
    FROM CENTRO_POBLADO cp
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    WHERE d.id_provincia = {yungay_id}
    ORDER BY cp.nombre_centro_poblado
""", conn_sql)
print(f"✅ {len(df_cp)} registros")

# 3.5 PERSONA (solo Yungay)
print("   ⏳ Exportando PERSONA (solo Yungay)...", end=" ")
df_persona = pd.read_sql(f"""
    SELECT p.* 
    FROM PERSONA p
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    WHERE d.id_provincia = {yungay_id}
""", conn_sql)
print(f"✅ {len(df_persona)} registros")

# 3.6 FAMILIA (solo Yungay)
print("   ⏳ Exportando FAMILIA (solo Yungay)...", end=" ")
df_familia = pd.read_sql(f"""
    SELECT DISTINCT f.* 
    FROM FAMILIA f
    INNER JOIN PERSONA p ON p.id_familia = f.id_familia
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    WHERE d.id_provincia = {yungay_id}
""", conn_sql)
print(f"✅ {len(df_familia)} registros")

# 3.7 DOCUMENTO (solo Yungay)
print("   ⏳ Exportando DOCUMENTO (solo Yungay)...", end=" ")
df_doc = pd.read_sql(f"""
    SELECT DISTINCT doc.* 
    FROM DOCUMENTO doc
    INNER JOIN PERSONA p ON p.id_documento = doc.id_documento
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    WHERE d.id_provincia = {yungay_id}
""", conn_sql)
print(f"✅ {len(df_doc)} registros")

# 3.8 PROGRAMA_SOCIAL (todas)
print("   ⏳ Exportando PROGRAMA_SOCIAL...", end=" ")
df_prog = pd.read_sql("SELECT * FROM PROGRAMA_SOCIAL", conn_sql)
print(f"✅ {len(df_prog)} registros")

# 3.9 PERSONA_PROGRAMA (solo Yungay)
print("   ⏳ Exportando PERSONA_PROGRAMA (solo Yungay)...", end=" ")
df_pp = pd.read_sql(f"""
    SELECT pp.* 
    FROM PERSONA_PROGRAMA pp
    INNER JOIN PERSONA p ON p.id_persona = pp.id_persona
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    WHERE d.id_provincia = {yungay_id}
""", conn_sql)
print(f"✅ {len(df_pp)} registros")

# 3.10 EESS (solo Yungay)
print("   ⏳ Exportando EESS (solo Yungay)...", end=" ")
df_eess = pd.read_sql(f"""
    SELECT DISTINCT e.* 
    FROM EESS e
    INNER JOIN PERSONA p ON p.id_eess = e.id_eess
    INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
    INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
    WHERE d.id_provincia = {yungay_id}
""", conn_sql)
print(f"✅ {len(df_eess)} registros")

# 3.11 MICRORED (todas)
print("   ⏳ Exportando MICRORED...", end=" ")
df_micro = pd.read_sql("SELECT * FROM MICRORED", conn_sql)
print(f"✅ {len(df_micro)} registros")

# 3.12 RED_SALUD (todas)
print("   ⏳ Exportando RED_SALUD...", end=" ")
df_red = pd.read_sql("SELECT * FROM RED_SALUD", conn_sql)
print(f"✅ {len(df_red)} registros")

# 3.13 INSTITUCION (todas)
print("   ⏳ Exportando INSTITUCION...", end=" ")
df_inst = pd.read_sql("SELECT * FROM INSTITUCION", conn_sql)
print(f"✅ {len(df_inst)} registros")

# Cerrar conexión SQL Server
conn_sql.close()
print("\n✅ Todas las tablas exportadas correctamente")

# ============================================
# PASO 4: CREAR SQLITE
# ============================================

print("\n📌 Creando base de datos SQLite...")

# Definir nombre del archivo
DB_NAME = 'base_padron_yungay.db'

# Eliminar archivo anterior si existe
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print(f"   ⚠️ Archivo anterior '{DB_NAME}' eliminado")

# Conectar a SQLite
conn_sqlite = sqlite3.connect(DB_NAME)
print(f"   ✅ Archivo '{DB_NAME}' creado")

# Guardar cada DataFrame
print("\n   Guardando tablas en SQLite...")

tablas = [
    ('DEPARTAMENTO', df_dep),
    ('PROVINCIA', df_prov),
    ('DISTRITO', df_dist),
    ('CENTRO_POBLADO', df_cp),
    ('PERSONA', df_persona),
    ('FAMILIA', df_familia),
    ('DOCUMENTO', df_doc),
    ('PROGRAMA_SOCIAL', df_prog),
    ('PERSONA_PROGRAMA', df_pp),
    ('EESS', df_eess),
    ('MICRORED', df_micro),
    ('RED_SALUD', df_red),
    ('INSTITUCION', df_inst),
]

for nombre, df in tablas:
    print(f"   ⏳ Guardando {nombre}...", end=" ")
    df.to_sql(nombre, conn_sqlite, if_exists='replace', index=False)
    print(f"✅ {len(df)} registros")

# Cerrar conexión SQLite
conn_sqlite.close()

# ============================================
# PASO 5: ESTADÍSTICAS FINALES
# ============================================

print("\n" + "=" * 70)
print("📊 EXPORTACIÓN COMPLETADA EXITOSAMENTE")
print("=" * 70)

size_mb = os.path.getsize(DB_NAME) / 1024 / 1024

print(f"\n📁 Archivo creado: {DB_NAME}")
print(f"📦 Tamaño: {size_mb:.2f} MB")
print(f"\n👶 Personas de Yungay: {len(df_persona):,}")
print(f"🏠 Familias de Yungay: {len(df_familia):,}")
print(f"📍 Distritos de Yungay: {len(df_dist)}")
print(f"🏥 Centros Poblados de Yungay: {len(df_cp)} (TODOS) ✅")
print(f"📄 Documentos: {len(df_doc):,}")
print(f"🔗 Relaciones Programa-Persona: {len(df_pp):,}")

print("\n" + "=" * 70)
print("✅ ¡Listo! Ahora el mapa mostrará TODOS los centros poblados de Yungay")
print("📌 El archivo se llama: base_padron_yungay.db")
print("=" * 70)