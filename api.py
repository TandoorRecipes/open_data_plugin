from rest_framework import viewsets

from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood
from recipes.plugins.open_data_plugin.serializer import OpenDataUnitSerializer, OpenDataFoodSerializer


class OpenDataUnitViewSet(viewsets.ModelViewSet):
    queryset = OpenDataUnit.objects
    serializer_class = OpenDataUnitSerializer


class OpenDataFoodViewSet(viewsets.ModelViewSet):
    queryset = OpenDataFood.objects
    serializer_class = OpenDataFoodSerializer
