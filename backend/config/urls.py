"""
URL configuration for config project.
TFG Idealista - Álvaro Carrera
API REST para el frontend Streamlit
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

# ✅ MANTENER TUS VIEWS EXISTENTES PERO AGREGAR API
from src.services.views import clustering_table_view, geographic_visualization_view, xgboost_prediction_view

def api_root(request):
    """Endpoint raíz de la API para el frontend"""
    return JsonResponse({
        'message': 'TFG Idealista API - Álvaro Carrera',
        'version': '1.0.0',
        'description': 'Análisis del mercado inmobiliario Madrid con Machine Learning',
        'endpoints': {
            'properties': '/api/properties/',
            'clustering': '/api/clustering/',
            'predict': '/api/predict/',
            'admin': '/admin/',
        },
        'legacy_endpoints': {
            'clustering_table': '/clustering/',
            'geographic_viz': '/geographic-visualization/',
            'xgboost': '/xgboost/',
        },
        'status': 'active',
        'total_properties': 6735,
        'clusters': 5,
        'deployment': 'production' if not settings.DEBUG else 'development'
    })

urlpatterns = [
    # ✅ ADMIN
    path('admin/', admin.site.urls),
    
    # ✅ API REST PARA STREAMLIT (NUEVAS)
    path('api/', api_root, name='api_root'),
    path('api/', include('src.services.api_urls')),  # URLs de la API REST
    
    # ✅ VIEWS EXISTENTES (MANTENER PARA COMPATIBILIDAD)
    path('clustering/', clustering_table_view, name='clustering'),
    path('geographic-visualization/', geographic_visualization_view, name='geographic_visualization'),
    path('xgboost/', xgboost_prediction_view, name='xgboost'),
]

# ✅ SERVIR ARCHIVOS ESTÁTICOS EN DESARROLLO
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)