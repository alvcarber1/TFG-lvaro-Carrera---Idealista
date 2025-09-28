import streamlit as st
import pandas as pd
import requests
from pathlib import Path
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="TFG Idealista - Análisis Inmobiliario Madrid",
    page_icon="🏠",
    layout="wide"
)

# ✅ CONFIGURACIÓN DE LA API PARA PRODUCCIÓN Y DESARROLLO
API_BASE_URL = os.getenv('BACKEND_URL', 'https://tfg-idealista-backend.onrender.com')

# ✅ TÍTULO CORREGIDO
st.title('🏠 TFG Idealista - Análisis del Mercado Inmobiliario Madrid')
st.markdown("**Álvaro Carrera** - Clustering de 6,735 propiedades con Machine Learning")

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Información del Proyecto")
    st.info("""
    **TFG - Análisis Inmobiliario Madrid:**
    1. 📊 Dataset: 6,735 propiedades reales de Idealista
    2. 🤖 ML: K-means clustering (5 segmentos)
    3. 📍 Cobertura: Todos los distritos de Madrid
    4. 🎯 Precisión: Silhouette Score 0.280

    **Tecnología:**
    - Backend: Django + scikit-learn
    - Frontend: Streamlit + Folium
    - Deploy: Render + Vercel
    """)
    
    # ✅ ESTADO DE CONEXIÓN CON BACKEND
    st.header("🔗 Estado del Sistema")
    try:
        response = requests.get(f"{API_BASE_URL}/api/", timeout=10)
        if response.status_code == 200:
            st.success("✅ Backend conectado")
        else:
            st.error(f"❌ Backend error: {response.status_code}")
    except Exception as e:
        st.error(f"❌ Sin conexión: {str(e)[:50]}...")
    
    st.info(f"🌐 Backend: {API_BASE_URL}")

# ✅ FUNCIÓN CORREGIDA PARA CARGAR DISTRITOS
@st.cache_data
def cargar_distritos_barrios():
    try:
        posibles_paths = [
            Path("districts_data.json"),
            Path("src/districts_data.json"),
            Path("frontend/src/districts_data.json")
        ]
        for path in posibles_paths:
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
    except Exception as e:
        st.warning(f"No se pudo cargar districts_data.json: {e}")
    # DATOS COMPLETOS DE MADRID
    return {
        "districts": [
            "Arganzuela", "Barajas", "Carabanchel", "Centro", "Chamartín", 
            "Chamberí", "Ciudad Lineal", "Fuencarral-El Pardo", "Hortaleza",
            "Latina", "Moncloa-Aravaca", "Moratalaz", "Puente de Vallecas",
            "Retiro", "Salamanca", "San Blas-Canillejas", "Tetuán",
            "Usera", "Vicálvaro", "Villa de Vallecas", "Villaverde"
        ],
        "neighborhoods_by_district": {
            "Centro": ["Sol", "Malasaña", "Chueca", "La Latina", "Lavapiés"],
            "Salamanca": ["Recoletos", "Goya", "Lista", "Castellana"],
            "Chamberí": ["Arapiles", "Trafalgar", "Almagro", "Vallehermoso"],
            "Retiro": ["Pacífico", "Adelfas", "Estrella", "Ibiza"],
            "Chamartín": ["El Viso", "Prosperidad", "Ciudad Jardín", "Hispanoamérica"],
            "Moncloa-Aravaca": ["Moncloa", "Aravaca", "Casa de Campo", "Arguelles"],
            "Tetuán": ["Bellas Vistas", "Cuatro Caminos", "Castillejos", "Almenara"],
            "Arganzuela": ["Imperial", "Acacias", "Chopera", "Legazpi"],
            "Carabanchel": ["Vista Alegre", "Puerta Bonita", "Abrantes", "Opañel"]
        }
    }

# ✅ FUNCIÓN CORREGIDA PARA CLUSTERING CON ENDPOINT REAL
@st.cache_data(ttl=300)
def cargar_clustering():
    try:
        response = requests.get(f"{API_BASE_URL}/api/clustering/", timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict) and 'properties' in data:
                return pd.DataFrame(data['properties']), None
            elif isinstance(data, list):
                return pd.DataFrame(data), None
            else:
                return pd.DataFrame(data), None
        else:
            return None, f"Error {response.status_code}: {response.text[:100]}"
    except requests.exceptions.RequestException as e:
        try:
            response = requests.get(f"{API_BASE_URL}/api/properties/", timeout=15)
            if response.status_code == 200:
                return pd.DataFrame(response.json()), None
        except Exception:
            pass
        return None, f"Error de conexión: {str(e)[:100]}"

