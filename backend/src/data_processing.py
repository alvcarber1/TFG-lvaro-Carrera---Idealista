import pandas as pd

def load_data(file_path):
    """Carga los datos desde un archivo CSV."""
    return pd.read_csv(file_path)

def filter_city(data, region_name="Madrid"):
    """Filtra el DataFrame para incluir todas las filas donde RegionName es 'Madrid' y RegionType es 'city'."""
    # Filtra el DataFrame con las condiciones especificadas
    filtered_data = data[(data['RegionName'] == region_name)]
    return filtered_data

def clean_data(data):
    """Realiza una limpieza básica de datos en el DataFrame."""
    # Por ejemplo, podrías limpiar filas con NaN o hacer otros ajustes aquí
    return data.dropna()

def save_processed_data(data, file_path):
    """Guarda el DataFrame procesado en un archivo CSV."""
    data.to_csv(file_path, index=False)
