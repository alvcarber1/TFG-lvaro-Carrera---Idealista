#!/usr/bin/env bash
set -o errexit

echo "🎨 TFG Idealista Frontend - Streamlit Deployment"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Actualizar pip y instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Verificar instalación de Streamlit
echo "Streamlit version: $(streamlit version)"

# Crear directorio de configuración
mkdir -p .streamlit

# Verificar estructura de archivos
echo "Verificando estructura:"
ls -la src/

# Iniciar Streamlit
echo "Iniciando aplicación Streamlit..."
streamlit run src/app.py \
  --server.port $PORT \
  --server.address 0.0.0.0 \
  --server.headless true \
  --browser.gatherUsageStats false