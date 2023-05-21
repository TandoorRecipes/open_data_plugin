from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood


class OpenDataUnitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataUnit
        fields = ('id', 'slug', 'name', 'plural_name',)


class OpenDataFoodSerializer(WritableNestedModelSerializer):
    preferred_unit_metric = OpenDataUnitSerializer(required=False)

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataFood
        fields = ('id', 'slug', 'name', 'plural_name', 'preferred_unit_metric')
