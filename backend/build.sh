#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 TFG Idealista Backend Build Script"
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"

# Actualizar pip y herramientas de build
pip install --upgrade pip setuptools wheel

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalaciones críticas
echo "✅ Django version: $(python -c 'import django; print(django.get_version())')"
echo "✅ Pandas version: $(python -c 'import pandas; print(pandas.__version__)')"

# Colectar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate

echo "🚀 Build completed successfully!"