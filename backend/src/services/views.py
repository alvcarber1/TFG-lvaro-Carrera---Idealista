
from django.http import JsonResponse, HttpResponse
import joblib
import pandas as pd
import folium
import os
import numpy as np
from src.services.custom_transformers import convert_to_float
from django.views.decorators.csrf import csrf_exempt
import json

# Las cargas de modelos se hacen dentro de las funciones/vistas


# Vista para el análisis causal
def get_causal_relationships():
    results = joblib.load('data/models/pcmci_results.joblib')
    graph = results['graph']
    var_names = results['var_names'] if 'var_names' in results else list(range(len(graph)))
    relaciones = []
    for i, var1 in enumerate(var_names):
        for j, var2 in enumerate(var_names):
            relation = graph[i][j]
            if isinstance(relation, (np.ndarray, list)):
                for lag, rel in enumerate(relation):
                    if rel:
                        relaciones.append(f"{var1} {rel} {var2} (lag={lag})")
            else:
                if relation:
                    relaciones.append(f"{var1} {relation} {var2}")
    return relaciones


# Vista para el clustering
from django.http import JsonResponse
import pandas as pd
import joblib

def clustering_table_view(request):
    # Cargar los datos originales
    datos_originales = pd.read_csv('data/unified_houses_madrid.csv')

    # Cargar el modelo y preprocesador solo cuando se usa
    preprocessor = joblib.load('data/models/preprocessor_kmeans.joblib')
    pca = joblib.load('data/models/pca_kmeans.joblib')
    kmeans_model = joblib.load('data/models/kmeans_model.joblib')

    # Seleccionar columnas relevantes
    columnas_usadas = ['latitude', 'longitude', 'sq_mt_built', 'n_rooms', 'n_bathrooms', 'buy_price', 'rent_price']
    datos_filtrados = datos_originales[columnas_usadas].fillna(datos_originales[columnas_usadas].median())

    # Preprocesar y clusterizar
    datos_preprocesados = preprocessor.transform(datos_filtrados)
    datos_pca = pca.transform(datos_preprocesados)
    clusters = kmeans_model.predict(datos_pca)
    datos_originales['cluster_kmeans'] = clusters

    # Filtrar por parámetros GET (ejemplo: ?cluster=1&min_price=100000)
    cluster = request.GET.get('cluster')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    df = datos_originales
    if cluster is not None:
        df = df[df['cluster_kmeans'] == int(cluster)]
    if min_price is not None:
        df = df[df['buy_price'] >= float(min_price)]
    if max_price is not None:
        df = df[df['buy_price'] <= float(max_price)]

    # Seleccionar columnas para la tabla
    columns_to_show = ['id', 'address', 'sq_mt_built', 'n_rooms', 'n_bathrooms', 'buy_price', 'rent_price', 'cluster_kmeans']
    table_json = df[columns_to_show].to_dict(orient='records')

    return JsonResponse(table_json, safe=False)


# Vista para la visualización geográfica
def geographic_visualization_view(request):
    file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
        'notebooks',
        'madrid_clusters_kmeans_map.html'
    )
    with open(file_path, 'r', encoding='utf-8') as file:
        map_html = file.read()
    return HttpResponse(map_html, content_type='text/html')

