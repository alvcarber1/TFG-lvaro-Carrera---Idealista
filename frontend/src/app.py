import streamlit as st
import pandas as pd
import requests
import streamlit.components.v1 as components
import plotly.graph_objects as go
from pathlib import Path
import json
import os

# Configuración de la página
st.set_page_config(
    page_title="Predictor de Precios Inmobiliarios Madrid",
    page_icon="🏠",
    layout="wide"
)

# Configuración de la API
API_BASE_URL = os.getenv('BACKEND_URL', 'https://tfg-idealista-backend.onrender.com')
#API_BASE_URL = 'http://localhost:8000'  # Para pruebas locales

st.title('🏠 Predictor de Precios Inmobiliarios Madrid')

# Sidebar con información
with st.sidebar:
    st.header("ℹ️ Cómo usar esta aplicación")
    st.info("""
    **Pasos simples:**
    1. 📐 Introduce las características básicas de tu vivienda
    2. 📍 Selecciona la ubicación (distrito y barrio)
    3. ✨ Añade características especiales (opcional)
    4. 🔮 ¡Obtén tu predicción de precio!
    
    **Tecnología:**
    - Machine Learning con XGBoost
    - Precisión del 99.38%
    - +6,000 propiedades analizadas
    """)

# Función para cargar datos de distritos y barrios
@st.cache_data
def cargar_distritos_barrios():
    try:
        # Intentar cargar desde el archivo JSON
        json_path = Path("districts_data.json")
        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    
    # Datos por defecto si no existe el archivo
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
            "Chamartín": ["El Viso", "Prosperidad", "Ciudad Jardín", "Hispanoamérica"]
        }
    }

# Función para validar coordenadas de Madrid
def validar_coordenadas(lat, lon):
    return (40.3 <= lat <= 40.6) and (-3.9 <= lon <= -3.5)

# Función para cargar datos de clustering
@st.cache_data(ttl=300)
def cargar_clustering():
    try:
        response = requests.get(f"{API_BASE_URL}/clustering/", timeout=10)
        if response.status_code == 200:
            return pd.DataFrame(response.json()), None
        else:
            return None, f"Error {response.status_code}: {response.text}"
    except requests.exceptions.RequestException as e:
        return None, f"Error de conexión: {str(e)}"

# Coordenadas aproximadas por distrito (centro del distrito)
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

# Mostrar tabla dinámica de clustering
st.header("📊 Análisis de Propiedades por Clusters")
df_clusters, error = cargar_clustering()

if error:
    st.error(error)
else:
    if df_clusters is not None and not df_clusters.empty:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Mostrar una muestra de los datos con columnas seleccionadas
            if len(df_clusters.columns) > 10:
                # Mostrar solo las columnas más relevantes
                cols_importantes = ['latitude', 'longitude', 'cluster', 'sq_mt_built', 'n_rooms', 'buy_price']
                cols_mostrar = [col for col in cols_importantes if col in df_clusters.columns]
                st.dataframe(df_clusters[cols_mostrar].head(100), use_container_width=True)
            else:
                st.dataframe(df_clusters.head(100), use_container_width=True)
        
        with col2:
            st.metric("Total propiedades", len(df_clusters))
            if 'cluster' in df_clusters.columns:
                st.metric("Clusters identificados", df_clusters['cluster'].nunique())
    else:
        st.warning("No hay datos de clustering disponibles.")

# Formulario MEJORADO para predicción XGBoost
st.header("💰 Predictor de Precio de Vivienda")

# Cargar datos de distritos y barrios
distritos_data = cargar_distritos_barrios()

# **SELECTORES DINÁMICOS FUERA DEL FORMULARIO**
st.subheader("📍 Selecciona la ubicación")
col_dist, col_barr = st.columns(2)

with col_dist:
    district = st.selectbox(
        "Distrito", 
        distritos_data["districts"], 
        index=distritos_data["districts"].index("Centro") if "Centro" in distritos_data["districts"] else 0,
        key="district_dynamic"
    )

