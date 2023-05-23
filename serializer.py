from django.db.models import Q
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from rest_framework import serializers

from cookbook.serializer import CustomDecimalField
from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataStoreCategory, OpenDataConversion, OpenDataFoodProperty


class OpenDataUnitSerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    def validate(self, data):
        slug_prefix = 'unit-'
        if not data['slug'].startswith(slug_prefix):
            raise serializers.ValidationError(f'Slug has to start with {slug_prefix}')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        obj, created = OpenDataUnit.objects.get_or_create(slug=validated_data['slug'], name=validated_data['name'], defaults=validated_data)
        return obj

    def update(self, instance, validated_data):
        return super(OpenDataUnitSerializer, self).update(instance, validated_data)

    class Meta:
        model = OpenDataUnit
        fields = ('id', 'slug', 'name', 'plural_name', 'base_unit', 'type', 'comment')
        read_only_fields = ('id',)


class OpenDataCategorySerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    def validate(self, data):
        slug_prefix = 'category-'
        if not data['slug'].startswith(slug_prefix):
            raise serializers.ValidationError(f'Slug has to start with {slug_prefix}')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        obj, created = OpenDataCategory.objects.get_or_create(slug=validated_data['slug'], name=validated_data['name'], defaults=validated_data)
        return obj

    def update(self, instance, validated_data):
        return super(OpenDataCategorySerializer, self).update(instance, validated_data)

    class Meta:
        model = OpenDataCategory
        fields = ('id', 'slug', 'name', 'comment',)
        read_only_fields = ('id',)


class OpenDataStoreCategorySerializer(WritableNestedModelSerializer):
    category = OpenDataCategorySerializer()

    class Meta:
        model = OpenDataStoreCategory
        fields = ('id', 'category', 'store', 'order',)


class OpenDataStoreSerializer(WritableNestedModelSerializer):
    category_to_store = OpenDataStoreCategorySerializer(many=True, allow_null=True)

    def validate(self, data):
        slug_prefix = 'store-'
        if not data['slug'].startswith(slug_prefix):
            raise serializers.ValidationError(f'Slug has to start with {slug_prefix}')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataStore
        fields = ('id', 'slug', 'name', 'category_to_store', 'comment',)


class OpenDataPropertySerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    def validate(self, data):
        slug_prefix = 'property-'
        if not data['slug'].startswith(slug_prefix):
            raise serializers.ValidationError(f'Slug has to start with {slug_prefix}')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        obj, created = OpenDataProperty.objects.get_or_create(slug=validated_data['slug'], name=validated_data['name'], defaults=validated_data)
        return obj

    class Meta:
        model = OpenDataProperty
        fields = ('id', 'slug', 'name', 'unit', 'comment',)


class OpenDataFoodPropertySerializer(WritableNestedModelSerializer):
    property = OpenDataPropertySerializer()
    property_amount = CustomDecimalField()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataFoodProperty
        fields = ('id', 'property', 'property_amount',)
        read_only_fields = ('id',)


class OpenDataFoodSerializer(WritableNestedModelSerializer):
    store_category = OpenDataCategorySerializer()
    preferred_unit_metric = OpenDataUnitSerializer()
    preferred_shopping_unit_metric = OpenDataUnitSerializer()
    preferred_unit_imperial = OpenDataUnitSerializer()
    preferred_shopping_unit_imperial = OpenDataUnitSerializer()
    properties = OpenDataFoodPropertySerializer(allow_null=True, many=True)
    properties_food_unit = OpenDataUnitSerializer()

    def validate(self, data):
        slug_prefix = 'food-'
        if not data['slug'].startswith(slug_prefix):
            raise serializers.ValidationError(f'Slug has to start with {slug_prefix}')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = OpenDataFood
        fields = ('id', 'slug', 'name', 'plural_name', 'store_category',
                  'preferred_unit_metric', 'preferred_shopping_unit_metric', 'preferred_unit_imperial',
                  'preferred_shopping_unit_imperial', 'properties', 'properties_food_amount', 'properties_food_unit', 'properties_source', 'fdc_id', 'comment',)
        read_only_fields = ('id',)


class OpenDataConversionSerializer(WritableNestedModelSerializer):
    food = OpenDataFoodSerializer()
    base_unit = OpenDataUnitSerializer()
    converted_unit = OpenDataUnitSerializer()
    base_amount = CustomDecimalField()
    converted_amount = CustomDecimalField()

    def validate(self, data):
        slug_prefix = 'conversion-'
        if not data['slug'].startswith(slug_prefix):
            raise serializers.ValidationError(f'Slug has to start with {slug_prefix}')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataConversion
        fields = ('id', 'slug', 'food', 'base_amount', 'base_unit', 'converted_amount', 'converted_unit', 'source', 'comment',)
