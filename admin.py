from django.contrib import admin
from .models import OpenDataUnit, OpenDataCategory, OpenDataStore, OpenDataFoodProperty, OpenDataFood, OpenDataConversion, OpenDataProperty, OpenDataUser


# Register your models here.

class OpenDataUserAdmin(admin.ModelAdmin):
    search_fields = ('user__username',)
    list_filter = ('moderator_user', 'verified_user',)
    list_display = ('name', 'moderator_user', 'verified_user',)

    @staticmethod
    def name(obj):
        return obj.user.username


admin.site.register(OpenDataUser, OpenDataUserAdmin)


class OpenDataUnitAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name', 'created_by__username',)
    list_filter = ('created_by',)
    autocomplete_fields = ('created_by',)

    list_display = ('slug', 'version', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataUnit, OpenDataUnitAdmin)


class OpenDataCategoryAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name', 'created_by__username',)
    list_filter = ('created_by',)
    autocomplete_fields = ('created_by',)

    list_display = ('slug', 'version', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataCategory, OpenDataCategoryAdmin)


class OpenDataStoreAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name', 'created_by__username',)
    list_filter = ('created_by',)
    autocomplete_fields = ('created_by',)

    list_display = ('slug', 'version', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataStore, OpenDataStoreAdmin)


class OpenDataPropertyAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name', 'created_by__username',)
    list_filter = ('created_by',)
    autocomplete_fields = ('created_by',)

    list_display = ('slug', 'version', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataProperty, OpenDataPropertyAdmin)


class OpenDataFoodPropertyAdmin(admin.ModelAdmin):
    list_display = ('property', 'property_amount')


admin.site.register(OpenDataFoodProperty, OpenDataFoodPropertyAdmin)


class OpenDataFoodAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name', 'created_by__username', 'fdc_id',)
    list_filter = ('created_by',)
    autocomplete_fields = ('created_by', 'store_category', 'properties_food_unit', 'preferred_unit_metric', 'preferred_shopping_unit_metric', 'preferred_unit_imperial', 'preferred_shopping_unit_imperial')
    filter_horizontal = ('properties',)

    list_display = ('slug', 'version', 'name', 'updated_at', 'created_by',)


admin.site.register(OpenDataFood, OpenDataFoodAdmin)


class OpenDataConversionAdmin(admin.ModelAdmin):
    search_fields = ('slug', 'name', 'created_by__username',)
    list_filter = ('created_by',)
    autocomplete_fields = ('created_by', 'food', 'base_unit', 'converted_unit')

    list_display = ('slug', 'version', 'food', 'base_unit', 'converted_unit', 'updated_at', 'created_by',)


admin.site.register(OpenDataConversion, OpenDataConversionAdmin)
