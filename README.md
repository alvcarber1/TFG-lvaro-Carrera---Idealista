# 🏠 TFG Alvaro Carrera - Idealista Housing Analysis

## 📋 Descripción del Proyecto

Aplicación web completa para el análisis y predicción de precios de viviendas en Madrid utilizando técnicas de Machine Learning y análisis geoespacial.

## 🏗️ Arquitectura del Sistema

### Backend (Django)
- **Framework**: Django 5.1.5
- **API REST** con endpoints para clustering y predicción
- **Modelo XGBoost** entrenado con R² = 0.9938
- **Preprocessor sklearn** con ColumnTransformer estándar

### Frontend (Streamlit)
- **Interfaz interactiva** para visualización y predicción
- **Formularios dinámicos** con validación
- **Visualizaciones** con Plotly y mapas interactivos
- **Tablas de clustering** con filtros

### Machine Learning
- **XGBoost Regressor**: Predicción de precios
- **K-Means Clustering**: Segmentación geográfica
- **Preprocessing avanzado**: 167 características

## 🚀 Instalación y Configuración

### 1. Crear el Entorno Conda
```bash
conda env create -f environment.yml
conda activate TFG-IDEALISTA
```

### 2. Estructura de Archivos
```
tfg-alvaro-carrera-idealista/
├── backend/                 # Servidor Django
│   ├── data/models/        # Modelos ML entrenados
│   ├── src/services/       # API endpoints
│   └── manage.py
├── frontend/               # Aplicación Streamlit
│   ├── src/app.py         # Interfaz principal
│   └── .streamlit/        # Configuración
├── tests/                  # Scripts de testing
│   ├── test_backend_api.py
│   └── test_model_simple.py
├── scripts/                # Scripts de utilidad
│   ├── run_backend.bat
│   └── run_frontend.bat
├── environment.yml
└── README.md
```

### 3. Ejecución Rápida

#### 🎯 Usando Scripts (Recomendado)
```bash
# 1. Backend
.\scripts\run_backend.bat

# 2. Frontend (nueva terminal)
.\scripts\run_frontend.bat

# 3. Testing
cd tests
python test_backend_api.py
```

#### Manual
```bash
# Backend
cd backend
python manage.py runserver

# Frontend
cd frontend  
streamlit run src/app.py
```

## 📊 Endpoints de la API

### Clustering
```http
GET http://localhost:8000/clustering/
```
Devuelve 6,735 registros de clustering geográfico.

### Predicción XGBoost
```http
POST http://localhost:8000/xgboost/
```

**Parámetros principales:**
- `size`: Metros cuadrados
- `rooms`: Habitaciones
- `bathrooms`: Baños
- `latitude`, `longitude`: Coordenadas
- `has_lift`, `has_parking_space`: Características binarias

**Respuesta:**
```json
{
  "prediction": 303076.34
}
```

## 🧪 Testing

### Probar Backend Completo
```bash
cd tests
python test_backend_api.py
```

### Probar Solo el Modelo
```bash
cd tests
python test_model_simple.py
```

**Resultados Esperados:**
- ✅ Servidor Django: OK
- ✅ Clustering: 6,735 registros
- ✅ Predicción: ~300k € (ejemplo)

## 📈 Rendimiento del Modelo

- **Algoritmo**: XGBoost Regressor
- **R² Score**: 0.9938
- **Features**: 167 características
- **Datos**: 5,388 entrenamiento + 1,347 prueba

### Tipos de Características
- **Numéricas**: metros, habitaciones, coordenadas
- **Binarias**: ascensor, parking, orientación
- **Categóricas**: barrio, distrito, certificado energético

## 📁 Archivos Clave

- `backend/data/models/mejor_modelo.joblib`: Modelo XGBoost
- `backend/data/models/preprocessor.joblib`: Preprocessor
- `frontend/.streamlit/secrets.toml`: Configuración URLs
- `backend/notebooks/model_training.ipynb`: Entrenamiento

## 🔍 Troubleshooting

### ✅ Problemas Resueltos
- **"need to call fit"**: Modelo correctamente entrenado
- **"ufunc isnan"**: Limpieza de tipos implementada
- **Error 404**: URLs actualizadas

### Reinstalar Entorno
```bash
conda env remove -n TFG-IDEALISTA
conda env create -f environment.yml
```

## 🎯 Sprint 4 - Completado ✅

### Funcionalidades Implementadas
- ✅ **Backend Django** con API REST
- ✅ **Frontend Streamlit** interactivo
- ✅ **Modelo XGBoost** R² = 0.9938
- ✅ **Clustering geográfico** 6,735 propiedades
- ✅ **Testing completo** de todos los componentes
- ✅ **Documentación técnica**

### Casos de Uso
- 🎯 Predicción de precios en tiempo real
- 📊 Análisis de clustering geográfico
- 🗺️ Visualización en mapas interactivos
- 📝 Formularios con validación
- 🔌 API REST para integraciones

## 👨‍💻 Autor

**Álvaro Carrera**  
TFG - Análisis de Datos de Viviendas Idealista

## 📄 Licencia

Trabajo de Fin de Grado (TFG) - Uso Académico

---

## 🎉 Estado: ✅ PRODUCCIÓN READY

**Versión**: Sprint 4 Final  
**Fecha**: 27 de Agosto de 2025  
**Testing**: 100% OK

### 🚀 Inicio Rápido
```bash
# Todo en uno:
.\scripts\run_backend.bat    # Terminal 1
.\scripts\run_frontend.bat   # Terminal 2
cd tests && python test_backend_api.py  # Verificar
```

**URLs:**
- 🔧 Backend: http://localhost:8000
- 💻 Frontend: http://localhost:8501
- 📊 API Clustering: http://localhost:8000/clustering/
- 🤖 API Predicción: http://localhost:8000/xgboost/

## 🛠️ Instalación

### Para desarrollo local (Recomendado)
```bash
# Crear entorno conda
conda env create -f environment.yml
conda activate TFG-IDEALISTA
```

### Para instalación simple
```bash
# Instalar dependencias básicas
pip install -r requirements.txt
```

## 🚀 Deployment
- **requirements.txt**: Usado por Render y Streamlit Cloud
- **environment.yml**: Para desarrollo local completo
