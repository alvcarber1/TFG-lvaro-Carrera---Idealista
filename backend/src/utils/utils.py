import decimal
from src.models.houses import House
import os
import csv

def importar_csv():
    # Ruta del archivo CSV
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(ruta_base, '../../data/unified_houses_madrid.csv')

    def convertir_a_int(valor):
        """Convierte el valor flotante a entero, redondeando si es necesario."""
        try:
            return int(round(float(valor)))
        except (ValueError, TypeError):
            return None

    def convertir_a_float(valor):
        """Convierte el valor a float, devolviendo None si no es convertible."""
        try:
            return float(valor) if valor else None
        except (ValueError, TypeError):
            return None

    def convertir_a_decimal(valor):
        """Convierte el valor a decimal, devolviendo None si no es convertible."""
        try:
            return decimal.Decimal(valor) if valor else None
        except (decimal.InvalidOperation, TypeError, ValueError):
            return None

    # Conjunto para almacenar las calles únicas
    calles_unicas = set()

    with open(ruta_csv, newline='', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            # Crear una clave única para la calle
            calle_clave = (fila.get('street_name'), fila.get('street_number'), fila.get('portal'))

            # Verificar si la calle ya está en el conjunto
            if calle_clave not in calles_unicas:
                # Agregar la calle al conjunto
                calles_unicas.add(calle_clave)

                # Verificar si ya existe un registro con la misma clave en la base de datos
                if not House.objects.filter(street_name=fila.get('street_name'), street_number=fila.get('street_number'), portal=fila.get('portal')).exists():
                    # Crear un nuevo objeto de la clase House
                    House.objects.create(
                        latitude=convertir_a_float(fila.get('latitude')),
                        longitude=convertir_a_float(fila.get('longitude')),
                        address=fila.get('address'),
                        sq_mt_built=convertir_a_float(fila.get('sq_mt_built')),
                        n_rooms=convertir_a_int(fila.get('n_rooms')),
                        n_bathrooms=convertir_a_int(fila.get('n_bathrooms')),
                        n_floors=convertir_a_int(fila.get('n_floors')),
                        sq_mt_allotment=convertir_a_float(fila.get('sq_mt_allotment')),
                        floor=fila.get('floor'),
                        buy_price=convertir_a_float(fila.get('buy_price')),
                        is_renewal_needed=fila.get('is_renewal_needed') == 'True',
                        has_lift=fila.get('has_lift') == 'True',
                        is_exterior=fila.get('is_exterior') == 'True',
                        energy_certificate=fila.get('energy_certificate'),
                        has_parking=fila.get('has_parking') == 'True',
                        neighborhood=fila.get('neighborhood'),
                        district=fila.get('district'),
                        house_type=fila.get('house_type'),
                        sq_mt_useful=convertir_a_float(fila.get('sq_mt_useful')),
                        raw_address=fila.get('raw_address'),
                        is_exact_address_hidden=fila.get('is_exact_address_hidden') == 'True',
                        street_name=fila.get('street_name'),
                        street_number=fila.get('street_number'),
                        portal=fila.get('portal'),
                        is_floor_under=fila.get('is_floor_under') == 'True',
                        door=fila.get('door'),
                        operation=fila.get('operation'),
                        rent_price=convertir_a_float(fila.get('rent_price')),
                        rent_price_by_area=convertir_a_float(fila.get('rent_price_by_area')),
                        is_rent_price_known=fila.get('is_rent_price_known') == 'True',
                        buy_price_by_area=convertir_a_float(fila.get('buy_price_by_area')),
                        is_buy_price_known=fila.get('is_buy_price_known') == 'True',
                        is_new_development=fila.get('is_new_development') == 'True',
                        built_year=convertir_a_int(fila.get('built_year')),
                        has_central_heating=fila.get('has_central_heating') == 'True',
                        has_individual_heating=fila.get('has_individual_heating') == 'True',
                        are_pets_allowed=fila.get('are_pets_allowed') == 'True',
                        has_ac=fila.get('has_ac') == 'True',
                        has_fitted_wardrobes=fila.get('has_fitted_wardrobes') == 'True',
                        has_garden=fila.get('has_garden') == 'True',
                        has_pool=fila.get('has_pool') == 'True',
                        has_terrace=fila.get('has_terrace') == 'True',
                        has_balcony=fila.get('has_balcony') == 'True',
                        has_storage_room=fila.get('has_storage_room') == 'True',
                        is_furnished=fila.get('is_furnished') == 'True',
                        is_kitchen_equipped=fila.get('is_kitchen_equipped') == 'True',
                        is_accessible=fila.get('is_accessible') == 'True',
                        has_green_zones=fila.get('has_green_zones') == 'True',
                        has_private_parking=fila.get('has_private_parking') == 'True',
                        has_public_parking=fila.get('has_public_parking') == 'True',
                        is_parking_included_in_price=fila.get('is_parking_included_in_price') == 'True',
                        parking_price=convertir_a_decimal(fila.get('parking_price')),
                        is_orientation_north=fila.get('is_orientation_north') == 'True',
                        is_orientation_west=fila.get('is_orientation_west') == 'True',
                        is_orientation_south=fila.get('is_orientation_south') == 'True',
                        is_orientation_east=fila.get('is_orientation_east') == 'True'
                    )