with col_barr:
    # 🔄 BARRIOS SE ACTUALIZAN AUTOMÁTICAMENTE
    barrios_disponibles = distritos_data["neighborhoods_by_district"].get(district, ["Otros"])
    if len(barrios_disponibles) == 0:
        barrios_disponibles = ["Otros"]
    
    neighborhood = st.selectbox(
        "Barrio", 
        barrios_disponibles,
        key="neighborhood_dynamic"
    )

# Coordenadas automáticas basadas en el distrito
coords_distrito = COORDENADAS_DISTRITOS.get(district, (40.4168, -3.7038))

# **FORMULARIO CON EL RESTO DE CAMPOS**
with st.form("prediccion_form"):
    # Sección 1: Características básicas (SIMPLIFICADAS)
    st.subheader("🏠 Características de la vivienda")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📐 Tamaño y distribución**")
        sq_mt_built = st.number_input("Metros cuadrados totales", min_value=20, max_value=800, value=80, step=5, 
                                     help="Superficie total de la vivienda")
        n_rooms = st.selectbox("Habitaciones", [1, 2, 3, 4, 5, 6, 7], index=2)
        n_bathrooms = st.selectbox("Baños", [1, 2, 3, 4, 5], index=1)
        floor = st.number_input("Planta", min_value=0, max_value=30, value=2, 
                               help="0 = Planta baja")
    
    with col2:
        st.write("**🏗️ Información del edificio**")
        built_year = st.slider("Año de construcción", min_value=1950, max_value=2025, value=2000)
        house_type = st.selectbox("Tipo de vivienda", 
                                 ["piso", "ático", "estudio", "dúplex", "chalet"], 
                                 help="Tipo de inmueble")
        energy_certificate = st.selectbox("Certificado energético", 
                                        ["A", "B", "C", "D", "E", "F", "G", "En trámite"],
                                        index=2)
    
    with col3:
        st.write("**📍 Coordenadas GPS (se calculan automáticamente)**")
        st.info(f"📍 **Distrito:** {district}\n📍 **Barrio:** {neighborhood}")
        
        with st.expander("🔧 Ajustar coordenadas manualmente (avanzado)", expanded=False):
            col_lat, col_lon = st.columns(2)
            with col_lat:
                latitude = st.number_input("Latitud", format="%.4f", value=coords_distrito[0], step=0.001)
            with col_lon:
                longitude = st.number_input("Longitud", format="%.4f", value=coords_distrito[1], step=0.001)
        
        # Si no se expande, usar coordenadas automáticas
        if "latitude" not in locals():
            latitude = coords_distrito[0]
            longitude = coords_distrito[1]

    # Sección 2: Características especiales (OPCIONALES)
    with st.expander("✨ Características especiales (opcional)", expanded=False):
        st.write("**Mejora tu predicción añadiendo características especiales:**")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.write("🏢 **Edificio**")
            has_lift = st.checkbox("Ascensor")
            has_parking = st.checkbox("Plaza de garaje")
            is_new_development = st.checkbox("Obra nueva")
        
        with col_b:
            st.write("🌡️ **Climatización**")
            has_central_heating = st.checkbox("Calefacción central")
            has_individual_heating = st.checkbox("Calefacción individual")
            has_ac = st.checkbox("Aire acondicionado")
        
        with col_c:
            st.write("🌿 **Extras**")
            is_exterior = st.checkbox("Vivienda exterior", value=True)
            has_terrace = st.checkbox("Terraza")
            has_storage_room = st.checkbox("Trastero")
            is_furnished = st.checkbox("Amueblado")

    # Sección 3: Precios de referencia (OPCIONAL)
    with st.expander("💰 Precios de referencia para comparar (opcional)", expanded=False):
        col_ref1, col_ref2 = st.columns(2)
        with col_ref1:
            buy_price = st.number_input("¿Tienes un precio de referencia? (€)", min_value=0, value=0, step=10000, 
                                       help="Opcional: precio que has visto en portales inmobiliarios")
        with col_ref2:
            rent_price = st.number_input("¿Precio de alquiler de referencia? (€/mes)", min_value=0, value=0, step=50, 
                                        help="Opcional: para calcular rentabilidad")

    # Botón de predicción prominente
    st.markdown("---")
    submitted = st.form_submit_button("🔮 **PREDECIR PRECIO**", use_container_width=True, type="primary")
    
    if submitted:
        # Validaciones básicas
        errores = []
        if sq_mt_built < 20:
            errores.append("La vivienda debe tener al menos 20 metros cuadrados")
        if not validar_coordenadas(latitude, longitude):
            errores.append("Las coordenadas no corresponden a Madrid")
        
        if errores:
            for error in errores:
                st.error(f"❌ {error}")
        else:
            # Calcular automáticamente metros útiles (aprox. 85% de los construidos)
            sq_mt_useful = round(sq_mt_built * 0.85, 1)
            
            # Calcular precio por m² estimado basado en el distrito
            precios_por_distrito = {
                "Centro": 4500, "Salamanca": 5000, "Chamberí": 4200, 
                "Retiro": 4800, "Chamartín": 4600, "Moncloa-Aravaca": 4000,
                "Tetuán": 3500, "Arganzuela": 3800, "Carabanchel": 2800,
                "Latina": 3200, "Fuencarral-El Pardo": 3600, "Hortaleza": 3400,
                "Ciudad Lineal": 3300, "Usera": 2600, "Puente de Vallecas": 2700,
                "Moratalaz": 3100, "Villaverde": 2500, "Villa de Vallecas": 2600,
                "Vicálvaro": 2800, "San Blas-Canillejas": 3000, "Barajas": 3400
            }
            buy_price_by_area = precios_por_distrito.get(district, 3500)
            
            # Payload con valores calculados automáticamente
            payload = {
                'size': float(sq_mt_built),
                'useful_size': float(sq_mt_useful),
                'rooms': int(n_rooms),
                'bathrooms': int(n_bathrooms),
                'floor': int(floor),
                'built_year': int(built_year),
                'buy_price_by_area': float(buy_price_by_area),
                'latitude': float(latitude),
                'longitude': float(longitude),
                'buy_price': float(buy_price),
                'rent_price': float(rent_price),
                'house_type': str(house_type),
                'energy_certificate': str(energy_certificate),
                'district': str(district),
                'neighborhood': str(neighborhood),
                'has_lift': bool(has_lift),
                'is_exterior': bool(is_exterior),
                'has_parking_space': bool(has_parking),
                'is_new_development': bool(is_new_development),
                'has_central_heating': bool(has_central_heating),
                'has_individual_heating': bool(has_individual_heating),
                'has_ac': bool(has_ac),
                'has_garden': False,  # Por defecto False para pisos
                'has_pool': False,    # Por defecto False 
                'has_terrace': bool(has_terrace),
                'has_storage_room': bool(has_storage_room),
                'is_furnished': bool(is_furnished),
                'is_orientation_north': False,   # Valores por defecto
                'is_orientation_south': True,    # Orientación sur por defecto
                'is_orientation_east': False,
                'is_orientation_west': False
            }
            
            try:
                with st.spinner("🔮 Analizando tu vivienda con IA..."):
                    pred_response = requests.post(
                        f"{API_BASE_URL}/xgboost/", 
                        data=payload,
                        timeout=30
                    )
                
                if pred_response.status_code == 200:
                    resultado = pred_response.json().get('prediction', None)
                    if resultado is not None:
                        # 🎉 RESULTADO EXITOSO
                        st.success("✅ ¡Predicción realizada con éxito!")
                        
                        # Layout de resultados
                        col_resultado1, col_resultado2, col_resultado3 = st.columns([1, 2, 1])
                        
                        with col_resultado2:
                            # Precio principal
                            st.metric(
                                label="💰 **Precio estimado de tu vivienda**", 
                                value=f"{resultado:,.0f} €",
                                delta=f"{resultado - buy_price:,.0f} €" if buy_price > 0 else None
                            )
                            
                            # Información adicional
                            precio_por_m2_real = resultado / sq_mt_built
                            col_info1, col_info2 = st.columns(2)
                            with col_info1:
                                st.info(f"📏 **{precio_por_m2_real:,.0f} €/m²**")
                            with col_info2:
                                if rent_price > 0:
                                    rentabilidad = (rent_price * 12 / resultado * 100)
                                    st.info(f"📈 **Rentabilidad: {rentabilidad:.1f}%**")
                                else:
                                    st.info(f"🏠 **{sq_mt_built} m² • {n_rooms} hab**")

                        # Análisis y consejos
                        st.markdown("---")
                        st.subheader(f"📊 Análisis para {district} - {neighborhood}")
                        
                        col_analisis1, col_analisis2 = st.columns(2)
                        
                        with col_analisis1:
                            # Comparativa con el mercado
                            precio_mercado = buy_price_by_area * sq_mt_built
                            diferencia_mercado = resultado - precio_mercado
                            
                            if diferencia_mercado > 0:
                                st.success(f"📈 Tu vivienda está **{diferencia_mercado:,.0f} €** por encima del precio medio del mercado en {district}")
                            else:
                                st.info(f"📊 Tu vivienda está cerca del precio medio del mercado en {district}")
                        
                        with col_analisis2:
                            # Consejos para mejorar el precio
                            consejos = []
                            if not has_lift and floor > 2:
                                consejos.append("🏢 Un ascensor podría aumentar el valor")
                            if not has_parking:
                                consejos.append("🚗 Una plaza de garaje añadiría valor")
                            if not has_ac:
                                consejos.append("❄️ El aire acondicionado es muy valorado")
                            if built_year < 1990:
                                consejos.append("🔧 Una reforma podría revalorizar mucho")
                            
                            if consejos:
                                st.write("💡 **Consejos para aumentar el valor:**")
                                for consejo in consejos[:2]:  # Máximo 2 consejos
                                    st.write(f"• {consejo}")

                        # Gráfico comparativo
                        fig = go.Figure()
                        
                        # Predicción
                        fig.add_trace(go.Bar(
                            name='🤖 Predicción IA', 
                            x=['Comparativa de Precios'], 
                            y=[resultado], 
                            marker_color='#2E86AB',
                            text=[f'{resultado:,.0f} €'],
                            textposition='auto',
                            textfont_size=14
                        ))
                        
                        # Precio de mercado
                        fig.add_trace(go.Bar(
                            name=f'📊 Precio medio {district}', 
                            x=['Comparativa de Precios'], 
                            y=[precio_mercado], 
                            marker_color='#F18F01',
                            text=[f'{precio_mercado:,.0f} €'],
                            textposition='auto',
                            textfont_size=14
                        ))
                        
                        # Referencias del usuario (si las hay)
                        if buy_price > 0:
                            fig.add_trace(go.Bar(
                                name='💰 Tu referencia', 
                                x=['Comparativa de Precios'], 
                                y=[buy_price], 
                                marker_color='#A23B72',
                                text=[f'{buy_price:,.0f} €'],
                                textposition='auto',
                                textfont_size=14
                            ))
                        
                        fig.update_layout(
                            title=f"📊 Comparativa de Precios - {district}, {neighborhood}",
                            barmode='group',
                            yaxis_title="Precio (€)",
                            showlegend=True,
                            height=400,
                            title_font_size=18
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("⚠️ No se pudo obtener una predicción. Inténtalo de nuevo.")
                else:
                    try:
                        error_msg = pred_response.json().get('error', 'Error desconocido')
                    except:
                        error_msg = pred_response.text
                    st.error(f"❌ Error en la predicción: {error_msg}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error de conexión: {e}")
                st.info("💡 Asegúrate de que el servidor backend esté funcionando")

# Mapa interactivo de clusters
st.header("🗺️ Mapa de Propiedades por Clusters")

# Buscar archivo de mapa
posibles_rutas = [
    Path(__file__).parent / "madrid_clusters_kmeans_map.html",
    Path(__file__).parent.parent / "notebooks" / "madrid_clusters_kmeans_map.html"
]
mapa_encontrado = False
for ruta in posibles_rutas:
    if ruta.exists():
        with open(ruta, "r", encoding="utf-8") as f:
            map_html = f.read()
        components.html(map_html, height=600)
        mapa_encontrado = True
        break

if not mapa_encontrado:
    st.warning("⚠️ No se pudo cargar el mapa interactivo.")
    # Mapa básico de Madrid
    st.info("📍 Vista general de Madrid:")
    map_data = pd.DataFrame({
        'lat': [40.4168],
        'lon': [-3.7038]
    })
    st.map(map_data, zoom=11)