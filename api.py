from rest_framework import viewsets

from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataConversion
from recipes.plugins.open_data_plugin.serializer import OpenDataUnitSerializer, OpenDataFoodSerializer, OpenDataCategorySerializer, OpenDataStoreSerializer, OpenDataPropertySerializer, OpenDataConversionSerializer


class OpenDataUnitViewSet(viewsets.ModelViewSet):
    queryset = OpenDataUnit.objects
    serializer_class = OpenDataUnitSerializer


class OpenDataCategoryViewSet(viewsets.ModelViewSet):
    queryset = OpenDataCategory.objects
    serializer_class = OpenDataCategorySerializer


class OpenDataStoreViewSet(viewsets.ModelViewSet):
    queryset = OpenDataStore.objects
    serializer_class = OpenDataStoreSerializer


class OpenDataPropertyViewSet(viewsets.ModelViewSet):
    queryset = OpenDataProperty.objects
    serializer_class = OpenDataPropertySerializer


class OpenDataFoodViewSet(viewsets.ModelViewSet):
    queryset = OpenDataFood.objects
    serializer_class = OpenDataFoodSerializer


class OpenDataConversionViewSet(viewsets.ModelViewSet):
    queryset = OpenDataConversion.objects
    serializer_class = OpenDataConversionSerializer
