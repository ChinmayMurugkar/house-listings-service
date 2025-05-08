from django.contrib import admin
from .models import House

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state', 'price', 'bedrooms', 'bathrooms', 'home_size')
    list_filter = ('city', 'state', 'home_type', 'bedrooms', 'bathrooms')
    search_fields = ('address', 'city', 'state', 'zipcode')
    ordering = ('-price',)
    readonly_fields = ('zillow_id',)
