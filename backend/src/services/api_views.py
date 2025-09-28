from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import pandas as pd
import joblib
from pathlib import Path
import numpy as np

class PropertyListAPIView(APIView):
    def get(self, request):
        try:
            data_path = Path(settings.BASE_DIR) / 'data' / 'unified_houses_madrid.csv'
            df = pd.read_csv(data_path)
            # Filtros
            min_price = request.GET.get('min_price')
            max_price = request.GET.get('max_price')
            district = request.GET.get('district')
            if min_price:
                df = df[df['buy_price'] >= float(min_price)]
            if max_price:
                df = df[df['buy_price'] <= float(max_price)]
            if district and district != 'Todos':
                df = df[df['district'] == district]
            limit = min(int(request.GET.get('limit', 1000)), 2000)
            df = df.head(limit)
            # 🔧 Limpia NaN, inf, -inf antes de convertir a dict (JSON compliant)
            df = df.replace([np.nan, np.inf, -np.inf], None)
            return Response({'count': len(df), 'properties': df.to_dict('records')})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class ClusteringAPIView(APIView):
    def get(self, request):
        try:
            data_path = Path(settings.BASE_DIR) / 'data' / 'unified_houses_madrid.csv'
            df = pd.read_csv(data_path)
            model_path = Path(settings.BASE_DIR) / 'data' / 'models' / 'kmeans_model.joblib'
            if model_path.exists():
                model = joblib.load(model_path)
                if 'cluster' not in df.columns:
                    # Usa solo las features con las que fue entrenado el modelo (ejemplo: latitude y longitude)
                    features = ['latitude', 'longitude']
                    available_features = [col for col in features if col in df.columns]
                    if len(available_features) == 2:
                        X = df[available_features].fillna(df[available_features].mean())
                        clusters = model.predict(X)
                        df['cluster'] = clusters
                    else:
                        return Response({'error': 'No se encontraron las columnas necesarias para clustering: latitude y longitude'}, status=400)
            if 'cluster' not in df.columns:
                df['cluster'] = pd.cut(df['buy_price'], bins=5, labels=[0,1,2,3,4])
            limit = min(int(request.GET.get('limit', 2000)), 3000)
            df = df.head(limit)
            # 🔧 Limpia NaN, inf, -inf antes de convertir a dict (JSON compliant)
            df = df.replace([np.nan, np.inf, -np.inf], None)
            return Response({'properties': df.to_dict('records'), 'total_properties': len(df)})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PredictAPIView(APIView):
    def get(self, request):
        return Response({'error': 'Método GET no permitido. Usa POST para predicción.'}, status=405)
    def post(self, request):
        try:
            data = request.data
            buy_price = float(data.get('buy_price', 0))
            if buy_price < 300000:
                cluster, segment = 0, "Económico"
            elif buy_price < 500000:
                cluster, segment = 1, "Medio-Bajo"
            elif buy_price < 800000:
                cluster, segment = 2, "Medio"
            elif buy_price < 1200000:
                cluster, segment = 3, "Medio-Alto"
            else:
                cluster, segment = 4, "Lujo"
            return Response({'cluster': cluster, 'segment': segment, 'confidence': 0.75})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class PropertiesAPIView(APIView):
    def get(self, request):
        try:
            data_path = Path(settings.BASE_DIR) / 'data' / 'unified_houses_madrid.csv'
            df = pd.read_csv(data_path)
            # 🔧 Limpia NaN, inf, -inf antes de convertir a dict (JSON compliant)
            df = df.replace([np.nan, np.inf, -np.inf], None)
            return Response({'count': len(df), 'properties': df.to_dict('records')})
        except Exception as e:
            return Response({'error': str(e)}, status=500)