# ✅ COORDENADAS EXACTAS DE MADRID
COORDENADAS_DISTRITOS = {
    "Centro": (40.4165, -3.7026),
    "Salamanca": (40.4309, -3.6763),
    "Chamberí": (40.4378, -3.7044),
    "Retiro": (40.4153, -3.6838),
    "Chamartín": (40.4607, -3.6774),
    "Moncloa-Aravaca": (40.4364, -3.7411),
    "Tetuán": (40.4659, -3.6993),
    "Arganzuela": (40.3973, -3.6993),
    "Carabanchel": (40.3815, -3.7363),
    "Latina": (40.3963, -3.7617),
    "Fuencarral-El Pardo": (40.5123, -3.7174),
    "Hortaleza": (40.4751, -3.6543),
    "Ciudad Lineal": (40.4567, -3.6234),
    "Usera": (40.3856, -3.6987),
    "Puente de Vallecas": (40.3912, -3.6543),
    "Moratalaz": (40.4078, -3.6421),
    "Villaverde": (40.3456, -3.7123),
    "Villa de Vallecas": (40.3723, -3.6234),
    "Vicálvaro": (40.3987, -3.6012),
    "San Blas-Canillejas": (40.4387, -3.6012),
    "Barajas": (40.4723, -3.5789)
}

# ✅ SECCIÓN PRINCIPAL: ANÁLISIS DE CLUSTERING
st.header("📊 Análisis de Propiedades por Clusters")

# Cargar datos de clustering
df_clusters, error = cargar_clustering()

if error:
    st.error(f"Error cargando datos: {error}")
    st.info("💡 Verifica que el backend esté funcionando correctamente")
