import pandas as pd
import json

# Mapeo de códigos de distrito a nombres
DISTRICT_NAMES = {
    1: "Centro",
    2: "Arganzuela", 
    3: "Retiro",
    4: "Salamanca",
    5: "Chamartín",
    6: "Tetuán",
    7: "Chamberí",
    8: "Fuencarral-El Pardo",
    9: "Moncloa-Aravaca",
    10: "Latina",
    11: "Carabanchel",
    12: "Usera",
    13: "Puente de Vallecas",
    14: "Moratalaz",
    15: "Ciudad Lineal",
    16: "Hortaleza",
    17: "Villaverde",
    18: "Villa de Vallecas",
    19: "Vicálvaro",
    20: "San Blas-Canillejas",
    21: "Barajas"
}

print("📊 Extrayendo distritos y barrios del dataset...")

try:
    df = pd.read_csv('../backend/data/unified_houses_madrid.csv')
    
    # Convertir códigos de distrito a nombres
    df['district_name'] = df['district'].map(DISTRICT_NAMES).fillna(df['district'])
    
    # Extraer distritos únicos (nombres)
    districts = sorted([name for name in DISTRICT_NAMES.values()])
    print(f"✅ Distritos encontrados: {len(districts)}")
    
    # Extraer barrios por distrito
    neighborhoods_by_district = {}
    
    for district_code, district_name in DISTRICT_NAMES.items():
        # Filtrar por código de distrito
        district_data = df[df['district'] == district_code]
        if not district_data.empty:
            neighborhoods = sorted(district_data['neighborhood'].dropna().unique().tolist())
            # Convertir números a strings si es necesario
            neighborhoods = [str(n) for n in neighborhoods]
            neighborhoods_by_district[district_name] = neighborhoods
            print(f"  📍 {district_name}: {len(neighborhoods)} barrios")
    
    # Guardar en un archivo JSON para usar en el frontend
    data = {
        "districts": districts,
        "neighborhoods_by_district": neighborhoods_by_district
    }
    
    with open('../frontend/src/districts_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos guardados en 'frontend/src/districts_data.json'")
    
    # Mostrar algunos ejemplos
    print("\n📋 Ejemplos de distritos y barrios:")
    for district_name in list(neighborhoods_by_district.keys())[:5]:  # Primeros 5 distritos
        neighborhoods = neighborhoods_by_district[district_name][:3]  # Primeros 3 barrios
        more_indicator = "..." if len(neighborhoods_by_district[district_name]) > 3 else ""
        print(f"  🏙️ {district_name}: {', '.join(neighborhoods)}{more_indicator}")
    
    # Mostrar estadísticas
    total_neighborhoods = sum(len(n) for n in neighborhoods_by_district.values())
    print(f"\n📊 Total: {len(districts)} distritos, {total_neighborhoods} barrios únicos")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()