from rest_framework import serializers

from recipes.plugins.open_data_plugin.models import OpenDataUnit


class OpenDataUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenDataUnit
        fields = (
            'id', 'slug', 'name',)