else:
    if df_clusters is not None and not df_clusters.empty:
        # ✅ MOSTRAR MÉTRICAS GENERALES
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Propiedades", len(df_clusters))
        
        with col2:
            if 'cluster' in df_clusters.columns:
                st.metric("Clusters", df_clusters['cluster'].nunique())
            else:
                st.metric("Clusters", "N/A")
        
        with col3:
            if 'buy_price' in df_clusters.columns:
                precio_medio = df_clusters['buy_price'].mean()
                st.metric("Precio Medio", f"€{precio_medio:,.0f}")
            else:
                st.metric("Precio Medio", "N/A")
        
        with col4:
            if 'sq_mt_built' in df_clusters.columns:
                superficie_media = df_clusters['sq_mt_built'].mean()
                st.metric("Superficie Media", f"{superficie_media:.0f} m²")
            else:
                st.metric("Superficie Media", "N/A")

        # ✅ PESTAÑAS PARA DIFERENTES ANÁLISIS
        tab1, tab2, tab3 = st.tabs(["🗺️ Mapa Interactivo", "📊 Análisis por Clusters", "📈 Estadísticas"])
        
        with tab1:
            st.subheader("🗺️ Distribución Geográfica de Propiedades")
            
            # ✅ FILTROS DINÁMICOS
            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                if 'buy_price' in df_clusters.columns:
                    min_precio = int(df_clusters['buy_price'].min())
                    max_precio = int(df_clusters['buy_price'].max())
                    precio_filtro = st.slider(
                        "Rango de precio (€)",
                        min_precio, max_precio, 
                        (min_precio, max_precio),
                        step=50000
                    )
                else:
                    precio_filtro = None
            
            with col_filtro2:
                if 'district' in df_clusters.columns:
                    distritos_disponibles = ["Todos"] + sorted(df_clusters['district'].unique().tolist())
                    distrito_filtro = st.selectbox("Filtrar por distrito", distritos_disponibles)
                else:
                    distrito_filtro = "Todos"
            
            with col_filtro3:
                if 'cluster' in df_clusters.columns:
                    clusters_disponibles = ["Todos"] + sorted(df_clusters['cluster'].unique().tolist())
                    cluster_filtro = st.selectbox("Filtrar por cluster", clusters_disponibles)
                else:
                    cluster_filtro = "Todos"
            
            # ✅ APLICAR FILTROS
            df_filtrado = df_clusters.copy()
            
            if precio_filtro and 'buy_price' in df_clusters.columns:
                df_filtrado = df_filtrado[
                    (df_filtrado['buy_price'] >= precio_filtro[0]) & 
                    (df_filtrado['buy_price'] <= precio_filtro[1])
                ]
            
            if distrito_filtro != "Todos" and 'district' in df_clusters.columns:
                df_filtrado = df_filtrado[df_filtrado['district'] == distrito_filtro]
            
            if cluster_filtro != "Todos" and 'cluster' in df_clusters.columns:
                df_filtrado = df_filtrado[df_filtrado['cluster'] == cluster_filtro]
            
            # ✅ MAPA BÁSICO CON STREAMLIT
            if not df_filtrado.empty and 'latitude' in df_filtrado.columns and 'longitude' in df_filtrado.columns:
                st.metric("Propiedades mostradas", len(df_filtrado))
                
                # Preparar datos para el mapa
                map_data = df_filtrado[['latitude', 'longitude']].dropna()
                
                if not map_data.empty:
                    st.map(map_data, zoom=11)
                else:
                    st.warning("No hay coordenadas válidas para mostrar en el mapa")
            else:
                st.warning("No hay datos de ubicación disponibles")
        
        with tab2:
            st.subheader("📊 Análisis Detallado por Clusters")
            
            if 'cluster' in df_clusters.columns:
                # ✅ RESUMEN POR CLUSTER
                numeric_cols = df_clusters.select_dtypes(include=['number']).columns.tolist()
                if 'cluster' in numeric_cols:
                    numeric_cols.remove('cluster')
                
                if numeric_cols:
                    cluster_summary = df_clusters.groupby('cluster')[numeric_cols].agg(['mean', 'count']).round(2)
                    st.dataframe(cluster_summary, use_container_width=True)
                
                # GRÁFICO DE DISPERSIÓN
                if 'buy_price' in df_clusters.columns and 'sq_mt_built' in df_clusters.columns:
                    import plotly.express as px
                    fig = px.scatter(
                        df_clusters.head(1000),
                        x='sq_mt_built',
                        y='buy_price',
                        color='cluster',
                        title="Distribución Precio vs Superficie por Cluster",
                        labels={
                            'sq_mt_built': 'Superficie (m²)',
                            'buy_price': 'Precio (€)',
                            'cluster': 'Cluster'
                        },
                        hover_data=['district'] if 'district' in df_clusters.columns else None
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No se encontraron datos de clustering")
        
        with tab3:
            st.subheader("📈 Estadísticas Descriptivas")
            
            # ✅ TABLA DE ESTADÍSTICAS
            numeric_data = df_clusters.select_dtypes(include=['number'])
            if not numeric_data.empty:
                st.dataframe(numeric_data.describe(), use_container_width=True)
            
            # DISTRIBUCIONES
            if 'buy_price' in df_clusters.columns:
                col_hist1, col_hist2 = st.columns(2)
                with col_hist1:
                    import plotly.express as px
                    fig_hist = px.histogram(
                        df_clusters.head(1000),
                        x='buy_price',
                        nbins=30,
                        title="Distribución de Precios"
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                with col_hist2:
                    if 'sq_mt_built' in df_clusters.columns:
                        fig_hist2 = px.histogram(
                            df_clusters.head(1000),
                            x='sq_mt_built',
                            nbins=30,
                            title="Distribución de Superficies"
                        )
                        st.plotly_chart(fig_hist2, use_container_width=True)
        
        # ✅ MOSTRAR MUESTRA DE DATOS
        with st.expander("📋 Ver muestra de datos", expanded=False):
            # Seleccionar columnas más relevantes
            cols_importantes = ['buy_price', 'sq_mt_built', 'n_rooms', 'district', 'cluster', 'latitude', 'longitude']
            cols_mostrar = [col for col in cols_importantes if col in df_clusters.columns]
            
            if cols_mostrar:
                st.dataframe(df_clusters[cols_mostrar].head(100), use_container_width=True)
            else:
                st.dataframe(df_clusters.head(100), use_container_width=True)

    else:
        st.warning("No hay datos de clustering disponibles en este momento")
        st.info("💡 El backend puede estar cargando los datos o no estar disponible")

# ✅ PREDICTOR SIMPLIFICADO (OPCIONAL - MANTENER SOLO SI LA API EXISTE)
if st.checkbox("🔮 Habilitar Predictor de Precios (Experimental)", value=False):
    st.header("💰 Predictor Experimental de Precios")
    st.warning("⚠️ Esta función requiere endpoints específicos en el backend")
    
    # Solo mostrar un formulario básico
    with st.form("prediccion_simple"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            superficie = st.number_input("Superficie (m²)", min_value=20, max_value=500, value=80)
            habitaciones = st.selectbox("Habitaciones", [1, 2, 3, 4, 5], index=2)
        
        with col2:
            distrito = st.selectbox("Distrito", ["Centro", "Salamanca", "Chamberí", "Retiro"])
            año = st.slider("Año construcción", 1950, 2024, 2000)
        
        with col3:
            lat = COORDENADAS_DISTRITOS[distrito][0]
            lon = COORDENADAS_DISTRITOS[distrito][1]
            st.info(f"Coordenadas: {lat:.3f}, {lon:.3f}")
        
        if st.form_submit_button("Estimar Precio"):
            precios_base = {"Centro": 4500, "Salamanca": 5000, "Chamberí": 4200, "Retiro": 4800}
            precio_estimado = superficie * precios_base.get(distrito, 4000)
            st.success(f"💰 Precio estimado: €{precio_estimado:,.0f}")
            st.info("📝 Esta es una estimación básica basada en promedios de mercado")

# ✅ PIE DE PÁGINA
st.markdown("---")
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("**🎓 TFG - Álvaro Carrera**")
    st.caption("Análisis del Mercado Inmobiliario Madrid")

with col_footer2:
    st.markdown("**🛠️ Stack Tecnológico**")
    st.caption("Django + Streamlit + scikit-learn + Folium")

with col_footer3:
    st.markdown("**📊 Dataset**")
    st.caption("6,735 propiedades reales de Idealista")