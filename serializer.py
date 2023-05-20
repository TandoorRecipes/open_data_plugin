from rest_framework import serializers

from recipes.plugins.open_data_plugin.models import OpenDataUnit


class OpenDataUnitSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = OpenDataUnit
        fields = ( 'id', 'slug', 'name', 'plural_name',)
