import re

from django.db.models import Q
from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from rest_framework import serializers

from cookbook.serializer import CustomDecimalField
from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataStoreCategory, OpenDataConversion, OpenDataFoodProperty, OpenDataVersion


def slug_validator(slug, prefix):
    if not re.fullmatch(r"(([a-z0-9])+(\-)*)+", slug):
        raise serializers.ValidationError(f'Slugs can only contain lower case characters and numbers connected with -')
    if not slug.startswith(prefix):
        raise serializers.ValidationError(f'Slug has to start with {prefix}')


def string_validator(input_string):
    if not re.fullmatch(r"([A-z0-9\-\(\)\&\s])+", input_string):
        raise serializers.ValidationError(f"<{input_string}> contains invalid characters (only A-z,0-9,-,(,),& and whitespace allowed) ")


class OpenDataVersionSerializer(UniqueFieldsMixin, serializers.ModelSerializer):

    def create(self, validated_data):
        if self.context['request'].user.opendatauser.moderator_user:
            obj, created = OpenDataVersion.objects.get_or_create(name=validated_data['name'], defaults=validated_data)
        else:
            obj = OpenDataVersion.objects.filter(name=validated_data['name']).first()
        return obj

    class Meta:
        model = OpenDataVersion
        fields = ('id', 'name', 'code', 'comment',)
        read_only_fields = ('id',)


class OpenDataUnitSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    created_by = serializers.SerializerMethodField('get_created_by_name')
    version = OpenDataVersionSerializer()

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def validate(self, data):
        slug_validator(data['slug'], 'unit-')
        string_validator(data['name'])
        string_validator(data['plural_name'])
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        super().create(validated_data)
        obj, created = OpenDataUnit.objects.get_or_create(slug=validated_data['slug'], name=validated_data['name'], defaults=validated_data)
        return obj

    def update(self, instance, validated_data):
        return super(OpenDataUnitSerializer, self).update(instance, validated_data)

    class Meta:
        model = OpenDataUnit
        fields = ('id', 'version', 'slug', 'name', 'plural_name', 'base_unit', 'type', 'comment', 'created_by')
        read_only_fields = ('id', 'created_by',)


class OpenDataCategorySerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    created_by = serializers.SerializerMethodField('get_created_by_name')
    version = OpenDataVersionSerializer()

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def validate(self, data):
        slug_validator(data['slug'], 'category-')
        string_validator(data['name'])
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        super().create(validated_data)
        obj, created = OpenDataCategory.objects.get_or_create(slug=validated_data['slug'], name=validated_data['name'], defaults=validated_data)
        return obj

    def update(self, instance, validated_data):
        return super(OpenDataCategorySerializer, self).update(instance, validated_data)

    class Meta:
        model = OpenDataCategory
        fields = ('id', 'version', 'slug', 'name', 'description', 'comment', 'created_by',)
        read_only_fields = ('id', 'created_by',)


class OpenDataStoreCategorySerializer(WritableNestedModelSerializer):
    category = OpenDataCategorySerializer()

    class Meta:
        model = OpenDataStoreCategory
        fields = ('id', 'category', 'store', 'order',)


class OpenDataStoreSerializer(WritableNestedModelSerializer):
    category_to_store = OpenDataStoreCategorySerializer(many=True, allow_null=True)
    created_by = serializers.SerializerMethodField('get_created_by_name')
    version = OpenDataVersionSerializer()

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def validate(self, data):
        slug_validator(data['slug'], 'store-')
        string_validator(data['name'])
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataStore
        fields = ('id', 'version', 'slug', 'name', 'category_to_store', 'comment', 'created_by',)
        read_only_fields = ('id', 'created_by',)


class OpenDataPropertySerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    created_by = serializers.SerializerMethodField('get_created_by_name')
    version = OpenDataVersionSerializer()

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def validate(self, data):
        slug_validator(data['slug'], 'property-')
        string_validator(data['name'])
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        super().create(validated_data)
        obj, created = OpenDataProperty.objects.get_or_create(slug=validated_data['slug'], name=validated_data['name'], defaults=validated_data)
        return obj

    class Meta:
        model = OpenDataProperty
        fields = ('id', 'version', 'slug', 'name', 'unit', 'fdc_id', 'comment', 'created_by',)
        read_only_fields = ('id', 'created_by',)


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


class OpenDataFoodSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    store_category = OpenDataCategorySerializer()
    preferred_unit_metric = OpenDataUnitSerializer(allow_null=True, required=False)
    preferred_shopping_unit_metric = OpenDataUnitSerializer(allow_null=True, required=False)
    preferred_unit_imperial = OpenDataUnitSerializer(allow_null=True, required=False)
    preferred_shopping_unit_imperial = OpenDataUnitSerializer(allow_null=True, required=False)
    properties = OpenDataFoodPropertySerializer(allow_null=True, many=True)
    properties_food_unit = OpenDataUnitSerializer()
    created_by = serializers.SerializerMethodField('get_created_by_name')
    version = OpenDataVersionSerializer()

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def validate(self, data):
        slug_validator(data['slug'], 'food-')
        string_validator(data['name'])
        string_validator(data['plural_name'])
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = OpenDataFood
        fields = ('id', 'version', 'slug', 'name', 'plural_name', 'store_category',
                  'preferred_unit_metric', 'preferred_shopping_unit_metric', 'preferred_unit_imperial',
                  'preferred_shopping_unit_imperial', 'properties', 'properties_food_amount', 'properties_food_unit', 'properties_source', 'fdc_id', 'comment', 'created_by',)
        read_only_fields = ('id', 'created_by',)


class OpenDataConversionSerializer(WritableNestedModelSerializer):
    food = OpenDataFoodSerializer()
    base_unit = OpenDataUnitSerializer()
    converted_unit = OpenDataUnitSerializer()
    base_amount = CustomDecimalField()
    converted_amount = CustomDecimalField()
    created_by = serializers.SerializerMethodField('get_created_by_name')
    version = OpenDataVersionSerializer()

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def validate(self, data):
        slug_validator(data['slug'], 'conversion-')
        return super().validate(data)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataConversion
        fields = ('id', 'version', 'slug', 'food', 'base_amount', 'base_unit', 'converted_amount', 'converted_unit', 'source', 'comment', 'created_by',)
        read_only_fields = ('id', 'created_by',)
