import requests
import json

def test_backend_api():
    """Prueba todos los endpoints del backend Django"""
    base_url = "http://localhost:8000"
    
    print("🧪 TESTING BACKEND API")
    print("=" * 50)
    
    results = {
        "server": False,
        "clustering": False,
        "prediction": False
    }
    
    # Test 1: Verificar que el servidor esté funcionando
    print("=== VERIFICANDO ESTADO DEL SERVIDOR ===")
    try:
        response = requests.get(base_url, timeout=5)
        results["server"] = True
        print("✅ Servidor Django está funcionando")
    except requests.exceptions.RequestException:
        print("❌ Servidor Django no responde")
        return results
    
    # Test 2: Endpoint de clustering
    print("=== PROBANDO ENDPOINT DE CLUSTERING ===")
    try:
        response = requests.get(f"{base_url}/clustering/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            results["clustering"] = True
            print(f"✅ Clustering endpoint funciona: {len(data)} registros")
        else:
            print(f"❌ Error clustering: {response.status_code}")
    except Exception as e:
        print(f"❌ Error clustering: {e}")
    
    # Test 3: Endpoint de predicción
    print("=== PROBANDO ENDPOINT DE PREDICCIÓN ===")
    payload = {
        'size': 100,
        'useful_size': 85,
        'rooms': 3,
        'bathrooms': 2,
        'floor': 2,
        'built_year': 2000,
        'buy_price_by_area': 3000,
        'latitude': 40.4168,
        'longitude': -3.7038,
        'buy_price': 300000,
        'rent_price': 1200,
        'house_type': 'piso',
        'energy_certificate': 'C',
        'district': 'Centro',
        'neighborhood': 'Malasaña',
        'has_lift': True,
        'is_exterior': True,
        'has_parking_space': False,
        'is_new_development': False,
        'has_central_heating': True,
        'has_individual_heating': False,
        'has_ac': True,
        'has_garden': False,
        'has_pool': False,
        'has_terrace': True,
        'has_storage_room': False,
        'is_furnished': True,
        'is_orientation_north': False,
        'is_orientation_south': True,
        'is_orientation_east': False,
        'is_orientation_west': False
    }
    
    try:
        response = requests.post(f"{base_url}/xgboost/", data=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            results["prediction"] = True
            print(f"✅ Predicción endpoint funciona: {data.get('prediction', 'N/A')} €")
        else:
            print(f"❌ Error predicción: {response.status_code}")
            print(f"Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Error predicción: {e}")
    
    # Resumen final
    print("=" * 50)
    print("📊 RESUMEN DE PRUEBAS")
    print(f"Servidor Django: {'✅ OK' if results['server'] else '❌ FALLO'}")
    print(f"Endpoint Clustering: {'✅ OK' if results['clustering'] else '❌ FALLO'}")
    print(f"Endpoint Predicción: {'✅ OK' if results['prediction'] else '❌ FALLO'}")
    
    if all(results.values()):
        print("\n🎉 ¡Todos los endpoints funcionan correctamente!")
        print("💡 Ahora puedes ejecutar el frontend con: .\\scripts\\run_frontend.bat")
    else:
        print("\n⚠️ Algunos endpoints fallan. Revisa el servidor Django.")
    
    return results

if __name__ == "__main__":
    test_backend_api()