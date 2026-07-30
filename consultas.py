# consultas.py - Todas las consultas SQL centralizadas

# ============================================
# CONSULTAS GENERALES PARA YUNGAY
# ============================================

TOTAL_POBLACION = """
SELECT COUNT(*) as total
FROM PERSONA p
INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
WHERE pr.nombre_provincia = 'YUNGAY'
"""

DISTRIBUCION_SEXO = """
SELECT
    p.sexo,
    COUNT(*) AS frecuencia,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS porcentaje
FROM PERSONA p
INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY p.sexo
"""

DISTRIBUCION_EDAD = """
SELECT
    p.edad_anios,
    COUNT(*) AS frecuencia,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS porcentaje
FROM PERSONA p
INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY p.edad_anios
ORDER BY p.edad_anios
"""

VARIABLES_SOCIOECONOMICAS = """
SELECT
    MIN(f.ingreso_familiar) AS ingreso_minimo,
    MAX(f.ingreso_familiar) AS ingreso_maximo,
    AVG(f.ingreso_familiar) AS ingreso_promedio,
    MIN(f.nro_hijos) AS hijos_minimo,
    MAX(f.nro_hijos) AS hijos_maximo,
    AVG(CAST(f.nro_hijos AS FLOAT)) AS hijos_promedio,
    MIN(f.indice_pobreza) AS pobreza_minima,
    MAX(f.indice_pobreza) AS pobreza_maxima,
    AVG(f.indice_pobreza) AS pobreza_promedio
FROM PERSONA p
INNER JOIN FAMILIA f ON p.id_familia = f.id_familia
INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
WHERE pr.nombre_provincia = 'YUNGAY'
"""

ACCESO_PROGRAMAS = """
SELECT
    CASE
        WHEN ps.nombre_programa IS NULL THEN 'SIN PROGRAMA'
        ELSE ps.nombre_programa
    END AS programa_social,
    COUNT(DISTINCT p.id_persona) AS cantidad,
    ROUND(COUNT(DISTINCT p.id_persona) * 100.0 / 
          SUM(COUNT(DISTINCT p.id_persona)) OVER(), 2) AS porcentaje
FROM PERSONA p
INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY 
    CASE
        WHEN ps.nombre_programa IS NULL THEN 'SIN PROGRAMA'
        ELSE ps.nombre_programa
    END
ORDER BY cantidad DESC
"""

INGRESO_VS_PROGRAMA = """
SELECT
    CASE 
        WHEN f.ingreso_familiar < 1000 THEN 'Bajo'
        WHEN f.ingreso_familiar BETWEEN 1000 AND 3000 THEN 'Medio'
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
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY 
    CASE 
        WHEN f.ingreso_familiar < 1000 THEN 'Bajo'
        WHEN f.ingreso_familiar BETWEEN 1000 AND 3000 THEN 'Medio'
        ELSE 'Alto'
    END,
    CASE 
        WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
        ELSE ps.nombre_programa
    END
ORDER BY nivel_ingreso, programa_social
"""

HIJOS_VS_PROGRAMA = """
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
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY
    CASE
        WHEN f.nro_hijos <= 1 THEN '0 - 1 hijos'
        WHEN f.nro_hijos <= 3 THEN '2 - 3 hijos'
        ELSE '4 o más hijos'
    END,
    CASE
        WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
        ELSE ps.nombre_programa
    END
ORDER BY categoria_hijos, programa_social
"""

POBREZA_VS_PROGRAMA = """
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
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY
    CASE
        WHEN f.indice_pobreza <= 30 THEN 'Bajo'
        WHEN f.indice_pobreza <= 45 THEN 'Medio'
        ELSE 'Alto'
    END,
    CASE
        WHEN ps.nombre_programa IS NULL THEN 'Sin programa'
        ELSE ps.nombre_programa
    END
ORDER BY nivel_pobreza, programa_social
"""

RESULTADOS_DISTRITO = """
SELECT
    d.nombre_distrito,
    COUNT(DISTINCT p.id_persona) AS total_menores,
    COUNT(DISTINCT CASE WHEN ps.nombre_programa = 'JUNTOS' THEN p.id_persona END) AS juntos,
    COUNT(DISTINCT CASE WHEN ps.nombre_programa = 'CUNA MAS' THEN p.id_persona END) AS cuna_mas,
    COUNT(DISTINCT CASE WHEN ps.nombre_programa IS NULL THEN p.id_persona END) AS sin_programa
FROM PERSONA p
INNER JOIN CENTRO_POBLADO cp ON p.id_centro_poblado = cp.id_centro_poblado
INNER JOIN DISTRITO d ON cp.id_distrito = d.id_distrito
INNER JOIN PROVINCIA pr ON d.id_provincia = pr.id_provincia
LEFT JOIN PERSONA_PROGRAMA pp ON p.id_persona = pp.id_persona
LEFT JOIN PROGRAMA_SOCIAL ps ON pp.id_programa = ps.id_programa
WHERE pr.nombre_provincia = 'YUNGAY'
GROUP BY d.nombre_distrito
ORDER BY total_menores DESC
"""

CENTROS_POBLADOS_YUNGAY = """
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

POBREZA_POR_CENTRO = """
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