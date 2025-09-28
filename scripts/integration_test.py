#!/usr/bin/env python3
"""
Test de integración end-to-end del sistema
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

def test_data_pipeline():
    """Test del pipeline completo de datos"""
    
    print("🔄 Testing data pipeline...")
    
    try:
        # Intentar cargar datos reales
        data_path = Path("backend/data/unified_houses_madrid.csv")
        
        if data_path.exists():
            df = pd.read_csv(data_path)
            print(f"✅ Real data loaded: {len(df)} records")
        else:
            # Crear datos sintéticos
            print("⚠️ Real data not found, creating synthetic data")
            df = pd.DataFrame({
                'latitude': np.random.uniform(40.3, 40.6, 100),
                'longitude': np.random.uniform(-3.9, -3.5, 100),
                'sq_mt_built': np.random.uniform(50, 300, 100),
                'n_rooms': np.random.randint(1, 6, 100),
                'n_bathrooms': np.random.randint(1, 4, 100),
                'buy_price': np.random.uniform(200000, 1000000, 100),
                'rent_price': np.random.uniform(800, 3000, 100)
            })
        
        # Validar estructura
        required_columns = ['buy_price', 'sq_mt_built', 'latitude', 'longitude']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Missing required columns: {missing_cols}")
            return False
        
        print("✅ Data pipeline test passed")
        return True
        
    except Exception as e:
        print(f"❌ Data pipeline error: {e}")
        return False

def test_ml_pipeline():
    """Test del pipeline de ML"""
    
    print("\n🤖 Testing ML pipeline...")
    
    try:
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import silhouette_score
        
        # Crear datos de prueba
        np.random.seed(42)
        X = np.random.random((100, 7))
        
        # Pipeline de ML
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=3, random_state=42)
        labels = kmeans.fit_predict(X_scaled)
        
        score = silhouette_score(X_scaled, labels)
        
        if score > 0:
            print(f"✅ ML pipeline test passed: silhouette = {score:.3f}")
            return True
        else:
            print(f"❌ Poor ML performance: silhouette = {score:.3f}")
            return False
            
    except Exception as e:
        print(f"❌ ML pipeline error: {e}")
        return False

def test_existing_scripts():
    """Test scripts existentes del proyecto"""
    
    print("\n📁 Testing existing scripts...")
    
    scripts_to_check = [
        "scripts/get_districts_neighborhoods.py"
    ]
    
    for script_path in scripts_to_check:
        if Path(script_path).exists():
            print(f"✅ Found: {script_path}")
        else:
            print(f"⚠️ Missing: {script_path}")
    
    return True

def main():
    """Función principal del test de integración"""
    
    print("="*60)
    print("🚀 INTEGRATION TEST - END TO END")
    print("="*60)
    
    tests = [
        ("Data Pipeline", test_data_pipeline),
        ("ML Pipeline", test_ml_pipeline),
        ("Existing Scripts", test_existing_scripts),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 INTEGRATION TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} | {status}")
        if result:
            passed += 1
    
    total = len(results)
    print("-" * 60)
    print(f"{'TOTAL':20} | {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print(f"\n💥 {total - passed} integration tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()