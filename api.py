from rest_framework import viewsets

from recipes.plugins.open_data_plugin.models import OpenDataUnit
from recipes.plugins.open_data_plugin.serializer import OpenDataUnitSerializer


class OpenDataUnitViewSet(viewsets.ModelViewSet):
    queryset = OpenDataUnit.objects
    serializer_class = OpenDataUnitSerializer
