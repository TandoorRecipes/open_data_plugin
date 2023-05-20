from django.contrib import admin
from .models import OpenDataUnit, OpenDataCategory, OpenDataStore, OpenDataFoodProperty, OpenDataFood, OpenDataConversion, OpenDataProperty


# Register your models here.
class OpenDataUnitAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataUnit, OpenDataUnitAdmin)


class OpenDataCategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataCategory, OpenDataCategoryAdmin)


class OpenDataStoreAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataStore, OpenDataStoreAdmin)


class OpenDataPropertyAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataProperty, OpenDataPropertyAdmin)


class OpenDataFoodPropertyAdmin(admin.ModelAdmin):
    list_display = ('property', 'property_amount')


admin.site.register(OpenDataFoodProperty, OpenDataFoodPropertyAdmin)


class OpenDataFoodAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataFood, OpenDataFoodAdmin)


class OpenDataConversionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'food', 'base_unit', 'converted_unit', 'updated_at', 'created_by',)


admin.site.register(OpenDataConversion, OpenDataConversionAdmin)