@csrf_exempt
def xgboost_prediction_view(request):
    print("Método recibido:", request.method)
    try:
        # Cargar el preprocesador y el modelo solo cuando se usa
        preprocessor = joblib.load('data/models/preprocessor.joblib')
        mejor_modelo = joblib.load('data/models/mejor_modelo.joblib')
        
        # Debug: Verificar el tipo y estado del modelo
        print(f"Tipo de modelo: {type(mejor_modelo)}")
        print(f"¿Tiene método predict?: {hasattr(mejor_modelo, 'predict')}")
        print(f"¿Es XGBRegressor?: {type(mejor_modelo).__name__ == 'XGBRegressor'}")

        if request.method == 'POST':
            # Obtener los datos del formulario
            form_data = request.POST
            print("Datos recibidos:", dict(form_data))
            
            # Convertir datos a formato del modelo
            try:
                data = {}
                
                # Campos numéricos con valores por defecto
                data['sq_mt_built'] = float(form_data.get('size', 100))
                data['sq_mt_useful'] = float(form_data.get('useful_size', form_data.get('size', 100)))
                data['n_rooms'] = int(form_data.get('rooms', 3))
                data['n_bathrooms'] = int(form_data.get('bathrooms', 2))
                data['floor'] = int(form_data.get('floor', 1))
                data['built_year'] = int(form_data.get('built_year', 2000))
                data['buy_price_by_area'] = float(form_data.get('price_by_area', 3000))
                data['latitude'] = float(form_data.get('latitude', 40.4168))
                data['longitude'] = float(form_data.get('longitude', -3.7038))
                
                # Inicializar todos los campos binarios en 0
                binary_fields = ['has_lift', 'is_exterior', 'has_parking', 'is_new_development',
                               'has_central_heating', 'has_individual_heating', 'has_ac',
                               'has_garden', 'has_pool', 'has_terrace', 'has_storage_room',
                               'is_furnished', 'is_orientation_north', 'is_orientation_south',
                               'is_orientation_east', 'is_orientation_west']
                
                for field in binary_fields:
                    data[field] = 0.0
                
                # Mapeo de campos del formulario a campos del modelo
                form_to_model_binary = {
                    'has_lift': 'has_lift',
                    'is_exterior': 'is_exterior', 
                    'has_parking_space': 'has_parking',
                    'has_air_conditioning': 'has_ac',
                    'has_garden': 'has_garden',
                    'has_swimming_pool': 'has_pool',
                    'has_terrace': 'has_terrace',
                    'has_box_room': 'has_storage_room',
                    'is_furnished': 'is_furnished'
                }
                
                # Actualizar con los valores del formulario
                for form_field, model_field in form_to_model_binary.items():
                    if form_field in form_data:
                        data[model_field] = 1.0 if form_data.get(form_field) == 'true' else 0.0
                
                # Campos categóricos
                data['house_type'] = 1  # Asumimos tipo flat por defecto
                data['energy_certificate'] = form_data.get('energy_certificate', 'E')
                data['district'] = form_data.get('district', 'Centro')
                data['neighborhood'] = form_data.get('neighborhood', 'Sol')
                
                print("Datos procesados:", data)
                
                # Crear DataFrame
                df = pd.DataFrame([data])
                print(f"DataFrame creado: {df.shape}")
                print(f"Columnas del DataFrame: {list(df.columns)}")
                
                # LIMPIEZA DE DATOS (igual que en test_simple.py)
                print("Aplicando limpieza de datos...")
                
                # Cargar estructura de datos de muestra para completar columnas faltantes
                sample_data = pd.read_csv('data/unified_houses_madrid.csv').iloc[:1]
                expected_columns = sample_data.columns.tolist()
                
                # Agregar columnas faltantes con valores por defecto
                missing_columns = set(expected_columns) - set(df.columns)
                if missing_columns:
                    print(f"Agregando columnas faltantes: {len(missing_columns)}")
                    for col in missing_columns:
                        if col in binary_fields:
                            df[col] = 0.0
                        else:
                            df[col] = sample_data[col].iloc[0] if col in sample_data.columns else 0
                
                # Reordenar columnas para que coincidan
                df = df.reindex(columns=expected_columns, fill_value=0)
                
                # Convertir tipos de datos explícitamente
                numeric_cols = ['sq_mt_built', 'sq_mt_useful', 'n_rooms', 'n_bathrooms', 
                               'floor', 'built_year', 'buy_price_by_area', 'latitude', 'longitude']
                
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                # Convertir columnas binarias explícitamente
                for col in binary_fields:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(float)
                
                # Asegurar que las columnas categóricas sean strings
                categorical_cols = ['house_type', 'energy_certificate', 'district', 'neighborhood']
                for col in categorical_cols:
                    if col in df.columns:
                        df[col] = df[col].astype(str).fillna('unknown')
                
                print(f"DataFrame después de limpieza: {df.shape}")
                print(f"Valores NaN: {df.isna().sum().sum()}")
                
                # Preprocesar los datos
                df_transformed = preprocessor.transform(df)
                print(f"Datos transformados: {df_transformed.shape}")

                # Realizar predicción
                prediction = mejor_modelo.predict(df_transformed)
                print(f"Predicción realizada: {prediction[0]}")

                # Devolver resultado
                return JsonResponse({'prediction': float(prediction[0])})
                
            except (ValueError, KeyError) as e:
                print(f"Error procesando datos: {e}")
                return JsonResponse({'error': f'Error en los datos: {e}'}, status=400)
        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)

    except Exception as e:
        print("ERROR XGBOOST:", e)
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=400)