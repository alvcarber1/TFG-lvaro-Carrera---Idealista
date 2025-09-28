
from django.contrib import admin
from .models.houses import House


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'latitude', 'longitude', 'raw_address', 'address', 'street_name',
        'street_number', 'portal', 'door', 'neighborhood', 'district', 'sq_mt_built',
        'sq_mt_useful', 'sq_mt_allotment', 'n_rooms', 'n_bathrooms', 'n_floors', 'floor',
        'built_year', 'house_type', 'is_renewal_needed', 'has_lift', 'is_exterior',
        'energy_certificate', 'has_parking', 'is_exact_address_hidden', 'is_floor_under',
        'operation', 'rent_price', 'rent_price_by_area', 'is_rent_price_known', 'buy_price',
        'buy_price_by_area', 'is_buy_price_known', 'is_new_development', 'has_central_heating',
        'has_individual_heating', 'are_pets_allowed', 'has_ac', 'has_fitted_wardrobes',
        'has_garden', 'has_pool', 'has_terrace', 'has_balcony', 'has_storage_room',
        'is_furnished', 'is_kitchen_equipped', 'is_accessible', 'has_green_zones',
        'has_private_parking', 'has_public_parking', 'is_parking_included_in_price',
        'parking_price', 'is_orientation_north', 'is_orientation_west', 'is_orientation_south',
        'is_orientation_east', 'created_at', 'updated_at'
    )

