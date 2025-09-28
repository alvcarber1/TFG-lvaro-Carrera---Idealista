import os
import sys
import pandas as pd
import joblib
import pytest
import numpy as np

# Cambiar al directorio backend

print("=== PRUEBA SIMPLE DE PREDICCIÓN ===")

try:
    # Cargar el modelo y preprocessor
    preprocessor = joblib.load('data/models/preprocessor.joblib')
    modelo = joblib.load('data/models/mejor_modelo.joblib')
    print("✅ Modelos cargados")
    
    # Cargar datos de muestra
    data_sample = pd.read_csv('data/unified_houses_madrid.csv').iloc[:1]
    print(f"Muestra de datos: {data_sample.shape}")
    
    # Limpiar y convertir tipos de datos
    print("\nLimpiando datos...")
    data_clean = data_sample.copy()
    
    # Convertir columnas numéricas
    numeric_cols = ['sq_mt_built', 'sq_mt_useful', 'n_rooms', 'n_bathrooms', 
                   'floor', 'built_year', 'buy_price_by_area', 'latitude', 'longitude']
    
    for col in numeric_cols:
        if col in data_clean.columns:
            data_clean[col] = pd.to_numeric(data_clean[col], errors='coerce')
            data_clean[col] = data_clean[col].fillna(0)
    
    # Convertir columnas binarias
    binary_cols = ['has_lift', 'is_exterior', 'has_parking', 'is_new_development',
                  'has_central_heating', 'has_individual_heating', 'has_ac',
                  'has_garden', 'has_pool', 'has_terrace', 'has_storage_room',
                  'is_furnished', 'is_orientation_north', 'is_orientation_south',
                  'is_orientation_east', 'is_orientation_west']
    
    for col in binary_cols:
        if col in data_clean.columns:
            data_clean[col] = data_clean[col].astype(str).str.lower()
            data_clean[col] = data_clean[col].map({'true': 1.0, 'false': 0.0, 'nan': 0.0, '1.0': 1.0, '0.0': 0.0})
            data_clean[col] = data_clean[col].fillna(0.0).astype(float)
    
    # Convertir categóricas
    categorical_cols = ['house_type', 'energy_certificate', 'district', 'neighborhood']
    for col in categorical_cols:
        if col in data_clean.columns:
            data_clean[col] = data_clean[col].astype(str).fillna('NO_DISPONIBLE')
    
    # Seleccionar columnas y predecir
    all_cols = numeric_cols + binary_cols + categorical_cols
    available_cols = [col for col in all_cols if col in data_clean.columns]
    X_clean = data_clean[available_cols]
    
    X_transformed = preprocessor.transform(X_clean)
    prediction = modelo.predict(X_transformed)
    print(f"✅ Predicción exitosa: {prediction[0]:.2f} €")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

class TestModelSimple:
    """Tests básicos para modelos simples"""
    
    def test_simple_linear_relationship(self):
        """Test relación lineal simple entre precio y metros cuadrados"""
        # Crear datos sintéticos con relación lineal
        np.random.seed(42)
        sq_mt = np.random.uniform(50, 200, 100)
        price = sq_mt * 3000 + np.random.normal(0, 10000, 100)  # 3000€/m² + ruido
        
        df = pd.DataFrame({
            'sq_mt_built': sq_mt,
            'buy_price': price
        })
        
        # Calcular correlación
        correlation = df['sq_mt_built'].corr(df['buy_price'])
        
        assert correlation > 0.8, f"Correlation should be strong positive, got {correlation:.3f}"
        print(f"✓ Linear relationship test passed: correlation = {correlation:.3f}")
    
    def test_price_per_sqm_calculation(self):
        """Test cálculo de precio por metro cuadrado"""
        test_data = pd.DataFrame({
            'buy_price': [300000, 450000, 600000],
            'sq_mt_built': [100, 150, 200]
        })
        
        # Calcular precio por m²
        test_data['price_per_sqm'] = test_data['buy_price'] / test_data['sq_mt_built']
        
        expected_prices = [3000, 3000, 3000]
        
        for i, expected in enumerate(expected_prices):
            calculated = test_data.iloc[i]['price_per_sqm']
            assert abs(calculated - expected) < 0.01, f"Price per sqm calculation failed for row {i}"
        
        print("✓ Price per sqm calculation test passed")
    
    def test_data_validation_simple(self):
        """Test validación simple de datos"""
        # Datos con algunos valores inválidos
        test_data = pd.DataFrame({
            'buy_price': [300000, -50000, 450000, 0, 600000],
            'sq_mt_built': [100, 120, -10, 150, 200],
            'n_rooms': [2, 3, 4, 0, 5]
        })
        
        # Filtrar datos válidos
        valid_data = test_data[
            (test_data['buy_price'] > 0) & 
            (test_data['sq_mt_built'] > 0) & 
            (test_data['n_rooms'] > 0)
        ]
        
        assert len(valid_data) == 2, f"Should have 2 valid records, got {len(valid_data)}"
        print(f"✓ Data validation test passed: {len(valid_data)} valid records")
    
    def test_basic_statistics(self):
        """Test estadísticas básicas"""
        np.random.seed(42)
        prices = np.random.uniform(200000, 800000, 100)
        
        df = pd.DataFrame({'buy_price': prices})
        
        # Calcular estadísticas
        mean_price = df['buy_price'].mean()
        median_price = df['buy_price'].median()
        std_price = df['buy_price'].std()
        
        # Verificaciones básicas
        assert 200000 <= mean_price <= 800000, "Mean should be within expected range"
        assert 200000 <= median_price <= 800000, "Median should be within expected range"
        assert std_price > 0, "Standard deviation should be positive"
        
        print(f"✓ Basic statistics test passed: mean={mean_price:.0f}, median={median_price:.0f}")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])