import json
import traceback

import requests
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.permissions import SAFE_METHODS

from recipes.plugins.open_data_plugin.models import OpenDataUnit, OpenDataFood, OpenDataCategory, OpenDataStore, OpenDataProperty, OpenDataConversion, OpenDataVersion
from recipes.plugins.open_data_plugin.serializer import OpenDataUnitSerializer, OpenDataFoodSerializer, OpenDataCategorySerializer, OpenDataStoreSerializer, OpenDataPropertySerializer, OpenDataConversionSerializer, OpenDataVersionSerializer
from recipes.settings import FDA_API_KEY


class OpenDataIsOwner(permissions.BasePermission):
    message = 'You cannot interact with this object as it is not owned by you!'

    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user or request.method in SAFE_METHODS


class OpenDataIsModerator(permissions.BasePermission):
    message = 'You cannot interact with this object as you are not a moderator'

    def has_permission(self, request, view):
        return request.user.opendatauser.moderator_user or request.method in SAFE_METHODS


class OpenDataIsVerified(permissions.BasePermission):
    message = 'You cannot interact with this object as you are not verified'

    def has_permission(self, request, view):
        return request.user.opendatauser.verified_user or request.method in SAFE_METHODS


class OpenDataVersionViewSet(viewsets.ModelViewSet):
    queryset = OpenDataVersion.objects.all()
    serializer_class = OpenDataVersionSerializer
    permission_classes = [OpenDataIsModerator]


class OpenDataUnitViewSet(viewsets.ModelViewSet):
    queryset = OpenDataUnit.objects.all()
    serializer_class = OpenDataUnitSerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]


class OpenDataCategoryViewSet(viewsets.ModelViewSet):
    queryset = OpenDataCategory.objects.all()
    serializer_class = OpenDataCategorySerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]


class OpenDataStoreViewSet(viewsets.ModelViewSet):
    queryset = OpenDataStore.objects.all()
    serializer_class = OpenDataStoreSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]


class OpenDataPropertyViewSet(viewsets.ModelViewSet):
    queryset = OpenDataProperty.objects.all()
    serializer_class = OpenDataPropertySerializer
    permission_classes = [OpenDataIsModerator | OpenDataIsVerified]


class OpenDataFoodViewSet(viewsets.ModelViewSet):
    queryset = OpenDataFood.objects.all()
    serializer_class = OpenDataFoodSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]


class OpenDataConversionViewSet(viewsets.ModelViewSet):
    queryset = OpenDataConversion.objects.all()
    serializer_class = OpenDataConversionSerializer
    permission_classes = [OpenDataIsOwner | OpenDataIsModerator | OpenDataIsVerified]


class FDCViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        response = requests.get(f'https://api.nal.usda.gov/fdc/v1/food/{pk}?api_key={FDA_API_KEY}')
        if response.status_code == 429:
            return JsonResponse({'error', 'API Key Rate Limit reached/exceeded, see https://api.data.gov/docs/rate-limits/ for more information'}, status=429, json_dumps_params={'indent': 4})

        try:
            data = json.loads(response.content)

            parsed_data = {
                'slug': f"food-{data['description'].lower().replace(' ', '-').replace(',', '')}",
                'name': data['description'],
                'plural_name': data['description'],
                'properties_food_amount': 100,
                'properties_source': f'https://fdc.nal.usda.gov/fdc-app.html#/food-details/{pk}/nutrients',
                'properties': [],
                'fdc_id': pk
            }

            unit_g = OpenDataUnit.objects.filter(base_unit='G').first()
            if unit_g:
                parsed_data['properties_food_unit'] = {'id': unit_g.id, 'slug': unit_g.slug, 'name': unit_g.name, 'type': unit_g.type, }

            if OpenDataProperty.objects.filter(fdc_id__isnull=False).count() == 0:  # TODO better solution with cache
                OpenDataProperty.objects.create(slug='property-calories', name='Calories', unit='kcal', fdc_id=1008, created_by=request.user)
                OpenDataProperty.objects.create(slug='property-proteins', name='Proteins', unit='g', fdc_id=1003, created_by=request.user)
                OpenDataProperty.objects.create(slug='property-carbohydrates', name='Carbohydrates', unit='g', fdc_id=1005, created_by=request.user)
                OpenDataProperty.objects.create(slug='property-fats', name='Fats', unit='g', fdc_id=1004, created_by=request.user)

            for fn in data['foodNutrients']:
                if fn['nutrient']['id'] == 1008:
                    p = OpenDataProperty.objects.get(fdc_id=1008)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name}, "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1003:
                    p = OpenDataProperty.objects.get(fdc_id=1003)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name}, "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1005:
                    p = OpenDataProperty.objects.get(fdc_id=1005)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name}, "property_amount": round(fn['amount'], 2)})
                if fn['nutrient']['id'] == 1004:
                    p = OpenDataProperty.objects.get(fdc_id=1004)
                    parsed_data['properties'].append({"property": {'id': p.id, 'slug': p.slug, 'name': p.name}, "property_amount": round(fn['amount'], 2)})

            return JsonResponse(parsed_data, json_dumps_params={'indent': 4})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': f'{e} - check server log'}, status=500, json_dumps_params={'indent': 4})
