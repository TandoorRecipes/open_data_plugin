from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataStoreCategory, OpenDataConversion, OpenDataFoodProperty


class OpenDataUnitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataUnit
        fields = ('id', 'slug', 'name', 'plural_name', 'base_unit', 'type', 'comment')


class OpenDataCategorySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataCategory
        fields = ('id', 'slug', 'name', 'comment',)


class OpenDataStoreCategorySerializer(WritableNestedModelSerializer):
    category = OpenDataCategorySerializer()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataStoreCategory
        fields = ('id', 'category', 'store', 'order',)


class OpenDataStoreSerializer(WritableNestedModelSerializer):
    category_to_store = OpenDataStoreCategorySerializer(many=True, allow_null=True)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataStore
        fields = ('id', 'slug', 'name', 'category_to_store', 'comment',)


class OpenDataPropertySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataProperty
        fields = ('id', 'slug', 'name', 'unit', 'comment',)


class OpenDataFoodPropertySerializer(WritableNestedModelSerializer):
    property = OpenDataPropertySerializer()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataFoodProperty
        fields = ('id', 'slug', 'property', 'property_amount', 'comment',)


class OpenDataFoodSerializer(WritableNestedModelSerializer):
    store_category = OpenDataUnitSerializer(required=False)
    preferred_unit_metric = OpenDataUnitSerializer(required=False)
    preferred_shopping_unit_metric = OpenDataUnitSerializer(required=False)
    preferred_unit_imperial = OpenDataUnitSerializer(required=False)
    preferred_shopping_unit_imperial = OpenDataUnitSerializer(required=False)
    properties = OpenDataFoodPropertySerializer(required=False, many=True)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataFood
        fields = ('id', 'slug', 'name', 'plural_name', 'store_category',
                  'preferred_unit_metric', 'preferred_shopping_unit_metric', 'preferred_unit_imperial',
                  'preferred_shopping_unit_imperial', 'properties', 'fdc_id', 'comment',)


class OpenDataConversionSerializer(WritableNestedModelSerializer):
    food = OpenDataFoodSerializer()
    base_unit = OpenDataUnitSerializer()
    converted_unit = OpenDataUnitSerializer()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataConversion
        fields = ('id', 'slug', 'food', 'base_amount', 'base_unit', 'converted_amount', 'converted_unit', 'source', 'comment',)
